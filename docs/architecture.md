# Architecture Documentation

## Overview

The `action-repo-maintenance` project is designed as a modular Python application that can run both as a GitHub Action and as a standalone CLI tool. The architecture prioritizes maintainability, testability, and extensibility.

## Design Principles

1. **Modularity**: Each feature (backup, health checks, etc.) is isolated in its own module
2. **Separation of Concerns**: GitHub API interactions, S3 operations, and business logic are separated
3. **Configurability**: All behavior is controlled via YAML configuration and environment variables
4. **Testability**: Components are designed for easy mocking and unit testing
5. **Extensibility**: New maintenance tasks can be added without modifying existing code

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions Runtime                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              GitHub Actions Workflow                   │ │
│  │          (.github/workflows/backup.yml)                │ │
│  └──────────────────────┬─────────────────────────────────┘ │
│                         │                                    │
│  ┌──────────────────────▼─────────────────────────────────┐ │
│  │                  Main Entry Point                      │ │
│  │                  (src/main.py)                         │ │
│  └──────────────────────┬─────────────────────────────────┘ │
│                         │                                    │
│  ┌──────────────────────▼─────────────────────────────────┐ │
│  │              Configuration Loader                      │ │
│  │              (config.yml parsing)                      │ │
│  └──────────────────────┬─────────────────────────────────┘ │
└─────────────────────────┼─────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐  ┌──────────────┐  ┌──────────────┐
│ BackupManager │  │HealthChecker │  │ Future Tasks │
│               │  │  (planned)   │  │   (planned)  │
└───────┬───────┘  └──────────────┘  └──────────────┘
        │
        │  Uses
        │
        ├──────────────┬──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│ RepoMatcher  │ │S3Handler │ │ GitHub API   │
│              │ │          │ │  (PyGithub)  │
└──────────────┘ └──────────┘ └──────────────┘
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│GitHub Repos  │ │  AWS S3  │ │   Git Clone  │
└──────────────┘ └──────────┘ └──────────────┘
```

## Component Details

### 1. Main Entry Point (`src/main.py`)

**Responsibilities:**
- Parse command-line arguments
- Load configuration from YAML file
- Initialize logging
- Dispatch to appropriate task handler (backup, report, etc.)
- Handle top-level error handling and exit codes

**Key Functions:**
- `main()`: Entry point
- `load_config()`: Load and validate YAML configuration
- `run_backup()`: Execute backup task
- `run_report()`: Generate backup report

### 2. Backup Module (`src/backup/`)

#### BackupManager (`backup_manager.py`)

**Responsibilities:**
- Coordinate the entire backup process
- Manage repository iteration
- Handle backup results and reporting
- Generate backup statistics

**Key Methods:**
- `backup_repositories()`: Main backup orchestration
- `_backup_single_repo()`: Backup individual repository
- `get_backup_report()`: Generate comprehensive backup report

**Process Flow:**
1. Get list of matching repositories
2. For each repository:
   - Check if backup already exists (if skip_existing)
   - Clone repository as mirror
   - Create compressed tarball
   - Upload to S3 with metadata
   - Verify upload
3. Return results summary

#### RepoMatcher (`repo_matcher.py`)

**Responsibilities:**
- Compile and store regex patterns
- Match repository names against patterns
- Filter organization repositories

**Key Methods:**
- `matches()`: Check if single repo matches any pattern
- `filter_repositories()`: Get all matching repos from organization

**Pattern Examples:**
- `lecture-.*` → matches `lecture-python.myst`, `lecture-julia`
- `quantecon-[a-z]+` → matches `quantecon-notebooks`, `quantecon-python`
- `^example-repo$` → exact match for `example-repo`

#### S3Handler (`s3_handler.py`)

**Responsibilities:**
- Upload files to S3
- Verify uploads via checksum and size
- List existing backups
- Check backup existence

**Key Methods:**
- `upload_file()`: Upload with MD5 verification
- `_calculate_md5()`: Compute file hash
- `_verify_upload()`: Verify successful upload
- `backup_exists()`: Check if backup already exists
- `list_backups()`: List all backups for a repository

**Upload Process:**
1. Calculate MD5 hash of local file
2. Upload to S3 with metadata
3. Verify upload by comparing sizes
4. Return success/failure

### 3. Configuration System

**Format:** YAML

**Structure:**
```yaml
backup:
  enabled: true
  organization: "quantecon"
  patterns:
    - "lecture-.*"
  s3:
    bucket: "bucket-name"
    region: "us-east-1"
    prefix: "backups/"
```

**Loading:**
- Configuration loaded via `yaml.safe_load()`
- Environment variables override config values
- Secrets (tokens, credentials) from environment only

### 4. GitHub Actions Integration

**Workflow File:** `.github/workflows/backup.yml`

**Triggers:**
- Scheduled (cron): Weekly on Sunday at 2 AM UTC
- Manual dispatch with parameters

**Secrets Required:**
- `GITHUB_TOKEN`: For GitHub API access (default or custom)
- `AWS_ACCESS_KEY_ID`: AWS credentials
- `AWS_SECRET_ACCESS_KEY`: AWS credentials

**Steps:**
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Configure AWS credentials
5. Run backup task
6. Generate report
7. Upload logs as artifacts

## Data Flow

### Backup Flow

```
1. GitHub Action Triggered
   ↓
