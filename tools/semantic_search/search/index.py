import os
import numpy as np
import pickle
import json
import fcntl
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import asdict
from .models import Chunk, SearchResult

class ForwardIndex:
    """Stores and manages Chunks and their Embeddings. Uses mmap for optimized load performance."""
    
    def __init__(self, index_dir: Path, dim: int = 4096):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.dim = dim
        self.embeddings_path = self.index_dir / "embeddings.npy"
        self.chunks_path = self.index_dir / "chunks.pkl"
        self.manifest_path = self.index_dir / "manifest.json"
        self.lock_path = self.index_dir / "index.lock"
        
        self.embeddings: Optional[np.ndarray] = None
        self.chunks: List[Chunk] = []
        self.manifest: Dict[str, Any] = {} # file_path -> {mtime, chunk_indices}
        
        self.load()

    def _get_lock(self, exclusive: bool = False):
        """Acquire a file lock."""
        mode = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        f = open(self.lock_path, 'w')
        fcntl.flock(f, mode)
        return f

    def load(self):
        """Load the index. Reads vectors in mmap mode."""
        if not self.manifest_path.exists():
            return

        with self._get_lock(exclusive=False) as _:
            with open(self.manifest_path, 'r') as f:
                self.manifest = json.load(f)
            
            if self.chunks_path.exists():
                with open(self.chunks_path, 'rb') as f:
                    self.chunks = pickle.load(f)
            
            if self.embeddings_path.exists():
                # Load in mmap read-only mode — nearly instantaneous
                self.embeddings = np.load(self.embeddings_path, mmap_mode='r')

    def save(self, new_chunks: List[Chunk], updated_files: Dict[str, float]):
        """Save / update the index. Requires an exclusive lock."""
        with self._get_lock(exclusive=True) as _:
            # 1. Update the chunks list
            # Note: this is a simple implementation. Production may need finer-grained incremental update logic.
            # We assume new_chunks are to be appended or replaced.

            # Simplified logic: load old, merge, save.
            # This slows down for very large indexes, but is fine for a personal knowledge base.
            all_chunks = self.chunks

            # Remove old chunks from files that were updated
            all_chunks = [c for c in all_chunks if c.source_file not in updated_files]

            # Append new chunks
            start_idx = len(all_chunks)
            all_chunks.extend(new_chunks)

            # Update manifest
            for file_path, mtime in updated_files.items():
                indices = [i for i, c in enumerate(all_chunks) if c.source_file == file_path]
                self.manifest[file_path] = {
                    "mtime": mtime,
                    "indices": indices
                }

            self.chunks = all_chunks

            # 2. Save metadata
            with open(self.chunks_path, 'wb') as f:
                pickle.dump(self.chunks, f)
            with open(self.manifest_path, 'w') as f:
                json.dump(self.manifest, f)

            # 3. Save embeddings
            # Combine all chunk embeddings into a single large matrix
            embeddings_list = [c.embedding for c in self.chunks]
            if embeddings_list:
                embeddings_array = np.array(embeddings_list, dtype=np.float32)
                np.save(self.embeddings_path, embeddings_array)
                # Reload in mmap mode
                self.embeddings = np.load(self.embeddings_path, mmap_mode='r')

    def get_subset(self, file_paths: List[str]) -> Tuple[List[Chunk], Optional[np.ndarray]]:
        """Get the subset of chunks corresponding to the given file list."""
        # Since we use mmap, we can access self.embeddings directly by index
        target_chunks = []
        indices = []
        
        file_set = set(file_paths)
        for i, chunk in enumerate(self.chunks):
            if chunk.source_file in file_set:
                target_chunks.append(chunk)
                indices.append(i)
        
        if not indices or self.embeddings is None:
            return target_chunks, None
            
        subset_embeddings = self.embeddings[indices]
        return target_chunks, subset_embeddings

    def needs_update(self, file_path: str, current_mtime: float) -> bool:
        """Check whether the file needs its features re-extracted."""
        record = self.manifest.get(file_path)
        if not record:
            return True
        return record.get("mtime") != current_mtime
