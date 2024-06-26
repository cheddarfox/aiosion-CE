# AioSion AI Assistant

AioSion is an advanced AI Assistant project aimed at developing a versatile, scalable, and user-friendly AI solution. This project leverages Python, Docker, and modern cloud technologies to create an assistant that's accessible on both desktop and mobile platforms.

## Project Overview

AioSion is designed to be:
- Versatile: Capable of handling a wide range of tasks and integrating multiple AI models
- Scalable: Built with a robust architecture that can grow with increasing demands
- User-friendly: Accessible through various interfaces including CLI, web, and mobile

## Current Status

We are currently in the MVP (Minimum Viable Product) development phase. Our immediate focus is on:

1. Finishing the Core AI Module implementation with multi-model support
2. Developing a basic Command-Line Interface (CLI)
3. Creating an initial Web API using FastAPI
4. Setting up a simple front-end using React
5. Implementing basic user authentication and authorization

## Features

### Implemented Features
- Core AI Module with multi-model support (OpenAI, Anthropic, Google PaLM, HuggingFace)
- Natural Language Processing (NLP) capabilities:
  - Tokenization
  - Part-of-speech tagging
  - Named Entity Recognition
  - Sentiment Analysis
  - Text Summarization
- Robust error handling and logging

### Planned Features
- Command-Line Interface (CLI) for direct interaction
- Web Interface with RESTful API
- Mobile compatibility
- Cloud deployment with auto-scaling capabilities
- User authentication and personalization
- Multi-modal capabilities (text, voice, potentially image)

## Getting Started

### Prerequisites

- Python 3.9+
- Anaconda or Miniconda
- Docker (for containerization)
- PyTorch (for machine learning capabilities)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/cheddarfox/aiosion-CE.git
   cd aiosion-CE
   ```

2. Create and activate the Conda environment:
   ```
   conda env create -f environment.yml
   conda activate aiosion
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Install PyTorch:
   ```
   pip install torch torchvision torchaudio
   ```

5. Download the spaCy language model:
   ```
   python -m spacy download en_core_web_sm
   ```

6. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_AI_API_KEY=your_google_ai_api_key
   ```

7. Run the main application:
   ```
   python src/main.py
   ```

### Docker Installation

1. Build and run using Docker Compose:
   ```
   docker-compose up --build
   ```

## Troubleshooting

### Package Conflicts
If you encounter conflicts between package versions, particularly with fastapi, anthropic, or anyio, try the following:

1. Uninstall the conflicting packages:
   ```
   pip uninstall fastapi anthropic anyio -y
   ```

2. Reinstall them with specific versions:
   ```
   pip install fastapi==0.95.2 anthropic==0.29.0 anyio==3.7.1
   ```

### PyTorch Installation Issues
If you encounter issues installing PyTorch, please refer to the official PyTorch installation guide for your specific operating system and CUDA version: https://pytorch.org/get-started/locally/

### spaCy Model Issues
If you face issues with the spaCy model, ensure you've downloaded it correctly:

```
python -m spacy download en_core_web_sm
```

If the issue persists, try downloading a specific version:

```
python -m spacy download en_core_web_sm==3.5.0
```

### Other Issues
For any other issues, please check the error logs and open an issue in the GitHub repository with a detailed description of the problem and the steps to reproduce it.

## Contributing

We welcome contributions from the community! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Development Roadmap

Please check our [kanban.md](kanban.md) file for the current development status and upcoming tasks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or concerns, please open an issue in this repository.

Thank you for your interest in AioSion!