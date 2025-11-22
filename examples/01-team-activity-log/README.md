# Example 1: Team Activity Log

Complete example of using TAC-9 to build a team activity logging feature for a Next.js + Supabase SaaS application.

## Feature Description

A comprehensive activity log that tracks all actions taken by team members with filtering, pagination, and real-time updates.

## What This Example Demonstrates

- **Multi-tenant data design**: Activity logs isolated per team
- **RLS policies**: Secure data access with Row Level Security
- **Server Actions**: CRUD operations for activities
- **React components**: Activity list, filters, pagination
- **E2E tests**: Complete user flow testing
- **Database tests**: RLS policy validation with pgTAP
- **Performance optimization**: Database indexes for fast queries

## Running This Example

```bash
cd examples/01-team-activity-log

# Run TAC-9 with the example config
uv run ../../orchestrator/cli.py full \
  "Add a team activity log that tracks all member actions with filtering by member, date range, and activity type. Include pagination and real-time updates."
```

## Expected Output

### 1. PRD (Product Requirements Document)

**Location**: `workspace/feature-team-activity-log/01-prd/prd.md`

Key sections:
- User personas (Team Owner, Team Member, Admin)
- User stories with acceptance criteria
- Technical considerations (packages, tables, permissions)
- Success metrics

### 2. Database Migration

**Location**: `workspace/feature-team-activity-log/03-database/migration.sql`

Creates:
```sql
CREATE TABLE public.team_activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES public.accounts(id),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  activity_type TEXT NOT NULL,
  activity_data JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_team_activities_account_id ON public.team_activities(account_id);
CREATE INDEX idx_team_activities_user_id ON public.team_activities(user_id);
CREATE INDEX idx_team_activities_created_at ON public.team_activities(created_at DESC);
CREATE INDEX idx_team_activities_type ON public.team_activities(activity_type);

-- RLS Policies
CREATE POLICY "Team members can view their team's activities"
  ON public.team_activities
  FOR SELECT
  USING (
    account_id IN (
      SELECT account_id FROM accounts_memberships
      WHERE user_id = auth.uid()
    )
  );
```

### 3. Server Actions

**Location**: `workspace/feature-team-activity-log/04-backend/server-actions.ts`

```typescript
'use server';

export const getTeamActivities = enhanceAction(
  async ({ accountId, filters, pagination }) => {
    const client = getSupabaseServerClient();

    let query = client
      .from('team_activities')
      .select('*, user:users(name, email)', { count: 'exact' })
      .eq('account_id', accountId)
      .order('created_at', { ascending: false });

    // Apply filters
    if (filters.userId) {
      query = query.eq('user_id', filters.userId);
    }

    if (filters.activityType) {
      query = query.eq('activity_type', filters.activityType);
    }

    if (filters.startDate) {
      query = query.gte('created_at', filters.startDate);
    }

    if (filters.endDate) {
      query = query.lte('created_at', filters.endDate);
    }

    // Pagination
    const { data, count, error } = await query
      .range(pagination.offset, pagination.offset + pagination.limit - 1);

    if (error) throw error;

    return {
      success: true,
      data: {
        activities: data,
        total: count,
        hasMore: count > pagination.offset + pagination.limit,
      },
    };
  }
);
```

### 4. React Components

**Location**: `workspace/feature-team-activity-log/05-frontend/components/`

- `team-activity-list.tsx`: Main list component
- `activity-filters.tsx`: Filter controls
- `activity-item.tsx`: Individual activity display
- `activity-pagination.tsx`: Pagination controls

### 5. E2E Tests

**Location**: `workspace/feature-team-activity-log/06-tests/e2e/team-activities.spec.ts`

