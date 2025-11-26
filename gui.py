import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

from user_logins import users, load_logins, check_disabled_logins
from features.admin import (
    add_user,
    edit_user_password,
    delete_user,
    disable_user,
    enable_user,
    list_users,
)
from camp_ops import create_camp, edit_camp, delete_camp
from features.logistics import (
    set_food_stock_data,
    top_up_food_data,
    set_pay_rate_data,
    compute_food_shortage,
    build_dashboard_data,
)
from features.notifications import load_notifications
from features.scout import (
    assign_camps_to_leader,
    bulk_assign_campers_from_csv,
    assign_food_amount_pure,
    record_activity_entry_data,
    engagement_scores_data,
    money_earned_per_camp_data,
    total_money_earned_value,
    activity_stats_data,
)
from messaging import get_conversations_for_user, get_conversation, send_message


class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(padx=10, pady=10)
        tk.Label(self, text="Username").grid(row=0, column=0, sticky="e")
        tk.Label(self, text="Password").grid(row=1, column=0, sticky="e")
        self.username = tk.Entry(self)
        self.password = tk.Entry(self, show="*")
        self.username.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        tk.Button(self, text="Login", command=self.attempt_login).grid(row=2, column=0, columnspan=2, pady=5)

    def attempt_login(self):
        uname = self.username.get().strip()
        pwd = self.password.get()
        load_logins()
        if check_disabled_logins(uname):
            messagebox.showerror("Login failed", "This account has been disabled.")
            return
        role = None
        if users["admin"]["username"] == uname and users["admin"]["password"] == pwd:
            role = "admin"
        else:
            for u in users["scout leader"]:
                if u["username"] == uname and u["password"] == pwd:
                    role = "scout leader"
                    break
            for u in users["logistics coordinator"]:
                if u["username"] == uname and u["password"] == pwd:
                    role = "logistics coordinator"
                    break
        if role:
            self.master.destroy()
            app = tk.Tk()
            app.title(f"CampTrack - {role}")
            if role == "admin":
                AdminWindow(app)
            elif role == "scout leader":
                ScoutWindow(app, uname)
            elif role == "logistics coordinator":
                LogisticsWindow(app)
            app.mainloop()
        else:
            messagebox.showerror("Login failed", "Invalid username or password.")


class AdminWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Button(self, text="List Users", command=self.list_users_ui).pack(fill="x")
        tk.Button(self, text="Add User", command=add_user).pack(fill="x")
        tk.Button(self, text="Edit User Password", command=edit_user_password).pack(fill="x")
        tk.Button(self, text="Delete User", command=delete_user).pack(fill="x")
        tk.Button(self, text="Disable User", command=disable_user).pack(fill="x")
        tk.Button(self, text="Enable User", command=enable_user).pack(fill="x")

    def list_users_ui(self):
        # reuse CLI print for now
        list_users()


class LogisticsWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Button(self, text="Create Camp", command=create_camp).pack(fill="x")
        tk.Button(self, text="Edit Camp", command=edit_camp).pack(fill="x")
        tk.Button(self, text="Delete Camp", command=delete_camp).pack(fill="x")
        tk.Button(self, text="Set Daily Food Stock", command=self.set_food_stock_ui).pack(fill="x")
        tk.Button(self, text="Top-Up Food Stock", command=self.top_up_food_ui).pack(fill="x")
        tk.Button(self, text="Set Pay Rate", command=self.set_pay_rate_ui).pack(fill="x")
        tk.Button(self, text="Check Food Shortage", command=self.shortage_ui).pack(fill="x")
        tk.Button(self, text="View Dashboard", command=self.dashboard_ui).pack(fill="x")
        tk.Button(self, text="Notifications", command=self.notifications_ui).pack(fill="x")

    def set_food_stock_ui(self):
        camp = simple_prompt("Camp name")
        if not camp:
            return
        val = simple_prompt_int("New daily stock")
        if val is None:
            return
        res = set_food_stock_data(camp, val)
        messagebox.showinfo("Result", res.get("status"))

    def top_up_food_ui(self):
        camp = simple_prompt("Camp name")
        if not camp:
            return
        val = simple_prompt_int("Amount to add")
        if val is None:
            return
        res = top_up_food_data(camp, val)
        messagebox.showinfo("Result", res.get("status"))

    def set_pay_rate_ui(self):
        camp = simple_prompt("Camp name")
        if not camp:
            return
        val = simple_prompt_int("Daily pay rate")
        if val is None:
            return
        res = set_pay_rate_data(camp, val)
        messagebox.showinfo("Result", res.get("status"))

    def shortage_ui(self):
        camp = simple_prompt("Camp name")
        if not camp:
            return
        res = compute_food_shortage(camp)
        status = res.get("status")
        if status == "shortage":
            message = f"{res['camp_name']} requires {res['required']} units vs available {res['available']}."
        elif status == "ok":
            message = "Food stock is sufficient."
        elif status == "missing_requirement":
            message = "No food requirement set. Ask scout leader to set daily food per camper."
        else:
            message = status
        messagebox.showinfo("Shortage Check", message)

    def dashboard_ui(self):
        df, summary = build_dashboard_data()
        if df is None:
            messagebox.showinfo("Dashboard", "No camps found.")
            return
        top = tk.Toplevel(self)
        top.title("Dashboard Summary")
        text = tk.Text(top, width=80, height=20)
        text.pack(fill="both", expand=True)
        text.insert("end", df.to_string(index=False))
        text.insert("end", "\n\nSummary:\n")
        for k, v in summary.items():
            text.insert("end", f"{k}: {v}\n")

    def notifications_ui(self):
        notes = load_notifications()
        messagebox.showinfo("Notifications", "\n".join(str(n) for n in notes) if notes else "No notifications")


