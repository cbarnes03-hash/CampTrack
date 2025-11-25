import json


def load_notifications():
    try:
        with open("notifications.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_notifications(notifications):
    with open("notifications.json", "w") as f:
        json.dump(notifications, f, indent=4)


def add_notification(message):
    data = load_notifications()
    data.append(message)
    save_notifications(data)
