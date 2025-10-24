import { Router } from "express";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";
import { supabaseAuthMiddleware } from "../middleware/auth";

dotenv.config();
const router = Router();
const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_ANON_KEY!);

// GET / -> list items with cursor pagination (cursor is created_at ISO or id)
router.get("/", async (req, res) => {
  try {
    const { cursor, limit = "10" } = req.query;
    const lim = Number(limit) || 10;

    let query = supabase.from("items").select("*").order("created_at", { ascending: false }).limit(lim + 1);
    if (cursor) {
      // cursor expected as ISO timestamp or UUID; we'll filter by created_at < cursor if ISO
      const cursorStr = String(cursor);
      const isDate = !isNaN(Date.parse(cursorStr));
      if (isDate) {
        query = supabase.from("items").select("*").lt("created_at", cursorStr).order("created_at", { ascending: false }).limit(lim + 1);
      } else {
        // fallback: get items with id < cursor (assuming numeric ids) - not ideal for UUIDs
        query = supabase.from("items").select("*").order("created_at", { ascending: false }).limit(lim + 1);
      }
    }

    const { data, error } = await query;
    if (error) return res.status(400).json({ error: error.message });

    let nextCursor = null;
    if (data && data.length > lim) {
      const next = data[lim];
      nextCursor = next.created_at;
      data.pop();
    }

    res.json({ items: data || [], nextCursor });
  } catch (err: any) {
    res.status(500).json({ error: err.message || "Server error" });
  }
});

// GET /:id -> get item detail
router.get("/:id", async (req, res) => {
  const { id } = req.params;
  const { data, error } = await supabase.from("items").select("*").eq("id", id).maybeSingle();
  if (error) return res.status(400).json({ error: error.message });
  res.json({ item: data });
});

// POST / -> create item (protected)
router.post("/", supabaseAuthMiddleware, async (req: any, res) => {
  const { title, content } = req.body;
  const user = req.user;
  if (!title) return res.status(400).json({ error: "title required" });

  const payload = { title, content, created_at: new Date().toISOString(), user_id: user?.id || null };
  const { data, error } = await supabase.from("items").insert([payload]).select().maybeSingle();
  if (error) return res.status(400).json({ error: error.message });
  res.status(201).json({ item: data });
});

// PUT /:id -> update item (protected)
router.put("/:id", supabaseAuthMiddleware, async (req: any, res) => {
  const { id } = req.params;
  const { title, content } = req.body;
  const user = req.user;

  // naive ownership check: ensure item's user_id == user.id (requires items table has user_id)
  const { data: existing, error: getErr } = await supabase.from("items").select("*").eq("id", id).maybeSingle();
  if (getErr) return res.status(400).json({ error: getErr.message });
  if (!existing) return res.status(404).json({ error: "Item not found" });
  if (existing.user_id && existing.user_id !== user.id) return res.status(403).json({ error: "Not owner" });

  const { data, error } = await supabase.from("items").update({ title, content }).eq("id", id).select().maybeSingle();
  if (error) return res.status(400).json({ error: error.message });
  res.json({ item: data });
});

// DELETE /:id -> delete item (protected)
router.delete("/:id", supabaseAuthMiddleware, async (req: any, res) => {
  const { id } = req.params;
  const user = req.user;

  const { data: existing, error: getErr } = await supabase.from("items").select("*").eq("id", id).maybeSingle();
  if (getErr) return res.status(400).json({ error: getErr.message });
  if (!existing) return res.status(404).json({ error: "Item not found" });
  if (existing.user_id && existing.user_id !== user.id) return res.status(403).json({ error: "Not owner" });

  const { error } = await supabase.from("items").delete().eq("id", id);
  if (error) return res.status(400).json({ error: error.message });
  res.json({ message: "Deleted" });
});

export default router;
