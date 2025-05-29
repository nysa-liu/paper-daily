# Paper-Daily Project Engineering Development Document

## 1. Project Overview

The `paper-daily` project is an open-source Python tool designed to automate the tracking and recommendation of the latest AI research papers. It fetches new papers daily from arXiv and OpenReview, processes them using semantic analysis, and recommends the Top 10 most impactful papers. The system supports both command-line and web-based interfaces and lays the groundwork for future enhancements like user personalization, multi-language support, and a semantic paper database.

This first version focuses on core functionality: data acquisition, parsing, semantic embedding, analysis, and basic display. The modular design ensures flexibility for future UI development (e.g., Streamlit or Flask-based interfaces) and functional expansions (e.g., additional data sources or advanced recommendation algorithms).

## 2. Repository Organization Structure

The repository is structured to promote modularity, maintainability, and scalability. Here’s the proposed layout:

```
paper-daily/
│
├── src/                         # Source code directory
│   ├── data_acquisition/        # Data fetching module
│   │   ├── arxiv_fetcher.py
│   │   ├── openreview_fetcher.py
│   │   └── scheduler.py
│   │
│   ├── parsing/                 # Paper parsing and preprocessing module
│   │   ├── pdf_parser.py
│   │   └── text_cleaner.py
│   │
│   ├── embedding/               # Semantic embedding and storage module
│   │   ├── embedder.py
│   │   └── vector_index.py
│   │
│   ├── analysis/                # Analysis and recommendation module
│   │   ├── rule_filter.py
│   │   ├── llm_evaluator.py
│   │   └── recommender.py
│   │
│   ├── display/                 # Output and interaction module
│   │   ├── web_display.py
│   │   └── cli_display.py
│   │
│   └── utils/                   # Utility functions
│       ├── config_manager.py
│       ├── logger.py
│       └── db_manager.py
│
├── tests/                       # Unit tests
│   ├── test_data_acquisition.py
│   ├── test_parsing.py
│   ├── test_embedding.py
│   ├── test_analysis.py
│   └── test_display.py
│
├── data/                        # Data storage (gitignored)
│   ├── raw/                     # Raw fetched data
│   ├── processed/               # Processed text and embeddings
│   └── db/                      # Database files
│
├── docs/                        # Documentation
│   ├── architecture.md
│   ├── api_reference.md
│   └── user_guide.md
│
├── requirements.txt             # Project dependencies
├── setup.py                     # Setup script for installation
├── README.md                    # Project overview and instructions
└── .gitignore                   # Git ignore file
```

## 3. Modules and File Functionality

### 3.1 Data Acquisition Module (`src/data_acquisition/`)

This module handles fetching papers from external sources.

- **`arxiv_fetcher.py`**
  - **Purpose**: Fetches the latest AI papers from arXiv using its API.
  - **Key Class/Methods**:
    - `ArxivFetcher` class
      - `__init__(self, categories: list[str])`: Initializes with a list of arXiv categories (e.g., `cs.AI`, `cs.LG`).
      - `fetch_papers(self, date: str) -> list[dict]`: Retrieves papers submitted on a given date, returning metadata (title, authors, abstract, PDF URL).

- **`openreview_fetcher.py`**
  - **Purpose**: Fetches new submissions or updates from OpenReview using its GraphQL API.
  - **Key Class/Methods**:
    - `OpenReviewFetcher` class
      - `__init__(self, conference_ids: list[str])`: Initializes with a list of conference IDs (e.g., `ICLR.cc/2024`).
      - `fetch_submissions(self, date: str) -> list[dict]`: Fetches submissions or updates for a given date.

- **`scheduler.py`**
  - **Purpose**: Schedules daily fetch tasks.
  - **Key Class/Methods**:
    - `Scheduler` class
      - `__init__(self)`: Initializes the scheduler.
      - `schedule_daily(self, fetcher: object, time: str)`: Sets up a daily fetch task at a specified time.

### 3.2 Parsing Module (`src/parsing/`)

This module processes raw paper data into usable formats.

- **`pdf_parser.py`**
  - **Purpose**: Extracts text from PDF papers.
  - **Key Class/Methods**:
    - `PDFParser` class
      - `__init__(self)`: Initializes the parser (e.g., with PyMuPDF).
      - `parse_pdf(self, pdf_url: str) -> dict`: Downloads and extracts text, returning a dictionary with sections (e.g., abstract, body).

- **`text_cleaner.py`**
  - **Purpose**: Cleans and preprocesses extracted text.
  - **Key Class/Methods**:
    - `TextCleaner` class
      - `__init__(self)`: Initializes the cleaner.
      - `clean_text(self, text: str) -> str`: Removes noise (e.g., LaTeX, stop words).
      - `extract_abstract(self, text: str) -> str`: Isolates the abstract.

### 3.3 Embedding Module (`src/embedding/`)

This module generates and stores semantic embeddings.

