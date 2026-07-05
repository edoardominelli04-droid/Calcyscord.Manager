"""
Calcyscord.Manager
Database Schema

Versione: v0.1
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "data", "calcyscord_manager.db")


def create_manager_teams_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manager_teams (
        user_id TEXT PRIMARY KEY,
        team_name TEXT NOT NULL UNIQUE,
        formation TEXT NOT NULL,
        pending_formation TEXT,
        created_at TEXT NOT NULL,
        last_active_at TEXT NOT NULL,
        active INTEGER DEFAULT 1
    )
    """)


def create_manager_players_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manager_players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        photo_url TEXT,
        club TEXT NOT NULL,
        league TEXT NOT NULL,
        nationality TEXT,
        position TEXT NOT NULL,
        age INTEGER,
        market_value INTEGER DEFAULT 0,
        base_value INTEGER DEFAULT 0,
        tier TEXT NOT NULL,
        status TEXT DEFAULT 'available',
        injured INTEGER DEFAULT 0,
        injury_end TEXT,
        contract_until TEXT,
        owner_id TEXT,
        retired INTEGER DEFAULT 0
    )
    """)


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    create_manager_teams_table(cursor)
    create_manager_players_table(cursor)

    conn.commit()
    conn.close()