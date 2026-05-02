# Solar Activity Setup Guide

Display current sunspot count and solar flare activity from NOAA SWPC.

## Overview

The Solar Activity plugin fetches the daily solar region summary from NOAA's Space Weather Prediction Center, including the active sunspot count and the highest X-ray flux class of the day. No API key required.

- API reference: https://www.swpc.noaa.gov/products/solar-region-summary

### Prerequisites

No API key or account required.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Solar Activity**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `solar_activity` plugin variables:
   ```
   {{{ solar_activity.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `solar_activity.sunspot_count` | Number of active sunspot regions | `7` |
| `solar_activity.flare_class` | Largest solar flare class today (A/B/C/M/X) | `M1.2` |
| `solar_activity.activity_level` | Human-readable activity level | `Moderate` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to fetch solar activity data. | `3600` |

## Troubleshooting

- **No data** — verify connectivity to `services.swpc.noaa.gov`.
- **Zero sunspots** — could mean solar minimum; data is accurate.

