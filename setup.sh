#!/bin/bash

# Digital Twin System - Quick Setup & Run Script
echo "🏭 Digital Twin System Setup & Launch"
echo "=====================================\n"

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p DATABASE LOGS SECURITY/audit_logs SECURITY/data_backups SECURITY/keys
mkdir -p ANALYTICS/models ANALYTICS/analysis_cache REPORTS/generated
mkdir -p WEB_APPLICATION/static/js

# Set permissions
chmod 755 DATABASE LOGS SECURITY
chmod 700 SECURITY/keys

# Generate sample data if database doesn't exist
if [ ! -f "DATABASE/health_data.db" ]; then
    echo "📊 Generating sample data..."
    python CONFIG/unified_data_generator.py
fi

# Initialize encryption keys if they don't exist
if [ ! -f "CONFIG/encryption.key" ]; then
    echo "🔐 Generating encryption keys..."
    python -c "
from cryptography.fernet import Fernet
import os
os.makedirs('CONFIG', exist_ok=True)
with open('CONFIG/encryption.key', 'wb') as f:
    f.write(Fernet.generate_key())
with open('CONFIG/salt.key', 'wb') as f:
    f.write(os.urandom(32))
print('Encryption keys generated successfully')
"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database initialization
echo "🗄️ Initializing database..."
python -c "
import sqlite3
import os
from pathlib import Path

Path('DATABASE').mkdir(exist_ok=True)
db_path = 'DATABASE/health_data.db'

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    
    # Create device_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            device_name TEXT,
            device_type TEXT,
            timestamp DATETIME NOT NULL,
            value REAL,
            unit TEXT,
            health_score REAL,
            efficiency_score REAL,
            status TEXT,
            location TEXT
        )
    ''')
    
    # Create system_metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            cpu_usage_percent REAL,
            memory_usage_percent REAL,
            disk_usage_percent REAL,
            network_io_mbps REAL,
            active_connections INTEGER
        )
    ''')
    
    # Create energy_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            power_consumption_kw REAL,
            energy_consumed_kwh REAL,
            efficiency_percent REAL,
            cost_usd REAL
        )
    ''')
    
    conn.commit()
    print('Database tables created successfully')
"

# Fix UI issues
echo "🎨 Applying UI fixes..."
python WEB_APPLICATION/button_fix_script.py

# Check system health
echo "🏥 Checking system health..."
python -c "
import sys
import os
sys.path.append('.')

try:
    from CONFIG.app_config import config
    print('✅ App config loaded successfully')
except ImportError as e:
    print(f'❌ Config import error: {e}')

try:
    from AI_MODULES.health_score import HealthScoreCalculator
    print('✅ Health calculator available')
except ImportError:
    print('⚠️ Health calculator not available')

try:
    from AI_MODULES.alert_manager import AlertManager
    print('✅ Alert manager available')
except ImportError:
    print('⚠️ Alert manager not available')
"

echo "\n🚀 Setup completed! Starting Digital Twin System..."
echo "📊 Dashboard will be available at: http://localhost:5000"
echo "📈 Enhanced Dashboard: http://localhost:5000/dashboard"
echo "\n⏳ Launching application..."

# Start the application
python WEB_APPLICATION/enhanced_flask_app_v2.py