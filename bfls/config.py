"""
Configuration settings for Brute Force Login Simulator
"""

# Login System Configuration
MAX_ATTEMPTS = 100  # बहुत बड़ा कर दें ताकि lock ना हो
LOCKOUT_TIME = 30  # seconds
RATE_LIMIT_DELAY = 0  # No delay for faster testing

# Brute Force Simulation Configuration
MAX_THREADS = 1
TIMEOUT = 5
LOG_LEVEL = "INFO"

# File Paths
USERS_FILE = "users.json"
PASSWORDS_FILE = "passwords.txt"
LOGS_FILE = "attack_logs.txt"

# Security Features
ENABLE_CAPTCHA = False
ENABLE_2FA = False
HASH_PASSWORDS = False

# Attack Settings
RESET_BEFORE_ATTACK = True
SKIP_LOCK_CHECK = True  # Lock check skip करें