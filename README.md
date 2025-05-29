# Paper Daily - AI Research Paper Tracker 🔬📚

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent, open-source Python tool that automates the tracking and recommendation of the latest AI research papers. Paper Daily fetches new papers daily from arXiv and OpenReview, processes them using advanced semantic analysis, and delivers personalized Top 10 recommendations to keep researchers up-to-date with cutting-edge developments.

## ✨ Features

- 🔍 **Automated Paper Fetching**: Daily collection from arXiv and OpenReview
- 🧠 **Semantic Analysis**: AI-powered paper evaluation using sentence transformers
- 📊 **Smart Recommendations**: Curated Top 10 list based on novelty, impact, and relevance
- 🖥️ **Multiple Interfaces**: Both command-line and web-based access
- 🔧 **Modular Architecture**: Easy to extend and customize for specific research domains
- 📈 **Configurable Scoring**: Customizable recommendation algorithms
- 📝 **Comprehensive Logging**: Full audit trail of all operations
- 🎯 **Category Filtering**: Focus on specific AI/ML research areas

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nysa-liu/paper-daily.git
   cd paper-daily
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run basic functionality test**
   ```bash
   python test_basic.py
   ```

### Basic Usage

```bash
# Get today's paper recommendations
python main.py

# View help and all options
python main.py --help

# Get papers for a specific date
python main.py --date 2025-05-28

# Launch interactive CLI mode
python main.py --cli

# Start web interface (requires streamlit)
python main.py --web
```

## 📋 Advanced Usage

### Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --web          Launch web interface using Streamlit
  --cli          Use interactive command line interface
  --config TEXT  Specify custom config file path (default: config.json)
  --date TEXT    Fetch papers for specific date (YYYY-MM-DD format)
  --help         Show help message and exit
```

### Configuration

Edit `config.json` to customize:

```json
{
    "arxiv": {
        "categories": ["cs.AI", "cs.LG", "cs.CL", "cs.CV"],
        "max_results": 100
    },
    "analysis": {
        "top_k": 10,
        "similarity_threshold": 0.7
    },
    "embedding": {
        "model_name": "all-MiniLM-L6-v2"
    }
}
```

## 🏗️ Project Architecture

```
paper-daily/
├── src/                         # Source code directory
│   ├── data_acquisition/        # Data fetching modules
│   │   ├── arxiv_fetcher.py     # arXiv API integration
│   │   └── openreview_fetcher.py # OpenReview API integration
│   ├── parsing/                 # Paper processing modules
│   │   ├── pdf_parser.py        # PDF text extraction
│   │   └── text_cleaner.py      # Text preprocessing
│   ├── embedding/               # Semantic analysis modules
│   │   ├── embedder.py          # Sentence transformer embeddings
│   │   └── vector_index.py      # Vector similarity search
│   ├── analysis/                # Recommendation engine
│   │   ├── rule_filter.py       # Rule-based filtering
│   │   ├── llm_evaluator.py     # LLM-based evaluation
│   │   └── recommender.py       # Recommendation algorithms
│   ├── display/                 # User interfaces
│   │   ├── cli_display.py       # Command line interface
│   │   └── web_display.py       # Web interface (Streamlit)
│   └── utils/                   # Utility modules
│       ├── config_manager.py    # Configuration management
│       ├── logger.py            # Logging system
│       └── db_manager.py        # Database operations
├── tests/                       # Unit tests
├── data/                        # Data storage (gitignored)
├── docs/                        # Documentation
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
└── main.py                      # Main application entry point
```

## 🔧 Core Components

### Data Acquisition
- **ArxivFetcher**: Fetches latest papers from arXiv API with category filtering
- **OpenReviewFetcher**: Integrates with OpenReview for conference submissions
- **Scheduler**: Manages daily automated fetching tasks

### Semantic Analysis
- **Embedder**: Generates semantic embeddings using sentence transformers
- **VectorIndex**: Manages similarity search with FAISS indexing
- **TextCleaner**: Preprocesses and cleans paper content

### Recommendation Engine
- **RuleFilter**: Applies configurable filtering rules
- **LLMEvaluator**: Uses large language models for paper scoring
- **Recommender**: Combines multiple signals for final ranking

### User Interfaces
- **CLI Display**: Rich command-line interface with interactive mode
- **Web Display**: Modern web interface using Streamlit

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Basic functionality test
python test_basic.py

# Unit tests (when implemented)
python -m pytest tests/

# Test specific components
python -c "from src.data_acquisition.arxiv_fetcher import ArxivFetcher; print('✓ ArxivFetcher working')"
```

## 📊 Sample Output

```
📚 TOP 10 AI PAPER RECOMMENDATIONS
Generated on: 2025-05-29 21:00:00
================================================================================

1. A Novel Approach to Deep Learning
   Score: 0.892 | Source: ARXIV | ID: 2405.12345
   Authors: John Doe, Jane Smith
   Abstract: This paper presents a novel approach to deep learning that achieves...
   Why recommended: Novel approach, Performance improvements, Core AI research
   Links: arXiv: https://arxiv.org/abs/2405.12345 | PDF: https://arxiv.org/pdf/2405.12345

2. Efficient Transformer Architecture
   Score: 0.847 | Source: ARXIV | ID: 2405.12346
   ...
```

## 🛠️ Development

### Setting up Development Environment

```bash
# Clone and setup
git clone https://github.com/nysa-liu/paper-daily.git
cd paper-daily

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run code formatting
black src/ tests/

# Run linting
flake8 src/ tests/
```

### Adding New Features

1. **New Data Sources**: Extend `data_acquisition/` with new fetcher classes
2. **Custom Embeddings**: Modify `embedding/embedder.py` for new models
3. **Recommendation Algorithms**: Add new strategies in `analysis/`
4. **UI Components**: Extend `display/` modules for new interfaces

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 code style
- Add type hints to all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## 📚 Documentation

- [Development Guide](dev_guide.md) - Detailed architecture and development instructions
- [Setup Complete Guide](SETUP_COMPLETE.md) - Project setup summary
- [API Reference](docs/api_reference.md) - Detailed API documentation (coming soon)

## 🔮 Roadmap

### Version 1.0 (Current)
- ✅ Core paper fetching from arXiv
- ✅ Basic semantic analysis
- ✅ CLI interface
- ✅ Configuration management

### Version 1.1 (Next)
- [ ] OpenReview integration
- [ ] PDF parsing functionality
- [ ] Streamlit web interface
- [ ] Database persistence

### Version 2.0 (Future)
- [ ] User personalization
- [ ] Multi-language support
- [ ] Advanced LLM evaluation
- [ ] Real-time notifications

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) for providing open access to research papers
- [OpenReview](https://openreview.net/) for conference paper access
- [Sentence Transformers](https://www.sbert.net/) for semantic embeddings
- [Streamlit](https://streamlit.io/) for rapid web app development

## 📞 Support

- 📧 Email: [nysa_liu@163.com](nysa_liu@163.com)
- 🐛 Issues: [GitHub Issues](https://github.com/nysa-liu/paper-daily/issues)

---

**Made with ❤️ for the AI research community** 