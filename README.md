# 🔐 Multi-Layer Authentication System with Hacker Dashboard

A comprehensive security-focused authentication system with an advanced hacker-themed network monitoring dashboard.

## 🎯 Features

### Authentication System
- **Multi-Layer Security**: Email/Password + OTP verification
- **CAPTCHA Protection**: Visual CAPTCHA on signup
- **Brute Force Protection**: Account blocking after failed attempts
- **Strong Password Policy**: Enforces complex password requirements
- **Password Reset**: Secure password recovery with OTP
- **Session Management**: Secure user sessions

### Hacker Dashboard (Post-Login)
- **System Information**: Detailed OS and hardware specs
- **Network Scanner**: Discover all network interfaces
- **Port Scanner**: Check if specific ports are open/closed
- **IP Geolocation**: Track IP addresses with location data
- **DNS Lookup**: Resolve domain names to IP addresses
- **Active Connections**: Monitor real-time network connections
- **Ping Tool**: Test connectivity to hosts
- **Traceroute**: Trace packet routes to destinations
- **Interactive Terminal**: Execute custom commands
- **Network Statistics**: Real-time bandwidth monitoring
- **Matrix Rain Effect**: Animated cyberpunk background

## 📁 Project Structure

```
project/
│
├── gui.py                 # Enhanced main application with dashboard API
├── auth.py                # Authentication logic
├── database.py            # Database operations
├── otp.py                 # OTP generation and email
├── captcha_gen.py         # CAPTCHA generation
├── logger.py              # Security logging
├── sql_injection.py       # SQL injection testing
├── br_force.py            # Brute force testing tool
├── requirements.txt       # Python dependencies
│
├── web/
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   ├── otp.html           # OTP verification (updated)
│   ├── forgot.html        # Password recovery
│   ├── reset.html         # Password reset
│   ├── dashboard.html     # Hacker dashboard (NEW)
│   └── welcome.html       # Welcome page
│
└── users.db               # SQLite database (auto-created)
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
git clone <your-repo-url>
cd <project-folder>
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Email (Optional but Recommended)
Edit `otp.py` and update the email credentials:
```python
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"  # Use App Password for Gmail
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the generated password in `otp.py`

### Step 4: Run the Application
```bash
python gui.py
```

## 🎮 Usage Guide

### First Time Setup
1. Launch the application
2. Click "Sign Up" to create an account
3. Enter your details and complete the CAPTCHA
4. Check your email for the OTP code
5. Verify your account with the OTP

### Login Process
1. Enter your email and password
2. If correct, an OTP will be sent to your email
3. Enter the OTP code to access the dashboard
4. **Brute Force Protection**: After 3 failed attempts, account is blocked for 3 minutes

### Dashboard Features

#### 1. System Overview
- View detailed system information
- Monitor network statistics in real-time
- Track bandwidth usage

#### 2. Network Scanner
- Discover all network interfaces
- View IP addresses, netmasks, and broadcast addresses

#### 3. Port Scanner
- Scan specific ports on any host
- Check if services are running
- Examples:
  - Port 80: HTTP
  - Port 443: HTTPS
  - Port 22: SSH
  - Port 3306: MySQL

#### 4. IP Tracker
- Get geolocation data for any IP
- Track your own IP
- View ISP and organization info

#### 5. DNS Lookup
- Resolve domain names to IP addresses
- Useful for network troubleshooting

#### 6. Active Connections
- View all active network connections
- See local and remote addresses
- Monitor connection status and PIDs

#### 7. Ping Tool
- Test connectivity to hosts
- Measure latency and packet loss

#### 8. Traceroute
- Trace the path packets take to reach a destination
- Identify network hops and routing issues

#### 9. Terminal
Available commands:
- `help` - Show available commands
- `clear` - Clear terminal
- `sysinfo` - Display system information
- `netstat` - Show network statistics
- `whoami` - Display current user
- `date` - Show current date/time
- `echo [text]` - Echo text back

## 🔒 Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (_, -, @, !)

### Brute Force Protection
- Maximum 3 login attempts
- Account blocked for 3 minutes after 3 failed attempts
- Automatic unblocking after timeout

