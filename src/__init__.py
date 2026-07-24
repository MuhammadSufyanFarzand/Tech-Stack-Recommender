"""
Tech Stack Recommender Package
Author: AI/ML Engineering Team
Description: Content-Based Filtering Tech Stack Recommender using TF-IDF Vectorization & Cosine Similarity.
"""

from .ingestion import SkillIngestor
from .vectorizer import TFIDFVectorizerModel
from .similarity import CosineSimilarityEngine

__version__ = "1.0.0"
__all__ = ["SkillIngestor", "TFIDFVectorizerModel", "CosineSimilarityEngine"]
