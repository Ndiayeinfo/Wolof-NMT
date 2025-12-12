# Changelog

All notable changes to the French-Wolof Translator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-XX

### Added
- Initial modular release of the French-Wolof Translator
- **Versioning System**: Semantic versioning implementation in `version.py`
- **Modular Architecture**: 
  - `config.py`: Centralized configuration management
  - `data_processor.py`: Dataset loading and preprocessing
  - `trainer.py`: Model training and fine-tuning
  - `evaluator.py`: BLEU score evaluation metrics
  - `translator.py`: Main translation interface
- **Training Pipeline**: Complete training script (`train.py`) with support for:
  - Custom dataset loading
  - Model fine-tuning
  - Evaluation metrics
  - HuggingFace Hub integration
  - Weights & Biases logging support
- **Translation Interface**: 
  - Bidirectional translation (French ↔ Wolof)
  - Convenience methods for each direction
  - Generic translate method with language specification
  - Device selection (CPU/CUDA)
- **Documentation**: 
  - Comprehensive README.md in English
  - Code documentation with docstrings
  - Usage examples
  - Configuration guide
- **Package Management**:
  - `requirements.txt` with all dependencies
  - `setup.py` for package installation
  - `.gitignore` for version control
- **Example Scripts**:
  - `main.py`: Demonstration of translator usage
  - `train.py`: Complete training pipeline

### Features
- Support for NLLB-200-distilled-600M model
- Automatic device detection (CUDA/CPU)
- Configurable model parameters
- Flexible training configuration
- BLEU score evaluation
- HuggingFace Hub model pushing

### Technical Details
- Built on HuggingFace Transformers library
- Uses Facebook's NLLB model architecture
- Supports mixed precision training (FP16)
- Compatible with Python 3.8+

---

## [Unreleased]

### Planned
- Additional evaluation metrics (METEOR, ROUGE)
- Batch translation support
- Web API interface
- Docker containerization
- Unit tests and integration tests
- Performance optimization

---

[1.0.0]: https://github.com/galsenai/french-wolof-translator/releases/tag/v1.0.0

