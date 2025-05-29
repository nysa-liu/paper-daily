"""
Embedder for Paper Daily

Generates semantic embeddings for paper text using sentence transformers.
"""

import numpy as np
from typing import List, Dict, Union
import os

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Using mock embeddings.")


class Embedder:
    """Generates semantic embeddings for text"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedder
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name
        self.model = None
        self.embedding_dim = 384  # Default for all-MiniLM-L6-v2
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                self.embedding_dim = self.model.get_sentence_embedding_dimension()
                print(f"Loaded embedding model: {model_name}")
            except Exception as e:
                print(f"Error loading model {model_name}: {e}")
                self.model = None
        
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Numpy array representing the embedding
        """
        if self.model is not None:
            try:
                embedding = self.model.encode(text, convert_to_numpy=True)
                return embedding
            except Exception as e:
                print(f"Error generating embedding: {e}")
                return self._generate_mock_embedding()
        else:
            return self._generate_mock_embedding()
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a batch of texts
        
        Args:
            texts: List of input texts
            
        Returns:
            Numpy array of embeddings
        """
        if self.model is not None:
            try:
                embeddings = self.model.encode(texts, convert_to_numpy=True)
                return embeddings
            except Exception as e:
                print(f"Error generating batch embeddings: {e}")
                return np.array([self._generate_mock_embedding() for _ in texts])
        else:
            return np.array([self._generate_mock_embedding() for _ in texts])
    
    def generate_paper_embedding(self, paper: Dict) -> np.ndarray:
        """
        Generate embedding for a paper using title and abstract
        
        Args:
            paper: Paper dictionary with 'title' and 'abstract' keys
            
        Returns:
            Numpy array representing the paper embedding
        """
        # Combine title and abstract
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        
        # Create combined text with more weight on title
        combined_text = f"{title}. {abstract}"
        
        return self.generate_embedding(combined_text)
    
    def _generate_mock_embedding(self) -> np.ndarray:
        """Generate a mock embedding for testing purposes"""
        # Generate a random embedding with the expected dimension
        return np.random.rand(self.embedding_dim).astype(np.float32)
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Cosine similarity score
        """
        try:
            # Normalize embeddings
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Compute cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            print(f"Error computing similarity: {e}")
            return 0.0
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary with model information
        """
        return {
            'model_name': self.model_name,
            'embedding_dimension': self.embedding_dim,
            'model_loaded': self.model is not None,
            'sentence_transformers_available': SENTENCE_TRANSFORMERS_AVAILABLE
        } 