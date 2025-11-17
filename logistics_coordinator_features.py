from camp_class import Camp, save_to_file, read_from_file
import pandas as pd
import json

#Tops up the food stock
def top_up_food(camp_name, amount):
    camps = read_from_file()
    for camp in camps:
        if camp.name == camp_name:
            camp.food_stock += amount
            save_to_file()
            print(f"Food stock for {camp_name} increased by {amount}.")
            return
    print("Camp not found.")

#Sets the daily food stock 
def set_food_stock(camp_name, new_stock):
    camps = read_from_file()
    for camp in camps:
        if camp.name == camp_name:
            camp.food_stock = new_stock
            save_to_file()
            print(f"Daily food stock for {camp_name} set to {new_stock}.")
            return
    print("Camp not found.")

#Shows a dashboard using Pandas
def dashboard():
    camps = read_from_file()
    if not camps:
        print("No camps found.")
        return
    
    data = [{
        "Camp": camp.name,
        "Location": camp.location,
        "Type": camp.camp_type,
        "Start Date": camp.start_date,
        "End Date": camp.end_date,
        "Leaders": len(camp.scout_leaders),
        "Campers": len(camp.campers),
        "Food Stock": camp.food_stock,
        "Pay Rate": getattr(camp, "pay_rate", 0)
    } for camp in camps]

    df = pd.DataFrame(data)
    print("\n--- Camp Dashboard ---")
    print(df)
    return df   

# Visualisations
import matplotlib.pyplot as plt

def plot_food_stock():
    df = dashboard()
    df.plot(kind="bar", x="Camp", y="Food Stock", title="Food Stock per Camp")
    plt.show()

#Shortage Notifications
def check_food_shortage(camp_name, required_amount):
    camps = read_from_file()
    for camp in camps:
        if camp.name == camp_name:
            if camp.food_stock < required_amount:
                notify(f"Food shortage at {camp_name}! Only {camp.food_stock} units left.")
            return
    print("Camp not found.")
#Note - required ammount should be computed as campers * food_per_camper * camp_duration_days
 #Scout Leaders assign food required per camper per day and coordinator checks shortages
 #adjust this function later to calculate required amount automatically - once leader features are ready




def notify(message):
    try:
        with open("notifications.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(message)

    with open("notifications.json", "w") as f:
        json.dump(data, f, indent=4)

#Sets Daily Pay Rate 
def set_pay_rate(camp_name, rate):
    camps = read_from_file()
    for camp in camps:
        if camp.name == camp_name:
            camp.pay_rate = rate
            save_to_file()
            print(f"Pay rate for {camp_name} set to {rate}.")
            return
    print("Camp not found.")
