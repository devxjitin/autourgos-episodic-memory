# Changelog

## [0.1.0] - 2026-08-31

- Initial release: `EpisodicMemory` (SQLite-persisted, structured task/outcome log) and
  `Episode` (frozen dataclass: `task`, `outcome`, `actions_taken`, `notes`, `timestamp`).
- Relevance scoring reuses `autourgos-semantic-memory`'s `KeywordRetriever` (TF-IDF) rather
  than duplicating that algorithm.
- `outcome` is validated to one of `"success"`, `"fail"`, `"partial"`.
