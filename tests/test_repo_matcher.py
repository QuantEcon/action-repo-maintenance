"""Unit tests for RepoMatcher."""

import pytest
from src.backup.repo_matcher import RepoMatcher


class TestRepoMatcher:
    """Test the RepoMatcher class."""

    def test_single_pattern_match(self):
        """Test matching with a single pattern."""
        matcher = RepoMatcher(["lecture-.*"])
        
        assert matcher.matches("lecture-python.myst") is True
        assert matcher.matches("lecture-julia") is True
        assert matcher.matches("other-repo") is False

    def test_multiple_patterns(self):
        """Test matching with multiple patterns."""
        matcher = RepoMatcher(["lecture-.*", "quantecon-.*"])
        
        assert matcher.matches("lecture-python.myst") is True
        assert matcher.matches("quantecon-notebooks") is True
        assert matcher.matches("other-repo") is False

    def test_exact_match(self):
        """Test exact repository name matching."""
        matcher = RepoMatcher(["^specific-repo$"])
        
        assert matcher.matches("specific-repo") is True
        assert matcher.matches("specific-repo-extra") is False
        assert matcher.matches("prefix-specific-repo") is False

    def test_filter_repositories(self, mock_github_client):
        """Test filtering repositories from an organization."""
        matcher = RepoMatcher(["lecture-.*"])
        
        repos = matcher.filter_repositories(mock_github_client, "quantecon")
        
        assert len(repos) == 2
        repo_names = [r.name for r in repos]
        assert "lecture-python.myst" in repo_names
        assert "lecture-julia" in repo_names

    def test_filter_multiple_patterns(self, mock_github_client):
        """Test filtering with multiple patterns."""
        matcher = RepoMatcher(["lecture-.*", "quantecon-.*"])
        
        repos = matcher.filter_repositories(mock_github_client, "quantecon")
        
        assert len(repos) == 3
        repo_names = [r.name for r in repos]
        assert "lecture-python.myst" in repo_names
        assert "lecture-julia" in repo_names
        assert "quantecon-notebooks-python" in repo_names

    def test_no_matches(self, mock_github_client):
        """Test when no repositories match the patterns."""
        matcher = RepoMatcher(["nonexistent-.*"])
        
        repos = matcher.filter_repositories(mock_github_client, "quantecon")
        
        assert len(repos) == 0

    def test_empty_patterns(self):
        """Test with empty pattern list."""
        matcher = RepoMatcher([])
        
        assert matcher.matches("any-repo") is False
