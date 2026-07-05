"""
Calcyscord.Manager
Database Schema

Questo file contiene tutta la struttura del database del progetto.

Qui verranno definite e create tutte le tabelle utilizzate dal gioco.

Versione: v0.1
"""

import sqlite3

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "data", "calcyscord_manager.db")

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()