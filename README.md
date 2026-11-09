# Server Telemetry Monitor

A lightweight system telemetry and diagnostics dashboard built with **FastAPI** and **psutil**. It provides real-time polling of host resource utilization (CPU, RAM, storage) and running process states across Windows and Linux server environments, exposing both a REST API endpoint and an operational web dashboard.

---

## Features

- **Core Resource Polling:** Tracks total, used, and percent metrics for CPU, RAM, and primary disk mounts.
- **Cross-Platform OS Detection:** Automatically detects underlying OS (`C:\` for Windows NT, `/` for POSIX/Linux) to report active partition capacity.
- **Top Process Diagnostics:** Automatically aggregates, sorts, and inspects the top 10 memory-consuming processes alongside real-time CPU utilization.
- **Dual-Mode Consumption:**
  - `GET /monitor/api/metrics`: Clean JSON payload designed for automated health checks, triage scripts, and monitoring aggregators.
  - `GET /monitor`: Built-in web dashboard styled for fast on-site visual triage.

---

## Tech Stack

- **Python 3.10+**
- **FastAPI:** High-performance asynchronous web framework
- **psutil:** Cross-platform process and system monitoring
- **Uvicorn:** Production-grade ASGI server

---

## Repository Structure

```text
server-telemetry-monitor/
├── app/
│   ├── __init__.py
│   └── ServerTelMonitor.py   # Core FastAPI application & telemetry routes
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
