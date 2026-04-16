"""Field Network Checker Flask app and live Ethernet status helpers."""

from datetime import datetime
import json
import os
import subprocess
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template_string, request, send_file, url_for

app = Flask(__name__)

HTTP_PORT = int(os.environ.get("FNC_HTTP_PORT", "8080"))
BIND_HOST = os.environ.get("FNC_BIND_HOST", "192.168.50.1")
ETH_IFNAME = os.environ.get("FNC_ETH_IFNAME", "eth0")
TARGET_PREFIX = os.environ.get("FNC_TARGET_PREFIX", "132.246.")

DATA_DIR = Path(os.environ.get("FNC_DATA_DIR", "/data"))
CONFIG_DIR = Path(os.environ.get("FNC_CONFIG_DIR", "/config"))
RECORDS_PATH = DATA_DIR / "records.jsonl"
CONFIG_PATH = CONFIG_DIR / "config.json"

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Field Network Checker</title>
  <style>
    :root {
      --bg: #f3f4f6;
      --card: #ffffff;
      --text: #111827;
      --muted: #6b7280;
      --ok: #15803d;
      --bad: #b91c1c;
      --border: #d1d5db;
      --accent: #1d4ed8;
      --tab-bg: #e5e7eb;
      --tab-active: #ffffff;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .page {
      max-width: 760px;
      margin: 0 auto;
      padding: 16px;
    }

    .section {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 18px;
      margin-bottom: 16px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    h1 {
      margin: 0 0 8px 0;
      font-size: 1.7rem;
      line-height: 1.2;
    }

    h2 {
      margin: 0 0 14px 0;
      font-size: 1.2rem;
      line-height: 1.2;
    }

    .subtitle {
      margin: 0;
      color: var(--muted);
      font-size: 0.98rem;
    }

    .tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      background: var(--tab-bg);
      padding: 6px;
      border-radius: 14px;
    }

    .tab-button {
      flex: 1;
      border: 0;
      border-radius: 10px;
      padding: 12px 14px;
      background: transparent;
      color: var(--text);
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
    }

    .tab-button.active {
      background: var(--tab-active);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }

    .tab-panel {
      display: none;
    }

    .tab-panel.active {
      display: block;
    }

    .dot {
      width: 24px;
      height: 24px;
      border-radius: 999px;
      background: var(--bad);
      box-shadow: 0 0 0 8px rgba(185, 28, 28, 0.12);
      flex: 0 0 24px;
    }

    .dot.ok {
      background: var(--ok);
      box-shadow: 0 0 0 8px rgba(21, 128, 61, 0.12);
    }

    .dot.warn {
      background: #b45309;
      box-shadow: 0 0 0 8px rgba(180, 83, 9, 0.12);
    }

    .live-status-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 14px 16px;
      background: #ffffff;
      transition: background-color 0.2s ease, border-color 0.2s ease;
    }

    .live-status-card.prefix-match {
      background: #000000;
      border-color: #000000;
    }

    .live-status-card.prefix-match .live-status-text.ok,
    .live-status-card.prefix-match .live-status-text.bad,
    .live-status-card.prefix-match .live-status-pill {
      color: #ffffff;
    }

    .live-status-card.prefix-match .live-status-pill {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.22);
    }

    .live-status-left {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .live-status-center {
      flex: 1;
      min-width: 0;
    }

    .live-status-text {
      font-size: 1.35rem;
      font-weight: 700;
      line-height: 1.1;
      margin-bottom: 8px;
    }

    .live-status-text.ok {
      color: var(--ok);
    }

    .live-status-text.bad {
      color: var(--bad);
    }

    .live-status-text.warn {
      color: #b45309;
    }

    .live-status-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .live-status-pill {
      display: inline-block;
      padding: 8px 10px;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #f9fafb;
      font-size: 0.98rem;
      font-weight: 600;
      word-break: break-word;
    }

    .status-note {
      margin-top: 10px;
      padding: 10px 12px;
      border: 1px solid #f59e0b;
      border-radius: 10px;
      background: #fffbeb;
      color: #92400e;
      font-size: 0.92rem;
      font-weight: 600;
    }

    .live-status-right {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .match-box {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: transparent;
    }

    .match-box.match {
      background: #000000;
      border-color: #000000;
    }

    .grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
    }

    .grid.two {
      grid-template-columns: 1fr;
    }

    .item {
      border-top: 1px solid var(--border);
      padding-top: 12px;
    }

    .label {
      font-size: 0.92rem;
      color: var(--muted);
      margin-bottom: 4px;
    }

    .value {
      font-size: 1.06rem;
      font-weight: 600;
      word-break: break-word;
    }

    form {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
    }

    .field label {
      display: block;
      margin-bottom: 6px;
      font-size: 0.95rem;
      color: var(--muted);
      font-weight: 600;
    }

    .field input {
      width: 100%;
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 12px;
      font-size: 1rem;
      background: #fff;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 4px;
    }

    button,
    .button-link {
      appearance: none;
      border: 0;
      border-radius: 12px;
      padding: 12px 16px;
      font-size: 1rem;
      font-weight: 600;
      background: var(--accent);
      color: white;
      text-decoration: none;
      cursor: pointer;
    }

    .button-secondary {
      background: #374151;
    }

    .message {
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: 12px;
      background: #eff6ff;
      color: #1e3a8a;
      font-size: 0.95rem;
    }

    @media (min-width: 640px) {
      .grid.two {
        grid-template-columns: 1fr 1fr;
      }

      form.two-col {
        grid-template-columns: 1fr 1fr;
      }

      .field.full {
        grid-column: 1 / -1;
      }
    }

    @media (max-width: 520px) {
      .live-status-card {
        align-items: center;
        gap: 12px;
      }

      .live-status-text {
        font-size: 1.2rem;
      }

      .match-box {
        width: 28px;
        height: 28px;
      }
    }
  </style>
</head>
<body>
  <div class="page">
    <div class="section">
      <h1>Field Network Checker</h1>
      <p class="subtitle">Local-first network port validation and metadata capture</p>
    </div>

    <div class="tabs">
      <button class="tab-button active" type="button" data-tab="main">Main</button>
      <button class="tab-button" type="button" data-tab="config">Config</button>
    </div>

    <div id="tab-main" class="tab-panel active">
      <div class="section">
        <h2>Live Ethernet status</h2>

        <div id="live-status-card" class="live-status-card">
          <div class="live-status-left">
            <div id="status-dot" class="dot"></div>
          </div>

          <div class="live-status-center">
            <div id="status-text" class="live-status-text bad">Link down</div>
            <div class="live-status-meta">
              <span id="ifname" class="live-status-pill">eth0</span>
              <span id="ip" class="live-status-pill">-</span>
            </div>
            <div id="status-note" class="status-note" style="display:none;">Status temporarily unavailable.</div>
          </div>
        </div>
      </div>

      <div class="section">
        <h2>Current port metadata</h2>
        <form method="post" action="{{ url_for('save_record') }}" class="two-col">
          <div class="field">
            <label for="site">Site</label>
            <input id="site" name="site" type="text" value="{{ config.site }}">
          </div>

          <div class="field">
            <label for="room">Room</label>
            <input id="room" name="room" type="text" value="{{ config.room }}">
          </div>

          <div class="field">
            <label for="tc_room">TC_Room</label>
            <input id="tc_room" name="tc_room" type="text" value="{{ config.tc_room }}">
          </div>

          <div class="field">
            <label for="port_number">PortNumber</label>
            <input id="port_number" name="port_number" type="text" placeholder="Example: 12A">
          </div>

          <div class="field full">
            <div class="actions">
              <button type="submit">Save record</button>
              <a class="button-link button-secondary" href="{{ url_for('download_jsonl') }}">Download JSONL</a>
            </div>
          </div>
        </form>

        {% if message %}
        <div class="message">{{ message }}</div>
        {% endif %}
      </div>
    </div>

    <div id="tab-config" class="tab-panel">
      <div class="section">
        <h2>Defaults and configuration</h2>
        <form method="post" action="{{ url_for('save_config') }}" class="two-col">
          <div class="field">
            <label for="cfg_site">Default Site</label>
            <input id="cfg_site" name="site" type="text" value="{{ config.site }}">
          </div>

          <div class="field">
            <label for="cfg_room">Default Room</label>
            <input id="cfg_room" name="room" type="text" value="{{ config.room }}">
          </div>

          <div class="field">
            <label for="cfg_tc_room">Default TC_Room</label>
            <input id="cfg_tc_room" name="tc_room" type="text" value="{{ config.tc_room }}">
          </div>

          <div class="field full">
            <div class="actions">
              <button type="submit">Save defaults</button>
            </div>
          </div>
        </form>
      </div>

      <div class="section">
        <h2>Time</h2>
        <div class="grid two">
          <div class="item">
            <div class="label">Raspberry Pi date and time</div>
            <div id="pi-time" class="value">{{ now }}</div>
          </div>
          <div class="item">
            <div class="label">Browser date and time</div>
            <div id="browser-time" class="value">-</div>
          </div>
        </div>

        <div class="actions">
          <button type="button" onclick="syncTime()">Sync Pi time to phone time</button>
        </div>

        <div id="time-message" class="message" style="display:none;"></div>
      </div>
    </div>
  </div>

  <script>
    function updateBrowserTime() {
      const now = new Date();
      const browserTime = document.getElementById("browser-time");
      if (browserTime) {
        browserTime.textContent = now.toLocaleString();
      }
    }

    async function refreshStatus() {
      try {
        const statusUrl = new URL("/api/status", window.location.origin);
        const pageParams = new URLSearchParams(window.location.search);
        const demoStatus = pageParams.get("demo_status");

        if (demoStatus) {
          statusUrl.searchParams.set("demo_status", demoStatus);
        }

        const response = await fetch(statusUrl, { cache: "no-store" });
        const data = await response.json();

        const linkUp = data.eth_link === true;
        const ip = data.ip || "";
        const ipMatch = data.is_legacy === true;
        const statusError = data.status_error || "";
        const statusUnavailable = statusError !== "";

        const card = document.getElementById("live-status-card");
        const dot = document.getElementById("status-dot");
        const text = document.getElementById("status-text");
        const ifname = document.getElementById("ifname");
        const ipField = document.getElementById("ip");
        const statusNote = document.getElementById("status-note");

        if (card) {
          card.className = ipMatch ? "live-status-card prefix-match" : "live-status-card";
        }

        if (dot) {
          dot.className = statusUnavailable ? "dot warn" : (linkUp ? "dot ok" : "dot");
        }

        if (text) {
          if (statusUnavailable) {
            text.className = "live-status-text warn";
            text.textContent = "Status unavailable";
          } else {
            text.className = linkUp ? "live-status-text ok" : "live-status-text bad";
            text.textContent = linkUp ? "Link up" : "Link down";
          }
        }

        if (ifname) {
          ifname.textContent = data.eth_ifname || "-";
        }

        if (ipField) {
          ipField.textContent = ip || "-";
        }

        if (statusNote) {
          statusNote.textContent = statusError;
          statusNote.style.display = statusUnavailable ? "block" : "none";
        }

        const piTime = document.getElementById("pi-time");
        if (piTime) {
          piTime.textContent = data.pi_time || "-";
        }
      } catch (error) {
        console.error(error);
      }
    }

    async function syncTime() {
      const message = document.getElementById("time-message");
      if (message) {
        message.style.display = "none";
      }

      try {
        const browserIso = new Date().toISOString();

        const response = await fetch("/api/time-sync", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ browser_time: browserIso })
        });

        const data = await response.json();

        if (message) {
          message.textContent = data.message;
          message.style.display = "block";
        }

        await refreshStatus();
      } catch (error) {
        if (message) {
          message.textContent = "Time sync failed.";
          message.style.display = "block";
        }
      }
    }

    function activateTab(name) {
      const mainPanel = document.getElementById("tab-main");
      const configPanel = document.getElementById("tab-config");

      document.querySelectorAll(".tab-button").forEach((button) => {
        const active = button.dataset.tab === name;
        button.classList.toggle("active", active);
      });

      if (mainPanel) {
        mainPanel.classList.toggle("active", name === "main");
      }

      if (configPanel) {
        configPanel.classList.toggle("active", name === "config");
      }
    }

    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll(".tab-button").forEach((button) => {
        button.addEventListener("click", function () {
          activateTab(button.dataset.tab);
        });
      });

      updateBrowserTime();
      refreshStatus();
      setInterval(updateBrowserTime, 1000);
      setInterval(refreshStatus, 1000);
    });
  </script>
