# Supabase Auth Template (with User Sync)

## Features
- Google Sign-In using Supabase
- Next.js frontend
- Flask backend that:
  - Verifies user's token
  - Inserts/updates user in Supabase `users` table securely

## Setup

### 1. Supabase
- Enable Google provider under Authentication
- Get:
  - Project URL
  - `anon` public key
  - `service_role` key
- Create `users` table:
```sql
create table users (
  id uuid primary key default uuid_generate_v4(),
  email text not null unique,
  name text,
  created_at timestamp default now()
);
```
- Enable RLS

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
