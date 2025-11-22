# Example 3: File Upload System

Build a secure, multi-tenant file upload system using Supabase Storage.

## Feature Description

A comprehensive file upload system with drag-and-drop, progress tracking, file type validation, virus scanning, and secure storage with RLS policies.

## What This Example Demonstrates

- **Supabase Storage**: Bucket policies and file management
- **File upload components**: Drag-and-drop with progress
- **Presigned URLs**: Secure file access
- **File type validation**: Client and server-side checks
- **Security scanning**: ClamAV integration (optional)
- **Storage optimization**: Compression and cleanup

## Running This Example

```bash
uv run tac9 full \
  "Add a file upload system with drag-and-drop support, progress tracking, file type validation, and secure storage. Support multiple files, show thumbnails for images, and allow file deletion. Integrate with Supabase Storage."
```

## Key Components

### Storage Bucket Policies

```sql
-- Create storage bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('team-files', 'team-files', false);

-- RLS Policies for storage
CREATE POLICY "Team members can upload files to their team folder"
  ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'team-files' AND
    (storage.foldername(name))[1] IN (
      SELECT id::text FROM accounts
      JOIN accounts_memberships ON accounts.id = accounts_memberships.account_id
      WHERE accounts_memberships.user_id = auth.uid()
    )
  );

CREATE POLICY "Team members can view their team files"
  ON storage.objects
  FOR SELECT
  USING (
    bucket_id = 'team-files' AND
    (storage.foldername(name))[1] IN (
      SELECT id::text FROM accounts
      JOIN accounts_memberships ON accounts.id = accounts_memberships.account_id
      WHERE accounts_memberships.user_id = auth.uid()
    )
  );
```

### File Upload Component

```typescript
'use client';

import { useDropzone } from 'react-dropzone';
import { uploadFile } from '../_lib/server/server-actions';

export function FileUploader({ accountId }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: async (files) => {
      for (const file of files) {
        await uploadFile({ accountId, file });
      }
    },
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/pdf': ['.pdf'],
      'application/vnd.ms-excel': ['.xls', '.xlsx'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  return (
    <div {...getRootProps()} className="border-2 border-dashed p-8">
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop files here...</p>
      ) : (
        <p>Drag & drop files, or click to select</p>
      )}
    </div>
  );
}
```

## Security Features

- File type validation (client and server)
- Size limits
- Virus scanning (optional ClamAV integration)
- Secure presigned URLs
- Automatic expiration
- RLS-based access control

## Integration Requirements

1. Enable Supabase Storage
2. Create storage bucket
3. Apply RLS policies
4. Add react-dropzone: `pnpm add react-dropzone`
5. Configure file size limits
6. (Optional) Set up ClamAV for scanning