</body>
</html>
"""

def ensure_dirs() -> None:
    """Create the data and config directories when they are missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> dict:
    """Load saved defaults and recreate the config file if it is missing or invalid."""
    ensure_dirs()

    default = {
        "site": "",
        "room": "",
        "tc_room": "",
    }

    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
        return default

    try:
        current = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        CONFIG_PATH.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
        return default

    merged = {
        "site": current.get("site", ""),
        "room": current.get("room", ""),
        "tc_room": current.get("tc_room", ""),
    }

    if merged != current:
        CONFIG_PATH.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    return merged

def read_link_up(ifname: str) -> bool:
    """Read the raw carrier state for an interface from sysfs."""
    carrier = Path(f"/sys/class/net/{ifname}/carrier")
    if not carrier.exists():
        return False
    return carrier.read_text(encoding="utf-8").strip() == "1"


def link_up(ifname: str) -> bool:
    """Return a safe best-effort link state for an interface."""
    try:
        return read_link_up(ifname)
    except OSError:
        return False


def read_ipv4(ifname: str) -> str:
    """Read the raw IPv4 address currently assigned to an interface."""
    output = subprocess.check_output(
        ["ip", "-4", "-o", "addr", "show", "dev", ifname],
        text=True
    )

    for line in output.splitlines():
        parts = line.split()
        if "inet" in parts:
            idx = parts.index("inet")
            return parts[idx + 1].split("/")[0]

    return ""


