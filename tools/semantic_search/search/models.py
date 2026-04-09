from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Tuple
import numpy as np

@dataclass
class Chunk:
    id: str                    # "{source_file}:{chunk_index}"
    text: str                  # chunk text content
    embedding: Optional[np.ndarray] = None  # float32 vector
    source_file: str = ""       # relative path of source file
    header: str = ""           # heading this chunk belongs to
    position: Tuple[int, int] = (0, 0)  # (start_line, end_line)
    metadata: Dict[str, Any] = None

    def to_dict(self, include_embedding: bool = False) -> Dict[str, Any]:
        d = asdict(self)
        if not include_embedding:
            d.pop('embedding')
        return d

@dataclass
class SearchResult:
    chunk: Chunk
    score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": float(self.score),
            "chunk": self.chunk.to_dict()
        }
