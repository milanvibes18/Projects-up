#!/usr/bin/env python3
"""
Enhanced Digital Twin Application
Alternative lightweight implementation for Digital Twin System.
"""

import os
import sys
import json
import logging
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import threading
import time
import uuid
import secrets

# Flask imports
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import eventlet

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class EnhancedDigitalTwinApp:
    """
    Enhanced Digital Twin Application - Lightweight version
    Focuses on core functionality with optimized performance
    """
    
    def __init__(self):
        self.app = None
        self.data_cache = {}
        self.last_cache_update = datetime.min
        self.cache_ttl = timedelta(minutes=2)  # Cache time-to-live
        
        # Initialize logging
        self.setup_logging()
        
        # Create Flask app
        self.create_app()
        
        # Setup routes
        self.setup_routes()
        
        # Initialize sample data
        self.initialize_sample_data()
    
    def setup_logging(self):
        """Setup logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('LOGS/digital_twin_app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('EnhancedApp')
        self.logger.info("Enhanced Digital Twin App initializing...")
    
    def create_app(self):
        """Create Flask application"""
        self.app = Flask(__name__)
        
        # Configuration
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
        self.app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        
        # CORS
        CORS(self.app)
        
        self.logger.info("Flask app created")
    
    def setup_routes(self):
        """Setup all application routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard"""
            return render_template('index.html')
        
        @self.app.route('/dashboard')
        def dashboard():
            """Enhanced dashboard"""
            return render_template('enhanced_dashboard.html')
        
        @self.app.route('/analytics')
        def analytics():
            """Analytics page"""
            return render_template('analytics.html')
        
        @self.app.route('/devices')
        def devices():
            """Devices management page"""
            return render_template('devices_view.html')
        
        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '2.0.0'
            })
        
        # API Routes
        @self.app.route('/api/dashboard_data')
        def api_dashboard_data():
            """Dashboard data API"""
            try:
                data = self.get_dashboard_data()
                return jsonify(data)
            except Exception as e:
                self.logger.error(f"Dashboard data error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/devices')
        def api_devices():
            """Devices data API"""
            try:
                devices = self.get_devices_data()
                return jsonify(devices)
            except Exception as e:
                self.logger.error(f"Devices data error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/alerts')
        def api_alerts():
            """Alerts API"""
            try:
                limit = request.args.get('limit', 10, type=int)
                alerts = self.get_alerts_data(limit)
                return jsonify(alerts)
            except Exception as e:
                self.logger.error(f"Alerts data error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/analytics')
        def api_analytics():
            """Analytics data API"""
            try:
                analytics = self.get_analytics_data()
                return jsonify(analytics)
            except Exception as e:
                self.logger.error(f"Analytics data error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/system_status')
        def api_system_status():
            """System status API"""
            try:
                status = self.get_system_status()
                return jsonify(status)
            except Exception as e:
                self.logger.error(f"System status error: {e}")
                return jsonify({'error': str(e)}), 500
        
        self.logger.info("Routes setup completed")
    
    def initialize_sample_data(self):
        """Initialize sample data for demonstration"""
        self.sample_devices = self.generate_sample_devices()
        self.sample_alerts = self.generate_sample_alerts()
        self.logger.info("Sample data initialized")
    
    def generate_sample_devices(self):
        """Generate sample device data"""
        device_types = [
            'temperature_sensor',
            'pressure_sensor', 
            'vibration_sensor',
            'humidity_sensor',
            'flow_meter'
        ]
        
        locations = [
            'Production Line 1',
            'Production Line 2',
            'Quality Control',
            'Warehouse A',
            'Warehouse B',
            'Maintenance Shop'
        ]
        
        devices = []
        
        for i in range(20):
            device_type = np.random.choice(device_types)
            
            # Determine status based on probability
            status_rand = np.random.random()
            if status_rand > 0.15:
                status = 'normal'
                health_score = np.random.uniform(0.8, 1.0)
            elif status_rand > 0.05:
                status = 'warning'
                health_score = np.random.uniform(0.5, 0.8)
            else:
                status = 'critical'
                health_score = np.random.uniform(0.1, 0.5)
            
            # Generate appropriate value based on device type
            if device_type == 'temperature_sensor':
                value = np.random.uniform(18, 35)
                unit = '°C'
            elif device_type == 'pressure_sensor':
                value = np.random.uniform(900, 1100)
                unit = 'hPa'
            elif device_type == 'vibration_sensor':
                value = np.random.uniform(0.1, 0.5)
                unit = 'mm/s'
            elif device_type == 'humidity_sensor':
                value = np.random.uniform(35, 75)
                unit = '%RH'
            else:  # flow_meter
                value = np.random.uniform(10, 50)
                unit = 'L/min'
            
            device = {
                'device_id': f'DEVICE_{i+1:03d}',
                'name': f'{device_type.replace("_", " ").title()} {i+1}',
                'device_type': device_type,
                'location': np.random.choice(locations),
                'status': status,
                'value': round(value, 2),
                'unit': unit,
                'health_score': health_score,
                'efficiency_score': np.random.uniform(0.7, 1.0),
                'last_maintenance': (datetime.now() - timedelta(days=np.random.randint(1, 90))).isoformat(),
                'installation_date': (datetime.now() - timedelta(days=np.random.randint(100, 1000))).isoformat(),
                'firmware_version': f'{np.random.randint(1, 5)}.{np.random.randint(0, 9)}.{np.random.randint(0, 9)}',
                'timestamp': datetime.now().isoformat()
            }
            
            devices.append(device)
        
        return devices
    
    def generate_sample_alerts(self):
        """Generate sample alerts"""
        alert_templates = [
            {
                'title': 'High Temperature Alert',
                'message': 'Temperature sensor reading above normal threshold',
                'severity': 'warning',
                'category': 'environmental'
            },
            {
                'title': 'Pressure Anomaly Detected',
                'message': 'Unusual pressure readings detected on production line',
                'severity': 'critical',
                'category': 'safety'
            },
            {
                'title': 'Vibration Level Elevated',
                'message': 'Machine vibration levels exceeding normal parameters',
                'severity': 'warning',
                'category': 'maintenance'
            },
            {
                'title': 'Device Communication Lost',
                'message': 'Lost communication with sensor device',
                'severity': 'critical',
                'category': 'connectivity'
            },
            {
                'title': 'Efficiency Drop Detected',
                'message': 'System efficiency has dropped below optimal levels',
                'severity': 'info',
                'category': 'performance'
            }
        ]
        
        alerts = []
        for i in range(15):
            template = np.random.choice(alert_templates)
            device_id = f'DEVICE_{np.random.randint(1, 21):03d}'
            
            alert = {
                'id': str(uuid.uuid4()),
                'title': template['title'],
                'message': f"{template['message']} - {device_id}",
                'severity': template['severity'],
                'category': template['category'],
                'device_id': device_id,
                'timestamp': (datetime.now() - timedelta(minutes=np.random.randint(1, 1440))).isoformat(),
                'acknowledged': np.random.choice([True, False]),
                'resolved': np.random.choice([True, False]) if np.random.random() > 0.7 else False
            }
            
            alerts.append(alert)
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        return alerts
    
    def get_dashboard_data(self):
        """Get dashboard data with caching"""
        now = datetime.now()
        
        # Check cache validity
        if (now - self.last_cache_update) > self.cache_ttl or 'dashboard' not in self.data_cache:
            self.data_cache['dashboard'] = self._fetch_dashboard_data()
            self.last_cache_update = now
        
        return self.data_cache['dashboard']
    
    def _fetch_dashboard_data(self):
        """Fetch fresh dashboard data"""
        try:
            # Update device data with some variation
            self._update_device_values()
            
            # Calculate metrics
            total_devices = len(self.sample_devices)
            active_devices = len([d for d in self.sample_devices if d['status'] == 'normal'])
            warning_devices = len([d for d in self.sample_devices if d['status'] == 'warning'])
            critical_devices = len([d for d in self.sample_devices if d['status'] == 'critical'])
            
            # Calculate average health and efficiency
            health_scores = [d['health_score'] for d in self.sample_devices]
            efficiency_scores = [d['efficiency_score'] for d in self.sample_devices]
            
            avg_health = np.mean(health_scores) * 100 if health_scores else 0
            avg_efficiency = np.mean(efficiency_scores) * 100 if efficiency_scores else 0
            
            # Simulate energy usage
            hour = datetime.now().hour
            base_energy = 1200
            hour_factor = np.sin(2 * np.pi * hour / 24) * 300
            energy_usage = base_energy + hour_factor + np.random.uniform(-50, 50)
            
            # Generate performance trends
            performance_data = self._generate_performance_trends()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'system_health': round(avg_health, 1),
                'active_devices': active_devices,
                'total_devices': total_devices,
                'warning_devices': warning_devices,
                'critical_devices': critical_devices,
                'efficiency': round(avg_efficiency, 1),
                'energy_usage': round(energy_usage, 1),
                'performance_data': performance_data,
                'status_distribution': {
                    'normal': active_devices,
                    'warning': warning_devices,
                    'critical': critical_devices
                },
                'uptime_percent': round(np.random.uniform(98.5, 99.9), 2),
                'response_time_ms': round(np.random.uniform(50, 200), 1)
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching dashboard data: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _update_device_values(self):
        """Update device values with realistic variations"""
        for device in self.sample_devices:
            # Add small random variations to device values
            current_value = device['value']
            variation = np.random.uniform(-0.1, 0.1) * current_value
            device['value'] = round(max(0, current_value + variation), 2)
            
            # Update timestamp
            device['timestamp'] = datetime.now().isoformat()
            
            # Occasionally change status
            if np.random.random() < 0.05:  # 5% chance
                statuses = ['normal', 'warning', 'critical']
                weights = [0.7, 0.25, 0.05]  # Probability weights
                device['status'] = np.random.choice(statuses, p=weights)
                
                # Adjust health score based on status
                if device['status'] == 'normal':
                    device['health_score'] = np.random.uniform(0.8, 1.0)
                elif device['status'] == 'warning':
                    device['health_score'] = np.random.uniform(0.5, 0.8)
                else:  # critical
                    device['health_score'] = np.random.uniform(0.1, 0.5)
    
    def _generate_performance_trends(self):
        """Generate performance trend data"""
        now = datetime.now()
        timestamps = []
        health_scores = []
        efficiency_scores = []
        
        # Generate last 24 hours of data
        for i in range(24):
            time_point = now - timedelta(hours=23-i)
            timestamps.append(time_point.strftime('%H:%M'))
            
            # Create realistic daily patterns
            hour = time_point.hour
            
            # Health score pattern (higher during day shift)
            if 8 <= hour <= 16:  # Day shift
                base_health = 90
            elif 16 <= hour <= 24 or 0 <= hour <= 8:  # Evening/night shift
                base_health = 85
            else:
                base_health = 80
            
            health = base_health + np.random.uniform(-5, 5)
            health_scores.append(round(max(0, min(100, health)), 1))
            
            # Efficiency pattern (similar to health but different base)
            base_efficiency = base_health - 5
            efficiency = base_efficiency + np.random.uniform(-8, 8)
            efficiency_scores.append(round(max(0, min(100, efficiency)), 1))
        
        return {
            'labels': timestamps,
            'health_scores': health_scores,
            'efficiency_scores': efficiency_scores
        }
    
    def get_devices_data(self):
        """Get devices data"""
        # Update device values
        self._update_device_values()
        return self.sample_devices
    
    def get_alerts_data(self, limit=10):
        """Get alerts data"""
        # Occasionally add new alerts
        if np.random.random() < 0.1:  # 10% chance of new alert
            self._add_random_alert()
        
        return self.sample_alerts[:limit]
    
    def _add_random_alert(self):
        """Add a random new alert"""
        alert_templates = [
            ('Sensor Reading Anomaly', 'warning'),
            ('System Performance Alert', 'info'),
            ('Connection Timeout', 'critical'),
            ('Maintenance Required', 'warning')
        ]
        
        title, severity = np.random.choice(alert_templates)
        device_id = f'DEVICE_{np.random.randint(1, 21):03d}'
        
        new_alert = {
            'id': str(uuid.uuid4()),
            'title': title,
            'message': f'{title} detected on {device_id}',
            'severity': severity,
            'category': 'system',
            'device_id': device_id,
            'timestamp': datetime.now().isoformat(),
            'acknowledged': False,
            'resolved': False
        }
        
        # Add to beginning of alerts list
        self.sample_alerts.insert(0, new_alert)
        
        # Keep only last 50 alerts
        self.sample_alerts = self.sample_alerts[:50]
    
    def get_analytics_data(self):
        """Get analytics data for charts"""
        try:
            now = datetime.now()
            timestamps = [(now - timedelta(hours=i)).strftime('%H:%M') for i in range(23, -1, -1)]
            
            # Generate realistic sensor data patterns
            analytics = {
                'temperature': {
                    'labels': timestamps,
                    'values': self._generate_sensor_pattern('temperature', 22, 3, 0.1),
                    'unit': '°C',
                    'threshold': {'min': 18, 'max': 28}
                },
                'pressure': {
                    'labels': timestamps,
                    'values': self._generate_sensor_pattern('pressure', 1013, 20, 0.05),
                    'unit': 'hPa',
                    'threshold': {'min': 980, 'max': 1040}
                },
                'vibration': {
                    'labels': timestamps,
                    'values': self._generate_sensor_pattern('vibration', 0.25, 0.1, 0.2),
                    'unit': 'mm/s',
                    'threshold': {'min': 0, 'max': 0.5}
                },
                'power': {
                    'labels': timestamps,
                    'values': self._generate_sensor_pattern('power', 1200, 300, 0.08),
                    'unit': 'W',
                    'threshold': {'min': 800, 'max': 1800}
                },
                'humidity': {
                    'labels': timestamps,
                    'values': self._generate_sensor_pattern('humidity', 55, 15, 0.12),
                    'unit': '%RH',
                    'threshold': {'min': 40, 'max': 70}
                }
            }
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error generating analytics data: {e}")
            return {}
    
    def _generate_sensor_pattern(self, sensor_type, base_value, amplitude, frequency):
        """Generate realistic sensor data pattern"""
        values = []
        
        for i in range(24):
            # Add daily pattern
            daily_pattern = amplitude * np.sin(2 * np.pi * i / 24 * frequency)
            
            # Add some noise
            noise = np.random.normal(0, amplitude * 0.1)
            
            # Add sensor-specific variations
            if sensor_type == 'vibration':
                # Vibration can have sudden spikes
                if np.random.random() < 0.05:
                    noise += np.random.exponential(0.1)
            elif sensor_type == 'power':
                # Power consumption higher during working hours
                if 8 <= i <= 18:
                    daily_pattern += amplitude * 0.3
            
            value = base_value + daily_pattern + noise
            
            # Ensure positive values for certain sensors
            if sensor_type in ['vibration', 'power']:
                value = max(0, value)
            elif sensor_type == 'humidity':
                value = max(0, min(100, value))
            
            values.append(round(value, 2))
        
        return values
    
    def get_system_status(self):
        """Get system status information"""
        try:
            # Simulate system metrics
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': round(np.random.uniform(20, 80), 1),
                'memory_usage': round(np.random.uniform(40, 75), 1),
                'disk_usage': round(np.random.uniform(45, 85), 1),
                'network_latency': round(np.random.uniform(10, 50), 1),
                'active_connections': len(self.sample_devices),
                'database_status': 'connected',
                'ai_modules_status': 'operational',
                'last_backup': (datetime.now() - timedelta(hours=6)).isoformat(),
                'uptime_hours': round(np.random.uniform(100, 500), 1)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the application"""
        self.logger.info(f"Starting Enhanced Digital Twin App on {host}:{port}")
        
        try:
            self.app.run(
                host=host,
                port=port,
                debug=debug,
                threaded=True
            )
        except KeyboardInterrupt:
            self.logger.info("Application stopped by user")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            raise


# Error handlers
def setup_error_handlers(app):
    """Setup error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500


def create_app():
    """Application factory"""
    try:
        app_instance = EnhancedDigitalTwinApp()
        setup_error_handlers(app_instance.app)
        return app_instance
    except Exception as e:
        logging.error(f"Failed to create app: {e}")
        raise


if __name__ == '__main__':
    # Create and run the application
    try:
        enhanced_app = create_app()
        
        # Get configuration
        host = os.environ.get('HOST', '0.0.0.0')
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        
        # Run application
        enhanced_app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        sys.exit(1)