### OTP Security
- 6-digit random OTP
- 1-minute expiration
- Resend functionality with new OTP

### Database Security
- Parameterized queries (prevents SQL injection)
- bcrypt password hashing
- Foreign key constraints

## 🧪 Testing Security

### SQL Injection Test
```bash
python sql_injection.py
```
This will test common SQL injection payloads against the login system.

### Brute Force Test
```bash
python br_force.py
```
This will attempt to crack passwords using a wordlist (for educational purposes only).

## 🎨 Customization

### Change Theme Colors
Edit the CSS in `web/dashboard.html`:
```css
--primary-color: #00ff41;  /* Matrix green */
--background: #0a0e27;     /* Dark blue */
--panel-bg: rgba(0, 20, 40, 0.6);
```

### Adjust Security Settings
Edit `auth.py`:
```python
OTP_EXPIRY_MINUTES = 1    # OTP validity period
BLOCK_MINUTES = 3         # Account block duration
MAX_ATTEMPTS = 3          # Maximum login attempts
```

### Add Custom Terminal Commands
Edit the `terminalCommands` object in `web/dashboard.html`:
```javascript
terminalCommands.mycommand = () => {
    return 'Custom output';
};
```

## 📊 Network Tools Explained

### Port Scanner
Common ports to scan:
- **20-21**: FTP (File Transfer)
- **22**: SSH (Secure Shell)
- **23**: Telnet
- **25**: SMTP (Email)
- **53**: DNS
- **80**: HTTP (Web)
- **443**: HTTPS (Secure Web)
- **3306**: MySQL
- **3389**: RDP (Remote Desktop)
- **5432**: PostgreSQL

### IP Tracking
The geolocation feature uses the ip-api.com service to provide:
- Country, region, and city
- Coordinates (latitude/longitude)
- ISP and organization
- Timezone information

### Network Statistics
Monitors:
- Bytes sent/received
- Packets sent/received
- Network errors
- Dropped packets

## ⚠️ Important Notes

### Legal and Ethical Use
- **Only use these tools on your own network or with explicit permission**
- Port scanning and network monitoring may be illegal without authorization
- This project is for educational purposes only
- Always respect privacy and legal boundaries

### Performance Considerations
- Traceroute can take 20-30 seconds to complete
- Port scanning multiple ports may trigger security alerts
- Network monitoring uses system resources

### Email Configuration
- Without email configuration, OTP will only be logged to console
- Use App Passwords for Gmail (not your regular password)
- Consider using environment variables for credentials in production

## 🐛 Troubleshooting

### "Email not sent" error
- Check your internet connection
- Verify email credentials in `otp.py`
- For Gmail, ensure "Less secure app access" is enabled or use App Password

### Port scanner shows all ports closed
- Check your firewall settings
- Try scanning well-known open ports (80, 443)
- Ensure you have permission to scan the target host

### Dashboard not loading
- Check that all files are in the correct directories
- Ensure `web/dashboard.html` exists
- Verify Python dependencies are installed

### Database locked error
- Close any other instances of the application
- Delete `users.db` to start fresh (you'll lose all data)
- Check file permissions

## 🔄 Updates and Improvements

### Planned Features
- [ ] Packet capture and analysis
- [ ] Network speed test
- [ ] WHOIS lookup integration
- [ ] Export scan results to CSV/JSON
- [ ] Real-time bandwidth graphs
- [ ] Multiple user profiles
- [ ] Two-factor authentication (TOTP)
- [ ] API key authentication

### Recent Changes
- ✅ Added comprehensive network monitoring dashboard
- ✅ Integrated real networking tools
- ✅ Added interactive terminal
- ✅ Implemented Matrix rain animation
- ✅ Added IP geolocation tracking

## 📝 License

This project is for educational purposes. Use responsibly and ethically.

## 👥 Contributing

Feel free to fork, improve, and submit pull requests!

## 📧 Support

For issues and questions, please check the troubleshooting section or create an issue in the repository.

---

**⚡ Powered by Python, pywebview, and cybersecurity principles ⚡**
