---
id: axiom_a06_framework_worldview_2026
category: ai_agentic
created: 2026-02-23
updated: 2026-02-23
---

# A6. Framework Choice is Worldview Lock-in

## 1. Core Axiom

In a rapidly evolving field, choosing an AI framework is not a technical decision — it is a philosophical bet on future adaptability. Every framework is not just a collection of tools, but a complete worldview: about how Agents should think, collaborate, and execute. Choosing a framework means seeing the world through the framework author's perspective, which, at a moment when the field's foundations have not yet settled, severely limits the depth of your understanding and your capacity to adapt.

---

## 2. Deep Implications

### 2.1 Every Framework is a Worldview

The mainstream frameworks in the Agentic AI field each represent a different understanding of what an Agent fundamentally is. AutoGen believes that asynchronous multi-agent collaboration is the key to solving complex problems — its entire architecture revolves around message passing and conversation between agents. LangGraph believes that workflows are essentially directed graphs, with state flowing between nodes and conditional edges determining the execution path; this perspective led to complex persistence, event systems, and async mechanisms. SmolAgents takes a completely different philosophy: code is the clearest intermediate medium, and agents should directly generate and execute code rather than going through abstract tool interfaces. All three frameworks work technically, but their design philosophies are mutually incompatible.

Committing to a framework means your thinking will be shaped by the assumptions of that framework's designers. If you later develop a different way of thinking — whether through your own practical experience or through a breakthrough in the field — switching frameworks may be more complex than starting from scratch. Migrating from SmolAgents to LangGraph is not merely a rewrite of code, but a transformation of an entire mode of thinking, because the foundational assumptions of the two frameworks are fundamentally incompatible.

### 2.2 The Cost of Premature Lock-in in a Rapidly Evolving Field

Agentic AI is still changing rapidly, and a breakthrough in understanding could occur at any moment. The shift from AutoGen v0.3 to v0.4 was essentially a complete rewrite, which shows that even mature frameworks may face fundamental rethinking. Premature lock-in not only creates technical debt, but limits your ability to fully understand the field. When you are constrained by a framework's abstractions, you cannot see the underlying real mechanisms; when new understanding emerges, you have already invested too much to pivot.

This problem does not exist in iOS development, because the foundations of GUI programming have been stable for decades. The reason MVC works is because it is built on foundations that have been validated and are unlikely to change. But the foundations of Agentic AI are still in flux. The high-level abstractions of frameworks are inherently fragile because they are built on assumptions that have not yet settled.

### 2.3 The Limited Real-World Value of Frameworks

From the perspective of short-term benefits, existing frameworks offer far less value than advertised. Building a complete Agent system (LLM + tool protocol + multi-round orchestration) takes only five minutes. This system contains all the core elements of Agentic AI: a language model that can call tools, a protocol that defines the tool interface, and a loop that manages multi-round conversation. Frameworks don't save much effort, and when you need customization they increase complexity.

What's worse, many frameworks suffer from over-abstraction. When you need to connect to existing interfaces or do custom work (which is very common in enterprise environments), you often have to trace through eight layers of abstract interfaces to find the place that needs modification. LangChain is notoriously infamous for this: you want to make a simple change, but find yourself deep in a class inheritance tree with each layer adding new abstractions. This is a typical failure pattern in fast-evolving fields — the framework's high-level abstractions replace the builder's intuition, and the result becomes an obstacle instead.

### 2.4 The Fundamental Difference Between Framework and Library

An important distinction needs to be made here. Not all Agentic AI tools are "frameworks." pi-mono provides an illuminating contrast: it is a library, not a framework. pi-mono provides only four basic tools (read, write, edit, bash), and the system prompt is no longer than 1,000 tokens. Its design philosophy is "what is missing is more important than what is included" — the author explicitly declined MCP support, sub-agents, plan mode, and other "trending" features, because these would increase context overhead or introduce black boxes.

Frameworks impose a worldview; libraries merely provide tools. A framework says "this is how you should think about problems"; a library says "here are tools you can use — how you use them is up to you." LangGraph is a framework; pi-mono is a library. This distinction is crucial, because libraries give you choices, while frameworks limit your choices.

---

## 3. Application Criteria

### 3.1 When to Use a Framework vs. a Library