class ScoutWindow(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Button(self, text="Select Camps to Supervise", command=self.select_camps_ui).pack(fill="x")
        tk.Button(self, text="Bulk Assign Campers from CSV", command=self.bulk_assign_ui).pack(fill="x")
        tk.Button(self, text="Assign Food per Camper per Day", command=self.food_req_ui).pack(fill="x")
        tk.Button(self, text="Record Activity", command=self.record_activity_ui).pack(fill="x")
        tk.Button(self, text="View Stats", command=self.stats_ui).pack(fill="x")
        tk.Button(self, text="Messaging", command=self.messaging_ui).pack(fill="x")

    def select_camps_ui(self):
        camps = read_from_file()
        if not camps:
            messagebox.showinfo("Select Camps", "No camps exist.")
            return
        options = {str(i+1): camp for i, camp in enumerate(camps)}
        sel = simple_prompt(f"Select camps by numbers separated by commas (1-{len(camps)}):\n" +
                            "\n".join(f"[{i}] {camp.name}" for i, camp in options.items()))
        if not sel:
            return
        try:
            indices = [int(x.strip())-1 for x in sel.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Invalid selection.")
            return
        res = assign_camps_to_leader(camps, self.username, indices)
        messagebox.showinfo("Result", res.get("status"))

    def bulk_assign_ui(self):
        camps = read_from_file()
        if not camps:
            messagebox.showinfo("Bulk Assign", "No camps exist.")
            return
        camp = simple_prompt("Camp name")
        if not camp:
            return
        filepath = filedialog.askopenfilename(title="Select campers CSV", filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        res = bulk_assign_campers_from_csv(camp, filepath)
        messagebox.showinfo("Result", res.get("status"))

    def food_req_ui(self):
        camp = simple_prompt("Camp name")
        if not camp:
            return
        units = simple_prompt_int("Daily food units per camper")
        if units is None:
            return
        res = assign_food_amount_pure(camp, units)
        messagebox.showinfo("Result", res.get("status"))

    def record_activity_ui(self):
        camp = simple_prompt("Camp name")
        if not camp:
            return
        date = simple_prompt("Date (YYYY-MM-DD)")
        if not date:
            return
        activity_name = simple_prompt("Activity name (optional)") or ""
        activity_time = simple_prompt("Time (optional)") or ""
        notes = simple_prompt("Notes/outcomes/incidents")
        if notes is None:
            return
        food = simple_prompt("Food units used (optional)")
        food_units = int(food) if food and food.isdigit() else None
        res = record_activity_entry_data(camp, date, activity_name, activity_time, notes, food_units)
        messagebox.showinfo("Result", res.get("status"))

    def stats_ui(self):
        camps = read_from_file()
        if not camps:
            messagebox.showinfo("Stats", "No camps exist.")
            return
        camp = simple_prompt("Camp name for activity stats (optional, leave blank to skip)")
        lines = []
        lines.append("Engagement:")
        for name, score in engagement_scores_data():
            lines.append(f"{name}: {score}")
        lines.append("\nMoney per camp:")
        for name, earned in money_earned_per_camp_data():
            lines.append(f"{name}: ${earned}")
        lines.append(f"\nTotal money: ${total_money_earned_value()}")
        if camp:
            camp_obj = find_camp_by_name(camp)
            if camp_obj:
                stats = activity_stats_data(camp_obj)
                if stats["status"] == "ok":
                    lines.append(f"\nActivity summary for {camp}:")
                    lines.append(f"Total entries: {stats['total_entries']}")
                    if stats["total_food_used"] is not None:
                        lines.append(f"Total food used: {stats['total_food_used']} units")
                else:
                    lines.append(f"\nNo activities recorded for {camp}.")
            else:
                lines.append(f"\nCamp {camp} not found.")
        messagebox.showinfo("Stats", "\n".join(lines))

    def messaging_ui(self):
        convo_win = tk.Toplevel(self)
        convo_win.title("Messaging")
        tk.Label(convo_win, text="Conversations").pack()
        listbox = tk.Listbox(convo_win)
        listbox.pack(fill="both", expand=True)
        partners = get_conversations_for_user(self.username)
        for p in partners:
            listbox.insert("end", p)
        tk.Label(convo_win, text="Recipient:").pack()
        recipient_entry = tk.Entry(convo_win)
        recipient_entry.pack()
        tk.Label(convo_win, text="Message:").pack()
        message_entry = tk.Entry(convo_win, width=50)
        message_entry.pack()

        def send():
            to = recipient_entry.get().strip()
            msg = message_entry.get().strip()
            if to and msg:
                send_message(self.username, to, msg)
                messagebox.showinfo("Sent", f"Message sent to {to}")
        tk.Button(convo_win, text="Send", command=send).pack(pady=5)


def simple_prompt(prompt):
    return tk.simpledialog.askstring("Input", prompt)


def simple_prompt_int(prompt):
    val = tk.simpledialog.askinteger("Input", prompt)
    return val


if __name__ == "__main__":
    load_logins()
    root = tk.Tk()
    root.title("CampTrack Login")
    LoginWindow(root)
    root.mainloop()
