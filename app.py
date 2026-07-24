#!/usr/bin/env python3
"""
Tech Stack Recommender - Main Application Entry Point
Content-Based Filtering using TF-IDF Vectorization & Cosine Similarity.
"""

import os
import sys
import json
from typing import List, Dict, Any

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

        # FIX: Ensure directory structure exists on host before saving file to prevent crash
        os.makedirs(os.path.dirname(self.model_file), exist_ok=True)

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
        from flask import Flask, request, jsonify, render_template_string, send_from_directory
        
        # FIX: Check if flask_cors is available to enable cross-origin requests
        try:
            from flask_cors import CORS
            has_cors = True
        except ImportError:
            has_cors = False
            
    except ImportError:
        print("Flask is not installed. Installing flask or running in CLI mode.")
        run_cli_interactive()
        return

    app = Flask(__name__)
    
    # FIX: Enable CORS if package is installed (resolves browser frontend blocking issues)
    if has_cors:
        CORS(app)
        print("🔓 CORS successfully enabled for all routes.")
    else:
        print("⚠️ flask-cors is not installed. External websites may have issues querying this API.")

    recommender_service.initialize()

    # Simple HTML template designed to display your custom tab image and the required credit footer
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tech Stack Recommender API</title>
        
        <!-- Tab image link configuration -->
        <link rel="icon" type="image/png" href="{{ url_for('static', filename='favicon.png') }}">
        
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #0f172a;
                color: #e2e8f0;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 60px auto;
                padding: 35px;
                background-color: #1e293b;
                border-radius: 12px;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
                flex: 1;
            }
            h1 {
                color: #38bdf8;
                font-size: 2.2rem;
                margin-top: 0;
                border-bottom: 2px solid #334155;
                padding-bottom: 15px;
            }
            .status {
                display: inline-block;
                background-color: #10b981;
                color: #ffffff;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 25px;
            }
            .info-section {
                margin-bottom: 30px;
            }
            .info-section h3 {
                color: #94a3b8;
                margin-bottom: 10px;
                font-size: 1.1rem;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background-color: #0f172a;
                margin-bottom: 12px;
                padding: 14px 18px;
                border-radius: 8px;
                border-left: 4px solid #38bdf8;
            }
            .endpoint-method {
                font-weight: bold;
                color: #38bdf8;
                margin-right: 10px;
            }
            footer {
                text-align: center;
                padding: 25px;
                color: #94a3b8;
                background-color: #0f172a;
                font-size: 0.95rem;
                border-top: 1px solid #1e293b;
                letter-spacing: 0.5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Tech Stack Recommender API</h1>
            <span class="status">● Service Status: Online & Ready</span>
            
            <div class="info-section">
                <h3>About the Service</h3>
                <p>This is a Content-Based Filtering recommendation service that utilizes <strong>TF-IDF Vectorization</strong> and <strong>Cosine Similarity</strong> to recommend technology stacks based on project requirements and developer skills.</p>
            </div>

            <div class="info-section">
                <h3>Available Endpoints</h3>
                <ul>
                    <li><span class="endpoint-method">GET</span> <code>/api/stacks</code> - Retrieve dataset tech stacks</li>
                    <li><span class="endpoint-method">POST</span> <code>/api/recommend</code> - Get TF-IDF Cosine Similarity recommendations</li>
                    <li><span class="endpoint-method">POST</span> <code>/api/retrain</code> - Reload dataset and retrain vectorizer</li>
                </ul>
            </div>
        </div>
        
        <footer>
            This webapp is developed by Muhammad Sufiyan Farzad
        </footer>
    </body>
    </html>
    """

    @app.route('/', methods=['GET'])
    def home():
        return render_template_string(HTML_TEMPLATE)

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        static_dir = os.path.join(app.root_path, 'static')
        filename = 'favicon.ico' if os.path.exists(os.path.join(static_dir, 'favicon.ico')) else 'favicon.png'
        mimetype = 'image/vnd.microsoft.icon' if filename.endswith('.ico') else 'image/png'
        return send_from_directory(static_dir, filename, mimetype=mimetype)

    @app.route('/api/stacks', methods=['GET'])
    def get_stacks():
        return jsonify({'status': 'success', 'data': recommender_service.get_all_stacks()})

    @app.route('/api/recommend', methods=['POST'])
    def recommend():
        try:
            data = request.get_json(force=True) or {}
            query = data.get('query', '')
            top_n = int(data.get('top_n', 5))
            if not query:
                return jsonify({'status': 'error', 'message': 'Missing query parameter'}), 400

            result = recommender_service.recommend_for_query(query, top_n=top_n)
            return jsonify({'status': 'success', 'data': result})
        except Exception as e:
            # Clean logging of error back to the client to make debugging simpler
            return jsonify({'status': 'error', 'message': f'Server failed to process recommendation: {str(e)}'}), 500

    @app.route('/api/retrain', methods=['POST'])
    def retrain():
        recommender_service.initialize(force_retrain=True)
        return jsonify({'status': 'success', 'message': 'Model retrained successfully'})

    print(f" Starting Flask REST API server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False) # Turned off debug=True for production environments


if __name__ == '__main__':
    if '--cli' in sys.argv:
        run_cli_interactive()
    else:
        # FIX: Dynamically read the assigned port from environment variables
        assigned_port = int(os.environ.get("PORT", 5000))
        run_flask_app(port=assigned_port)