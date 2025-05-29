"""
ArXiv Fetcher for Paper Daily

Fetches latest AI papers from arXiv using its API.
"""

import requests
import feedparser
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urlencode


class ArxivFetcher:
    """Fetches papers from arXiv API"""
    
    def __init__(self, categories: List[str] = None):
        """
        Initialize the arXiv fetcher
        
        Args:
            categories: List of arXiv categories to search (e.g., ['cs.AI', 'cs.LG'])
        """
        self.categories = categories or ['cs.AI', 'cs.LG', 'cs.CL']
        self.base_url = "http://export.arxiv.org/api/query"
        self.max_results = 100
        
    def fetch_papers(self, date: str = None, max_results: int = None) -> List[Dict]:
        """
        Fetch papers from arXiv for a specific date
        
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
            max_results: Maximum number of results to fetch
            
        Returns:
            List of paper dictionaries with metadata
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        if max_results is None:
            max_results = self.max_results
            
        papers = []
        
        for category in self.categories:
            try:
                category_papers = self._fetch_category_papers(category, date, max_results)
                papers.extend(category_papers)
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error fetching papers for category {category}: {e}")
                continue
        
        # Remove duplicates based on arXiv ID
        unique_papers = self._remove_duplicates(papers)
        
        return unique_papers
    
    def _fetch_category_papers(self, category: str, date: str, max_results: int) -> List[Dict]:
        """Fetch papers for a specific category"""
        
        # Build search query
        query_params = {
            'search_query': f'cat:{category}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        url = f"{self.base_url}?{urlencode(query_params)}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse the Atom feed
            feed = feedparser.parse(response.content)
            
            papers = []
            target_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            for entry in feed.entries:
                # Parse submission date
                submitted_date = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ').date()
                
                # Filter by date (papers from the target date)
                if submitted_date == target_date:
                    paper = self._parse_paper_entry(entry, category)
                    papers.append(paper)
            
            return papers
            
        except requests.RequestException as e:
            print(f"Network error fetching arXiv papers: {e}")
            return []
        except Exception as e:
            print(f"Error parsing arXiv response: {e}")
            return []
    
    def _parse_paper_entry(self, entry, category: str) -> Dict:
        """Parse a single paper entry from arXiv feed"""
        
        # Extract arXiv ID
        arxiv_id = entry.id.split('/')[-1]
        
        # Extract authors
        authors = []
        if hasattr(entry, 'authors'):
            authors = [author.name for author in entry.authors]
        elif hasattr(entry, 'author'):
            authors = [entry.author]
        
        # Extract PDF URL
        pdf_url = None
        if hasattr(entry, 'links'):
            for link in entry.links:
                if link.type == 'application/pdf':
                    pdf_url = link.href
                    break
        
        # Extract categories
        categories = []
        if hasattr(entry, 'tags'):
            categories = [tag.term for tag in entry.tags]
        
        paper = {
            'id': arxiv_id,
            'title': entry.title,
            'authors': authors,
            'abstract': entry.summary,
            'published_date': entry.published,
            'updated_date': entry.updated if hasattr(entry, 'updated') else entry.published,
            'categories': categories,
            'primary_category': category,
            'pdf_url': pdf_url,
            'arxiv_url': entry.link,
            'source': 'arxiv'
        }
        
        return paper
    
    def _remove_duplicates(self, papers: List[Dict]) -> List[Dict]:
        """Remove duplicate papers based on arXiv ID"""
        seen_ids = set()
        unique_papers = []
        
        for paper in papers:
            if paper['id'] not in seen_ids:
                seen_ids.add(paper['id'])
                unique_papers.append(paper)
        
        return unique_papers
    
    def search_papers(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Search papers by query string
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of matching papers
        """
        query_params = {
            'search_query': query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        url = f"{self.base_url}?{urlencode(query_params)}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            papers = []
            for entry in feed.entries:
                paper = self._parse_paper_entry(entry, 'search')
                papers.append(paper)
            
            return papers
            
        except Exception as e:
            print(f"Error searching arXiv papers: {e}")
            return [] 