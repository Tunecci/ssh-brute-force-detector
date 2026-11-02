# SSH Brute Force Detection Report

## 1. Project Objective

The objective of this project was to develop a Python script that analyses Linux SSH authentication logs, identifies repeated failed login attempts, groups attempts by source IP address, and flags possible brute-force activity when a configurable threshold is reached.

## 2. Lab Environment

- Operating System: Kali Linux
- Programming Language: Python 3.13.12
- Log Source: systemd journal (systemd-journald)
- Service: OpenSSH
- Detection Tool: Custom Python script

## 3. Detection Method

The script reads SSH authentication log entries and searches for lines containing the phrase `Failed password`.

It extracts the source IP address, validates it using Python's `ipaddress` module, and counts failed login attempts for each valid IP address.

The default alert threshold is three failed attempts. The threshold can also be supplied as a command-line argument.

## 4. Testing and Results

The script was tested using actual local SSH authentication logs and controlled sample log files.

| Test | Result |
|---|---|
| Actual SSH log analysis | Detected 2 failed attempts from 127.0.0.1; below threshold |
| Simulated brute-force test | Detected 3 attempts from 192.168.1.50; alert triggered |
| Multiple IP test | Detected 4 attempts across 2 IP addresses; 1 alert triggered |
| Invalid IP test | Rejected 999.999.999.999 and counted the valid IP |
| Custom threshold test | With threshold set to 5, 3 attempts did not trigger an alert |

## 5. Findings

The actual SSH log sample contained two explicit failed password attempts originating from the local loopback address, 127.0.0.1.

These attempts were below the configured threshold of three, so no alert was generated.

The controlled test files confirmed that the script could identify repeated failed attempts, distinguish activity from multiple IP addresses, reject invalid IP addresses, and apply different detection thresholds.

No external intrusion was established from the limited actual log sample examined.

## 6. Limitations

- The script detects explicit `Failed password` entries only.
- It analyses saved log files rather than continuously monitoring live SSH activity.
- It does not automatically block suspicious IP addresses.
- It does not perform IP reputation checks or geographic enrichment.
- Its threshold-based detection does not consider the time interval between attempts.

## 7. Recommendations

- Integrate the detection logic with a SIEM platform for centralised monitoring.
- Introduce time-based correlation to identify rapid login attempts.
- Consider IP reputation enrichment for additional investigation context.
- Use security controls such as Fail2ban where appropriate.
- Review SSH authentication logs regularly and investigate repeated failures.

## 8. Conclusion

This project demonstrates a basic security monitoring and detection workflow using Python. It shows how authentication logs can be analysed to identify repeated failed SSH login attempts and generate alerts based on configurable thresholds.
