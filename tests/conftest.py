"""Test fixtures for backup tests."""

import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_github_repo():
    """Create a mock GitHub repository."""
    repo = Mock()
    repo.name = "test-repo"
    repo.full_name = "quantecon/test-repo"
    repo.clone_url = "https://github.com/quantecon/test-repo.git"
    repo.default_branch = "main"
    return repo


@pytest.fixture
def mock_github_client():
    """Create a mock GitHub client."""
    client = Mock()
    org = Mock()
    
    # Create mock repos
    repos = [
        Mock(name="lecture-python.myst", full_name="quantecon/lecture-python.myst"),
        Mock(name="lecture-julia", full_name="quantecon/lecture-julia"),
        Mock(name="quantecon-notebooks-python", full_name="quantecon/quantecon-notebooks-python"),
        Mock(name="other-repo", full_name="quantecon/other-repo"),
    ]
    
    org.get_repos.return_value = repos
    client.get_organization.return_value = org
    
    return client


@pytest.fixture
def mock_s3_client():
    """Create a mock S3 client."""
    client = Mock()
    
    # Mock successful upload
    client.upload_file.return_value = None
    
    # Mock head_object for verification
    client.head_object.return_value = {
        "ContentLength": 1024,
        "LastModified": datetime.utcnow(),
    }
    
    return client


@pytest.fixture
def sample_config():
    """Provide a sample configuration."""
    return {
        "backup": {
            "enabled": True,
            "organization": "quantecon",
            "patterns": ["lecture-.*", "quantecon-.*"],
            "s3": {
                "bucket": "test-bucket",
                "region": "us-east-1",
                "prefix": "backups/",
            },
        }
    }
