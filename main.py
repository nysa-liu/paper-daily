#!/usr/bin/env python3
"""
Paper Daily - Main Entry Point

This is the main entry point for the Paper Daily application.
It supports both CLI and web interfaces.
"""

import click
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.config_manager import ConfigManager
from utils.logger import Logger
from data_acquisition.arxiv_fetcher import ArxivFetcher
from data_acquisition.openreview_fetcher import OpenReviewFetcher
from parsing.pdf_parser import PDFParser
from parsing.text_cleaner import TextCleaner
from embedding.embedder import Embedder
from analysis.recommender import Recommender
from display.cli_display import CLIDisplay
from display.web_display import WebDisplay


@click.command()
@click.option('--web', is_flag=True, help='Launch web interface')
@click.option('--cli', is_flag=True, help='Use command line interface')
@click.option('--config', default='config.json', help='Config file path')
@click.option('--date', default=None, help='Specific date to fetch papers (YYYY-MM-DD)')
def main(web, cli, config, date):
    """Paper Daily - AI Research Paper Tracker"""
    
    # Initialize components
    config_manager = ConfigManager(config)
    logger = Logger("paper_daily.log")
    
    logger.log("Starting Paper Daily application", "INFO")
    
    if web:
        # Launch web interface
        logger.log("Launching web interface", "INFO")
        web_display = WebDisplay()
        web_display.run()
    elif cli:
        # Use CLI interface
        run_cli_mode(config_manager, logger, date)
    else:
        # Default: run daily fetch and recommendation
        run_daily_pipeline(config_manager, logger, date)


def run_daily_pipeline(config_manager, logger, date=None):
    """Run the complete daily paper processing pipeline"""
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    logger.log(f"Running daily pipeline for date: {date}", "INFO")
    
    try:
        # 1. Fetch papers
        arxiv_fetcher = ArxivFetcher(['cs.AI', 'cs.LG', 'cs.CL'])
        papers = arxiv_fetcher.fetch_papers(date)
        logger.log(f"Fetched {len(papers)} papers from arXiv", "INFO")
        
        # 2. Process papers (simplified for warm-up)
        embedder = Embedder()
        recommender = Recommender()
        
        # 3. Generate recommendations
        recommendations = recommender.recommend_top_10(papers)
        
        # 4. Display results
        cli_display = CLIDisplay()
        cli_display.print_recommendations(recommendations)
        
        logger.log("Daily pipeline completed successfully", "INFO")
        
    except Exception as e:
        logger.log(f"Error in daily pipeline: {str(e)}", "ERROR")
        raise


def run_cli_mode(config_manager, logger, date=None):
    """Run in CLI interactive mode"""
    logger.log("Starting CLI mode", "INFO")
    
    cli_display = CLIDisplay()
    cli_display.run_interactive_mode()


if __name__ == '__main__':
    main() 