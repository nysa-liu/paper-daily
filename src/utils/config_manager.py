"""
Configuration Manager for Paper Daily

Handles loading and accessing configuration settings from JSON files.
"""

import json
import os
from typing import Any, Dict
from pathlib import Path


class ConfigManager:
    """Manages configuration settings for the application"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize the configuration manager
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default configuration if file doesn't exist
                return self._get_default_config()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "arxiv": {
                "categories": ["cs.AI", "cs.LG", "cs.CL"],
                "max_results": 50,
                "api_url": "http://export.arxiv.org/api/query"
            },
            "embedding": {
                "model_name": "all-MiniLM-L6-v2",
                "max_seq_length": 512,
                "batch_size": 32
            },
            "analysis": {
                "top_k": 10,
                "similarity_threshold": 0.7
            },
            "database": {
                "db_path": "data/db/papers.db",
                "vector_index_path": "data/db/vector_index.faiss"
            }
        }
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        
        Args:
            key: Configuration key (supports dot notation like 'arxiv.categories')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_config(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        self.config = self._load_config() 