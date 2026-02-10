"""
Brute Force Login Simulator - Simple Version
"""

import json
import time
import hashlib
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import config

class Logger:
    """Logging utility"""
    
    def __init__(self, log_file: str = config.LOGS_FILE):
        self.log_file = log_file
        
    def log(self, level: str, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')

class LoginSystem:
    """Simplified login system"""
    
    def __init__(self):
        self.logger = Logger()
        self.users = self.load_users()
        
    def load_users(self) -> Dict:
        """Load users from JSON file"""
        try:
            with open(config.USERS_FILE, 'r') as f:
                data = json.load(f)
                users_dict = {user['username']: user for user in data['users']}
                print(f"✓ Loaded {len(users_dict)} users")
                return users_dict
        except FileNotFoundError:
            print("✗ Users database not found!")
            return {}
    
    def hash_password(self, password: str) -> str:
        """Simulate password hashing"""
        if config.HASH_PASSWORDS:
            return hashlib.sha256(password.encode()).hexdigest()
        return password
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Simple login check - no lockouts for testing"""
        if username not in self.users:
            return False, "User not found"
        
        user = self.users[username]
        
        # Check credentials directly
        stored_password = self.hash_password(user['password'])
        attempted_password = self.hash_password(password)
        
        if stored_password == attempted_password:
            return True, "Login successful"
        else:
            return False, "Wrong password"

class BruteForceSimulator:
    """Simple brute force simulator"""
    
    def __init__(self, login_system: LoginSystem):
        self.login_system = login_system
        self.logger = Logger()
        self.passwords = self.load_passwords()
        
    def load_passwords(self) -> List[str]:
        """Load password dictionary"""
        try:
            with open(config.PASSWORDS_FILE, 'r') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"✓ Loaded {len(passwords)} passwords")
            return passwords
        except FileNotFoundError:
            print("✗ Password dictionary not found!")
            return []
    
    def attack_single_user(self, username: str) -> Optional[str]:
        """Attack single user"""
        if username not in self.login_system.users:
            print(f"✗ User '{username}' not found")
            return None
        
        print(f"\n{'='*50}")
        print(f"ATTACKING USER: {username}")
        print(f"{'='*50}")
        
        start_time = time.time()
        
        for i, password in enumerate(self.passwords, 1):
            print(f"Trying password {i}/{len(self.passwords)}: {password}")
            
            success, message = self.login_system.login(username, password)
            
            if success:
                elapsed = time.time() - start_time
                print(f"\n✓ SUCCESS! Password found: {password}")
                print(f"  Time: {elapsed:.2f}s, Attempts: {i}")
                return password
            
            time.sleep(0.1)  # Small delay
        
        elapsed = time.time() - start_time
        print(f"\n✗ FAILED! No password found for {username}")
        print(f"  Total time: {elapsed:.2f}s")
        return None
    
    def attack_all_users(self):
        """Attack all users"""
        usernames = list(self.login_system.users.keys())
        results = {}
        
        print(f"\n{'='*50}")
        print(f"STARTING ATTACK ON {len(usernames)} USERS")
        print(f"{'='*50}")
        
        for username in usernames:
            password = self.attack_single_user(username)
            results[username] = password
        
        return results

def main():
    """Main program"""
    print("\n" + "="*60)
    print("BRUTE FORCE SIMULATOR - SIMPLE VERSION")
    print("="*60)
    
    # Create fresh log file
    with open(config.LOGS_FILE, 'w') as f:
        f.write("=== Attack Logs ===\n")
        f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    login_system = LoginSystem()
    simulator = BruteForceSimulator(login_system)
    
    print("\nOptions:")
    print("1. Attack single user")
    print("2. Attack all users")
    print("3. Exit")
    
    while True:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            username = input("Enter username to attack: ").strip()
            if username:
                password = simulator.attack_single_user(username)
                if password:
                    print(f"\n✓ CRACKED: {username} -> {password}")
                else:
                    print(f"\n✗ FAILED: Could not crack {username}")
        
        elif choice == "2":
            print("\nStarting attack on all users...")
            results = simulator.attack_all_users()
            
            print("\n" + "="*50)
            print("FINAL RESULTS")
            print("="*50)
            
            success_count = 0
            for username, password in results.items():
                if password:
                    print(f"✓ {username}: {password}")
                    success_count += 1
                else:
                    print(f"✗ {username}: NOT FOUND")
            
            print(f"\nSuccessfully cracked: {success_count}/{len(results)} users")
        
        elif choice == "3":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()