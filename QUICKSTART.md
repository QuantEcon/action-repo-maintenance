# Quick Start Guide

This guide will help you get started with the QuantEcon Repository Maintenance Action for backing up repositories to AWS S3.

## Prerequisites

- Python 3.9 or higher
- GitHub personal access token with `repo` scope
- AWS account with S3 bucket created
- AWS credentials (Access Key ID and Secret Access Key)

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/quantecon/action-repo-maintenance.git
cd action-repo-maintenance
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Application

Copy the example configuration and customize it:

```bash
cp config.example.yml config.yml
```

Edit `config.yml`:

```yaml
backup:
  enabled: true
  organization: "quantecon"
  patterns:
    - "lecture-.*"
    - "quantecon-.*"
  s3:
    bucket: "your-bucket-name"
    region: "us-east-1"
    prefix: "backups/"
```

### 4. Set Environment Variables

```bash
export GITHUB_TOKEN="your_github_token"
export AWS_ACCESS_KEY_ID="your_aws_access_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
```

### 5. Run Your First Backup

```bash
# Backup repositories
python -m src.main --config config.yml --task backup

# Generate a report
python -m src.main --config config.yml --task report
```

## GitHub Actions Setup

### 1. Set Up AWS S3 Bucket

Create an S3 bucket for backups:

```bash
aws s3 mb s3://quantecon-repo-backups --region us-east-1
```

### 2. Configure GitHub Secrets

In your GitHub repository settings, add these secrets:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `REPO_BACKUP_TOKEN`: GitHub token with `repo` scope (optional, falls back to `GITHUB_TOKEN`)

### 3. Configure Repository Variables (Optional)

- `AWS_REGION`: AWS region for S3 bucket (default: us-east-1)

### 4. Commit Your Configuration

```bash
# Copy and customize config
cp config.example.yml config.yml
# Edit config.yml with your settings

# Commit to repository
git add config.yml
git commit -m "Add backup configuration"
git push
```

### 5. Test the Workflow

You can trigger the workflow manually:

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Repository Backup" workflow
4. Click "Run workflow"
5. (Optional) Override organization or force backup

## Understanding the Backup Process

### What Gets Backed Up

- Complete Git repository (all branches, tags, and history)
- Repository is cloned as a mirror
- Compressed as a tar.gz archive
- Uploaded to S3 with metadata

### Backup Naming Convention

```
s3://bucket-name/backups/{repo-name}/{repo-name}-{YYYYMMDD}.tar.gz
```

Example:
```
s3://quantecon-repo-backups/backups/lecture-python.myst/lecture-python.myst-20251027.tar.gz
```

### Backup Schedule

By default, backups run weekly on Sunday at 2 AM UTC. You can customize this in `.github/workflows/backup.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM UTC
```

### Repository Pattern Matching

Repositories are selected using Python regex patterns:

- `lecture-.*` matches all repos starting with "lecture-"
- `quantecon-.*` matches all repos starting with "quantecon-"
- `^exact-match$` matches exactly "exact-match"

## Testing Your Setup

### Test Pattern Matching

Create a test script to verify which repositories will be backed up:

```python
import os
from github import Github
from src.backup.repo_matcher import RepoMatcher

github_token = os.getenv("GITHUB_TOKEN")
github = Github(github_token)

matcher = RepoMatcher(["lecture-.*"])
org = github.get_organization("quantecon")

print("Matching repositories:")
for repo in org.get_repos():
    if matcher.matches(repo.name):
        print(f"  ✓ {repo.full_name}")
```

### Test S3 Upload

Verify S3 credentials and bucket access:

```bash
# List bucket contents
aws s3 ls s3://quantecon-repo-backups/backups/

# Test write access
echo "test" > test.txt
aws s3 cp test.txt s3://quantecon-repo-backups/test/
aws s3 rm s3://quantecon-repo-backups/test/test.txt
rm test.txt
```

## Common Tasks

### Force Re-backup

Skip the check for existing backups:

```bash
python -m src.main --config config.yml --task backup --force
```

### Check Backup Status

Generate a report of all backups:

```bash
python -m src.main --config config.yml --task report
```

### Backup Specific Organization

Override the organization in config:

```bash
python -m src.main --config config.yml --task backup --organization my-org
```

### Enable Debug Logging

```bash
python -m src.main --config config.yml --task backup --verbose
```

## Troubleshooting

### Issue: "GITHUB_TOKEN environment variable not set"

**Solution**: Export the GitHub token:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### Issue: "Failed to upload to S3: Access Denied"

**Solutions**:
1. Verify AWS credentials are correct
2. Check S3 bucket exists and you have write permissions
3. Verify IAM policy allows `s3:PutObject` on the bucket

### Issue: "No repositories matched patterns"

**Solutions**:
1. Check your patterns are correct Python regex
2. Verify you have access to the organization
3. Test patterns with the test script above

### Issue: Backup too large or timing out

**Solutions**:
1. Exclude very large repositories from patterns
2. Increase GitHub Actions timeout
3. Consider backing up large repos separately

## Next Steps

- Review [architecture documentation](docs/architecture.md)
- Check [CHANGELOG.md](CHANGELOG.md) for latest updates
- Read [.copilot-instructions.md](.copilot-instructions.md) for development guidelines
- Add more repository patterns to your config
- Set up notifications for backup failures (planned feature)
- Configure retention policies (planned feature)

## Getting Help

- Check existing [GitHub Issues](https://github.com/quantecon/action-repo-maintenance/issues)
- Review the documentation in the `docs/` directory
- Contact the QuantEcon development team

---

**Note**: This project is in active development. Features and configuration options may change before v1.0.0 release.
