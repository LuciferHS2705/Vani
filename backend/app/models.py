from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .db import metadata

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("password_hash", String, nullable=False),
    Column("name", String),
    Column("created_at", DateTime, server_default=func.now()),
)

progress = Table(
    "progress", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("title", String),
    Column("details", Text),
    Column("percent", Integer, default=0),
    Column("created_at", DateTime, server_default=func.now()),
)

mock_interviews = Table(
    "mock_interviews", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("topic", String),
    Column("notes", Text),
    Column("score", Integer),
    Column("created_at", DateTime, server_default=func.now()),
)

uploads = Table(
    "uploads", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("filename", String),
    Column("mime", String),
    Column("supabase_path", String),  # path in Supabase Storage
    Column("created_at", DateTime, server_default=func.now()),
)

