#!/usr/bin/env python3
"""
Initialize the Garmin SQLite database
包含完整字段列表，与 garmin_db_reader.py 保持一致
"""
import sqlite3
import os
from pathlib import Path

DB_PATH = Path.home() / ".clawdbot" / "garmin" / "data.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ─── daily_metrics（每日健康指标）─────────────────────
# 原始23字段 + 新增3字段 = 26字段
c.execute("""CREATE TABLE IF NOT EXISTS daily_metrics (
    date TEXT PRIMARY KEY,
    steps INTEGER,
    distance_km REAL,
    calories INTEGER,
    active_seconds INTEGER,
    floors INTEGER,
    resting_heart_rate INTEGER,
    min_heart_rate INTEGER,
    max_heart_rate INTEGER,
    body_battery_current INTEGER,
    body_battery_highest INTEGER,
    body_battery_lowest INTEGER,
    body_battery_charged INTEGER,
    body_battery_drained INTEGER,
    avg_stress INTEGER,
    max_stress INTEGER,
    hrv_value INTEGER,
    breathing_rate REAL,
    vo2_max REAL,
    fitness_age INTEGER,
    last_sync TEXT,
    -- 新增字段（与 SKILL.md 保持一致）
    moderate_intensity_minutes INTEGER,
    vigorous_intensity_minutes INTEGER,
    stress_average INTEGER,
    -- 原始缺失字段（保证兼容性）
    calories_active REAL,
    calories_bmr REAL,
    floors_descended REAL,
    intensity_minutes INTEGER
)""")

# ─── sleep_data（睡眠数据）──────────────────────────
# 原始10字段 + 新增5字段 = 15字段
c.execute("""CREATE TABLE IF NOT EXISTS sleep_data (
    date TEXT PRIMARY KEY,
    total_sleep_hours REAL,
    deep_sleep_hours REAL,
    light_sleep_hours REAL,
    rem_sleep_hours REAL,
    awake_time_minutes INTEGER,
    sleep_score INTEGER,
    sleep_quality TEXT,
    avg_heart_rate REAL,
    avg_spo2 REAL,
    last_sync TEXT,
    -- 新增字段
    duration_minutes INTEGER,
    nap_count INTEGER,
    nap_total_minutes INTEGER,
    nap_details TEXT,
    sleep_source TEXT
)""")

# ─── workouts（运动记录）────────────────────────────
c.execute("""CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    type TEXT,
    name TEXT,
    distance_km REAL,
    duration_seconds INTEGER,
    calories INTEGER,
    avg_heart_rate INTEGER,
    max_heart_rate INTEGER,
    last_sync TEXT
)""")

# ─── sync_log（同步日志）────────────────────────────
c.execute("""CREATE TABLE IF NOT EXISTS sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_time TEXT,
    source TEXT,
    records INTEGER,
    status TEXT
)""")

conn.commit()
conn.close()
print(f"✅ Database initialized at {DB_PATH}")
