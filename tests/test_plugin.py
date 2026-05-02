"""Tests for the solar_activity plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.solar_activity import SolarActivityPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "solar_activity",
    "name": "Solar Activity",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to fetch solar activity data.",
                "default": 3600,
                "minimum": 1800
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
[
    {
        "region": 3615,
        "latestXrayClass": "M1.2",
        "numspots": 8
    },
    {
        "region": 3614,
        "latestXrayClass": "C3.0",
        "numspots": 5
    },
    {
        "region": 3613,
        "latestXrayClass": "B7.0",
        "numspots": 3
    }
]
""")


@pytest.fixture
def plugin():
    return SolarActivityPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = SolarActivityPlugin(MANIFEST)
    p.config = json.loads("""
{}
""")
    return p


class TestSolarActivityPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "solar_activity"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.solar_activity.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "sunspot_count" in result.data, "missing variable: sunspot_count"
        assert "flare_class" in result.data, "missing variable: flare_class"
        assert "activity_level" in result.data, "missing variable: activity_level"

    @patch("plugins.solar_activity.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.solar_activity.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

