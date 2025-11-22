"""
Agent Registry - Loads and manages specialist agents
"""

from typing import Dict, Type

from agents.base import BaseAgent
from orchestrator.core.models import AgentRole

# Import all specialist agents
from agents.product.product_manager import ProductManagerAgent
from agents.product.ux_researcher import UXResearcherAgent
from agents.product.business_analyst import BusinessAnalystAgent

from agents.architecture.solutions_architect import SolutionsArchitectAgent
from agents.architecture.database_architect import DatabaseArchitectAgent
from agents.architecture.security_architect import SecurityArchitectAgent

from agents.implementation.database_engineer import DatabaseEngineerAgent
from agents.implementation.backend_engineer import BackendEngineerAgent
from agents.implementation.frontend_engineer import FrontendEngineerAgent

from agents.testing.qa_engineer import QAEngineerAgent
from agents.testing.e2e_test_engineer import E2ETestEngineerAgent
from agents.testing.db_test_engineer import DBTestEngineerAgent

from agents.review.security_engineer import SecurityEngineerAgent
from agents.review.code_reviewer import CodeReviewerAgent
from agents.review.performance_engineer import PerformanceEngineerAgent

from agents.deployment.technical_writer import TechnicalWriterAgent
from agents.deployment.devops_engineer import DevOpsEngineerAgent


class AgentRegistry:
    """
    Central registry for all specialist agents.

    Maps agent roles to their implementation classes.
    """

    _agents: Dict[AgentRole, Type[BaseAgent]] = {
        # Product Phase
        AgentRole.PRODUCT_MANAGER: ProductManagerAgent,
        AgentRole.UX_RESEARCHER: UXResearcherAgent,
        AgentRole.BUSINESS_ANALYST: BusinessAnalystAgent,

        # Architecture Phase
        AgentRole.SOLUTIONS_ARCHITECT: SolutionsArchitectAgent,
        AgentRole.DATABASE_ARCHITECT: DatabaseArchitectAgent,
        AgentRole.SECURITY_ARCHITECT: SecurityArchitectAgent,

        # Implementation Phase
        AgentRole.DATABASE_ENGINEER: DatabaseEngineerAgent,
        AgentRole.BACKEND_ENGINEER: BackendEngineerAgent,
        AgentRole.FRONTEND_ENGINEER: FrontendEngineerAgent,

        # Testing Phase
        AgentRole.QA_ENGINEER: QAEngineerAgent,
        AgentRole.E2E_TEST_ENGINEER: E2ETestEngineerAgent,
        AgentRole.DB_TEST_ENGINEER: DBTestEngineerAgent,

        # Review Phase
        AgentRole.SECURITY_ENGINEER: SecurityEngineerAgent,
        AgentRole.CODE_REVIEWER: CodeReviewerAgent,
        AgentRole.PERFORMANCE_ENGINEER: PerformanceEngineerAgent,

        # Deployment Phase
        AgentRole.TECHNICAL_WRITER: TechnicalWriterAgent,
        AgentRole.DEVOPS_ENGINEER: DevOpsEngineerAgent,
    }

    @classmethod
    def get_agent(cls, role: AgentRole) -> BaseAgent:
        """
        Get an agent instance by role.

        Args:
            role: Agent role to instantiate

        Returns:
            Agent instance

        Raises:
            ValueError: If agent role not found
        """
        agent_class = cls._agents.get(role)
        if not agent_class:
            raise ValueError(f"No agent registered for role: {role}")

        return agent_class()

    @classmethod
    def list_agents(cls) -> list[AgentRole]:
        """List all registered agent roles"""
        return list(cls._agents.keys())

    @classmethod
    def has_agent(cls, role: AgentRole) -> bool:
        """Check if agent is registered"""
        return role in cls._agents


# Global registry instance
agent_registry = AgentRegistry()
