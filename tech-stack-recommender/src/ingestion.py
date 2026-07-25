import os
import csv
import re
from typing import List, Dict, Any, Union

class SkillIngestor:
    """
    Handles ingestion, data validation, text cleaning, and feature string synthesis
    for tech stack datasets. Supports both pandas DataFrame and standard CSV fallback.
    """

    ENGLISH_STOPWORDS = {
        'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 
        'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 
        'by', 'can', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 
        'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 
        'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 
        'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 
        'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 
        'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 
        'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 
        'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 
        'why', 'with', 'would', 'you', 'your', 'yours', 'yourself', 'yourselves', 'using', 'used',
        'with', 'and', 'for', 'the', 'or', 'to', 'in', 'of', 'a'
    }

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.raw_data: List[Dict[str, Any]] = []
        self.processed_data: List[Dict[str, Any]] = []

    def load_dataset(self) -> List[Dict[str, Any]]:
        """Reads CSV dataset and parses records into structured dictionaries."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset file not found at: {self.data_path}")

        records = []
        try:
            import pandas as pd
            df = pd.read_csv(self.data_path)
            # Fill NaN values with empty strings
            df = df.fillna('')
            records = df.to_dict(orient='records')
        except ImportError:
            # Fallback to standard Python csv reader if pandas is not installed
            with open(self.data_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append({k: (v if v is not None else '') for k, v in row.items()})

        self.raw_data = records
        return self.raw_data

    @classmethod
    def clean_text(cls, text: str) -> str:
        """
        Cleans text by lowercasing, stripping special punctuation while retaining
        programming tokens (like C++, C#, .js), and removing common stop words.
        """
        if not text or not isinstance(text, str):
            return ""

        # Normalize special programming language names
        text = text.replace('C++', 'cpp_lang').replace('C#', 'csharp_lang').replace('.js', 'js_ext')
        
        # Convert to lowercase
        text = text.lower()

        # Remove non-alphanumeric chars except space and underscore
        text = re.sub(r'[^a-z0-9_\s]', ' ', text)

        # Restore special tokens
        text = text.replace('cpp_lang', 'cpp').replace('csharp_lang', 'csharp').replace('js_ext', 'js')

        # Split into tokens
        tokens = text.split()

        # Remove stopwords and short single-character noise (except 'c', 'go', 'r')
        filtered_tokens = [
            t for t in tokens 
            if t not in cls.ENGLISH_STOPWORDS and (len(t) > 1 or t in {'c', 'r'})
        ]

        return " ".join(filtered_tokens)

    def prepare_features(self) -> List[Dict[str, Any]]:
        """
        Synthesizes raw CSV fields into a unified combined feature document string
        for TF-IDF vectorization.
        """
        if not self.raw_data:
            self.load_dataset()

        processed = []
        for row in self.raw_data:
            # Extract attributes
            stack_id = str(row.get('stack_id', ''))
            stack_name = str(row.get('stack_name', ''))
            category = str(row.get('category', ''))
            roles = str(row.get('roles', ''))
            primary_lang = str(row.get('primary_language', ''))
            frameworks = str(row.get('frameworks_libraries', ''))
            database = str(row.get('database_storage', ''))
            infra = str(row.get('infrastructure_tools', ''))
            description = str(row.get('skills_description', ''))

            # Weight primary language and frameworks higher by repeating them in feature string
            raw_feature_string = f"{stack_name} {category} {roles} {primary_lang} {primary_lang} {frameworks} {frameworks} {database} {infra} {description}"
            cleaned_features = self.clean_text(raw_feature_string)

            item = {
                'stack_id': stack_id,
                'stack_name': stack_name,
                'category': category,
                'roles': roles,
                'primary_language': primary_lang,
                'frameworks_libraries': frameworks,
                'database_storage': database,
                'infrastructure_tools': infra,
                'skills_description': description,
                'combined_features': cleaned_features
            }
            processed.append(item)

        self.processed_data = processed
        return self.processed_data
