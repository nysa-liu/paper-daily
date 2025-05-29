"""
Recommender for Paper Daily
"""

import random
from typing import List, Dict


class Recommender:
    """Generates paper recommendations"""
    
    def __init__(self, top_k: int = 10):
        self.top_k = top_k
        
    def recommend_top_10(self, papers: List[Dict]) -> List[Dict]:
        """Generate top 10 paper recommendations"""
        if not papers:
            return []
        
        # Simple scoring for warm-up
        scored_papers = []
        for paper in papers:
            score = random.random()  # Mock scoring
            paper_copy = paper.copy()
            paper_copy['score'] = score
            paper_copy['reasons'] = ['Mock reason']
            scored_papers.append(paper_copy)
        
        # Sort by score
        scored_papers.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_papers[:self.top_k] 