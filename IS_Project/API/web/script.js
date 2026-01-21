let resendTimerInterval;
let blockTimerInterval;
let allRequirementsMet = false;

// 1. PASSWORD VALIDATION
function validatePassword(p) {
    const hasAlpha = /[A-Za-z]/.test(p);
    const hasNumber = /[0-9]/.test(p);
    const hasSymbol = /[_@!-]/.test(p);
    const hasLength = p.length >= 8;

    // Update UI (MATCHES HTML IDS)
    updateRule("rule-alpha", hasAlpha, "Letters (A-Z)");
    updateRule("rule-num", hasNumber, "Numbers (0-9)");
    updateRule("rule-sym", hasSymbol, "Symbols (_@!-)");

    allRequirementsMet = hasAlpha && hasNumber && hasSymbol && hasLength;

    // 🔥 Enable / Disable button LIVE
    const btn = document.getElementById("update-btn");
    if (btn) {
        btn.disabled = !allRequirementsMet;
        btn.style.opacity = allRequirementsMet ? "1" : "0.5";
    }
}

function updateRule(id, ok, text) {
    const el = document.getElementById(id);
    if (el) {
        el.innerText = (ok ? "✔ " : "✖ ") + text;
        el.style.color = ok ? "#22c55e" : "#ef4444";
    }
}

// 2. CAPTCHA REVEAL LOGIC
function handlePasswordEnter(event) {
    if (event.key === "Enter") {
        if (allRequirementsMet) {
            const captchaSec = document.getElementById("captcha-section");
            const signupBtn = document.getElementById("signup-btn");
            if (captchaSec) captchaSec.style.display = "block";
            if (signupBtn) signupBtn.style.display = "block";
            refreshCaptcha();
        } else {
            alert("Please fulfill all password requirements first!");
        }
    }
}

function refreshCaptcha() {
    window.pywebview.api.get_new_captcha().then(imgData => {
        const img = document.getElementById("captcha-img");
        if (img) img.src = imgData;
    });
}


function signupUser() {
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let captcha = document.getElementById("captcha-input").value.trim();

    if (!captcha) {
        alert("Please enter the CAPTCHA.");
        return;
    }

    window.pywebview.api.signup(name, email, password, captcha)
        .then(result => {
            console.log("Signup result:", result); // 🔍 debug

            if (!result || !result.status) {
                alert("Unexpected response from server.");
                return;
            }

            if (result.status === "error") {
                alert(result.message);
                refreshCaptcha();
                return;
            }

            if (result.status === "success") {
                alert("OTP sent to email.");
                window.pywebview.api.open_otp_page(email, "signup");
            }
        });
}

function loginUser() {
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let captchaInput = document.getElementById("captcha-input").value.trim();
    let btn = document.getElementById("login-btn");
    let captchaSec = document.getElementById("captcha-section");

    // If captcha is not showing, we are in Step 1: Check Password
    if (captchaSec.style.display === "none") {
        btn.disabled = true; btn.innerText = "Checking...";
        
        window.pywebview.api.login(email, password).then(result => {
            btn.disabled = false; btn.innerText = "Login";
            
            if (result.status === "otp_sent") {
                // Password correct! Now show captcha instead of jumping to OTP
                captchaSec.style.display = "block";
                refreshCaptcha();
                alert("Credentials verified. Please complete CAPTCHA.");
            } else if (result.status === "wrong") {
                alert("Wrong password!");
            } else if (result.status === "blocked") {
                startBlockTimer(result.remaining_time);
            } else {
                alert(result.message);
            }
        });
    } 
    // If captcha IS showing, we are in Step 2: Verify Captcha
    else {
        if (!captchaInput) {
            alert("Please enter the CAPTCHA code.");
            return;
        }

        window.pywebview.api.check_captcha(captchaInput).then(isValid => {
            if (isValid) {
                // Success! Now we move to OTP page
                // Note: You might need your backend to actually send the OTP here
                window.pywebview.api.open_otp_page(email, 'login');
            } else {
                alert("Invalid CAPTCHA code. Try again.");
                refreshCaptcha();
            }
        });
    }
}

// Ensure this matches your gui.py function name
function refreshCaptcha() {
    window.pywebview.api.get_new_captcha().then(imgData => {
        document.getElementById("captcha-img").src = imgData;
    });
}

function verifyOtpUser() {
    let params = new URLSearchParams(window.location.search);
    let email = params.get("email");
    let mode = params.get("mode");
    let otp = document.getElementById("otp-input").value.trim();
    window.pywebview.api.verify_otp(email, otp).then(result => {
        if (result.status === "ok") {
            if (mode === 'signup') { alert("Account created! Login now"); window.pywebview.api.open_login(); } 
            else if (mode === 'forgot') { window.pywebview.api.open_reset(email, result.username); }
            else { alert("Login Successful!"); window.pywebview.api.open_welcome(result.username); }
        } else {
            alert(result.message);
        }
    });
}

