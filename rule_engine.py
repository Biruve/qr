import re
from urllib.parse import urlparse, parse_qs

def identify_bank(upi_id):
    if not upi_id:
        return "Unknown Bank"

    domain = upi_id.split("@")[-1]

    bank_map = {
        "okaxis": "Axis Bank",
        "okhdfc": "HDFC Bank",
        "oksbi": "State Bank of India",
        "okicici": "ICICI Bank",
        "ybl": "Yes Bank",
        "ibl": "IDBI Bank",
        "paytm": "Paytm Payments Bank",
        "upi": "BHIM / NPCI"
    }

    for key in bank_map:
        if key in domain:
            return bank_map[key]

    return "Other Bank"

def analyze_qr_data(data):
    data_lower = data.lower()

    # ===============================
    # ✅ UPI PAYMENT QR ANALYSIS
    # ===============================
    if data_lower.startswith("upi://"):
        parsed = urlparse(data)
        params = parse_qs(parsed.query)

        upi_id = params.get("pa", ["Unknown"])[0]
        name = params.get("pn", ["Not Provided"])[0]

        bank = identify_bank(upi_id)

        return {
            "qr_type": "PAYMENT_QR",
            "status": "SAFE",
            "identity": {
                "Name": name,
                "UPI ID": upi_id
            },
            "reasons": [
                "Valid UPI payment QR detected",
                "No redirection to external websites"
            ],
            "advisory": "Verify recipient name before making payment."
        }

    # ===============================
    # ❌ NON-UPI / URL QR ANALYSIS
    # ===============================
    reasons = []
    risk_score = 0

    if not data_lower.startswith("http"):
        return {
            "qr_type": "UNKNOWN",
            "status": "SUSPICIOUS",
            "identity": None,
            "reasons": ["QR does not contain UPI or valid website URL"],
            "advisory": "Avoid scanning unknown QR codes."
        }

    # Rule 1: URL Shorteners
    if any(s in data_lower for s in ["bit.ly", "tinyurl", "goo.gl", "t.co"]):
        risk_score += 3
        reasons.append("Shortened URL detected")

    # Rule 2: IP-based URL
    if re.search(r"http[s]?://\d+\.\d+\.\d+\.\d+", data_lower):
        risk_score += 3
        reasons.append("IP-based URL detected")

    # Rule 3: No HTTPS
    if not data_lower.startswith("https"):
        risk_score += 2
        reasons.append("Website is not using HTTPS")

    # Rule 4: Phishing keywords
    if any(k in data_lower for k in ["login", "verify", "reward", "free", "update", "bank", "secure"]):
        risk_score += 3
        reasons.append("Phishing-related keywords found")

    # Rule 5: Long URL
    if len(data) > 75:
        risk_score += 1
        reasons.append("Unusually long URL")

    # Decision
    if risk_score >= 6:
        status = "SCAM"
        advisory = "DO NOT open this QR. High risk of phishing or fraud."
    elif risk_score >= 3:
        status = "SUSPICIOUS"
        advisory = "Avoid scanning unless the source is trusted."
    else:
        status = "SAFE"
        advisory = "No major threats detected, but stay cautious."

    return {
        "qr_type": "URL_QR",
        "status": status,
        "identity": None,
        "reasons": reasons,
        "advisory": advisory
    }