| Scenario | Use a Framework | Use a Library |
|----------|-----------------|---------------|
| **Domain maturity** | Core concepts are stable (e.g., iOS GUI) | Domain is still rapidly evolving (e.g., Agentic AI) |
| **Team size** | Large team needs a unified way of thinking | Small team or solo project |
| **Customization needs** | Low (the framework's defaults are sufficient) | High (frequent need to modify underlying logic) |
| **Learning curve** | Willing to invest time learning the framework's concepts | Prefer to get started quickly and deepen gradually |
| **Long-term stability** | The framework's major versions won't change | Can accept changes in the underlying implementation |
| **Integration complexity** | Integrations within the framework are simple | Need to connect multiple external systems |

### 3.2 Decision Criteria

Before choosing a framework, ask yourself these questions:

1. **Are the foundational concepts of this field already stable?** If the answer is no, the framework's high-level abstractions will quickly become obsolete.
2. **Do I understand the framework's core assumptions?** If you cannot clearly articulate what the framework author's worldview is, you are not yet ready to be locked into it.
3. **If I need to change my way of thinking, what is the migration cost?** If the migration cost is high, the risk of choosing a framework is great.
4. **Does the framework provide AI-friendly documentation?** If the framework's documentation cannot be directly understood and used by AI tools (like Cursor), its value in the AI era is greatly diminished.
5. **Can I quickly build a prototype without using the framework?** If yes, then the value of the framework is limited.

---

## 4. Pitfalls and Insights

### 4.1 The "Eight Layers of Abstraction" Nightmare

When using an over-abstracted framework, a simple modification becomes a nightmare. You want to change the behavior of a tool, but the tool is wrapped in a class that inherits from another class, which depends on a third class... ultimately you find yourself needing to understand eight layers of abstract interfaces just to find the place that actually needs to change. This wastes time and leaves your understanding of the framework fragmented.

This problem is especially severe in fast-evolving fields, because framework designers cannot anticipate all use cases. Their abstraction assumptions will quickly become outdated, and you are stuck in those outdated assumptions. pi-mono's author explicitly criticized this: they said "over-abstraction is the failure pattern of fast-developing fields."

### 4.2 The Insight of the "Five-Minute Prototype"

Building a basic Agent system takes only five minutes. This fact matters because it shows that the value of a framework lies primarily not in saving initial development time, but in providing a "best practices" template. But in a fast-evolving field like Agentic AI, "best practices" are themselves uncertain. The framework author's best practices may be obsolete in six months.

This means that rather than relying on a framework's "best practices," it is better to build the system from first principles yourself. The additional cost of doing this is small (because the basic system is simple), but the benefits are great (because you maintain complete flexibility and depth of understanding).

### 4.3 The Shift to "Builder's Mindset"

Frameworks encourage a passive tool-user mentality: you learn the framework's API, think the way the framework does, and accept the framework's constraints. But the Agentic AI era calls for a builder's mindset: when existing tools don't meet your needs, you should be able to quickly build your own tools. This shift in thinking is critical.

pi-mono's design embodies this: it provides a minimal toolset, then encourages users to extend functionality by writing Extensions (TypeScript modules) or Skills (markdown files). When an Agent needs a new capability, it can read the code of existing extensions, write a new extension, and have it take effect immediately. This is a shift from "using a framework" to "building your own tools."

### 4.4 The Absence of "AI-Friendly Documentation"

Existing Agentic AI frameworks all lack documentation designed specifically for AI. LangGraph, AutoGen, and SmolAgents documentation is all written for humans, full of the vagueness and implicit assumptions of natural language. When AI tools (like Cursor) try to use these frameworks, they must do extensive trial and error because the information in the documentation isn't precise enough.

By contrast, pi-mono's tools are themselves code, and the documentation is the code's comments and README. This allows AI to read and understand directly, without additional explanation. This is an important design insight: in the AI era, the usability of a tool depends not only on whether humans can understand it, but also on whether AI can understand it.

---

## 5. Related Axioms

**A9. Builder's Mindset is a Moat** — The decision to choose a framework should be based on whether you have the ability and willingness to be a builder. If you choose a framework, you give up the flexibility of a builder; if you stay with the library approach, you preserve the power of a builder.

---

## 6. Practical Recommendations

### 6.1 How to Make Framework Choices in the Agentic AI Field

1. **Start from first principles**: don't jump straight to a framework. First understand the core concepts of an Agent: LLM, tools, multi-round orchestration. Use agentic programming tools like Cursor to gradually build your own system. This process is itself learning.

2. **Stay framework-neutral**: before the field stabilizes, don't deeply depend on any framework. If you must use a framework, choose ones that provide minimal abstractions (like pi-mono), rather than ones that impose a worldview (like LangGraph).

3. **Reassess regularly**: every three months, ask yourself: is my current framework choice still reasonable? What new understanding has emerged in the field? Am I being constrained by the framework's limitations?

4. **Invest in transferable knowledge**: don't just learn a framework's API — learn the foundational concepts of Agentic AI. This knowledge is useful in any framework, while a framework's API will keep changing.

5. **Embrace the builder's mindset**: when a framework doesn't meet your needs, don't try to force it to fit — build your own tools. In the AI era, this has become especially easy, because AI can help you prototype quickly.

### 6.2 When a Framework Can Be Considered

Only when all of the following conditions are met is it worth considering a framework:

- The domain's foundational concepts are already stable (at least 2–3 years without a fundamental change)
- The framework's major versions remain stable (not subject to frequent major overhauls)
- Your team is large enough that a unified way of thinking is needed to coordinate
- The "best practices" provided by the framework genuinely and significantly accelerate development
- The framework's documentation is clear enough for AI tools to understand as well

In the Agentic AI field, none of these conditions are currently met. So now is not the time to choose a framework.

---

## 7. Summary

Framework choice is a long-term commitment that affects your way of thinking, your learning path, and your adaptability. In a fast-evolving field, this commitment carries high risk. Agentic AI is still rapidly evolving, foundational concepts are still settling, and any framework's worldview may be proven incomplete or wrong in the near future.

The wisest approach is to remain framework-neutral, start from first principles, use libraries rather than frameworks, and embrace the builder's mindset. The cost of doing this is low (because the basic system is simple), but the benefits are high (because you maintain complete flexibility and depth of understanding). When the field eventually stabilizes, the value of frameworks will truly become apparent. By then, you will already have enough knowledge and experience to make a wise choice.
