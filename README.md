# ISS Transit Platform

ISS Transit Platform is a Python Telegram bot that searches for satellite transits and close approaches near selected celestial bodies. It is designed to run from GitHub Actions, so it does not need a personal server.

The bot can send a daily report, respond to Telegram commands, and update selected settings in `config.json`.

The private source repository also contains a maintainer workflow that publishes a clean stable copy to a public repository.

## Features

- Searches for visible events for ISS, Tiangong, and Hubble.
- Checks the Sun, Moon, Jupiter, and Saturn.
- Reports transits and close approaches when available.
- Sends Telegram reports with event details, coordinates, Google Maps links, diagnostics, and PNG diagrams for grouped transits.
- Supports manual `/run` searches from Telegram.
- Supports read-only Telegram commands for status and configuration.
- Supports controlled Telegram updates to selected `config.json` fields.
- Restricts Telegram command execution to `TELEGRAM_CHAT_ID`.
- Supports Italian, English, and German via `config.json`.
- Runs with GitHub Actions schedules or manual workflow dispatch.

## Repository Structure

```text
iss-transit-platform/
├─ send_telegram.py
├─ process_telegram_commands.py
├─ setup_telegram_commands.py
├─ config.json
├─ requirements.txt
├─ core/
│  ├─ astronomy.py
│  ├─ config_editor.py
│  ├─ graphics.py
│  ├─ i18n.py
│  ├─ messages.py
│  ├─ settings.py
│  ├─ telegram_commands.py
│  └─ telegram_utils.py
├─ locales/
│  ├─ it.json
│  ├─ en.json
│  └─ de.json
├─ state/
│  └─ telegram_state.json
└─ .github/
   └─ workflows/
      ├─ daily.yml
      ├─ process-telegram-commands.yml
      └─ setup-telegram-commands.yml
```

The private source repository also contains `.github/workflows/publish-stable.yml`. That workflow is maintainer-only and is not published to the public stable repository.

## Important Files

- `send_telegram.py`: entry point for the daily/manual transit search.
- `process_telegram_commands.py`: processes pending Telegram updates once, then exits.
- `setup_telegram_commands.py`: registers the bot command menu with Telegram.
- `core/astronomy.py`: TLE loading, grid scanning, transit detection, and close-approach detection.
- `core/messages.py`: localized report and caption builders.
- `core/graphics.py`: PNG transit diagram generation.
- `core/telegram_commands.py`: command registry, routing, authorization, and command handlers.
- `core/config_editor.py`: safe updates to editable config fields.
- `core/i18n.py`: translation loading, language fallback, and shared localized labels.
- `locales/*.json`: Italian, English, and German translations.
- `state/telegram_state.json`: last processed Telegram update ID.
- `.github/workflows/daily.yml`: daily/manual transit search.
- `.github/workflows/process-telegram-commands.yml`: scheduled/manual Telegram command processing.
- `.github/workflows/setup-telegram-commands.yml`: manual Telegram command menu setup.

## Quick Start

1. Fork the public stable repository.
2. Decide whether the fork should be private. If `config.json` contains real coordinates and the fork is public, those coordinates are public.
3. Create a Telegram bot with BotFather.
4. Send one message to the new bot from the Telegram chat you want to authorize.
5. Find your chat ID with Telegram `getUpdates`.
6. Edit `config.json` with your location and preferences.
7. Add the required GitHub Secrets.
8. Enable GitHub Actions in the fork if GitHub asks you to do so.
9. Set workflow permissions to allow read and write access.
10. Run `Setup Telegram Commands` manually once.
11. Send `/help` to the bot on Telegram.
12. Run `Process Telegram Commands` manually once, or wait for the schedule.
13. After the bot responds, test `/config` and `/run`.

The detailed setup steps are below.

## Telegram Bot Setup

Open Telegram and search for:

```text
@BotFather
```

Create a new bot:

```text
/newbot
```

Save the generated token. It will be used as the `TELEGRAM_BOT_TOKEN` GitHub Secret.

Then send any message to your new bot from the chat you want to use.

To find your chat ID, open this URL in a browser, replacing `YOUR_TOKEN` with the bot token:

```text
https://api.telegram.org/botYOUR_TOKEN/getUpdates
```

Look for:

```json
"chat": {
  "id": 123456789
}
```

Use that number as `TELEGRAM_CHAT_ID`.

## Configuration

The main configuration lives in the tracked `config.json` file:

```json
{
  "users": [
    {
      "lat": 46.0,
      "lon": 9.0,
      "radius_km": 25,
      "search_hours": 72,
      "coarse_grid_step_km": 10,
      "fine_grid_radius_km": 10,
      "fine_grid_step_km": 2,
      "language": "it",
      "enabled_satellites": ["ISS", "Tiangong", "Hubble"]
    }
  ]
}
```

Supported `enabled_satellites` values:

- `ISS`
- `Tiangong`
- `Hubble`

Supported `language` values:

- `it`
- `en`
- `de`

If `language` is missing or invalid, the bot falls back to Italian.

Current command validation limits:

- `radius_km` must be positive and no more than `500`.
- `search_hours` must be positive and no more than `168`.

The public repository contains safe placeholder coordinates:

```json
"lat": 46.0,
"lon": 9.0
```

After forking, replace them with your own search center.

Important: if your fork is public, coordinates stored in `config.json` are public too. For privacy, make your fork private or use `USER_LAT` and `USER_LON` GitHub Secrets as optional coordinate overrides.

## GitHub Setup

In your fork, go to:

```text
Settings -> Secrets and variables -> Actions
```

Add these required repository secrets:

