# CampTrack

CLI tool to manage camps for Admin, Scout Leader, and Logistics Coordinator roles.

## Setup

1) Create/activate a virtualenv (optional but recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

Start the app:
```bash
python app.py
```

## Data files

Runtime data is stored under `data/`:
- `camp_data.json` – camps, leaders, campers, activities, records
- `messages.json` – messaging threads
- `notifications.json` – system notifications
- `food_requirements.json` – per-camp food requirements

User/login data remains in `logins.txt` and `disabled_logins.txt` at the project root.