def get_ipv4(ifname: str) -> str:
    """Return a safe best-effort IPv4 address for an interface."""
    try:
        return read_ipv4(ifname)
    except (subprocess.CalledProcessError, OSError):
        return ""


def demo_status_snapshot(mode: str) -> dict | None:
    """Return a demo status payload for UI screenshots when requested."""
    if mode != "unavailable":
        return None

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pi_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "eth_ifname": ETH_IFNAME,
        "eth_link": False,
        "ip": "",
        "is_legacy": False,
        "status_error": "Unable to read live Ethernet status.",
    }


def live_status_snapshot() -> dict:
    """Build the current live status payload used by the UI and save flow."""
    status_error = ""

    try:
        eth_link = read_link_up(ETH_IFNAME)
    except OSError:
        eth_link = False
        status_error = "Unable to read live Ethernet status."

    ip = ""
    if not status_error and eth_link:
        try:
            ip = read_ipv4(ETH_IFNAME)
        except (subprocess.CalledProcessError, OSError):
            status_error = "Unable to read live IP address."

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pi_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "eth_ifname": ETH_IFNAME,
        "eth_link": eth_link,
        "ip": ip,
        "is_legacy": ip.startswith(TARGET_PREFIX) if ip else False,
        "status_error": status_error,
    }