- **`embedder.py`**
  - **Purpose**: Creates embeddings for paper text.
  - **Key Class/Methods**:
    - `Embedder` class
      - `__init__(self, model_name: str)`: Initializes with a model (e.g., `all-MiniLM-L6-v2` from SentenceTransformers).
      - `generate_embedding(self, text: str) -> np.ndarray`: Produces a vector embedding for the input text.

- **`vector_index.py`**
  - **Purpose**: Manages storage and retrieval of embeddings.
  - **Key Class/Methods**:
    - `VectorIndex` class
      - `__init__(self, index_path: str)`: Initializes with a FAISS index path.
      - `add_embedding(self, embedding: np.ndarray, paper_id: str)`: Adds an embedding to the index.
      - `search_similar(self, query_embedding: np.ndarray, k: int) -> list[str]`: Finds `k` similar paper IDs.

### 3.4 Analysis Module (`src/analysis/`)

This module evaluates and recommends papers.

- **`rule_filter.py`**
  - **Purpose**: Applies rule-based filtering to papers.
  - **Key Class/Methods**:
    - `RuleFilter` class
      - `__init__(self, rules: dict)`: Initializes with rules (e.g., keywords, min length).
      - `filter_papers(self, papers: list[dict]) -> list[dict]`: Filters papers based on rules.

- **`llm_evaluator.py`**
  - **Purpose**: Uses an LLM to score papers.
  - **Key Class/Methods**:
    - `LLMEvaluator` class
      - `__init__(self, model_name: str)`: Initializes with an LLM (e.g., `Mistral-7B` or OpenAI API).
      - `evaluate_paper(self, text: str) -> dict`: Returns a score and summary based on novelty and impact.

- **`recommender.py`**
  - **Purpose**: Generates the Top 10 recommendations.
  - **Key Class/Methods**:
    - `Recommender` class
      - `__init__(self, filter: RuleFilter, evaluator: LLMEvaluator)`: Initializes with filter and evaluator instances.
      - `recommend_top_10(self, papers: list[dict]) -> list[dict]`: Combines scores and diversity criteria to select Top 10.

### 3.5 Display Module (`src/display/`)

This module handles user interaction and output.

- **`web_display.py`**
  - **Purpose**: Provides a web interface using Streamlit.
  - **Key Class/Methods**:
    - `WebDisplay` class
      - `__init__(self)`: Initializes the Streamlit app.
      - `show_recommendations(self, recommendations: list[dict])`: Displays the Top 10 list.
      - `search_papers(self, query: str)`: Allows searching historical papers (future extension).

- **`cli_display.py`**
  - **Purpose**: Provides a command-line interface.
  - **Key Class/Methods**:
    - `CLIDisplay` class
      - `__init__(self)`: Initializes the CLI.
      - `print_recommendations(self, recommendations: list[dict])`: Prints the Top 10 in a formatted way.

### 3.6 Utilities Module (`src/utils/`)

This module provides supporting functionality.

- **`config_manager.py`**
  - **Purpose**: Manages configuration settings.
  - **Key Class/Methods**:
    - `ConfigManager` class
      - `__init__(self, config_file: str)`: Loads config from a file (e.g., JSON/YAML).
      - `get_config(self, key: str) -> Any`: Retrieves a config value.

- **`logger.py`**
  - **Purpose**: Handles logging.
  - **Key Class/Methods**:
    - `Logger` class
      - `__init__(self, log_file: str)`: Sets up logging.
      - `log(self, message: str, level: str)`: Logs a message.

- **`db_manager.py`**
  - **Purpose**: Manages SQLite database operations.
  - **Key Class/Methods**:
    - `DBManager` class
      - `__init__(self, db_path: str)`: Connects to the database.
      - `save_paper(self, paper: dict)`: Stores paper metadata.

## 4. Extensibility Considerations

- **UI Development**: The `display` module uses Streamlit for rapid prototyping, but its separation from core logic allows migration to Flask/React for richer interfaces later. The `WebDisplay` class can be extended with user authentication or interactive features.
- **Functional Scalability**: New data sources (e.g., ACL Anthology) can be added by creating additional fetcher classes in `data_acquisition/`. The modular design supports plugging in new embedding models or LLMs without affecting other components.
- **Performance**: Asynchronous task handling (e.g., via Celery) can be integrated into `scheduler.py` for large-scale fetching or processing.
- **Multi-Language Support**: The `parsing` and `embedding` modules can adopt multi-language models (e.g., BGE-multilingual) in the future.
- **Database Growth**: The `vector_index` and `db_manager` can scale to Qdrant or PostgreSQL+pgvector as the paper volume increases.

## 5. Development Guidelines

- **Code Style**: Adhere to PEP 8, use type hints, and document with docstrings.
- **Testing**: Write unit tests for each module in `tests/` using `pytest`.
- **Dependencies**: List all requirements (e.g., `requests`, `sentence-transformers`, `streamlit`) in `requirements.txt`.
- **Version Control**: Use Git with meaningful commits and tags for releases.