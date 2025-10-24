# Vani FastAPI Backend (Vercel + Supabase Postgres + JWT auth)

This scaffold implements a FastAPI backend that matches the features of your Vani frontend:
- Signup / Login (custom JWT)
- User profile
- Dashboard (recent uploads, progress items, interview count)
- Progress CRUD
- Mock interview CRUD
- Uploads using **Supabase Storage** (file uploaded to a bucket; DB stores path + public URL)

## Environment variables (required)
- DATABASE_URL = your Supabase Postgres connection string (e.g., from Supabase Project -> Settings -> Database -> Connection string)
- SUPABASE_URL = e.g. https://xyz.supabase.co
- SUPABASE_KEY = Supabase service_role key (for server-side storage access)
- SUPABASE_BUCKET = (optional) bucket name, default `vani-uploads`
- JWT_SECRET = secret for signing tokens

## Deployment notes
- This project is designed to be deployed to Vercel (Python runtime). Vercel will run FastAPI as a serverless function — long-lived DB connections are discouraged; however, Supabase Postgres is fine for persistence.
- Make sure to set the env vars in Vercel dashboard.
- Create the database tables (see migration below) or use the provided SQL to create tables via Supabase SQL editor.

## Create tables (example SQL)
Run this in Supabase SQL editor or psql:
```sql
-- users
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- progress
CREATE TABLE IF NOT EXISTS progress (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title TEXT,
  details TEXT,
  percent INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT now()
);

-- mock_interviews
CREATE TABLE IF NOT EXISTS mock_interviews (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  topic TEXT,
  notes TEXT,
  score INTEGER,
  created_at TIMESTAMP DEFAULT now()
);

-- uploads
CREATE TABLE IF NOT EXISTS uploads (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  filename TEXT,
  mime TEXT,
  supabase_path TEXT,
  created_at TIMESTAMP DEFAULT now()
);
```

## How to use locally
1. Set environment variables (DATABASE_URL, SUPABASE_URL, SUPABASE_KEY, JWT_SECRET).
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Next steps / security
- Use service_role key only on the server (do not expose in frontend).
- For production, consider Supabase Auth for user management (swap custom JWT).
- Add input validation and rate-limiting.

