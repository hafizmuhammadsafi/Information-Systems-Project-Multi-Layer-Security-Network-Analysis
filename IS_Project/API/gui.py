import webview
from auth import login_backend, signup_backend, forgot_backend, verify_otp_backend, reset_password_backend, resend_otp_backend
from database import init_db
from captcha_gen import generate_visual_captcha
import socket
import platform
import psutil
import requests
from datetime import datetime
import subprocess
import json

init_db()

class API:
    def __init__(self):
        self.current_captcha = ""
        self.logged_in_user = None

    def get_new_captcha(self):
        answer, img_data = generate_visual_captcha()
        self.current_captcha = answer
        return img_data

    def check_captcha(self, user_input):
        if not user_input or not self.current_captcha:
            return False
        clean_input = user_input.replace(" ", "").upper()
        clean_answer = self.current_captcha.replace(" ", "").upper()
        return clean_input == clean_answer

    def login(self, email, password):
        return login_backend(email, password)

    def signup(self, name, email, password, captcha_text):
        if not self.check_captcha(captcha_text):
           return {"status": "error", "message": "Invalid CAPTCHA code!"}
        return signup_backend(name, email, password)

    def verify_otp(self, email, otp):
        result = verify_otp_backend(email, otp)
        if result["status"] == "ok":
            self.logged_in_user = result["username"]
        return result

    def forgot(self, email):
        return forgot_backend(email)

    def reset_password(self, email, new_password):
        return reset_password_backend(email, new_password)

    def resend_otp(self, email):
        return resend_otp_backend(email)

    # --- HACKER DASHBOARD FUNCTIONS ---
    
    def get_system_info(self):
        """Get detailed system information"""
        try:
            return {
                "status": "success",
                "data": {
                    "hostname": socket.gethostname(),
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "platform_version": platform.version(),
                    "architecture": platform.machine(),
                    "processor": platform.processor(),
                    "ram": f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB",
                    "cpu_count": psutil.cpu_count(),
                    "cpu_percent": psutil.cpu_percent(interval=1),
                    "ip_address": socket.gethostbyname(socket.gethostname())
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_network_interfaces(self):
        """Get all network interfaces"""
        try:
            interfaces = psutil.net_if_addrs()
            result = {}
            for interface_name, interface_addresses in interfaces.items():
                result[interface_name] = []
                for address in interface_addresses:
                    result[interface_name].append({
                        "family": str(address.family),
                        "address": address.address,
                        "netmask": address.netmask,
                        "broadcast": address.broadcast
                    })
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def scan_port(self, host, port):
        """Scan a specific port on a host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, int(port)))
            sock.close()
            return {
                "status": "success",
                "open": result == 0,
                "port": port,
                "host": host
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_ip_info(self, ip=None):
        """Get geolocation info for an IP address"""
        try:
            if not ip:
                ip = requests.get('https://api.ipify.org').text
            
            response = requests.get(f'http://ip-api.com/json/{ip}')
            data = response.json()
            
            return {
                "status": "success",
                "data": {
                    "ip": data.get("query"),
                    "country": data.get("country"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "zip": data.get("zip"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon"),
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "timezone": data.get("timezone")
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def dns_lookup(self, domain):
        """Perform DNS lookup"""
        try:
            ip = socket.gethostbyname(domain)
            return {
                "status": "success",
                "domain": domain,
                "ip": ip
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_network_stats(self):
        """Get network statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                "status": "success",
                "data": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                    "errin": net_io.errin,
                    "errout": net_io.errout,
                    "dropin": net_io.dropin,
                    "dropout": net_io.dropout
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def ping_host(self, host):
        """Ping a host"""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '4', host]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            return {
                "status": "success",
                "output": output
            }
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.output}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def traceroute(self, host):
        """Traceroute to a host"""
        try:
            command = ['tracert', host] if platform.system().lower() == 'windows' else ['traceroute', host]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, timeout=30)
            return {
                "status": "success",
                "output": output
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Traceroute timed out"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.output}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_active_connections(self):
        """Get active network connections"""
        try:
            connections = psutil.net_connections(kind='inet')
            result = []
            for conn in connections[:50]:  # Limit to 50 connections
                result.append({
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                    "status": conn.status,
                    "pid": conn.pid
                })
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def whois_lookup(self, domain):
        """Perform WHOIS lookup (simplified)"""
        try:
            # This is a basic implementation
            ip = socket.gethostbyname(domain)
            return {
                "status": "success",
                "domain": domain,
                "ip": ip,
                "message": "Basic WHOIS - install python-whois for detailed info"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- NAVIGATION ---
    def open_signup(self): 
        window.load_url("web/signup.html")
    
    def open_login(self): 
        window.load_url("web/login.html")
    
    def open_otp_page(self, email, mode='login'): 
        window.load_url(f"web/otp.html?email={email}&mode={mode}")
    
    def open_reset(self, email, username): 
        window.load_url(f"web/reset.html?email={email}&user={username}")
    
    def open_forgot(self): 
        window.load_url("web/forgot.html")
    
    def open_welcome(self, username): 
        window.load_url(f"web/welcome.html?user={username}")
    
    def open_dashboard(self, username):
        """Open the hacker dashboard"""
        window.load_url(f"web/dashboard.html?user={username}")
    
    def logout(self):
        """Logout user"""
        self.logged_in_user = None
        window.load_url("web/login.html")

def start():
    global window
    api = API()
    window = webview.create_window(
        "CyberSec Login System", 
        "web/login.html", 
        width=1400, 
        height=900, 
        resizable=True, 
        js_api=api
    )
    webview.start()

if __name__ == "__main__":
    start()