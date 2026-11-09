import os
import psutil
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Server Telemetry Monitor")
monitor_router = APIRouter(prefix="/monitor")


def get_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=None)

    mem = psutil.virtual_memory()
    ram_data = {
        "percent": mem.percent,
        "used_gb": round(mem.used / (1024**3), 2),
        "total_gb": round(mem.total / (1024**3), 2),
    }

    drive = "C:\\" if os.name == "nt" else "/"
    disk = psutil.disk_usage(drive)
    disk_data = {
        "mount": drive,
        "percent": disk.percent,
        "free_gb": round(disk.free / (1024**3), 2),
        "total_gb": round(disk.total / (1024**3), 2),
    }

    top_procs = []
    for proc in sorted(
        psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]),
        key=lambda p: p.info["memory_percent"] or 0,
        reverse=True,
    )[:10]:
        top_procs.append(
            {
                "pid": proc.info["pid"],
                "name": proc.info["name"],
                "mem_pct": round(proc.info["memory_percent"] or 0, 1),
                "cpu_pct": round(proc.info["cpu_percent"] or 0, 1),
            }
        )

    return {
        "cpu": cpu_percent,
        "ram": ram_data,
        "disk": disk_data,
        "top_processes": top_procs,
    }


@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/monitor")


@monitor_router.get("/api/metrics")
def metrics_api():
    return get_system_metrics()


@monitor_router.get("", response_class=HTMLResponse)
@monitor_router.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>DOSIS Systems - Site Server Telemetry</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Segoe UI", Arial, Helvetica, sans-serif; }
            body { background-color: #f7f9fa; color: #333; font-size: 13px; }

            /* Top Primary Navigation */
            .header-nav {
                background: linear-gradient(to bottom, #00567a 0%, #004563 100%);
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 6px 16px;
                border-bottom: 2px solid #003248;
            }
            .header-left { display: flex; align-items: center; gap: 24px; }
            .brand-logo { font-size: 24px; font-weight: 900; letter-spacing: -0.5px; color: #fff; }
            .brand-logo span { color: #5bc0de; }
            .brand-sub { font-size: 9px; color: #bce8f1; display: block; margin-top: -4px; }
            
            .stats-bar { display: flex; gap: 16px; font-size: 13px; font-weight: 600; }
            .stats-item span { color: #5bc0de; font-weight: 700; }

            .nav-menu { display: flex; gap: 14px; font-size: 13px; }
            .nav-item { cursor: pointer; color: #e0f2fe; text-decoration: none; }
            .nav-item:hover { color: #ffffff; text-decoration: underline; }

            .header-right { display: flex; align-items: center; gap: 12px; }
            .user-badge {
                background-color: #f4fbf4;
                color: #274d28;
                border: 1px solid #c2e2c4;
                border-radius: 4px;
                padding: 4px 10px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            .user-close {
                background-color: #d9534f;
                color: #fff;
                font-size: 10px;
                padding: 1px 4px;
                border-radius: 2px;
                cursor: pointer;
            }

            /* Subheader Green Banner */
            .sub-banner {
                background: linear-gradient(to bottom, #44ba8b 0%, #35a479 100%);
                color: white;
                text-align: center;
                padding: 8px 16px;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 0.3px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.15);
                position: relative;
            }
            .search-box {
                position: absolute;
                right: 16px;
                top: 8px;
                font-size: 12px;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            .search-box input {
                border-radius: 3px;
                border: 1px solid #287a5a;
                padding: 2px 6px;
                outline: none;
            }

            /* Secondary Tab Bar */
            .tab-bar {
                background-color: #ffffff;
                display: flex;
                gap: 4px;
                padding: 6px 12px 0 12px;
                border-bottom: 1px solid #d1d5db;
            }
            .tab-btn {
                padding: 6px 14px;
                font-size: 12px;
                color: #0284c7;
                background: transparent;
                border: 1px solid transparent;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                cursor: pointer;
            }
            .tab-btn.active {
                background: #f7f9fa;
                border-color: #d1d5db;
                color: #374151;
                font-weight: 600;
            }

            /* Main Content Container */
            .main-content { padding: 16px; }

            /* Telemetry Overview Cards */
            .vitals-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 16px;
                margin-bottom: 20px;
            }
            .vital-card {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 14px;
            }
            .vital-header {
                display: flex;
                justify-content: space-between;
                font-size: 12px;
                font-weight: bold;
                color: #006080;
                margin-bottom: 8px;
                text-transform: uppercase;
            }
            .vital-metric { font-size: 26px; font-weight: bold; color: #1f2937; margin-bottom: 6px; }
            .vital-subtext { font-size: 11px; color: #6b7280; margin-bottom: 8px; }
            .bar-shell { background-color: #e5e7eb; height: 10px; border-radius: 5px; overflow: hidden; }
            .bar-fill { height: 100%; width: 0%; transition: width 0.4s ease; }
            .fill-normal { background-color: #10b981; }
            .fill-warn { background-color: #f59e0b; }
            .fill-crit { background-color: #ef4444; }

            /* Data Table (Standard DOSIS Grid) */
            .table-container {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                overflow: hidden;
            }
            .dosis-table { width: 100%; border-collapse: collapse; text-align: left; }
            .dosis-table th {
                background-color: #008eb7;
                color: #ffffff;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 600;
                border-right: 1px solid #007799;
            }
            .dosis-table th:last-child { border-right: none; }
            .dosis-table td {
                padding: 6px 12px;
                border-bottom: 1px solid #e5e7eb;
                font-size: 12px;
                color: #374151;
            }
            .dosis-table tr:nth-child(even) { background-color: #f9fafb; }
            .dosis-table tr:hover { background-color: #f0fdf4; }

            .input-cell {
                background: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 3px;
                padding: 3px 8px;
                font-family: inherit;
                font-size: 12px;
                color: #334155;
                width: 100%;
                display: inline-block;
            }

            .badge {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: 600;
            }
            .badge-active { background-color: #e0f2fe; color: #0369a1; }
        </style>
    </head>
    <body>

        <!-- Primary Top Bar -->
        <header class="header-nav">
            <div class="header-left">
                <div>
                    <div class="brand-logo">D<span>O</span>SIS</div>
                    <span class="brand-sub">by MANCHAC SYSTEMS</span>
                </div>
                <div class="stats-bar">
                    <div class="stats-item">CPU: <span id="top-cpu">--%</span></div>
                    <div class="stats-item">RAM: <span id="top-ram">--%</span></div>
                    <div class="stats-item">Disk: <span id="top-disk">--%</span></div>
                </div>
                <nav class="nav-menu">
                    <a class="nav-item">Automation ▾</a>
                    <a class="nav-item">Diagnostics ▾</a>
                    <a class="nav-item">Reports ▾</a>
                    <a class="nav-item">Settings ▾</a>
                    <a class="nav-item">SUPPORT ▾</a>
                </nav>
            </div>
            <div class="header-right">
                <div class="user-badge">
                    <span>swsupport</span>
                    <span class="user-close">✖</span>
                </div>
            </div>
        </header>

        <!-- View Title Bar -->
        <div class="sub-banner">
            Site Server Telemetry & System Health
            <div class="search-box">
                <label>Filter:</label>
                <input type="text" placeholder="Search processes...">
            </div>
        </div>

        <!-- Sub Tabs -->
        <div class="tab-bar">
            <button class="