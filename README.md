# QuantEcon Repository Maintenance Action

[![GitHub](https://img.shields.io/badge/github-QuantEcon%2Faction--repo--maintenance-blue?logo=github)](https://github.com/QuantEcon/action-repo-maintenance)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> ⚠️ **CURRENTLY IN DEVELOPMENT** - This action is under active development. Features and APIs may change as we iterate on the implementation.

A GitHub Action for automating maintenance tasks across QuantEcon repositories.

## Overview

This action automates routine maintenance tasks for the QuantEcon organization on GitHub, starting with repository backups and expandable to other maintenance operations.

## Features

### 🔄 Repository Backup (In Development)

Automatically backs up QuantEcon repositories to AWS S3 for disaster recovery and compliance.

**Key Capabilities:**
- Pattern-based repository selection using regex (e.g., `lecture-.*`)
- Automated backup to AWS S3 bucket
- Configurable backup schedules
- Support for incremental and full backups
- Backup verification and reporting

## Configuration

Create a `config.yml` file in your workflow directory:

```yaml
backup:
  enabled: true
  patterns:
    - "lecture-.*"
    - "quantecon-.*"
  s3:
    bucket: "quantecon-repo-backups"
    region: "us-east-1"
    prefix: "backups/"
```

See `config.example.yml` for a complete configuration example.

## Prerequisites

- Python 3.9+
- AWS credentials configured (for S3 backups)
- GitHub token with appropriate permissions

## Usage

### As a GitHub Action

```yaml
name: Repository Maintenance
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: quantecon/action-repo-maintenance@v1
        with:
          task: backup
          config: .github/config.yml
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run backup task
python -m src.backup.main --config config.yml

# Run tests
pytest tests/
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Development Status

This project is in active development. Current focus:

- [x] Project structure setup
- [ ] S3 backup implementation
- [ ] Repository pattern matching
- [ ] Backup verification
- [ ] Error handling and logging
- [ ] Integration tests
- [ ] Documentation completion

## Contributing

Contributions are welcome! Please:

1. Review the architecture documentation
2. Check existing issues and PRs
3. Follow the coding standards in `.copilot-instructions.md`
4. Add tests for new features
5. Update documentation

## Technology Stack

- **Language**: Python 3.9+
- **Cloud Storage**: AWS S3
- **GitHub API**: PyGithub
- **Testing**: pytest
- **CI/CD**: GitHub Actions

## License

[Add appropriate license]

## Support

For issues and questions:
- Open an issue in this repository
- Contact the QuantEcon development team

---

**Note**: This is a QuantEcon internal tool. Please ensure you have appropriate permissions before using it with organization repositories.
