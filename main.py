from qr_scanner import scan_qr
from realtime_scanner import scan_qr_realtime
from rule_engine import analyze_qr_data

print("\n==============================")
print(" UNIVERSAL QR CODE SCANNER ")
print("==============================")
print("1. Scan from Image")
print("2. Scan using Camera")
print("==============================\n")

choice = input("Enter choice (1/2): ")

qr_data = None

if choice == "1":
    path = input("Enter image path: ")
    qr_data = scan_qr(path)

elif choice == "2":
    qr_data = scan_qr_realtime()

else:
    print("❌ Invalid option")
    exit()

if not qr_data:
    print("\n❌ No QR detected")
    exit()

print("\n📌 QR DATA FOUND:")
print(qr_data)

result = analyze_qr_data(qr_data)

print("\n🔍 ANALYSIS REPORT")
print("QR Type :", result["qr_type"])
print("Status  :", result["status"])

# Show identity info if available
if "identity" in result and result["identity"]:
    print("\n👤 RECIPIENT DETAILS")
    for k, v in result["identity"].items():
        print(f"{k} : {v}")

print("\n📌 SECURITY FINDINGS")
for r in result["reasons"]:
    print("-", r)

print("\n🚨 SECURITY ADVISORY")
print(result["advisory"])
