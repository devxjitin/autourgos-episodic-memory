# autourgos-episodic-memory — Features

A structured task/outcome log for Autourgos agents. Unlike the rest of the memory family, which stores conversation, `EpisodicMemory` stores **attempts** — what was tried, whether it worked, and what actions were taken — so a future run can check "have I done this before, and did it succeed?" before repeating a known-bad approach.

## Full Feature List

- `EpisodicMemory.remember(task, outcome, actions_taken=None, notes="")` — records one attempt; `outcome` is one of `"success"` / `"fail"` / `"partial"`; returns a frozen `Episode` dataclass (`task`/`outcome`/`actions_taken`/`notes`/`timestamp`)
- `EpisodicMemory.retrieve(query, top_k=5)` — TF-IDF relevance-ranked recall of past episodes matching a query, returned as `autourgos_memory.Document` objects carrying the original episode fields in `metadata`
- SQLite persistence (`db_path=`) — survives restarts, episodes are reloaded and re-indexed on the next construction; `db_path=":memory:"` (default) for ephemeral in-process use
- `max_episodes` — oldest episodes dropped once the cap is exceeded
- Context-manager support (`with EpisodicMemory(...) as memory:`), closing the connection automatically
- Deliberately a separate data shape from conversational memory — keeps "recall a relevant past conversation" (handled by `autourgos-vector-memory`/`autourgos-semantic-memory`) distinct from "recall a relevant past task result"
- Depends on `autourgos-memory` (base interfaces) and `autourgos-semantic-memory` (its TF-IDF `KeywordRetriever` does the actual relevance scoring — no relevance logic is reimplemented here); SQLite persistence itself is stdlib, no extra dependency

## Competitor Comparison

There is no mainstream, standalone Python package doing exactly this narrow thing (a typed, queryable task/outcome log as a first-class memory primitive). The closest comparisons are the *pattern* this package implements — the Reflexion-style "episodic memory of past attempts" — and the broader agent-memory platforms that include something adjacent as one feature among many.

| Capability | **autourgos-episodic-memory** | [Reflexion (research pattern/reference implementations)](https://arxiv.org/abs/2303.11366) | [Letta (MemGPT lineage)](https://www.letta.com/) | [Mem0](https://mem0.ai/) | Hand-rolled logging table |
|---|---|---|---|---|---|
| Scope | Standalone, focused library — one job | Research pattern; various non-standardized reference/community implementations | Full agent-memory platform (self-editing context, archival/recall memory) | Managed/self-hosted cross-session memory-extraction layer | DIY |
| Explicit `task`/`outcome`/`actions_taken` schema | Yes, first-class typed `Episode` | Conceptually yes, but as free-text "self-reflection" strings, not a structured outcome field | Not a dedicated outcome-log schema — memory is general fact/context blocks | Not outcome-structured — extracts general facts/preferences, not pass/fail task records | Whatever you build |
| Success/fail/partial outcome tracking | Yes, explicit enum-like field | Implicit in the reflection text, not queryable as a field | No dedicated field | No dedicated field | Possible if designed in |
| Relevance-ranked retrieval of past attempts | Yes, TF-IDF via `autourgos-semantic-memory` | Typically just prepended to context, not retrieval-ranked across many past trials | Yes, via its recall-memory search | Yes, via its retrieval layer (semantic/vector-based) | Only if built |
| Persistence | Yes, SQLite file or in-memory | Not standardized — depends on the implementation | Yes, managed/self-hosted store | Yes, managed | Depends |
| Standalone, no framework lock-in | Yes — depends only on `autourgos-memory`/`autourgos-semantic-memory` | N/A (a pattern, not a package) | No — adopting Letta means adopting its agent runtime/server model | Partial — SDK-based but can be used with any agent stack | Yes |
| Dependencies | `autourgos-memory`, `autourgos-semantic-memory`, stdlib SQLite | N/A | Full platform/server | SDK + managed backend (or self-hosted vector store) | None |
| Pricing | Free, open source | Free (research) | Free (self-hosted) / paid (managed) | Free tier + paid managed plans | Free |

### How to read this

- **This is a narrow, honest niche**: there is no direct one-to-one competing *package* for "structured task/outcome episodic log" — it's a pattern (Reflexion) more often built ad hoc inside a larger agent system than shipped as its own installable library. autourgos-episodic-memory's actual competitive position is "the smallest possible dependency to get that pattern with a typed schema and TF-IDF recall," not displacing a mature product category.
- **vs. Reflexion-style hand-rolled reflection**: most Reflexion implementations store free-text self-critiques, not a structured, queryable `outcome` field — this package trades some of that narrative richness for a schema you can filter/aggregate on (e.g. "how many times has this task failed?").
- **vs. Letta/Mem0**: both are much larger platforms whose "remember what happened" capability is one feature inside a broader self-editing or fact-extraction memory system, not a dedicated task/outcome ledger; adopting either means adopting their runtime or managed service, whereas this package is a small, composable SQLite-backed class.
- **Genuine gap to flag**: because there's no like-for-like package competitor, the fairest comparison is against the pattern and against rolling your own — if a team already has Letta or Mem0 in their stack, this package is redundant with what those platforms already do less explicitly.

Sources:
- [Reflexion Agent Pattern — Agent Patterns documentation](https://agent-patterns.readthedocs.io/en/stable/patterns/reflexion.html)
- [The Memory Problem in AI Agents Is Half Solved. Here's the Other Half.](https://medium.com/data-unlocked/the-memory-problem-in-ai-agents-is-half-solved-heres-the-other-half-ebbf218ae4d5)
- [Episodic Memory in AI Agents - GeeksforGeeks](https://www.geeksforgeeks.org/artificial-intelligence/episodic-memory-in-ai-agents/)
- [Best AI Agent Memory Frameworks in 2026: Compared and Ranked](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/)
- [Best Memory Layer for AI Agents in 2026: Mem0 vs Zep vs Letta vs More](https://www.stork.ai/blog/best-memory-layer-ai-agents-2026)
