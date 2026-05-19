# ISS Transit Platform

ISS Transit Platform is a Python bot that searches for visible satellite transits and close approaches near selected celestial bodies, then sends the results to Telegram.

The project is designed to run from GitHub Actions. It does not require a personal server.

## What It Checks

The current code checks these satellites:

- ISS
- Tiangong
- Hubble

The current code checks these celestial bodies:

- Sun
- Moon
- Jupiter
- Saturn

For the Sun, the bot reports transits. For the Moon, Jupiter, and Saturn, it reports both transits and close approaches when available.

## What It Sends

Each GitHub Actions run sends a Telegram message with:

- search results for transits;
- close approaches within the configured limit;
- event coordinates;
- Google Maps links;
- search diagnostics;
- a generated PNG image for each grouped transit found.

If no transit is found, the bot still sends a daily report.

## How It Works

On each run, the bot:

1. loads the user configuration from `config.json`;
2. reads Telegram credentials from GitHub Secrets;
3. optionally overrides coordinates with `USER_LAT` and `USER_LON` if those secrets are set;
4. downloads current satellite TLE data from CelesTrak using Skyfield;
5. computes satellite and celestial-body positions;
6. scans a geographic grid around the configured location;
7. refines promising areas with a smaller grid;
8. sends the report and transit images to Telegram.

## Project Structure

```text
iss-transit-platform/
├─ send_telegram.py
├─ config.json
├─ core/
│  ├─ __init__.py
│  ├─ astronomy.py
│  ├─ graphics.py
│  ├─ messages.py
│  ├─ settings.py
│  └─ telegram_utils.py
└─ .github/
   └─ workflows/
      └─ daily.yml
```

## Important Files

- `send_telegram.py`: main entry point run by GitHub Actions.
- `core/astronomy.py`: satellite loading, grid scanning, transit detection, and close-approach detection.
- `core/messages.py`: Telegram report formatting.
- `core/graphics.py`: PNG transit diagram generation.
- `core/settings.py`: configuration and environment variable loading.
- `core/telegram_utils.py`: Telegram API calls.
- `config.json`: search radius, time window, and grid settings.
- `.github/workflows/daily.yml`: scheduled and manual GitHub Actions workflow.

## Requirements

The workflow uses Python 3.11 and installs these third-party packages:

```text
requests
skyfield
matplotlib
```

Dependencies are listed in `requirements.txt` and installed by `.github/workflows/daily.yml`.

## Setup

### 1. Fork The Repository

Fork this repository into your own GitHub account.

### 2. Create A Telegram Bot

Open Telegram and search for:

```text
@BotFather
```

Create a new bot with:

```text
/newbot
```

Save the generated token. You will use it as:

```text
TELEGRAM_BOT_TOKEN
```

### 3. Find Your Telegram Chat ID

Send a message to your new bot, then open this URL in a browser:

```text
https://api.telegram.org/botYOUR_TOKEN/getUpdates
```

Look for a value like:

```json
"chat": {
  "id": 123456789
}
```

Use that number as:

```text
TELEGRAM_CHAT_ID
```

### 4. Configure Your Fork

After forking, edit `config.json` in your fork.

The public repository contains safe placeholder coordinates:

```json
"lat": 46.000000,
"lon": 9.000000
```

Replace them with the center of your own search area.

Important: if your fork is public, the coordinates in `config.json` are public too. For privacy, make your fork private or use the optional `USER_LAT` and `USER_LON` GitHub Secrets as coordinate overrides.

### 5. Add GitHub Secrets

In your forked repository, go to:

```text
Settings -> Secrets and variables -> Actions
```

Add these required repository secrets:

| Secret | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Telegram chat ID that receives the messages |

These optional repository secrets can override the coordinates from `config.json`:

| Secret | Description |
|---|---|
| `USER_LAT` | Optional latitude override |
| `USER_LON` | Optional longitude override |

## Configuration

The main configuration lives in the tracked `config.json` file:

```json
{
  "users": [
    {
      "lat": 46.000000,
      "lon": 9.000000,
      "radius_km": 40,
      "search_hours": 72,
      "coarse_grid_step_km": 10,
      "fine_grid_radius_km": 10,
      "fine_grid_step_km": 2,
      "enabled_satellites": ["ISS", "Tiangong", "Hubble"]
    }
  ]
}
```

The code currently reads these fields:

- `lat`
- `lon`
- `radius_km`
- `search_hours`
- `coarse_grid_step_km`
- `fine_grid_radius_km`
- `fine_grid_step_km`
- `enabled_satellites`

The `enabled_satellites` field controls which known satellites are checked. Supported values are currently `ISS`, `Tiangong`, and `Hubble`.

`USER_LAT` and `USER_LON` are optional overrides. If they are not set, the bot uses `lat` and `lon` from `config.json`.

## Running From GitHub Actions

The workflow is defined in:

```text
.github/workflows/daily.yml
```

It can be started manually from:

```text
Actions -> Daily ISS Transit Platform -> Run workflow
```

It is also scheduled with:

```yaml
cron: "0 5 * * *"
```

GitHub Actions cron schedules use UTC time.

## Running Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set the required environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

Then edit `config.json` with your coordinates and search settings. Alternatively, set `USER_LAT` and `USER_LON` to override the coordinates from `config.json`.

Run:

```bash
python send_telegram.py
```

The script sends real Telegram messages when it runs.

## Notes And Limitations

- The project currently has no web app or `app/index.html` file.
- The bot uses live external services: CelesTrak for TLE data and Telegram for message delivery.
- PNG diagrams are simple schematic transit diagrams generated with Matplotlib.
- There is no test suite or dependency lock file in the current repository.

## License

Personal / amateur astronomy project.
