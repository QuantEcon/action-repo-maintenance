# Project Structure

This document provides an overview of the complete project structure for `action-repo-maintenance`.

## Directory Tree

```
action-repo-maintenance/
├── .github/
│   └── workflows/
│       └── backup.yml              # GitHub Actions workflow for automated backups
│
├── docs/
│   ├── architecture.md             # Comprehensive architecture documentation
│   └── releases/
│       └── README.md               # Release notes directory
│
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # Main entry point and CLI
│   └── backup/
│       ├── __init__.py             # Backup module exports
│       ├── backup_manager.py       # Main backup orchestration
│       ├── repo_matcher.py         # Repository pattern matching
│       └── s3_handler.py           # S3 upload and verification
│
├── tests/
│   ├── conftest.py                 # Pytest fixtures and configuration
│   └── test_repo_matcher.py        # Unit tests for RepoMatcher
│
├── .copilot-instructions.md        # GitHub Copilot development rules
├── .gitignore                      # Git ignore patterns
├── CHANGELOG.md                    # Project changelog
├── config.example.yml              # Example configuration file
├── LICENSE                         # MIT License
├── pyproject.toml                  # Python project configuration
├── QUICKSTART.md                   # Quick start guide
├── README.md                       # Main project documentation
├── requirements.txt                # Python dependencies
└── setup-dev.sh                    # Development environment setup script
```

## File Purposes

### Configuration Files

- **pyproject.toml**: Python project metadata, dependencies, and tool configurations (black, ruff, pytest, mypy)
- **requirements.txt**: Production dependencies (PyGithub, boto3, pyyaml, etc.)
- **config.example.yml**: Example configuration showing all available options
- **.gitignore**: Specifies files to exclude from version control

### Documentation

- **README.md**: Main project overview, features, and usage instructions
- **QUICKSTART.md**: Step-by-step guide to get started quickly
- **CHANGELOG.md**: Version history and changes
- **LICENSE**: MIT License
- **.copilot-instructions.md**: Development guidelines and custom rules for GitHub Copilot
- **docs/architecture.md**: Detailed architecture, design decisions, and component documentation
- **docs/releases/**: Directory for version-specific release notes

### Source Code

#### Main Entry Point
- **src/main.py**: CLI argument parsing, task dispatching, configuration loading

#### Backup Module
- **src/backup/backup_manager.py**: Orchestrates backup process, handles repository iteration
- **src/backup/repo_matcher.py**: Matches repositories using regex patterns
- **src/backup/s3_handler.py**: Handles S3 uploads with verification

### Tests

- **tests/conftest.py**: Pytest fixtures (mock GitHub client, S3 client, etc.)
- **tests/test_repo_matcher.py**: Unit tests for repository pattern matching

### Automation

- **.github/workflows/backup.yml**: GitHub Actions workflow for scheduled/manual backups
- **setup-dev.sh**: Bash script to set up development environment

## Key Features Implemented

### ✅ Complete Features

1. **Repository Backup**
   - Pattern-based repository selection
   - Mirror cloning (all branches and tags)
   - Compressed tar.gz archives
   - Upload to S3 with metadata
   - Checksum verification

2. **GitHub Integration**
   - GitHub API integration via PyGithub
   - Organization repository listing
   - Automated via GitHub Actions

3. **AWS S3 Integration**
   - Upload with MD5 verification
   - Metadata attachment
   - Backup existence checking
   - Listing existing backups

4. **Configuration System**
   - YAML-based configuration
   - Environment variable support
   - Example configuration provided

5. **CLI Interface**
   - Backup task
   - Report generation
   - Verbose logging option
   - Force backup option

6. **Testing Infrastructure**
   - Pytest configuration
   - Mock fixtures
   - Unit test examples

### 🔄 In Development

- Additional unit tests
- Integration tests
- Error handling improvements
- Logging enhancements

### 📋 Planned Features

- Backup retention policies
- Incremental backups
- Repository health checks
- Notification system
- Parallel processing
- Restore functionality
- Metrics and dashboards

## Component Dependencies

```
main.py
  └── load_config() → config.yml
  └── run_backup()
      └── BackupManager
          ├── RepoMatcher → GitHub API
          ├── S3Handler → AWS S3
          └── git clone → Local filesystem
```

## Development Workflow

1. **Setup**: Run `./setup-dev.sh` to initialize development environment
2. **Configure**: Edit `config.yml` with your settings
3. **Develop**: Make changes to source code in `src/`
4. **Test**: Run `pytest tests/` to verify changes
5. **Document**: Update README.md, CHANGELOG.md, or docs/
6. **Commit**: Follow Git workflow with descriptive commits

## Environment Requirements

### Development
- Python 3.9+
- pip for package management
- Virtual environment (venv)
- Git for version control

### Runtime
- GitHub token (repo scope)
- AWS credentials (S3 access)
- Network access to GitHub and AWS

### GitHub Actions
- Ubuntu latest runner
- AWS credentials in GitHub Secrets
- GitHub token (automatic or custom)

## Important Files for Development

| File | Purpose | When to Edit |
|------|---------|--------------|
| `src/backup/*.py` | Core backup logic | Adding/fixing features |
| `tests/*.py` | Test suite | Adding new tests |
| `config.example.yml` | Configuration template | Adding new config options |
| `README.md` | Main documentation | Major changes/features |
| `CHANGELOG.md` | Version history | Every PR/change |
| `.copilot-instructions.md` | Dev guidelines | Workflow changes |
| `docs/architecture.md` | Technical docs | Architecture changes |
| `.github/workflows/*.yml` | CI/CD | Automation changes |

## Data Flow Summary

```
GitHub Actions Schedule/Manual Trigger
    ↓
Load config.yml
    ↓
Initialize BackupManager
    ↓
Query GitHub API for repos
    ↓
Filter repos by patterns
    ↓
For each matched repo:
    - Clone as mirror
    - Create tar.gz
    - Upload to S3
    - Verify upload
    ↓
Generate results summary
    ↓
Exit with status code
```

## Quick Commands Reference

```bash
# Setup development environment
./setup-dev.sh

# Run backup locally
python -m src.main --config config.yml --task backup

# Generate backup report
python -m src.main --config config.yml --task report

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

## Notes

- This project follows semantic versioning (MAJOR.MINOR.PATCH)
- Currently in pre-release (0.1.0-dev)
- Breaking changes may occur before v1.0.0
- All custom development rules are in `.copilot-instructions.md`
- Release notes go in `docs/releases/vX.Y.Z.md`, not separate SUMMARY files

---

**Last Updated**: 2025-10-27  
**Version**: 0.1.0-dev  
**Status**: In Active Development
