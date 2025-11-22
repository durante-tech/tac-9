"""
Tests for the core orchestrator
"""

import pytest
from pathlib import Path

from orchestrator.core.models import FeatureRequest, WorkflowMode
from orchestrator.core.orchestrator import SDLCOrchestrator


@pytest.fixture
def orchestrator():
    """Create an orchestrator instance"""
    return SDLCOrchestrator()


@pytest.fixture
def sample_request():
    """Create a sample feature request"""
    return FeatureRequest(
        description="Add a team activity log showing all member actions",
        user_stories=["As a team owner, I want to see all team member activities"],
        acceptance_criteria=["Activity log displays recent actions", "Filter by date range"],
    )


@pytest.mark.asyncio
async def test_orchestrator_creates_workspace(orchestrator, sample_request):
    """Test that orchestrator creates a workspace"""
    execution = await orchestrator.execute_feature_request(sample_request, WorkflowMode.FULL)

    assert execution.workspace_context is not None
    assert execution.workspace_context.workspace_path.exists()
    assert execution.workspace_context.feature_name is not None


@pytest.mark.asyncio
async def test_workspace_has_required_directories(orchestrator, sample_request):
    """Test that workspace has all required subdirectories"""
    execution = await orchestrator.execute_feature_request(sample_request, WorkflowMode.FULL)

    workspace_path = execution.workspace_context.workspace_path

    expected_dirs = [
        "01-prd",
        "02-architecture",
        "03-database",
        "04-backend",
        "05-frontend",
        "06-tests",
        "07-reviews",
        "08-docs",
    ]

    for dir_name in expected_dirs:
        dir_path = workspace_path / dir_name
        assert dir_path.exists(), f"Directory {dir_name} should exist"
        assert dir_path.is_dir(), f"{dir_name} should be a directory"


def test_generate_feature_name(orchestrator):
    """Test feature name generation"""
    description = "Add a Team Activity Log with Filtering!"
    feature_name = orchestrator._generate_feature_name(description)

    assert "team-activity-log" in feature_name
    assert "!" not in feature_name  # Special chars removed
    assert " " not in feature_name  # Spaces replaced with dashes
