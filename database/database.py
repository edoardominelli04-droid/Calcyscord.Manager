"""
Calcyscord.Manager
Database Utilities

Funzioni base per comunicare con il database SQLite.
Versione: v0.1
"""

import sqlite3
from database.schema import DB_NAME


def get_connection():
    """
    Crea e restituisce una connessione al database.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query, params=()):
    """
    Esegue una query INSERT, UPDATE o DELETE.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_one(query, params=()):
    """
    Esegue una SELECT e restituisce una sola riga.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row


def fetch_all(query, params=()):
    """
    Esegue una SELECT e restituisce tutte le righe.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows