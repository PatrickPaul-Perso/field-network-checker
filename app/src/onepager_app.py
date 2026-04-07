from datetime import datetime
import json
import os
import subprocess
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template_string, request, send_file, url_for

app = Flask(__name__)

HTTP_PORT = int(os.environ.get("FNC_HTTP_PORT", "8080"))
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
    }

    * { box-sizing: border-box; }

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
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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

    .status-hero {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 14px;
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

    .hero-text {
      font-size: 1.5rem;
      font-weight: 700;
      line-height: 1.1;
    }

    .hero-text.ok { color: var(--ok); }
    .hero-text.bad { color: var(--bad); }

    .grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
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

    button, .button-link {
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
  </style>
</head>
<body>
  <div class="page">
    <div class="section">
      <h1>Field Network Checker</h1>
      <p class="subtitle">Local-first network port validation and metadata capture</p>
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

    <div class="section">
      <h2>Live Ethernet status</h2>
      <div class="status-hero">
        <div id="status-dot" class="dot"></div>
        <div id="status-text" class="hero-text bad">Link down</div>
      </div>
      <div class="grid two">
        <div class="item">
          <div class="label">Interface</div>
          <div id="ifname" class="value">-</div>
        </div>
        <div class="item">
          <div class="label">IPv4 address</div>
          <div id="ip" class="value">-</div>
        </div>
        <div class="item">
          <div class="label">Target prefix</div>
          <div id="prefix" class="value">{{ target_prefix }}</div>
        </div>
        <div class="item">
          <div class="label">Target match</div>
          <div id="target-match" class="value">-</div>
        </div>
        <div class="item">
          <div class="label">Last update</div>
          <div id="status-time" class="value">-</div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>Metadata</h2>
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

  <script>
    function updateBrowserTime() {
      const now = new Date();
      document.getElementById("browser-time").textContent = now.toLocaleString();
    }

    async function refreshStatus() {
      try {
        const response = await fetch("/api/status", { cache: "no-store" });
        const data = await response.json();

        const linkUp = data.eth_link === true;

        const dot = document.getElementById("status-dot");
        const text = document.getElementById("status-text");

        dot.className = linkUp ? "dot ok" : "dot";
        text.className = linkUp ? "hero-text ok" : "hero-text bad";
        text.textContent = linkUp ? "Link up" : "Link down";

        document.getElementById("ifname").textContent = data.eth_ifname || "-";
        document.getElementById("ip").textContent = data.ip || "-";
        document.getElementById("target-match").textContent = data.dhcp_ok ? "Yes" : "No";
        document.getElementById("status-time").textContent = data.timestamp || "-";
        document.getElementById("pi-time").textContent = data.pi_time || "-";
      } catch (error) {
        console.error(error);
      }
    }

    async function syncTime() {
      const message = document.getElementById("time-message");
      message.style.display = "none";

      try {
        const browserIso = new Date().toISOString();

        const response = await fetch("/api/time-sync", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ browser_time: browserIso })
        });

        const data = await response.json();

        message.textContent = data.message;
        message.style.display = "block";

        await refreshStatus();
      } catch (error) {
        message.textContent = "Time sync failed.";
        message.style.display = "block";
      }
    }

    updateBrowserTime();
    refreshStatus();
    setInterval(updateBrowserTime, 1000);
    setInterval(refreshStatus, 1000);
  </script>
</body>
</html>
"""

def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> dict:
    ensure_dirs()
    if not CONFIG_PATH.exists():
        default = {
            "site": "",
            "room": "",
            "tc_room": "",
        }
        CONFIG_PATH.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
        return default
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

def link_up(ifname: str) -> bool:
    carrier = Path(f"/sys/class/net/{ifname}/carrier")
    if not carrier.exists():
        return False
    return carrier.read_text(encoding="utf-8").strip() == "1"

def get_ipv4(ifname: str) -> str:
    try:
        output = subprocess.check_output(
            ["ip", "-4", "-o", "addr", "show", "dev", ifname],
            text=True
        )
    except subprocess.CalledProcessError:
        return ""

    for line in output.splitlines():
        parts = line.split()
        if "inet" in parts:
            idx = parts.index("inet")
            return parts[idx + 1].split("/")[0]

    return ""

def next_test_id() -> str:
    if not RECORDS_PATH.exists():
        return "T0001"

    count = 0
    with RECORDS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1

    return f"T{count + 1:04d}"

def append_record(record: dict) -> None:
    ensure_dirs()
    with RECORDS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

@app.get("/")
def index():
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
    ip = get_ipv4(ETH_IFNAME)
    return jsonify({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pi_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "eth_ifname": ETH_IFNAME,
        "eth_link": link_up(ETH_IFNAME),
        "ip": ip,
        "dhcp_ok": ip.startswith(TARGET_PREFIX) if ip else False,
    })

@app.post("/api/time-sync")
def time_sync():
    payload = request.get_json(silent=True) or {}
    browser_time = payload.get("browser_time", "").strip()

    if not browser_time:
        return jsonify({"ok": False, "message": "No browser time received."}), 400

    try:
        parsed = datetime.fromisoformat(browser_time.replace("Z", "+00:00"))
        local_value = parsed.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["date", "-s", local_value], check=True, capture_output=True, text=True)
        return jsonify({"ok": True, "message": f"Pi time updated to {local_value}."})
    except Exception:
        return jsonify({"ok": False, "message": "Unable to update Pi time from this container."}), 500

@app.post("/save")
def save_record():
    config = load_config()
    ip = get_ipv4(ETH_IFNAME)

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "test_id": next_test_id(),
        "site": request.form.get("site", "").strip() or config.get("site", ""),
        "room": request.form.get("room", "").strip() or config.get("room", ""),
        "tc_room": request.form.get("tc_room", "").strip() or config.get("tc_room", ""),
        "port_number": request.form.get("port_number", "").strip(),
        "eth_ifname": ETH_IFNAME,
        "eth_link": link_up(ETH_IFNAME),
        "ip": ip,
        "dhcp_ok": ip.startswith(TARGET_PREFIX) if ip else False,
    }

    append_record(record)
    return redirect(url_for("index", message=f"Saved {record['test_id']}"))

@app.get("/download/jsonl")
def download_jsonl():
    ensure_dirs()
    if not RECORDS_PATH.exists():
        RECORDS_PATH.write_text("", encoding="utf-8")
    return send_file(RECORDS_PATH, as_attachment=True, download_name="records.jsonl")

@app.get("/health")
def health():
    return "ok\\n", 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    ensure_dirs()
    app.run(host="0.0.0.0", port=HTTP_PORT)
