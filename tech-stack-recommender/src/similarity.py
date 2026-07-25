import math
from typing import List, Dict, Any, Tuple, Union

class CosineSimilarityEngine:
    """
    Computes Cosine Similarity scores between query vector and tech stack feature vectors.
    Ranks recommendations and extracts salient matching terms.
    """

    @staticmethod
    def dot_product(vec_a: List[float], vec_b: List[float]) -> float:
        """Calculates dot product between two equal-length numeric vectors."""
        return sum(a * b for a, b in zip(vec_a, vec_b))

    @staticmethod
    def vector_norm(vec: List[float]) -> float:
        """Calculates L2 Euclidean norm of a numeric vector."""
        return math.sqrt(sum(v * v for v in vec))

    @classmethod
    def compute_similarity(cls, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes cosine similarity between two vectors: dot(a, b) / (norm(a) * norm(b)).
        Bounded between 0.0 and 1.0 for positive TF-IDF vectors.
        """
        dot = cls.dot_product(vec_a, vec_b)
        norm_a = cls.vector_norm(vec_a)
        norm_b = cls.vector_norm(vec_b)

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        similarity = dot / (norm_a * norm_b)
        # Numerical precision clamp
        return max(0.0, min(1.0, float(similarity)))

    @classmethod
    def recommend(
        cls,
        query_vector: List[float],
        dataset_vectors: List[List[float]],
        dataset_records: List[Dict[str, Any]],
        feature_names: List[str],
        top_n: int = 5,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Ranks dataset items by cosine similarity to query vector.
        Extracts overlapping terms and term contribution weights.
        """
        results = []

        for idx, (doc_vector, record) in enumerate(zip(dataset_vectors, dataset_records)):
            sim_score = cls.compute_similarity(query_vector, doc_vector)

            if sim_score >= min_score:
                # Find matching non-zero terms contributing to similarity
                matching_terms = []
                for f_idx, (q_val, d_val) in enumerate(zip(query_vector, doc_vector)):
                    if q_val > 0.0 and d_val > 0.0:
                        term_name = feature_names[f_idx] if f_idx < len(feature_names) else f"term_{f_idx}"
                        contribution = q_val * d_val
                        matching_terms.append({
                            'term': term_name,
                            'query_weight': round(q_val, 4),
                            'doc_weight': round(d_val, 4),
                            'contribution': round(contribution, 4)
                        })

                # Sort matching terms by contribution descending
                matching_terms.sort(key=lambda x: x['contribution'], reverse=True)

                results.append({
                    'rank': 0,
                    'similarity_score': round(sim_score, 4),
                    'match_percentage': round(sim_score * 100, 1),
                    'stack_id': record.get('stack_id'),
                    'stack_name': record.get('stack_name'),
                    'category': record.get('category'),
                    'roles': record.get('roles'),
                    'primary_language': record.get('primary_language'),
                    'frameworks_libraries': record.get('frameworks_libraries'),
                    'database_storage': record.get('database_storage'),
                    'infrastructure_tools': record.get('infrastructure_tools'),
                    'skills_description': record.get('skills_description'),
                    'matching_terms': matching_terms[:8]
                })

        # Sort overall recommendations by cosine similarity score descending
        results.sort(key=lambda item: item['similarity_score'], reverse=True)

        # Assign 1-indexed ranks
        for rank_idx, item in enumerate(results[:top_n], start=1):
            item['rank'] = rank_idx

        return results[:top_n]
