import React, { useState } from 'react';
import { supabase } from '../lib/supabaseClient';
import { callBackend } from '../services/api';

export default function UploadFile() {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState('');

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return;

    const bucket = import.meta.env.VITE_SUPABASE_BUCKET;
    const { data, error } = await supabase.storage
      .from(bucket)
      .upload(`${Date.now()}_${file.name}`, file);
    if (error) return setMsg('Upload failed: ' + error.message);

    const publicURL = supabase.storage.from(bucket).getPublicUrl(`${Date.now()}_${file.name}`).data.publicUrl;
    await callBackend('/api/uploads', {
      method: 'POST',
      body: JSON.stringify({ filename: file.name, public_url: publicURL }),
    });
    setMsg('Upload success!');
  }

  return (
    <form onSubmit={handleUpload}>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button type="submit">Upload</button>
      <div>{msg}</div>
    </form>
  );
}
