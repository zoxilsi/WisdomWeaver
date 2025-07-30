"""
Helper to load the RAG system for web applications.
Usage: from load_rag import get_rag_system
"""

import os
from functools import lru_cache
from rag_bhagavad_gita import BhagavadGitaRAG

@lru_cache(maxsize=1)
def get_rag_system(csv_path: str = 'bhagavad_gita_verses.csv'):
    """Get cached RAG system instance."""
    return BhagavadGitaRAG(csv_path)

# For direct import
rag = get_rag_system()
