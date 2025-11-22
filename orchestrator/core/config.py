"""
Configuration management for TAC-9 Orchestrator
"""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """TAC-9 Orchestrator Settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # AI Providers
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    default_agent_model: str = "claude-sonnet-4.5"
    default_agent_temperature: float = 0.1

    # Target Project
    target_project_path: Path = Field(default=Path("."))
    target_project_type: Literal["nextjs-supabase", "nextjs-only", "custom"] = "nextjs-supabase"

    # Supabase Configuration
    supabase_url: str = "http://localhost:54321"
    supabase_anon_key: str | None = None
    supabase_service_role_key: str | None = None

    # GitHub Integration
    github_token: str | None = None
    github_repo: str | None = None
    github_default_branch: str = "main"
    auto_create_pr: bool = False

    # Orchestrator Settings
    max_parallel_agents: int = 3
    agent_timeout_seconds: int = 600
    debug: bool = False
    log_level: str = "INFO"
    workspace_dir: Path = Field(default=Path("./workspace"))
    cache_dir: Path = Field(default=Path("./.cache"))

    # Automation Settings
    enable_auto_commit: bool = False
    enable_auto_pr: bool = False
    enable_auto_test: bool = True
    enable_auto_security_scan: bool = True

    # Agent Phase Configuration
    enable_product_phase: bool = True
    enable_architecture_phase: bool = True
    enable_implementation_phase: bool = True
    enable_testing_phase: bool = True
    enable_review_phase: bool = True
    enable_deployment_phase: bool = True

    # Specific Agents
    enable_product_manager: bool = True
    enable_solutions_architect: bool = True
    enable_database_architect: bool = True
    enable_database_engineer: bool = True
    enable_backend_engineer: bool = True
    enable_frontend_engineer: bool = True
    enable_e2e_test_engineer: bool = True
    enable_db_test_engineer: bool = True
    enable_security_engineer: bool = True
    enable_code_reviewer: bool = True
    enable_performance_engineer: bool = True
    enable_technical_writer: bool = True
    enable_devops_engineer: bool = True

    # Quality Gates
    min_test_coverage: int = 80
    max_bundle_size_increase: int = 100
    fail_on_security_vulnerabilities: bool = True
    fail_on_typescript_errors: bool = True
    fail_on_failed_tests: bool = True

    # Notifications
    slack_webhook_url: str | None = None
    discord_webhook_url: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    notification_email: str | None = None

    # Advanced Settings
    agent_max_retries: int = 2
    template_dir: Path = Field(default=Path("./templates"))
    enable_streaming: bool = True
    save_agent_conversations: bool = True
    conversation_dir: Path = Field(default=Path("./logs/conversations"))

    def model_post_init(self, __context):
        """Ensure directories exist"""
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.conversation_dir.mkdir(parents=True, exist_ok=True)
        self.template_dir.mkdir(parents=True, exist_ok=True)

    @property
    def has_openai(self) -> bool:
        """Check if OpenAI is configured"""
        return self.openai_api_key is not None

    @property
    def has_anthropic(self) -> bool:
        """Check if Anthropic is configured"""
        return self.anthropic_api_key is not None

    @property
    def has_github(self) -> bool:
        """Check if GitHub is configured"""
        return self.github_token is not None and self.github_repo is not None

    @property
    def has_supabase(self) -> bool:
        """Check if Supabase is configured"""
        return self.supabase_anon_key is not None and self.supabase_service_role_key is not None


# Global settings instance
settings = Settings()
