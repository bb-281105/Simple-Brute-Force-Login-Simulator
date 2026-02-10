"""
Brute Force Login Simulator
A simulation tool to demonstrate brute force attacks and defense mechanisms
"""

import json
import time
import hashlib
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import config

class Logger:
    """Logging utility for tracking attacks"""
    
    def __init__(self, log_file: str = config.LOGS_FILE):
        self.log_file = log_file
        self.clear_logs()
        
    def log(self, level: str, message: str):
        """Log message with timestamp and level"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def clear_logs(self):
        """Clear existing logs"""
        with open(self.log_file, 'w') as f:
            f.write("=== Brute Force Attack Logs ===\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

class LoginSystem:
    """Simulated login system with security features"""
    
    def __init__(self):
        self.logger = Logger()
        self.users = self.load_users()
        self.lock = threading.Lock()
        
    def load_users(self) -> Dict:
        """Load users from JSON file"""
        try:
            with open(config.USERS_FILE, 'r') as f:
                data = json.load(f)
                users_dict = {user['username']: user for user in data['users']}
                self.logger.log("INFO", f"Loaded {len(users_dict)} users from database")
                return users_dict
        except FileNotFoundError:
            self.logger.log("ERROR", "Users database not found!")
            return {}
    
    def save_users(self):
        """Save users to JSON file"""
        with self.lock:
            users_list = list(self.users.values())
            data = {"users": users_list}
            with open(config.USERS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Simulate password hashing"""
        if config.HASH_PASSWORDS:
            return hashlib.sha256(password.encode()).hexdigest()
        return password
    
    def is_account_locked(self, username: str) -> bool:
        """Check if account is locked"""
        if username not in self.users:
            return False
            
        user = self.users[username]
        if user['account_locked'] and user['lockout_until']:
            lockout_time = datetime.fromisoformat(user['lockout_until'])
            if datetime.now() < lockout_time:
                return True
            else:
                # Auto-unlock after lockout period
                user['account_locked'] = False
                user['failed_attempts'] = 0
                user['lockout_until'] = None
                self.save_users()
                return False
        return False
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Attempt login with security checks"""
        if username not in self.users:
            self.logger.log("WARNING", f"Login failed: User '{username}' not found")
            return False, "Invalid credentials"
        
        user = self.users[username]
        
        # Check if account is locked
        if self.is_account_locked(username):
            lockout_time = datetime.fromisoformat(user['lockout_until'])
            remaining = lockout_time - datetime.now()
            self.logger.log("WARNING", f"Account '{username}' is locked. Remaining: {remaining.seconds}s")
            return False, f"Account locked. Try again in {remaining.seconds} seconds"
        
        # Rate limiting simulation
        time.sleep(config.RATE_LIMIT_DELAY)
        
        # Check credentials
        stored_password = self.hash_password(user['password'])
        attempted_password = self.hash_password(password)
        
        if stored_password == attempted_password:
            # Successful login - reset failed attempts
            user['failed_attempts'] = 0
            user['account_locked'] = False
            user['lockout_until'] = None
            self.save_users()
            
            self.logger.log("SUCCESS", f"Successful login for user '{username}'")
            return True, "Login successful"
        else:
            # Failed login
            with self.lock:
                user['failed_attempts'] += 1
                
                if user['failed_attempts'] >= config.MAX_ATTEMPTS:
                    user['account_locked'] = True
                    lockout_until = datetime.now() + timedelta(seconds=config.LOCKOUT_TIME)
                    user['lockout_until'] = lockout_until.isoformat()
                    self.logger.log("SECURITY", f"Account '{username}' locked after {config.MAX_ATTEMPTS} failed attempts")
                
                self.save_users()
            
            self.logger.log("FAILURE", f"Failed login for user '{username}'. Attempt {user['failed_attempts']}/{config.MAX_ATTEMPTS}")
            return False, "Invalid credentials"

class BruteForceSimulator:
    """Simulate brute force attacks"""
    
    def __init__(self, login_system: LoginSystem):
        self.login_system = login_system
        self.logger = login_system.logger
        self.passwords = self.load_passwords()
        
    def load_passwords(self) -> List[str]:
        """Load password dictionary"""
        try:
            with open(config.PASSWORDS_FILE, 'r') as f:
                passwords = [line.strip() for line in f if line.strip()]
            self.logger.log("INFO", f"Loaded {len(passwords)} passwords from dictionary")
            return passwords
        except FileNotFoundError:
            self.logger.log("ERROR", "Password dictionary not found!")
            return []
    
    def attack_single_user(self, username: str) -> Optional[str]:
        """Brute force attack on a single user"""
        if username not in self.login_system.users:
            self.logger.log("ERROR", f"User '{username}' not found in database")
            return None
        
        self.logger.log("INFO", f"Starting brute force attack on user: {username}")
        self.logger.log("INFO", f"Testing {len(self.passwords)} passwords...")
        
        start_time = time.time()
        attempts = 0
        
        for password in self.passwords:
            attempts += 1
            
            # Check if account got locked during attack
            if self.login_system.is_account_locked(username):
                self.logger.log("WARNING", f"Attack stopped: Account '{username}' is locked")
                break
            
            success, message = self.login_system.login(username, password)
            
            if success:
                elapsed = time.time() - start_time
                self.logger.log("CRACKED", f"Password found for '{username}': {password}")
                self.logger.log("CRACKED", f"Time taken: {elapsed:.2f}s, Attempts: {attempts}")
                return password
            
            if attempts % 5 == 0:
                self.logger.log("DEBUG", f"Tested {attempts} passwords...")
        
        elapsed = time.time() - start_time
        self.logger.log("FAILED", f"Attack completed. No password found for '{username}'")
        self.logger.log("FAILED", f"Total time: {elapsed:.2f}s, Total attempts: {attempts}")
        return None
    
    def attack_all_users(self):
        """Attack all users in the database"""
        usernames = list(self.login_system.users.keys())
        results = {}
        
        self.logger.log("INFO", f"Starting attack on {len(usernames)} users")
        
        for username in usernames:
            self.logger.log("INFO", "\n" + "="*50)
            password = self.attack_single_user(username)
            results[username] = password
        
        return results

def display_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("BRUTE FORCE LOGIN SIMULATOR")
    print("="*60)
    print("1. Test single user login")
    print("2. Brute force single user")
    print("3. Brute force all users")
    print("4. View current users")
    print("5. Reset all accounts")
    print("6. View attack logs")
    print("7. Exit")
    print("="*60)

def test_single_login(login_system: LoginSystem):
    """Test manual login"""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    success, message = login_system.login(username, password)
    print(f"\nResult: {message}")
    print(f"Success: {success}")

def main():
    """Main program entry point"""
    print("Initializing Brute Force Login Simulator...")
    
    login_system = LoginSystem()
    simulator = BruteForceSimulator(login_system)
    
    while True:
        display_menu()
        
        try:
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                test_single_login(login_system)
            
            elif choice == "2":
                username = input("Enter username to attack: ").strip()
                if username:
                    password = simulator.attack_single_user(username)
                    if password:
                        print(f"\n✓ Password cracked: {password}")
                    else:
                        print("\n✗ Password not found in dictionary")
            
            elif choice == "3":
                print("\nStarting attack on all users...")
                results = simulator.attack_all_users()
                
                print("\n" + "="*50)
                print("ATTACK SUMMARY")
                print("="*50)
                for username, password in results.items():
                    status = f"✓ {password}" if password else "✗ Not found"
                    print(f"{username}: {status}")
            
            elif choice == "4":
                print("\n" + "="*50)
                print("CURRENT USERS")
                print("="*50)
                for username, user in login_system.users.items():
                    locked = "🔒 LOCKED" if user['account_locked'] else "✅ ACTIVE"
                    attempts = user['failed_attempts']
                    print(f"{username} - {locked} (Failed attempts: {attempts})")
            
            elif choice == "5":
                confirm = input("Reset all accounts? (yes/no): ").strip().lower()
                if confirm == "yes":
                    for user in login_system.users.values():
                        user['failed_attempts'] = 0
                        user['account_locked'] = False
                        user['lockout_until'] = None
                    login_system.save_users()
                    print("All accounts reset successfully!")
            
            elif choice == "6":
                try:
                    with open(config.LOGS_FILE, 'r') as f:
                        print("\n" + "="*60)
                        print("ATTACK LOGS")
                        print("="*60)
                        print(f.read())
                except FileNotFoundError:
                    print("No logs found!")
            
            elif choice == "7":
                print("\nExiting simulator. Goodbye!")
                break
            
            else:
                print("Invalid choice! Please select 1-7")
        
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()