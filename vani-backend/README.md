# vani-backend (Supabase)

This is a ready-to-upload Express + TypeScript backend that uses Supabase (Auth + Postgres) via the Supabase JS client.

## What this package contains
- Express server (TypeScript)
- Auth routes that proxy to Supabase Auth
- Items routes that use Supabase table `items` for CRUD and cursor pagination
- `.env` pre-filled with your Supabase project URL and anon key (replace if needed)

## Before uploading to GitHub
1. Create a Supabase project (you already have one).
2. In Supabase SQL Editor, create the `items` table:

```sql
create table if not exists public.items (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text,
  created_at timestamptz default now()
);
```

3. Optionally, enable Row Level Security and create policies that allow authenticated users to insert/select/update/delete their own items (or keep it open for testing).

## How to run locally (using a GUI IDE or Cursor)
- Open this folder in Cursor or VS Code.
- Install dependencies via the IDE's package manager GUI (or use the terminal if you change your mind).
- Ensure `.env` values are correct.
- Run the `dev` script via your IDE's Run/Debug (ts-node-dev).

## Notes
- This backend relies on the Supabase anon key for client operations. For server-side admin actions you should use the service_role key (keep it secret).
- The auth middleware verifies the user's access token by calling Supabase's `auth.getUser` with the provided token.