| Secret | Required | Description |
|---|---:|---|
| `TELEGRAM_BOT_TOKEN` | Yes | Telegram bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Yes | Authorized chat ID and default destination chat |

Optional coordinate overrides:

| Secret | Required | Description |
|---|---:|---|
| `USER_LAT` | No | Latitude override |
| `USER_LON` | No | Longitude override |

`TELEGRAM_CHAT_ID` is also the authorization source for Telegram commands. Commands from other chats are rejected and cannot run searches or modify `config.json`.

For Telegram commands that update `config.json` or `state/telegram_state.json`, GitHub Actions must be allowed to push commits back to the repository.

Check:

```text
Settings -> Actions -> General -> Workflow permissions
```

Select:

```text
Read and write permissions
```

Then save the setting.

If GitHub shows a banner asking you to enable workflows in the fork, enable them before running the bot.

### Maintainer-Only Stable Publishing

The private source repository also needs this secret if you maintain the public stable mirror:

| Secret | Required | Description |
|---|---:|---|
| `PUBLIC_REPO_TOKEN` | Only in private source repo | Personal access token used by `publish-stable.yml` to update the public stable repository |

Normal users do not need `PUBLIC_REPO_TOKEN`.

## Telegram Commands

The bot supports these commands:

```text
/start
/help
/status
/config
/run
/setlocation <lat> <lon>
/setradius <km>
/setsatellites <list>
/setsearchhours <hours>
/setlanguage <it|en|de>
```

What they do:

- `/start`: shows a short introduction.
- `/help`: shows the current command list from the command registry.
- `/status`: shows current bot status and main settings.
- `/config`: shows the current configuration.
- `/run`: starts a manual transit search in the same workflow process.
- `/setlocation <lat> <lon>`: updates `config.json` coordinates.
- `/setradius <km>`: updates the search radius.
- `/setsatellites <list>`: updates enabled satellites, for example `iss,tiangong,hubble`.
- `/setsearchhours <hours>`: updates the search window.
- `/setlanguage <it|en|de>`: updates the bot language.

Config-changing commands update `config.json`. The command-processing workflow commits and pushes the change back to the repository when the file changed.

If commands do not seem to run automatically, open:

```text
Actions -> Process Telegram Commands
```

Run it manually once and check the logs. Scheduled GitHub Actions can be delayed, especially in low-activity repositories or forks.

## Setup Telegram Command Menu

The Telegram command menu is generated from the real command registry.

After setting `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, run this workflow manually:

```text
Actions -> Setup Telegram Commands -> Run workflow
```

This runs:

```bash
python setup_telegram_commands.py
```

Run it again after publishing new commands or changing command descriptions.

## GitHub Actions Workflows

### Daily ISS Transit Platform

File:

```text
.github/workflows/daily.yml
```

Runs the main transit search:

```bash
python send_telegram.py
```

Triggers:

- manual `workflow_dispatch`
- daily schedule at `05:00 UTC`

### Process Telegram Commands

File:

```text
.github/workflows/process-telegram-commands.yml
```

Checks Telegram updates once, processes new commands, updates `state/telegram_state.json`, and commits config/state changes when needed.

Triggers:

- manual `workflow_dispatch`
- scheduled every 5 minutes

GitHub scheduled workflows can be delayed. A 5-minute cron is not guaranteed to run exactly every 5 minutes.

### Setup Telegram Commands

File:

```text
.github/workflows/setup-telegram-commands.yml
```

Registers the visible Telegram command menu with `setMyCommands`. It is manual only.

### Publish Stable

File:

```text
.github/workflows/publish-stable.yml
```

This workflow is intended for the private source repository only. It is not included in the public stable repository. It publishes a clean copy to:

```text
ericcatta/iss-transit-platform-stable
```

It publishes the files needed by third-party users, including:

- source code;
- translations;
- config placeholder;
- Telegram scripts;
- user-facing workflows;
- clean initial Telegram state.

It does not publish `publish-stable.yml` itself, and normal users do not need this workflow.

## Public Stable Repo vs Private Fork

Recommended maintainer/user setup:

- Public stable repository: contains clean code, safe placeholder `config.json`, translations, and user-facing workflows.
- Private fork: contains your personal coordinates, active Telegram secrets, workflow state, and real automation runs.

Users can fork the public stable repository, edit `config.json`, add Telegram secrets, enable workflow write permissions, and run the setup workflow.

If privacy matters, make your fork private before adding real coordinates to `config.json`.

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Set required environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

Optional coordinate overrides:

```bash
export USER_LAT="45.123"
export USER_LON="9.456"
```

Run the main search:

```bash
python send_telegram.py
```

Process Telegram commands once:

```bash
python process_telegram_commands.py
```

Register the Telegram command menu:

```bash
python setup_telegram_commands.py
```

These scripts can send real Telegram messages.

If your system does not provide a `python` command, use `python3` for the local commands above.

## Notes And Limits

- The project currently has no web app or `app/index.html` file.
- The bot depends on live external services: CelesTrak for TLE data and Telegram for delivery.
- GitHub Actions schedules can be delayed or skipped by GitHub under load.
- PNG diagrams are schematic Matplotlib diagrams.
- The command processor is not a persistent process, webhook, or server. It runs once per workflow execution.
- The project supports one configured user entry at the moment: `users[0]`.
- The private source repository contains a small test suite for message/report builders, but tests may be omitted from the public stable mirror.

## Short Roadmap

- Improve README examples as the public stable repository is finalized.
- Add more tests around config editing and command routing.
- Improve robustness around very rapid Telegram command sequences.

## License

Personal / amateur astronomy project.