function startBlockTimer(seconds) {
    document.body.classList.add("blocked-mode");
    let timeLeft = seconds;
    const btn = document.getElementById("login-btn") || document.querySelector("button");
    const card = document.querySelector(".card");
    
    // Create or find the timer container
    let timerContainer = document.getElementById("block-timer-container");
    if (!timerContainer) {
        timerContainer = document.createElement("div");
        timerContainer.id = "block-timer-container";
        // Apply styling for the red cornered block
        timerContainer.style.border = "2px solid #ef4444";
        timerContainer.style.borderRadius = "8px";
        timerContainer.style.padding = "10px";
        timerContainer.style.marginTop = "15px";
        timerContainer.style.backgroundColor = "#fff5f5";
        card.appendChild(timerContainer);
    }

    if (btn) { 
        btn.disabled = true; 
        btn.innerText = "LOCKED"; 
        btn.style.opacity = "0.5";
    }

    clearInterval(blockTimerInterval);
    blockTimerInterval = setInterval(() => {
        const mins = Math.floor(timeLeft / 60);
        const secs = timeLeft % 60;
        const timeStr = `${mins}:${secs < 10 ? '0' : ''}${secs}`;

        // Update the inner HTML with specific font sizes
        timerContainer.innerHTML = `
            <div style="color: #ef4444; font-weight: bold; font-size: 20px; margin-bottom: 5px;">ACCESS DENIED</div>
            <div style="color: #333; font-size: 18px; font-family: monospace;">${timeStr}</div>
        `;
        
        if (timeLeft <= 0) {
            clearInterval(blockTimerInterval);
            document.body.classList.remove("blocked-mode");
            if (btn) { 
                btn.disabled = false; 
                btn.innerText = "Login"; 
                btn.style.opacity = "1";
            }
            timerContainer.remove();
        }
        timeLeft--;
    }, 1000);
}

function startResendTimer() {
    let countdownSpan = document.getElementById("countdown");
    if (!countdownSpan) return;
    let timeLeft = 60;
    let btn = document.getElementById("resend-btn");
    let msg = document.getElementById("timer-msg");
    btn.disabled = true;
    btn.style.backgroundColor = "#ccc";
    msg.style.display = "block";
    countdownSpan.innerText = timeLeft;

    clearInterval(resendTimerInterval);
    resendTimerInterval = setInterval(() => {
        timeLeft--;
        countdownSpan.innerText = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(resendTimerInterval);
            btn.disabled = false;
            btn.style.backgroundColor = "#1877f2";
            btn.innerText = "Resend OTP";
            msg.style.display = "none";
        }
    }, 1000);
}

function resendOtp() {
    let params = new URLSearchParams(window.location.search);
    let email = params.get("email");
    let btn = document.getElementById("resend-btn");
    btn.innerText = "Sending...";
    btn.disabled = true;
    window.pywebview.api.resend_otp(email).then(result => {
        if (result.status === "ok") {
            alert("New OTP sent!");
            startResendTimer();
        } else {
            alert("Error: " + result.message);
            btn.disabled = false; 
            btn.innerText = "Resend OTP";
        }
    });
}

function forgotPass() {
    let email = document.getElementById("email").value.trim();
    window.pywebview.api.forgot(email).then(result => {
        if (result.status === "error") alert("Email not found.");
        else { alert("OTP sent!"); window.pywebview.api.open_otp_page(email, 'forgot'); }
    });
}
function logindirectly() {
    // 1. Get the current URL parameters
    const params = new URLSearchParams(window.location.search);
    
    // 2. Extract the 'user' value (which was passed to reset.html by Python)
    const nameToPass = params.get("user") || "User"; 

    // 3. Tell Python to switch the page
    window.pywebview.api.open_welcome(nameToPass);
}
function validateResetPassword(p) {
    validatePassword(p);
}

function submitNewPass() {
    const newPass = document.getElementById("new-password").value.trim();
    const confirmPass = document.getElementById("confirm-password").value.trim();

    if (!newPass || !confirmPass) {
        alert("Please fill all fields.");
        return;
    }

    if (newPass !== confirmPass) {
        alert("Passwords do not match.");
        return;
    }

    if (!allRequirementsMet) {
        alert("Password does not meet security requirements.");
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const email = params.get("email");

    if (!email) {
        alert("Unauthorized request.");
        window.pywebview.api.open_login();
        return;
    }

    window.pywebview.api.reset_password(email, newPass).then(result => {
        if (result.status === "error") {
            alert(result.message);
            return;
        }

        alert("Password updated successfully!");

        window.pywebview.api.login(email, newPass).then(loginRes => {
            if (loginRes.status === "success") {
                window.pywebview.api.open_welcome(loginRes.username);
            } else {
                window.pywebview.api.open_login();
            }
        });
    });
}


function openService(url, title) { window.pywebview.api.open_service_window(url, title); }
function goSignup() { window.pywebview.api.open_signup(); }
function goLogin() { window.pywebview.api.open_login(); }
function goForgot() { window.pywebview.api.open_forgot(); }