2. Load Configuration (config.yml)
   ↓
3. Initialize Components
   - GitHub Client (with token)
   - S3Handler (with credentials)
   - RepoMatcher (with patterns)
   - BackupManager (orchestrator)
   ↓
4. Fetch Repositories
   - Query GitHub API for org repos
   - Filter by patterns
   ↓
5. For Each Matched Repository
   ↓
   5a. Check if Backup Exists
       ↓
   5b. Clone Repository (git clone --mirror)
       ↓
   5c. Create Tarball (tar -czf)
       ↓
   5d. Upload to S3
       - Calculate MD5
       - Upload with metadata
       - Verify upload
       ↓
   5e. Clean up temp files
   ↓
6. Generate Results Summary
   ↓
7. Return Exit Code
```

## Storage Structure

### S3 Bucket Organization

```
s3://bucket-name/
└── backups/
    ├── lecture-python.myst/
    │   ├── lecture-python.myst-20251027.tar.gz
    │   ├── lecture-python.myst-20251103.tar.gz
    │   └── lecture-python.myst-20251110.tar.gz
    ├── lecture-julia/
    │   ├── lecture-julia-20251027.tar.gz
    │   └── lecture-julia-20251103.tar.gz
    └── quantecon-notebooks-python/
        └── quantecon-notebooks-python-20251027.tar.gz
```

### Backup Metadata

Each backup object includes metadata:
- `repository`: Full repository name (org/repo)
- `backup_date`: ISO 8601 timestamp
- `default_branch`: Default branch name
- `size_bytes`: Archive size

## Error Handling

### Levels of Error Handling

1. **Component Level**: Each component catches and logs its own errors
2. **Task Level**: Task handlers catch component errors and continue processing
3. **Main Level**: Main entry point catches all errors and returns appropriate exit codes

### Error Strategy

- **Transient Errors**: Retry with exponential backoff (future enhancement)
- **Permanent Errors**: Log error, mark repository as failed, continue with next
- **Critical Errors**: Fail entire task if configuration invalid or credentials missing

### Logging

- **Level**: INFO (default), DEBUG (verbose mode)
- **Format**: Timestamp - Logger - Level - Message
- **Outputs**: stdout, optionally to file
- **Structure**: Contextual (includes repo names, file paths, etc.)

## Security Considerations

### Credential Management

- **Never** commit credentials to repository
- Use GitHub Secrets for sensitive data
- Support IAM roles when running in AWS
- Validate all inputs and sanitize outputs

### Access Control

- Minimum required permissions for GitHub token
- S3 bucket policy restricts access
- No public access to backup bucket

### Data Protection

- Backups encrypted in transit (TLS)
- S3 server-side encryption optional
- Audit logging enabled for S3 access

## Testing Strategy

### Unit Tests

- Test individual components in isolation
- Mock external dependencies (GitHub API, S3)
- Focus on business logic correctness

### Integration Tests

- Test component interactions
- Use test fixtures for GitHub/S3 responses
- Validate end-to-end flows

### Test Organization

```
tests/
├── unit/
│   ├── test_repo_matcher.py
│   ├── test_s3_handler.py
│   └── test_backup_manager.py
├── integration/
│   └── test_backup_flow.py
└── fixtures/
    ├── github_responses.json
    └── test_repos.json
```

## Future Enhancements

### Planned Features

1. **Incremental Backups**: Only backup changed files
2. **Backup Retention**: Automatic cleanup of old backups
3. **Repository Health Checks**: Detect outdated dependencies, missing docs
4. **Notification System**: Email/Slack alerts for failures
5. **Metrics Dashboard**: Backup status visualization
6. **Parallel Processing**: Backup multiple repos concurrently
7. **Restore Functionality**: Restore repositories from backups

### Extensibility Points

- New task types can be added by creating new modules
- New storage backends by implementing storage interface
- New notification channels by implementing notifier interface

## Performance Considerations

### Optimization Strategies

1. **Pagination**: Handle large result sets efficiently
2. **Streaming**: Stream large files rather than loading in memory
3. **Concurrency**: Backup multiple repos in parallel (future)
4. **Caching**: Cache GitHub API responses when appropriate
5. **Compression**: Use efficient compression for backups

### Resource Limits

- GitHub Actions: 6 hour timeout per run
- GitHub API: 5000 requests/hour for authenticated users
- S3: No practical upload limit
- Network: Depends on repository size

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run backup locally
python -m src.main --config config.yml --task backup
```

### GitHub Actions

- Automatically triggered on schedule or manual dispatch
- Uses organization secrets for credentials
- Logs uploaded as artifacts

## Monitoring and Observability

### Logging

- Structured logging with context
- Log levels: DEBUG, INFO, WARNING, ERROR
- Logs uploaded as GitHub Actions artifacts

### Metrics (Future)

- Number of repos backed up
- Success/failure rates
- Backup sizes
- Duration of operations
- S3 storage costs

### Alerting (Future)

- Failed backups
- Storage threshold exceeded
- API rate limit approaching
- Missing backups for critical repos

## Contributing Guidelines

See `.copilot-instructions.md` for:
- Code style standards
- Documentation requirements
- Testing requirements
- Git workflow
- Release process

---

**Last Updated**: 2025-10-27  
**Version**: 0.1.0-dev
