"""
CLI Display for Paper Daily

Provides command-line interface for displaying papers and recommendations.
"""

from typing import List, Dict
from datetime import datetime


class CLIDisplay:
    """Command-line interface for Paper Daily"""
    
    def __init__(self):
        """Initialize CLI display"""
        self.width = 80
        
    def print_recommendations(self, recommendations: List[Dict]) -> None:
        """
        Print paper recommendations to console
        
        Args:
            recommendations: List of recommended papers with scores
        """
        if not recommendations:
            print("No recommendations found.")
            return
        
        print("\n" + "="*self.width)
        print(f"📚 TOP {len(recommendations)} AI PAPER RECOMMENDATIONS")
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*self.width)
        
        for i, paper in enumerate(recommendations, 1):
            self._print_paper(paper, i)
            if i < len(recommendations):
                print("-" * self.width)
        
        print("="*self.width)
        print("🔗 Happy reading! 📖\n")
    
    def _print_paper(self, paper: Dict, rank: int) -> None:
        """Print a single paper"""
        title = paper.get('title', 'No title')
        authors = paper.get('authors', [])
        abstract = paper.get('abstract', 'No abstract')
        score = paper.get('score', 0.0)
        source = paper.get('source', 'unknown')
        paper_id = paper.get('id', 'unknown')
        
        print(f"\n{rank}. {title}")
        print(f"   Score: {score:.3f} | Source: {source.upper()} | ID: {paper_id}")
        
        if authors:
            author_str = ", ".join(authors[:3])  # Show first 3 authors
            if len(authors) > 3:
                author_str += f" et al. ({len(authors)} authors)"
            print(f"   Authors: {author_str}")
        
        # Print abstract (truncated)
        if abstract:
            abstract_short = self._truncate_text(abstract, 200)
            print(f"   Abstract: {abstract_short}")
        
        # Print recommendation reasons if available
        reasons = paper.get('reasons', [])
        if reasons:
            print(f"   Why recommended: {', '.join(reasons)}")
        
        # Print URLs if available
        urls = []
        if paper.get('arxiv_url'):
            urls.append(f"arXiv: {paper['arxiv_url']}")
        if paper.get('pdf_url'):
            urls.append(f"PDF: {paper['pdf_url']}")
        
        if urls:
            print(f"   Links: {' | '.join(urls)}")
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def print_summary(self, total_papers: int, recommendations: List[Dict]) -> None:
        """Print a summary of the recommendation process"""
        print(f"\n📊 SUMMARY")
        print(f"Total papers processed: {total_papers}")
        print(f"Recommendations generated: {len(recommendations)}")
        
        if recommendations:
            avg_score = sum(p.get('score', 0) for p in recommendations) / len(recommendations)
            print(f"Average recommendation score: {avg_score:.3f}")
    
    def run_interactive_mode(self) -> None:
        """Run interactive CLI mode"""
        print("\n🤖 Paper Daily - Interactive Mode")
        print("Commands: 'help', 'fetch', 'recommend', 'search <query>', 'quit'")
        
        while True:
            try:
                command = input("\npaper-daily> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("Goodbye! 👋")
                    break
                elif command == 'help':
                    self._print_help()
                elif command == 'fetch':
                    print("Fetching latest papers... (not implemented in warm-up)")
                elif command.startswith('search '):
                    query = command[7:]
                    print(f"Searching for: '{query}' (not implemented in warm-up)")
                elif command == 'recommend':
                    print("Generating recommendations... (not implemented in warm-up)")
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except EOFError:
                print("\nGoodbye! 👋")
                break
    
    def _print_help(self) -> None:
        """Print help information"""
        help_text = """
Available commands:
  help                 - Show this help message
  fetch               - Fetch latest papers from arXiv and OpenReview
  recommend           - Generate Top 10 recommendations
  search <query>      - Search papers by keyword
  quit/exit           - Exit the program

Example usage:
  paper-daily> fetch
  paper-daily> recommend
  paper-daily> search transformer
"""
        print(help_text) 