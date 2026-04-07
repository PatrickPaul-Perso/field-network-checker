from datetime import datetime
import os
import re
import subprocess
from pathlib import Path

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

ETH_IFNAME = os.environ.get("FNC_ETH_IFNAME", "eth0")
HTTP_PORT = int(os.environ.get("FNC_HTTP_PORT", "8080"))

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
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .page {
      max-width: 680px;
      margin: 0 auto;
      padding: 16px;
    }

    .card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    h1 {
      margin: 0 0 6px 0;
      font-size: 1.6rem;
      line-height: 1.2;
    }

    .subtitle {
      margin: 0 0 18px 0;
      color: var(--muted);
      font-size: 1rem;
    }

    .hero {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 18px;
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
      font-size: 1.6rem;
      font-weight: 700;
      line-height: 1.15;
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
      padding-top: 14px;
    }

    .label {
      font-size: 0.92rem;
      color: var(--muted);
      margin-bottom: 4px;
    }

    .value {
      font-size: 1.08rem;
      font-weight: 600;
      word-break: break-word;
    }

    .footer {
      margin-top: 18px;
      color: var(--muted);
      font-size: 0.9rem;
      text-align: center;
    }

    @media (min-width: 520px) {
      .grid {
        grid-template-columns: 1fr 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="page">
    <div class="card">
      <h1>Field Network Checker</h1>
      <p class="subtitle">Live Ethernet link state</p>

      <div class="hero">
        <div id="status-dot" class="dot"></div>
        <div id="status-text" class="hero-text bad">Link down</div>
      </div>

      <div class="grid">
        <div class="item">
          <div class="label">Interface</div>
          <div id="ifname" class="value">-</div>
        </div>

        <div class="item">
          <div class="label">IPv4 address</div>
          <div id="ip" class="value">-</div>
        </div>

        <div class="item">
          <div class="label">Last update</div>
          <div id="timestamp" class="value">-</div>
        </div>
      </div>

      <div class="footer">Refresh every second</div>
    </div>
  </div>

  <script>
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
        document.getElementById("timestamp").textContent = data.timestamp || "-";
      } catch (error) {
        console.error(error);
      }
    }

    refreshStatus();
    setInterval(refreshStatus, 1000);
  </script>
</body>
</html>
"""

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

@app.get("/")
def index():
    return render_template_string(PAGE)

@app.get("/api/status")
def api_status():
    return jsonify({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "eth_ifname": ETH_IFNAME,
        "eth_link": link_up(ETH_IFNAME),
        "ip": get_ipv4(ETH_IFNAME),
    })

@app.get("/health")
def health():
    return "ok\n", 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HTTP_PORT)
