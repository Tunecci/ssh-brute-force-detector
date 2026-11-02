import re
import sys
import ipaddress
from datetime import datetime
from collections import Counter

LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "sample-logs/auth.log"

try:
    THRESHOLD = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    if THRESHOLD < 1:
        raise ValueError

except ValueError:
    print("Error: Threshold must be a positive whole number.")
    sys.exit(1)

failed_attempts = Counter()

try:
    with open(LOG_FILE, "r") as file:
        for line in file:
            if "Failed password" in line:
                match = re.search(r"from (\S+)", line)

                if match:
                    ip_address = match.group(1)

                    try:
                        ipaddress.ip_address(ip_address)
                        failed_attempts[ip_address] += 1
                    except ValueError:
                        print(f"Invalid IP address skipped: {ip_address}")

    print("\nSSH BRUTE FORCE DETECTION REPORT")
    print("-" * 40)
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log File Analysed: {LOG_FILE}")
    print(f"Detection Threshold: {THRESHOLD}")
    print("-" * 40)

    total_attempts = sum(failed_attempts.values())
    unique_ips = len(failed_attempts)
    alert_count = sum(
        1 for count in failed_attempts.values()
        if count >= THRESHOLD
    )

    print(f"Total Failed Attempts: {total_attempts}")
    print(f"Unique Source IPs: {unique_ips}")
    print(f"IPs Triggering Alerts: {alert_count}")
    print("-" * 40)

    if not failed_attempts:
        print("No failed SSH login attempts detected.")

    for ip, count in failed_attempts.items():
        print(f"IP Address: {ip}")
        print(f"Failed Attempts: {count}")

        if count >= THRESHOLD:
            print("ALERT: Possible brute-force activity detected!")
        else:
            print("Status: Below alert threshold")

        print("-" * 40)

except FileNotFoundError:
    print(f"Error: Log file '{LOG_FILE}' not found.")
