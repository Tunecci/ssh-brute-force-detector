
# SSH Brute Force Detection with Python

## Project Overview

A Python-based security monitoring tool that analyses Linux SSH authentication logs, identifies repeated failed login attempts, counts attempts by source IP address, and flags possible brute-force activity using a configurable detection threshold.

## Project Objectives

- Analyse SSH authentication logs.
- Identify failed SSH login attempts.
- Extract and validate source IP addresses.
- Count failed attempts per IP address.
- Generate alerts when an IP reaches the configured threshold.
- Handle invalid IP addresses and invalid threshold values.

## Tools and Technologies

- Kali Linux
- Python 3.13
- OpenSSH
- systemd-journald
- Python libraries: re, sys, ipaddress, datetime, collections

## Project Structure

```text
ssh-brute-force-detector/
├── README.md
├── reports/
│   └── detection-summary.md
├── sample-logs/
├── screenshots/
└── scripts/
    └── detect_ssh_bruteforce.py
```

## How It Works

1. Reads an SSH authentication log file.
2. Searches for explicit Failed password entries.
3. Extracts and validates source IP addresses.
4. Counts failed attempts per IP.
5. Generates an alert when the configured threshold is reached.

The default detection threshold is three failed attempts per IP.

## How to Run

Default sample log:

```bash
python3 scripts/detect_ssh_bruteforce.py
```

Simulated brute-force test:

```bash
python3 scripts/detect_ssh_bruteforce.py sample-logs/test-auth.log
```

Custom threshold:

```bash
python3 scripts/detect_ssh_bruteforce.py sample-logs/test-auth.log 5
```

## Collecting SSH Logs

```bash
sudo journalctl -u ssh --since "today" --no-pager -o cat | grep -E "Failed password|Invalid user|authentication failure" > sample-logs/auth.log
```

The detector counts explicit Failed password entries only.

## Testing

Tests cover:

- Repeated failed login attempts.
- Multiple source IP addresses.
- Invalid IP address handling.
- Configurable detection thresholds.
- Invalid threshold input.
- Actual local SSH authentication logs.

## Results

The actual local SSH log sample contained two failed password attempts from 127.0.0.1, below the default threshold of three.

A controlled test containing three failed attempts from 192.168.1.50 successfully triggered an alert.

See reports/detection-summary.md for detailed findings.

## Limitations

This is a basic log-analysis tool. It does not provide continuous monitoring, automated IP blocking, IP reputation checks, or time-based correlation.

## Disclaimer

This project was developed for educational purposes using a controlled lab environment and sample authentication logs.

## Author

GitHub: https://github.com/Tunecci
