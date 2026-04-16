"""Targeted unit tests for the Flask app entry points and helpers."""

# pylint: disable=redefined-outer-name,unused-argument

import json
import subprocess
import sys
from unittest.mock import patch

import pytest
import app as app_module
from app import (
    CONFIG_PATH,
    CONFIG_DIR as APP_CONFIG_DIR,
    DATA_DIR as APP_DATA_DIR,
    RECORDS_PATH,
    app,
    append_record,
    ensure_dirs,
    get_ipv4,
    link_up,
    live_status_snapshot,
    load_config,
    next_test_id,
    read_ipv4,
)

DATA_DIR = APP_DATA_DIR
CONFIG_DIR = APP_CONFIG_DIR


@pytest.fixture
def client():
    """Provide a Flask test client for route-level checks."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_dirs(tmp_path, monkeypatch):
    """Redirect data and config paths into a temporary test workspace."""
    data_dir = tmp_path / "data"
    config_dir = tmp_path / "config"
    monkeypatch.setattr(app_module, "DATA_DIR", data_dir)
    monkeypatch.setattr(app_module, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(app_module, "RECORDS_PATH", data_dir / "records.jsonl")
    monkeypatch.setattr(app_module, "CONFIG_PATH", config_dir / "config.json")
    module = sys.modules[__name__]
    monkeypatch.setattr(module, "DATA_DIR", data_dir)
    monkeypatch.setattr(module, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(module, "RECORDS_PATH", data_dir / "records.jsonl")
    monkeypatch.setattr(module, "CONFIG_PATH", config_dir / "config.json")


def test_load_config_defaults(temp_dirs):
    """load_config should create and return empty defaults on first run."""
    ensure_dirs()
    config = load_config()
    assert config == {"site": "", "room": "", "tc_room": ""}


def test_load_config_existing(temp_dirs):
    """load_config should preserve saved site and room values."""
    ensure_dirs()
    CONFIG_PATH.write_text('{"site": "TestSite", "room": "TestRoom"}', encoding="utf-8")
    config = load_config()
    assert config["site"] == "TestSite"
    assert config["room"] == "TestRoom"


def test_link_up_true(temp_dirs):
    """link_up should return True when carrier reports an active link."""
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.read_text", return_value="1\n"):
        assert link_up("eth0") is True


def test_link_up_false(temp_dirs):
    """link_up should return False when carrier reports no active link."""
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.read_text", return_value="0\n"):
        assert link_up("eth0") is False


def test_get_ipv4_success(temp_dirs):
    """get_ipv4 should return the parsed IPv4 address when the ip command succeeds."""
    output = "2: eth0    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0\\n"
    with patch("subprocess.check_output", return_value=output):
        assert get_ipv4("eth0") == "192.168.1.100"


def test_get_ipv4_no_ip(temp_dirs):
    """get_ipv4 should return an empty string when the ip command fails normally."""
    with patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "ip")):
        assert get_ipv4("eth0") == ""


def test_get_ipv4_command_failure_returns_empty_string(temp_dirs):
    """get_ipv4 should fail safe when the ip command is unavailable."""
    with patch("subprocess.check_output", side_effect=FileNotFoundError):
        assert get_ipv4("eth0") == ""


def test_read_ipv4_success(temp_dirs):
    """read_ipv4 should parse the raw IPv4 value from ip command output."""
    output = "2: eth0    inet 10.0.0.25/24 brd 10.0.0.255 scope global dynamic eth0\n"
    with patch("subprocess.check_output", return_value=output):
        assert read_ipv4("eth0") == "10.0.0.25"


def test_live_status_snapshot_handles_link_read_failure(temp_dirs):
    """The live snapshot should expose a status error when link reads fail."""
    with (
        patch("app.read_link_up", side_effect=OSError),
        patch("app.read_ipv4") as read_ipv4_mock,
    ):
        status = live_status_snapshot()

    assert status["eth_link"] is False
    assert status["ip"] == ""
    assert status["is_legacy"] is False
    assert status["status_error"] == "Unable to read live Ethernet status."
    read_ipv4_mock.assert_not_called()


def test_live_status_snapshot_handles_ip_read_failure(temp_dirs):
    """The live snapshot should expose a status error when IP reads fail."""
    with (
        patch("app.read_link_up", return_value=True),
        patch("app.read_ipv4", side_effect=FileNotFoundError),
    ):
        status = live_status_snapshot()

    assert status["eth_link"] is True
    assert status["ip"] == ""
    assert status["is_legacy"] is False
    assert status["status_error"] == "Unable to read live IP address."


def test_next_test_id_empty(temp_dirs):
    """next_test_id should start at T0001 when no records exist yet."""
    ensure_dirs()
    assert next_test_id() == "T0001"


def test_next_test_id_existing(temp_dirs):
    """next_test_id should increment past the last saved record identifier."""
    ensure_dirs()
    RECORDS_PATH.write_text('{"test_id": "T0001"}\n{"test_id": "T0002"}\n', encoding="utf-8")
    assert next_test_id() == "T0003"


def test_append_record(temp_dirs):
    """append_record should write one JSON object line to the records file."""
    ensure_dirs()
    record = {"test_id": "T0001", "ip": "192.168.1.100"}
    append_record(record)
    content = RECORDS_PATH.read_text(encoding="utf-8")
    assert json.loads(content.strip()) == record


def test_api_status_link_up(client, temp_dirs):
    """The status API should report link-up details with no status error."""
    with patch("app.read_link_up", return_value=True), \
         patch("app.read_ipv4", return_value="192.168.1.100"):
        response = client.get("/api/status")
        data = response.get_json()
        assert data["eth_link"] is True
        assert data["ip"] == "192.168.1.100"
        assert data["is_legacy"] is False
        assert data["status_error"] == ""


def test_api_status_no_link(client, temp_dirs):
    """The status API should report link down without attempting an IP lookup."""
    with patch("app.read_link_up", return_value=False), \
         patch("app.read_ipv4") as read_ipv4_mock:
        response = client.get("/api/status")
        data = response.get_json()
        assert data["eth_link"] is False
        assert data["ip"] == ""
        assert data["status_error"] == ""
        read_ipv4_mock.assert_not_called()


def test_index_uses_backend_status_fields(client, temp_dirs):
    """The page script should read status flags from the backend payload."""
    response = client.get("/")
    page = response.get_data(as_text=True)
    assert "const ipMatch = data.is_legacy === true;" in page
    assert 'const statusError = data.status_error || "";' in page
    assert "Status unavailable" in page
    assert "ip.startsWith(\"132.246.\")" not in page


def test_save_record(client, temp_dirs):
    """Saving a record should persist submitted metadata and live legacy status."""
    ensure_dirs()
    with patch("app.read_link_up", return_value=True), \
         patch("app.read_ipv4", return_value="132.246.1.100"):
        response = client.post("/save", data={
            "site": "TestSite",
            "room": "TestRoom",
            "port_number": "A1"
        }, follow_redirects=True)
        assert b"Saved T0001" in response.data
        content = RECORDS_PATH.read_text(encoding="utf-8")
        record = json.loads(content.strip())
        assert record["site"] == "TestSite"
        assert record["is_legacy"] is True


def test_save_record_uses_single_live_status_snapshot(client, temp_dirs):
    """Saving should capture one consistent live status snapshot for the record."""
    ensure_dirs()
    with (
        patch("app.read_link_up", side_effect=[True, False]) as link_up_mock,
        patch("app.read_ipv4", return_value="132.246.1.100") as get_ipv4_mock,
    ):
        response = client.post("/save", data={
            "site": "TestSite",
            "room": "TestRoom",
            "port_number": "A1"
        })

    assert response.status_code == 302
    assert link_up_mock.call_count == 1
    assert get_ipv4_mock.call_count == 1

    content = RECORDS_PATH.read_text(encoding="utf-8")
    record = json.loads(content.strip())
    assert record["eth_link"] is True
    assert record["ip"] == "132.246.1.100"
