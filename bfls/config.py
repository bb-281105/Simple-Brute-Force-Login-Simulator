"""
Configuration settings for Brute Force Login Simulator
"""

# Login System Configuration
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 30  # seconds
RATE_LIMIT_DELAY = 1  # seconds between attempts

# Brute Force Simulation Configuration
MAX_THREADS = 1  # Set to 1 for sequential, increase for parallel attacks
TIMEOUT = 5  # Request timeout in seconds
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR

# File Paths
USERS_FILE = "users.json"
PASSWORDS_FILE = "passwords.txt"
LOGS_FILE = "attack_logs.txt"

# Security Features (for simulation purposes)
ENABLE_CAPTCHA = False
ENABLE_2FA = False
HASH_PASSWORDS = False  # Simulate hashed passwords