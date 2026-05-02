"""Display current sunspot count and solar flare activity from NOAA SWPC."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://services.swpc.noaa.gov/json/solar_regions.json"
USER_AGENT = "FiestaBoard Solar Activity Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--solar-activity)"


class SolarActivityPlugin(PluginBase):
    """Solar Activity plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "solar_activity"

    def fetch_data(self) -> PluginResult:
        try:
            response = requests.get(
                API_URL,
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            response.raise_for_status()
            records = response.json()

            sunspot_count = len(records) if isinstance(records, list) else 0

            # Determine highest flare class from region data
            flare_class = "None"
            flare_order = {"X": 5, "M": 4, "C": 3, "B": 2, "A": 1, "None": 0}
            highest = 0
            for region in (records if isinstance(records, list) else []):
                flare = region.get("latestXrayClass", "None") or "None"
                letter = flare[0].upper() if flare and flare[0].upper() in flare_order else "None"
                rank = flare_order.get(letter, 0)
                if rank > highest:
                    highest = rank
                    flare_class = flare

            activity_map = {5: "Extreme", 4: "Strong", 3: "Moderate", 2: "Low", 1: "Very Low", 0: "None"}
            activity_level = activity_map.get(highest, "None")

            return PluginResult(
                available=True,
                data={
                    "sunspot_count": sunspot_count,
                    "flare_class": flare_class,
                    "activity_level": activity_level,
                },
            )
        except Exception as e:
            logger.exception("Error fetching solar activity")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
