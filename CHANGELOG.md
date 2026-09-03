# Changelog

## [1.0.0] - 2026-09-03

- Version bump to 1.0.0 to declare the public API stable. No breaking changes —
  `EpisodicMemory`/`Episode`/`EpisodicMemoryError` behavior is unchanged from 0.2.1.
- Added `features.md` documenting the feature set and a competitor comparison.

## [0.2.1] - 2026-09-01

- Metadata: added `maintainers` (Sonia, Vishwanil Suman) to `pyproject.toml`,
  and added Contributor badges for both to the README (Sonia's linked to
  her GitHub profile, https://github.com/dahiyasonia). No code changes.

## [0.2.0] - 2026-09-01

- Added: `EpisodicMemory` supports the context-manager protocol
  (`with EpisodicMemory(...) as mem:`), closing its connection
  automatically.

## [0.1.0] - 2026-08-31

- Initial release: `EpisodicMemory` (SQLite-persisted, structured task/outcome log) and
  `Episode` (frozen dataclass: `task`, `outcome`, `actions_taken`, `notes`, `timestamp`).
- Relevance scoring reuses `autourgos-semantic-memory`'s `KeywordRetriever` (TF-IDF) rather
  than duplicating that algorithm.
- `outcome` is validated to one of `"success"`, `"fail"`, `"partial"`.
