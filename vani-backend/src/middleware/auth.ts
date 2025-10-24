import { Request, Response, NextFunction } from "express";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";

dotenv.config();
const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_ANON_KEY!);

export async function supabaseAuthMiddleware(req: Request, res: Response, next: NextFunction) {
  try {
    const authHeader = (req.headers.authorization || "");
    const token = authHeader.startsWith("Bearer ") ? authHeader.split(" ")[1] : null;
    if (!token) return res.status(401).json({ error: "No token provided" });

    // Attempt to get user from Supabase using the token
    const { data, error } = await supabase.auth.getUser(token);
    if (error || !data?.user) return res.status(401).json({ error: "Invalid or expired token" });

    // attach user to request
    (req as any).user = data.user;
    next();
  } catch (err) {
    return res.status(500).json({ error: "Auth verification failed" });
  }
}
