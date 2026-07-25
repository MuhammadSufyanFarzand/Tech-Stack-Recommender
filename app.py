#!/usr/bin/env python3
"""
Tech Stack Recommender - Main Application Entry Point
Content-Based Filtering using TF-IDF Vectorization & Cosine Similarity.
"""

import os
import sys
import json
from typing import List, Dict, Any

# Ensure src package is in Python import path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ingestion import SkillIngestor
from src.vectorizer import TFIDFVectorizerModel
from src.similarity import CosineSimilarityEngine

class TechStackRecommenderService:
    """
    Service orchestration layer connecting Ingestion, Vectorizer, and Similarity Engine.
    """

    def __init__(self, data_path: str = None, model_dir: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = data_path or os.path.join(base_dir, "data", "raw_skills.csv")
        self.model_dir = model_dir or os.path.join(base_dir, "models")
        self.model_file = os.path.join(self.model_dir, "tfidf_vectorizer.pkl")

        self.ingestor = SkillIngestor(self.data_path)
        self.vectorizer = TFIDFVectorizerModel(max_features=500, ngram_range=(1, 2))
        self.processed_records: List[Dict[str, Any]] = []
        self.dataset_vectors: List[List[float]] = []
        self.is_initialized = False

    def initialize(self, force_retrain: bool = False):
        """Loads data, prepares combined feature documents, fits TF-IDF matrix, and saves model."""
        print("🔄 Loading dataset and preparing features...")
        self.processed_records = self.ingestor.prepare_features()

        corpus = [r['combined_features'] for r in self.processed_records]

        print("⚡ Fitting TF-IDF Vectorizer model on corpus...")
        self.dataset_vectors = self.vectorizer.fit_transform(corpus)

        # Save model weights to models/
        self.vectorizer.save_model(self.model_file)
        self.is_initialized = True
        print(f"✅ Initialized recommender with {len(self.processed_records)} tech stacks and {len(self.vectorizer.get_feature_names())} TF-IDF vocabulary terms.")

    def recommend_for_query(self, query_text: str, top_n: int = 5, min_score: float = 0.0) -> Dict[str, Any]:
        """
        Processes query, transforms into TF-IDF vector space, and computes cosine similarity.
        """
        if not self.is_initialized:
            self.initialize()

        cleaned_query = SkillIngestor.clean_text(query_text)
        query_vector = self.vectorizer.transform(cleaned_query)[0]

        recommendations = CosineSimilarityEngine.recommend(
            query_vector=query_vector,
            dataset_vectors=self.dataset_vectors,
            dataset_records=self.processed_records,
            feature_names=self.vectorizer.get_feature_names(),
            top_n=top_n,
            min_score=min_score
        )

        return {
            'query_raw': query_text,
            'query_cleaned': cleaned_query,
            'total_stacks_analyzed': len(self.processed_records),
            'top_n': top_n,
            'recommendations': recommendations
        }

    def get_all_stacks(self) -> List[Dict[str, Any]]:
        if not self.is_initialized:
            self.initialize()
        return [
            {
                'stack_id': r['stack_id'],
                'stack_name': r['stack_name'],
                'category': r['category'],
                'roles': r['roles'],
                'primary_language': r['primary_language'],
                'frameworks_libraries': r['frameworks_libraries'],
                'database_storage': r['database_storage'],
                'infrastructure_tools': r['infrastructure_tools'],
                'skills_description': r['skills_description']
            }
            for r in self.processed_records
        ]


# Global service instance
recommender_service = TechStackRecommenderService()


def run_cli_interactive():
    """Runs interactive command-line interface for recommendation testing."""
    print("=" * 65)
    print("🚀 TECH STACK RECOMMENDER - TF-IDF & COSINE SIMILARITY DEMO")
    print("=" * 65)
    recommender_service.initialize()

    while True:
        print("\nEnter target project requirements, job roles, or developer skills:")
        print("(e.g., 'Looking for a Python backend with FastAPI, PostgreSQL, Docker for ML microservices')")
        user_input = input("\n👉 Query (or 'q' to quit): ").strip()

        if not user_input or user_input.lower() in {'q', 'quit', 'exit'}:
            print("Goodbye!")
            break

        res = recommender_service.recommend_for_query(user_input, top_n=3)
        recs = res['recommendations']

        print(f"\n📊 TOP {len(recs)} RECOMMENDED TECH STACKS:")
        print("-" * 65)
        for r in recs:
            print(f"Rank {r['rank']} | {r['stack_name']} [{r['category']}]")
            print(f"  • Cosine Similarity Match: {r['match_percentage']}% (Score: {r['similarity_score']})")
            print(f"  • Primary Lang: {r['primary_language']}")
            print(f"  • Frameworks: {r['frameworks_libraries']}")
            print(f"  • Database: {r['database_storage']}")
            print(f"  • Matching Key Terms: {', '.join([t['term'] for t in r['matching_terms']]) or 'General alignment'}")
            print("-" * 65)


def run_flask_app(port=5000):
    """Launches Flask HTTP REST API server."""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("Flask is not installed. Installing flask or running in CLI mode.")
        run_cli_interactive()
        return

    app = Flask(__name__)
    recommender_service.initialize()

    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            'service': 'Tech Stack Recommender API',
            'version': '1.0.0',
            'algorithm': 'Content-Based Filtering (TF-IDF Vectorization + Cosine Similarity)',
            'status': 'healthy',
            'endpoints': {
                'GET /api/stacks': 'Retrieve dataset tech stacks',
                'POST /api/recommend': 'Get TF-IDF Cosine Similarity recommendations',
                'POST /api/retrain': 'Reload dataset and retrain vectorizer'
            }
        })

    @app.route('/api/stacks', methods=['GET'])
    def get_stacks():
        return jsonify({'status': 'success', 'data': recommender_service.get_all_stacks()})

    @app.route('/api/recommend', methods=['POST'])
    def recommend():
        data = request.get_json(force=True) or {}
        query = data.get('query', '')
        top_n = int(data.get('top_n', 5))
        if not query:
            return jsonify({'status': 'error', 'message': 'Missing query parameter'}), 400

        result = recommender_service.recommend_for_query(query, top_n=top_n)
        return jsonify({'status': 'success', 'data': result})

    @app.route('/api/retrain', methods=['POST'])
    def retrain():
        recommender_service.initialize(force_retrain=True)
        return jsonify({'status': 'success', 'message': 'Model retrained successfully'})

    print(f"🚀 Starting Flask REST API server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    if '--cli' in sys.argv:
        run_cli_interactive()
    else:
        run_flask_app()
