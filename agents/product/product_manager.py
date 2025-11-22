"""
Product Manager Agent

Converts feature ideas into comprehensive PRDs with user stories,
acceptance criteria, and technical considerations.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, Deliverable, WorkspaceContext


class ProductManagerAgent(BaseAgent):
    """
    Product Manager Agent

    Expertise:
    - User story mapping
    - Acceptance criteria definition
    - Multi-tenant SaaS patterns (personal vs team accounts)
    - Next.js + Supabase architecture
    - Feature prioritization
    """

    def __init__(self):
        super().__init__(
            role=AgentRole.PRODUCT_MANAGER,
            model="claude-sonnet-4.5",
            temperature=0.3,  # Slightly higher for creative thinking
        )

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        """Execute Product Manager tasks"""
        workspace = input_data.workspace_context

        # Generate system and user prompts
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        # Call LLM to generate PRD
        prd_content = await self.call_llm(system_prompt, user_prompt)

        # Save PRD to workspace
        prd_path = workspace.workspace_path / "01-prd" / "prd.md"
        self.save_file(prd_path, prd_content)

        # Create deliverable
        prd_deliverable = self.create_deliverable(
            name="Product Requirements Document",
            deliverable_type="document",
            path=prd_path,
            content=prd_content,
            metadata={
                "format": "markdown",
                "sections": ["overview", "user-stories", "acceptance-criteria"],
            },
        )

        # Quality gate: Check PRD has required sections
        has_user_stories = "## User Stories" in prd_content or "## User stories" in prd_content
        has_acceptance = (
            "Acceptance Criteria" in prd_content or "acceptance criteria" in prd_content.lower()
        )

        prd_quality_gate = self.create_quality_gate(
            name="PRD Completeness",
            passed=has_user_stories and has_acceptance,
            message="PRD includes user stories and acceptance criteria"
            if has_user_stories and has_acceptance
            else "PRD missing required sections",
            details={
                "has_user_stories": has_user_stories,
                "has_acceptance_criteria": has_acceptance,
            },
        )

        return AgentOutput(
            deliverables=[prd_deliverable],
            quality_gates=[prd_quality_gate],
            metadata={
                "feature_name": workspace.feature_name,
                "estimated_complexity": "medium",  # Could be extracted from PRD
            },
            success=True,
        )

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        """Get system prompt for Product Manager agent"""
        return f"""You are an expert Product Manager specializing in Next.js + Supabase SaaS applications.

# Your Expertise

- **User story mapping**: Creating clear, actionable user stories with acceptance criteria
- **Multi-tenant architecture**: Understanding personal accounts vs team accounts
- **SaaS patterns**: Subscription models, billing, permissions, roles
- **Next.js patterns**: App Router, Server Components, Server Actions
- **Supabase patterns**: PostgreSQL, Row Level Security (RLS), database functions
- **Feature scoping**: Balancing user needs with technical feasibility

# Target Stack

The application uses:
- **Frontend**: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Shadcn UI
- **Backend**: Next.js Server Actions, Supabase PostgreSQL
- **Auth**: Supabase Auth with RLS policies
- **Architecture**: Turborepo monorepo with packages for features, billing, CMS, etc.

# Your Deliverables

1. **Comprehensive PRD** (Markdown format)
   - Feature overview and problem statement
   - User personas (personal user, team member, team owner, admin)
   - User stories with "As a [persona], I want to [action] so that [benefit]"
   - Acceptance criteria for each user story
   - Technical considerations (affected packages, new tables, permissions)
   - Success metrics

# Output Format

Write a complete PRD in Markdown using this template:

```markdown
# PRD: [Feature Name]

## Overview
[Brief description of the feature and the problem it solves]

## User Personas
- **Personal Account User**: Individual using their own account
- **Team Member**: User belonging to a team workspace
- **Team Owner**: User who created and owns a team
- **Admin**: User with elevated system permissions

## User Stories

### Story 1: [Title]
**As a** [persona]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

[Repeat for each user story]

## Technical Considerations

### Affected Packages
- `packages/features/[package-name]` - [reason]
- `apps/web/app/home/[account]/[route]` - [reason]

### New Database Tables
- `[table_name]` - [purpose and key fields]

### New Permissions
- `[resource].[action]` - [description]

### Integration Points
- [Existing feature or system that needs integration]

## Success Metrics
- Metric 1: [description and target]
- Metric 2: [description and target]

## Out of Scope
- [Things explicitly not included in this feature]

## Future Considerations
- [Potential enhancements for future iterations]
```

# Guidelines

1. **Be specific**: Vague requirements lead to implementation problems
2. **Consider multi-tenancy**: Features may need to work for both personal and team accounts
3. **Think about permissions**: Who can view/edit/delete this resource?
4. **Database first**: Consider RLS policies and data isolation
5. **Mobile responsive**: All features must work on mobile
6. **Internationalization**: Consider i18n from the start
7. **Accessibility**: ARIA compliant, keyboard navigation

# Important

- Use the exact Markdown template provided above
- Include ALL sections (don't skip any)
- Provide at least 3-5 user stories
- Each user story must have 3-5 acceptance criteria
- Be thorough but concise

Project Path: {workspace_context.project_path}
Feature Workspace: {workspace_context.workspace_path}
"""

    def get_user_prompt(
        self, workspace_context: WorkspaceContext, previous_deliverables: list[Deliverable]
    ) -> str:
        """Get user prompt for Product Manager agent"""
        return f"""Create a comprehensive PRD for this feature:

**Feature Description:**
{workspace_context.request.description}

**Additional Context:**
{self._format_additional_context(workspace_context)}

Please analyze this feature request and create a detailed PRD following the template in your system instructions.

Consider:
1. What problem does this solve for users?
2. Which user personas will use this feature?
3. How does this fit into the existing multi-tenant architecture?
4. What are the core user flows?
5. What data needs to be stored and protected with RLS?
6. Which packages/routes will be affected?

Write the PRD now in Markdown format.
"""

    def _format_additional_context(self, workspace_context: WorkspaceContext) -> str:
        """Format additional context from the feature request"""
        context_parts = []

        if workspace_context.request.user_stories:
            context_parts.append("**User Stories Provided:**")
            for story in workspace_context.request.user_stories:
                context_parts.append(f"- {story}")

        if workspace_context.request.acceptance_criteria:
            context_parts.append("\n**Acceptance Criteria Provided:**")
            for criterion in workspace_context.request.acceptance_criteria:
                context_parts.append(f"- {criterion}")

        if workspace_context.request.target_package:
            context_parts.append(
                f"\n**Target Package:** {workspace_context.request.target_package}"
            )

        return "\n".join(context_parts) if context_parts else "None provided"
