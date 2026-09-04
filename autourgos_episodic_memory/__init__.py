"""
autourgos-episodic-memory — Structured task/outcome log for Autourgos agents.

Records what an agent tried and what happened (success/fail/partial), so a
future run can retrieve relevant past attempts before repeating a
known-bad approach. Persisted to SQLite; relevance scoring reuses
autourgos-semantic-memory's TF-IDF KeywordRetriever.

    from autourgos_episodic_memory import EpisodicMemory

    memory = EpisodicMemory(db_path="episodes.db")
    memory.remember(
        task="Deploy the app to production",
        outcome="fail",
        actions_taken=["ran deploy.sh", "hit permission error on S3 bucket"],
        notes="Needs IAM role update before retrying.",
    )

    for ep in memory.retrieve("deploying the app", top_k=3):
        print(ep.content)
"""
from .memory import Episode, EpisodicMemory, EpisodicMemoryError

from autourgos_core import package_version

__version__ = package_version("autourgos-episodic-memory", fallback="1.0.1")

__all__ = ["EpisodicMemory", "Episode", "EpisodicMemoryError"]