def next_test_id() -> str:
    """Return the next sequential test identifier for a new saved record."""
    if not RECORDS_PATH.exists():
        return "T0001"

    count = 0
    with RECORDS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1

    return f"T{count + 1:04d}"

def append_record(record: dict) -> None:
    """Append a single saved field record to the JSONL log."""
    ensure_dirs()
    with RECORDS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

@app.get("/")
def index():
    """Render the main application page with saved defaults and status UI."""
    config = load_config()
    return render_template_string(
        PAGE,
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        target_prefix=TARGET_PREFIX,
        config=config,
        message=request.args.get("message", "")
    )

@app.get("/api/status")
def api_status():
    """Return the current live Ethernet status payload as JSON."""
    demo_status = request.args.get("demo_status", "").strip().lower()
    demo_snapshot = demo_status_snapshot(demo_status)
    if demo_snapshot is not None:
        return jsonify(demo_snapshot)
    return jsonify(live_status_snapshot())

@app.post("/api/time-sync")
def time_sync():
    """Update the device clock from the browser-provided timestamp."""
    payload = request.get_json(silent=True) or {}
    browser_time = payload.get("browser_time", "").strip()

    if not browser_time:
        return jsonify({"ok": False, "message": "No browser time received."}), 400

    try:
        parsed = datetime.fromisoformat(browser_time.replace("Z", "+00:00"))
        local_value = parsed.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(
            ["sudo", "date", "-s", local_value],
            check=True,
            capture_output=True,
            text=True,
        )
        return jsonify({"ok": True, "message": f"Pi time updated to {local_value}."})
    except (ValueError, OSError, subprocess.SubprocessError):
        return jsonify(
            {"ok": False, "message": "Unable to update Pi time from this container."},
        ), 500

