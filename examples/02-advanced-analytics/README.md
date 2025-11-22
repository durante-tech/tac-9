# Example 2: Advanced Analytics Dashboard

Build a real-time analytics dashboard with Recharts visualization for team metrics.

## Feature Description

A comprehensive analytics dashboard showing team metrics, usage trends, and performance indicators with interactive charts and real-time updates.

## What This Example Demonstrates

- **Database views**: Materialized views for analytics
- **Scheduled jobs**: pg_cron for metric aggregation
- **Real-time subscriptions**: Live data updates
- **Chart components**: Recharts integration
- **Performance optimization**: Caching and indexing
- **Complex queries**: Aggregations, joins, window functions

## Running This Example

```bash
uv run tac9 full \
  "Add an advanced analytics dashboard showing team usage metrics, activity trends over time, top contributors, and performance indicators. Include line charts, bar charts, and pie charts with date range filtering and real-time updates."
```

## Key Components

### Database Schema

```sql
-- Analytics metrics table
CREATE TABLE public.team_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID NOT NULL REFERENCES accounts(id),
  metric_name TEXT NOT NULL,
  metric_value NUMERIC NOT NULL,
  metric_date DATE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Materialized view for dashboard
CREATE MATERIALIZED VIEW team_analytics_daily AS
SELECT
  account_id,
  DATE(created_at) as metric_date,
  COUNT(*) as total_activities,
  COUNT(DISTINCT user_id) as active_users,
  jsonb_object_agg(activity_type, type_count) as activity_breakdown
FROM (
  SELECT
    account_id,
    created_at,
    user_id,
    activity_type,
    COUNT(*) as type_count
  FROM team_activities
  GROUP BY account_id, DATE(created_at), user_id, activity_type
) subquery
GROUP BY account_id, DATE(created_at);

-- Refresh schedule
SELECT cron.schedule(
  'refresh-analytics',
  '0 0 * * *', -- Daily at midnight
  $$REFRESH MATERIALIZED VIEW CONCURRENTLY team_analytics_daily$$
);
```

### React Chart Component

```typescript
'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { useEffect, useState } from 'react';
import { getTeamAnalytics } from '../_lib/server/server-actions';

export function ActivityTrendChart({ accountId }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function loadData() {
      const result = await getTeamAnalytics({ accountId, days: 30 });
      setData(result.data);
    }
    loadData();
  }, [accountId]);

  return (
    <LineChart width={800} height={400} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="activities" stroke="#8884d8" />
      <Line type="monotone" dataKey="users" stroke="#82ca9d" />
    </LineChart>
  );
}
```

## Integration Steps

1. Enable pg_cron extension in Supabase
2. Apply migrations with views and scheduled jobs
3. Add Recharts dependency: `pnpm add recharts`
4. Copy analytics components
5. Create dashboard route
6. Configure refresh schedule

## Performance Optimizations

- Materialized views for pre-computed metrics
- Scheduled jobs instead of real-time aggregation
- Database-level caching
- Optimized indexes on date columns
- Client-side data caching with React Query
