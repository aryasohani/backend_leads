import sqlite3
from typing import Dict, Any, List

DB = "leads.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS offers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      value_props TEXT,
      ideal_use_cases TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS leads (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      role TEXT,
      company TEXT,
      industry TEXT,
      location TEXT,
      linkedin_bio TEXT,
      score INTEGER,
      intent TEXT,
      reasoning TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_offer(offer: Dict[str,Any]):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO offers (name, value_props, ideal_use_cases) VALUES (?, ?, ?)",
              (offer['name'], ",".join(offer['value_props']), ",".join(offer['ideal_use_cases'])))
    conn.commit()
    conn.close()

def fetch_latest_offer():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, value_props, ideal_use_cases FROM offers ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "value_props": row[1].split(","), "ideal_use_cases": row[2].split(",")}
    return None

def save_leads_bulk(leads: List[Dict[str,str]]):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    for lead in leads:
        c.execute("INSERT INTO leads (name,role,company,industry,location,linkedin_bio) VALUES (?,?,?,?,?,?)",
                  (lead['name'], lead['role'], lead['company'], lead['industry'], lead['location'], lead.get('linkedin_bio','')))
    conn.commit()
    conn.close()

def fetch_all_leads_unscored():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE score IS NULL")
    rows = c.fetchall()
    conn.close()
    return rows

def update_lead_score(lead_id:int, score:int, intent:str, reasoning:str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE leads SET score=?, intent=?, reasoning=? WHERE id=?", (score, intent, reasoning, lead_id))
    conn.commit()
    conn.close()

def fetch_all_results():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE score IS NOT NULL")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]
