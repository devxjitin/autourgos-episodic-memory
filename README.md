# autourgos-episodic-memory

[![Framework: Autourgos](https://img.shields.io/badge/Framework-Autourgos-orange.svg)](https://github.com/devxjitin)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/autourgos-episodic-memory/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/devxjitin/autourgos-episodic-memory/blob/main/LICENSE)
[![Author](https://img.shields.io/badge/Author-Jitin%20Kumar%20Sengar-blue.svg)](https://github.com/devxjitin)
[![Contributor](https://img.shields.io/badge/Contributor-Sonia-blueviolet.svg)](https://github.com/dahiyasonia)
[![Contributor](https://img.shields.io/badge/Contributor-Vishwanil%20Suman-blueviolet.svg)]()

Structured task/outcome log for [Autourgos](https://github.com/devxjitin) agents. Unlike the
freeform conversational recall the rest of the memory family provides, `EpisodicMemory`
records **what was tried and what happened** — so a future run can check "have I attempted
this before, and did it work?" before repeating a known-bad approach.

```python
from autourgos_episodic_memory import EpisodicMemory

memory = EpisodicMemory(db_path="episodes.db")  # persists across restarts

memory.remember(
    task="Deploy the app to production",
    outcome="fail",
    actions_taken=["ran deploy.sh", "hit permission error on S3 bucket"],
    notes="Needs IAM role update before retrying.",
)

for episode in memory.retrieve("deploying the app", top_k=3):
    print(episode.metadata["outcome"], "-", episode.content)
```

---

## Table of Contents

- [Install](#install)
- [Why a separate package](#why-a-separate-package)
- [Quick Start](#quick-start)
- [Constructor Reference](#constructor-reference)
- [License](#license)

---

## Install

```bash
pip install autourgos-episodic-memory
```

Depends on `autourgos-memory` and `autourgos-semantic-memory` (its TF-IDF `KeywordRetriever`
does the relevance scoring — this package doesn't reimplement it). SQLite persistence is
stdlib, no extra dependency.

---

## Why a separate package

The rest of the memory family stores *conversation* (what was said). `EpisodicMemory` stores
*attempts* (what was done and whether it worked) — a different shape of data with its own
`outcome` field (`"success"` / `"fail"` / `"partial"`) and `actions_taken` list, not a chat
turn. Keeping it separate from `autourgos-vector-memory`/`autourgos-semantic-memory` avoids
conflating "recall a relevant past conversation" with "recall a relevant past task result."

---

## Quick Start

```python
from autourgos_episodic_memory import EpisodicMemory

memory = EpisodicMemory(db_path="agent_episodes.db", max_episodes=500)

memory.remember(
    task="Fix the failing test suite",
    outcome="success",
    actions_taken=["reran pytest -x", "found stale fixture", "regenerated fixture"],
)

memory.remember(
    task="Fix the failing test suite",
    outcome="fail",
    actions_taken=["tried deleting __pycache__"],
    notes="Did not address the root cause.",
)

# Before trying again, check what happened last time:
past = memory.retrieve("failing test suite", top_k=5)
for ep in past:
    print(f"[{ep.metadata['outcome']}] {ep.metadata['task']}")
```

`db_path=":memory:"` (the default) keeps everything in RAM for the process lifetime. Pass a
real file path for recall across restarts — episodes are reloaded and re-indexed on the next
`EpisodicMemory(db_path=...)` construction.

`EpisodicMemory` supports the context-manager protocol, closing its connection automatically:

```python
with EpisodicMemory(db_path="agent_episodes.db") as memory:
    memory.remember(task="Deploy the app", outcome="success")
# connection is closed here automatically
```

---

## Constructor Reference

### `EpisodicMemory`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `db_path` | `str` | `":memory:"` | SQLite file path, or `:memory:` for no persistence |
| `max_episodes` | `int`, optional | `None` | Oldest episodes dropped once this count is exceeded |

### `EpisodicMemory.remember(task, outcome, actions_taken=None, notes="")`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task` | `str` | yes | What was attempted. Non-empty. |
| `outcome` | `str` | yes | One of `"success"`, `"fail"`, `"partial"` |
| `actions_taken` | `list[str]` | no | Steps taken during the attempt |
| `notes` | `str` | no | Freeform extra context (why it failed, what to try next, etc.) |

Returns an `Episode` (frozen dataclass with `task`/`outcome`/`actions_taken`/`notes`/`timestamp`).

### `EpisodicMemory.retrieve(query, top_k=5)`

Returns a list of `autourgos_memory.Document`, ranked by TF-IDF relevance to `query`. Each
`Document.metadata` carries `task`, `outcome`, `actions_taken`, `notes`, `timestamp`.

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).
