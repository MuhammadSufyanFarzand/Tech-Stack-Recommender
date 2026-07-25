import os
import math
import pickle
import json
from typing import List, Dict, Any, Tuple, Union

class TFIDFVectorizerModel:
    """
    TF-IDF Vectorizer wrapper with scikit-learn support and built-in pure Python math fallback.
    Computes Term Frequency (TF) and Inverse Document Frequency (IDF) representations.
    """

    def __init__(self, max_features: int = 500, ngram_range: Tuple[int, int] = (1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vocabulary_: Dict[str, int] = {}
        self.feature_names_: List[str] = []
        self.idf_weights_: List[float] = []
        self.is_sklearn = False
        self.sklearn_vectorizer = None

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.sklearn_vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                stop_words='english',
                sublinear_tf=True
            )
            self.is_sklearn = True
        except ImportError:
            self.is_sklearn = False

    def _generate_ngrams(self, text: str) -> List[str]:
        tokens = text.split()
        ngrams = []
        min_n, max_n = self.ngram_range
        for n in range(min_n, max_n + 1):
            for i in range(len(tokens) - n + 1):
                ngrams.append(" ".join(tokens[i:i+n]))
        return ngrams

    def fit_transform(self, corpus: List[str]):
        """
        Fits vectorizer vocabulary and computes TF-IDF feature matrix for given document corpus.
        Returns matrix as list of vectors (2D array).
        """
        if self.is_sklearn and self.sklearn_vectorizer is not None:
            tfidf_matrix = self.sklearn_vectorizer.fit_transform(corpus)
            self.feature_names_ = self.sklearn_vectorizer.get_feature_names_out().tolist()
            self.idf_weights_ = self.sklearn_vectorizer.idf_.tolist()
            self.vocabulary_ = self.sklearn_vectorizer.vocabulary_
            return tfidf_matrix.toarray().tolist()

        # Pure Python standard math implementation fallback
        doc_ngrams_list = [self._generate_ngrams(doc) for doc in corpus]
        
        # Count document frequencies across corpus
        doc_freq: Dict[str, int] = {}
        term_total_freq: Dict[str, int] = {}

        for doc_ngrams in doc_ngrams_list:
            unique_terms = set(doc_ngrams)
            for term in unique_terms:
                doc_freq[term] = doc_freq.get(term, 0) + 1
            for term in doc_ngrams:
                term_total_freq[term] = term_total_freq.get(term, 0) + 1

        # Select top max_features by total frequency
        sorted_terms = sorted(term_total_freq.keys(), key=lambda t: term_total_freq[t], reverse=True)
        top_terms = sorted_terms[:self.max_features] if self.max_features else sorted_terms

        self.vocabulary_ = {term: idx for idx, term in enumerate(top_terms)}
        self.feature_names_ = top_terms

        num_docs = len(corpus)
        # Compute IDF: idf(t) = log((1 + N) / (1 + df(t))) + 1
        self.idf_weights_ = [
            math.log((1.0 + num_docs) / (1.0 + doc_freq.get(term, 0))) + 1.0
            for term in top_terms
        ]

        # Compute TF-IDF matrix for each doc
        matrix = []
        for doc_ngrams in doc_ngrams_list:
            vector = [0.0] * len(top_terms)
            total_tokens = max(1, len(doc_ngrams))
            
            # Count term frequencies in document
            tf_counts: Dict[str, int] = {}
            for term in doc_ngrams:
                if term in self.vocabulary_:
                    tf_counts[term] = tf_counts.get(term, 0) + 1

            for term, count in tf_counts.items():
                idx = self.vocabulary_[term]
                # Sublinear TF scaling: 1 + log(tf)
                tf_val = 1.0 + math.log(count)
                vector[idx] = tf_val * self.idf_weights_[idx]

            # L2 Euclidean normalization
            squared_sum = sum(v * v for v in vector)
            norm = math.sqrt(squared_sum) if squared_sum > 0 else 1.0
            norm_vector = [v / norm for v in vector]
            matrix.append(norm_vector)

        return matrix

    def transform(self, queries: Union[List[str], str]) -> List[List[float]]:
        """
        Transforms unseen text queries into TF-IDF vector space using fitted vocabulary and IDFs.
        """
        if isinstance(queries, str):
            queries = [queries]

        if self.is_sklearn and self.sklearn_vectorizer is not None:
            tfidf_matrix = self.sklearn_vectorizer.transform(queries)
            return tfidf_matrix.toarray().tolist()

        matrix = []
        for q in queries:
            ngrams = self._generate_ngrams(q)
            vector = [0.0] * len(self.feature_names_)
            
            tf_counts: Dict[str, int] = {}
            for term in ngrams:
                if term in self.vocabulary_:
                    tf_counts[term] = tf_counts.get(term, 0) + 1

            for term, count in tf_counts.items():
                idx = self.vocabulary_[term]
                tf_val = 1.0 + math.log(count)
                vector[idx] = tf_val * self.idf_weights_[idx]

            squared_sum = sum(v * v for v in vector)
            norm = math.sqrt(squared_sum) if squared_sum > 0 else 1.0
            norm_vector = [v / norm for v in vector]
            matrix.append(norm_vector)

        return matrix

    def get_feature_names(self) -> List[str]:
        """Returns vocabulary feature terms."""
        return self.feature_names_

    def save_model(self, model_path: str):
        """Saves vectorizer weights and vocabulary to pickle/json file."""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        if self.is_sklearn and self.sklearn_vectorizer is not None:
            with open(model_path, 'wb') as f:
                pickle.dump(self.sklearn_vectorizer, f)
        else:
            state = {
                'vocabulary_': self.vocabulary_,
                'feature_names_': self.feature_names_,
                'idf_weights_': self.idf_weights_,
                'max_features': self.max_features,
                'ngram_range': self.ngram_range
            }
            json_path = model_path.replace('.pkl', '.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)

    def load_model(self, model_path: str):
        """Loads fitted vectorizer weights and vocabulary."""
        if os.path.exists(model_path) and model_path.endswith('.pkl'):
            try:
                with open(model_path, 'rb') as f:
                    self.sklearn_vectorizer = pickle.load(f)
                    self.is_sklearn = True
                    self.feature_names_ = self.sklearn_vectorizer.get_feature_names_out().tolist()
                    self.idf_weights_ = self.sklearn_vectorizer.idf_.tolist()
                    self.vocabulary_ = self.sklearn_vectorizer.vocabulary_
                    return
            except Exception:
                pass

        json_path = model_path.replace('.pkl', '.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.vocabulary_ = state['vocabulary_']
                self.feature_names_ = state['feature_names_']
                self.idf_weights_ = state['idf_weights_']
                self.max_features = state.get('max_features', 500)
                self.ngram_range = tuple(state.get('ngram_range', (1, 2)))
                self.is_sklearn = False