@app.post("/save")
def save_record():
    """Save the current form values together with one live status snapshot."""
    config = load_config()
    status = live_status_snapshot()

    submitted_site = request.form.get("site", "").strip()
    submitted_room = request.form.get("room", "").strip()
    submitted_tc_room = request.form.get("tc_room", "").strip()
    submitted_port_number = request.form.get("port_number", "").strip()

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "test_id": next_test_id(),
        "site": submitted_site or config.get("site", ""),
        "room": submitted_room or config.get("room", ""),
        "tc_room": submitted_tc_room or config.get("tc_room", ""),
        "port_number": submitted_port_number,
        "eth_ifname": status["eth_ifname"],
        "eth_link": status["eth_link"],
        "ip": status["ip"],
        "is_legacy": status["is_legacy"],
    }

    append_record(record)

    updated_config = {
        "site": config.get("site", ""),
        "room": config.get("room", ""),
        "tc_room": config.get("tc_room", ""),
    }

    if submitted_site:
        updated_config["site"] = submitted_site

    if submitted_room:
        updated_config["room"] = submitted_room

    if submitted_tc_room:
        updated_config["tc_room"] = submitted_tc_room

    CONFIG_PATH.write_text(json.dumps(updated_config, indent=2) + "\n", encoding="utf-8")

    return redirect(url_for("index", message=f"Saved {record['test_id']}"))

@app.get("/download/jsonl")
def download_jsonl():
    """Download the saved JSONL records file, creating it if needed."""
    ensure_dirs()
    if not RECORDS_PATH.exists():
        RECORDS_PATH.write_text("", encoding="utf-8")
    return send_file(RECORDS_PATH, as_attachment=True, download_name="records.jsonl")

@app.get("/health")
def health():
    """Return a simple health response for container and service checks."""
    return "ok\n", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.post("/config/save")
def save_config():
    """Save the operator's default site and room values."""
    ensure_dirs()

    config = {
        "site": request.form.get("site", "").strip(),
        "room": request.form.get("room", "").strip(),
        "tc_room": request.form.get("tc_room", "").strip(),
    }

    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return redirect(url_for("index", message="Defaults saved"))

if __name__ == "__main__":
    ensure_dirs()
    app.run(host=BIND_HOST, port=HTTP_PORT)