```typescript
test('should display team activities', async ({ page }) => {
  await page.goto('/home/test-team/activities');

  // Verify list renders
  await expect(page.locator('[data-test="activity-list"]')).toBeVisible();

  // Verify activities are shown
  const activities = page.locator('[data-test="activity-item"]');
  await expect(activities).toHaveCount(10);
});

test('should filter activities by user', async ({ page }) => {
  await page.goto('/home/test-team/activities');

  // Select user filter
  await page.selectOption('[data-test="user-filter"]', 'user-123');

  // Click apply
  await page.click('[data-test="apply-filters"]');

  // Verify filtered results
  const activities = page.locator('[data-test="activity-item"]');
  await expect(activities.first()).toContainText('John Doe');
});

test('should paginate activities', async ({ page }) => {
  await page.goto('/home/test-team/activities');

  // Verify first page
  const firstActivity = page.locator('[data-test="activity-item"]').first();
  const firstText = await firstActivity.textContent();

  // Go to next page
  await page.click('[data-test="next-page"]');

  // Verify different activities shown
  const newFirstActivity = page.locator('[data-test="activity-item"]').first();
  const newFirstText = await newFirstActivity.textContent();

  expect(newFirstText).not.toBe(firstText);
});
```

### 6. Database Tests

**Location**: `workspace/feature-team-activity-log/06-tests/db/activity-tests.sql`

```sql
-- Test RLS policies
BEGIN;
SELECT plan(5);

-- Test: Team members can see their team's activities
SET LOCAL role TO authenticated;
SET LOCAL request.jwt.claims TO '{"sub": "user-1"}';

SELECT results_eq(
  'SELECT count(*)::int FROM team_activities WHERE account_id = ''team-1''',
  ARRAY[10],
  'User can see their team activities'
);

-- Test: Team members cannot see other teams' activities
SELECT is_empty(
  'SELECT * FROM team_activities WHERE account_id = ''team-2''',
  'User cannot see other team activities'
);

SELECT * FROM finish();
ROLLBACK;
```

### 7. Security Audit

**Location**: `workspace/feature-team-activity-log/07-reviews/security-audit.md`

Reports:
- ✅ No SQL injection vulnerabilities
- ✅ RLS policies properly isolate data
- ✅ Input validation via Zod schemas
- ✅ No sensitive data in activity logs
- ⚠️ Consider rate limiting for activity creation

### 8. Documentation

**Location**: `workspace/feature-team-activity-log/08-docs/README.md`

Includes:
- Feature overview
- API reference
- Usage examples
- Configuration options
- Troubleshooting

## Integration with Your Project

### 1. Apply Migration

```bash
cd your-nextjs-project

# Copy migration
cp workspace/feature-team-activity-log/03-database/migration.sql \
  supabase/migrations/$(date +%Y%m%d%H%M%S)_team_activities.sql

# Apply migration
pnpm supabase db push
```

### 2. Add Server Actions

```bash
# Create feature package
mkdir -p packages/features/team-activities/_lib/server

# Copy files
cp workspace/feature-team-activity-log/04-backend/* \
  packages/features/team-activities/_lib/server/
```

### 3. Add Components

```bash
# Copy components
cp workspace/feature-team-activity-log/05-frontend/components/* \
  packages/features/team-activities/_components/
```

### 4. Add Route

```bash
# Create page
mkdir -p apps/web/app/home/[account]/activities

# Create page.tsx
cat > apps/web/app/home/[account]/activities/page.tsx <<'EOF'
import { TeamActivityList } from '@/packages/features/team-activities';

export default async function ActivitiesPage({ params }) {
  const account = (await params).account;

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Team Activities</h1>
      <TeamActivityList accountSlug={account} />
    </div>
  );
}
EOF
```

### 5. Run Tests

```bash
# Copy E2E tests
cp workspace/feature-team-activity-log/06-tests/e2e/* \
  apps/e2e/tests/team-activities/

# Run tests
pnpm test:e2e
```

## Key Learnings

1. **Multi-tenant Design**: Activity logs must be scoped to accounts
2. **Performance**: Indexes are critical for date-range queries
3. **Security**: RLS ensures users only see their team's data
4. **Testing**: E2E tests validate complete user flows
5. **Documentation**: Generated docs help with future maintenance

## Customization

You can modify the generated code to add:
- **Real-time updates**: Use Supabase Realtime subscriptions
- **Export functionality**: Download activities as CSV
- **Advanced filters**: Search by keyword, multiple activity types
- **Activity details**: Expand items to show full JSON data
- **Notifications**: Alert on specific activity types

## Production Checklist

Before deploying:
- [ ] Review all generated code
- [ ] Run security audit recommendations
- [ ] Test with real data
- [ ] Add error boundaries
- [ ] Configure rate limiting
- [ ] Set up monitoring/alerts
- [ ] Update team navigation to include Activities link
- [ ] Train users on new feature
