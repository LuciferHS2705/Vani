import { supabase } from '../lib/supabaseClient';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

async function getAuthHeader() {
  const { data } = await supabase.auth.getSession();
  const token = data?.session?.access_token;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function callBackend(path, options = {}) {
  const headers = await getAuthHeader();
  const res = await fetch(`${BACKEND_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...headers, ...(options.headers || {}) },
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}
