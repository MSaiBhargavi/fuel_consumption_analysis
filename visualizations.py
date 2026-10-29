<<<<<<< HEAD

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from db_connection import get_connection

IMAGE_DIR = os.path.join("static", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)


def load_chart_data():
    conn = get_connection()
    try:
        sql = """
            SELECT v.vehicle_name, v.vehicle_number, f.fuel_date,
                   f.distance, f.fuel_litres, f.price_per_litre,
                   f.mileage, f.total_cost
            FROM fuel_entries f
            JOIN vehicles v ON v.vehicle_id = f.vehicle_id
            ORDER BY f.fuel_date, f.entry_id
        """
        return pd.read_sql(sql, conn)
    finally:
        conn.close()


def save_chart(fig, filename):
    fig.tight_layout()
    fig.savefig(
        os.path.join(IMAGE_DIR, filename),
        dpi=150,
        bbox_inches="tight"
    )
    plt.close(fig)


def empty_chart(filename, title):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.text(
        0.5, 0.5, "No data available yet",
        ha="center", va="center",
        transform=ax.transAxes
    )
    ax.set_title(title)
    ax.axis("off")
    save_chart(fig, filename)


def mileage_comparison_chart(df):
    filename = "mileage_comparison.png"
    valid = df[
        df["mileage"].notna() & (df["mileage"] > 0)
    ] if not df.empty else df

    if valid.empty:
        return empty_chart(filename, "Average Mileage by Vehicle")

    values = valid.groupby("vehicle_name")["mileage"].mean().sort_values()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    values.plot(kind="bar", ax=ax)
    ax.set_title("Average Mileage by Vehicle")
    ax.set_xlabel("Vehicle")
    ax.set_ylabel("Mileage (km/L)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    save_chart(fig, filename)


def monthly_expenses_chart(df):
    filename = "monthly_expenses.png"
    if df.empty:
        return empty_chart(filename, "Monthly Fuel Expenses")

    df = df.copy()
    df["fuel_date"] = pd.to_datetime(df["fuel_date"], errors="coerce")
    df = df.dropna(subset=["fuel_date"])

    if df.empty:
        return empty_chart(filename, "Monthly Fuel Expenses")

    df["month"] = df["fuel_date"].dt.to_period("M").astype(str)
    values = df.groupby("month")["total_cost"].sum().sort_index()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(values.index, values.values, marker="o")
    ax.set_title("Monthly Fuel Expenses")
    ax.set_xlabel("Month")
    ax.set_ylabel("Expense (₹)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(alpha=0.25)
    save_chart(fig, filename)


def fuel_consumption_chart(df):
    filename = "fuel_consumption.png"
    if df.empty:
        return empty_chart(filename, "Fuel Consumption by Vehicle")

    values = df.groupby("vehicle_name")["fuel_litres"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    values.plot(kind="bar", ax=ax)
    ax.set_title("Total Fuel Consumption by Vehicle")
    ax.set_xlabel("Vehicle")
    ax.set_ylabel("Fuel used (litres)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    save_chart(fig, filename)


def cost_per_kilometre_chart(df):
    filename = "cost_per_kilometre.png"
    valid = df[
        (df["distance"] > 0) & (df["total_cost"] >= 0)
    ] if not df.empty else df

    if valid.empty:
        return empty_chart(filename, "Fuel Cost per Kilometre")

    distance = valid.groupby("vehicle_name")["distance"].sum()
    cost = valid.groupby("vehicle_name")["total_cost"].sum()
    values = (cost / distance).dropna().sort_values()

    if values.empty:
        return empty_chart(filename, "Fuel Cost per Kilometre")

    fig, ax = plt.subplots(figsize=(9, 4.5))
    values.plot(kind="bar", ax=ax)
    ax.set_title("Fuel Cost per Kilometre by Vehicle")
    ax.set_xlabel("Vehicle")
    ax.set_ylabel("Fuel cost (₹/km)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    save_chart(fig, filename)


def monthly_consumption_chart(df):
    filename = "monthly_consumption.png"
    if df.empty:
        return empty_chart(filename, "Monthly Fuel Consumption")

    df = df.copy()
    df["fuel_date"] = pd.to_datetime(df["fuel_date"], errors="coerce")
    df = df.dropna(subset=["fuel_date"])

    if df.empty:
        return empty_chart(filename, "Monthly Fuel Consumption")

    df["month"] = df["fuel_date"].dt.to_period("M").astype(str)
    values = df.groupby("month")["fuel_litres"].sum().sort_index()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(values.index, values.values, marker="o")
    ax.set_title("Monthly Fuel Consumption")
    ax.set_xlabel("Month")
    ax.set_ylabel("Fuel used (litres)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(alpha=0.25)
    save_chart(fig, filename)


def vehicle_performance_chart(df):
    # Different from mileage: this compares total distance travelled.
    filename = "vehicle_performance.png"
    valid = df[df["distance"] > 0] if not df.empty else df

    if valid.empty:
        return empty_chart(filename, "Distance Travelled by Vehicle")

    values = valid.groupby("vehicle_name")["distance"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    values.plot(kind="bar", ax=ax)
    ax.set_title("Total Distance Travelled by Vehicle")
    ax.set_xlabel("Vehicle")
    ax.set_ylabel("Distance (km)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    save_chart(fig, filename)


def generate_all_charts():
    df = load_chart_data()

    mileage_comparison_chart(df)
    monthly_expenses_chart(df)
    fuel_consumption_chart(df)
    cost_per_kilometre_chart(df)
    monthly_consumption_chart(df)
    vehicle_performance_chart(df)


if __name__ == "__main__":
    generate_all_charts()
    print("All six charts generated in static/images/")
=======
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd

from db_connection import get_connection

def get_mileage_data():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            v.vehicle_name,
            AVG(f.mileage) AS average_mileage
        FROM vehicles v
        JOIN fuel_entries f
            ON v.vehicle_id = f.vehicle_id
        GROUP BY v.vehicle_id, v.vehicle_name
        ORDER BY v.vehicle_name
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows)
        return df

    finally:
        cursor.close()
        connection.close()

def plot_mileage_comparison():
    df = get_mileage_data()

    if df.empty:
        print("No mileage data available.")
        return

    plt.figure(figsize=(10, 5))

    plt.bar(
        df["vehicle_name"],
        df["average_mileage"]
    )

    plt.title("Average Mileage Comparison by Vehicle")
    plt.xlabel("Vehicle Name")
    plt.ylabel("Average Mileage (km/litre)")
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig("static/images/mileage_comparison.png")
    plt.close()


def get_monthly_expenses():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            DATE_FORMAT(fuel_date, '%Y-%m') AS month,
            SUM(total_cost) AS monthly_expense
        FROM fuel_entries
        GROUP BY DATE_FORMAT(fuel_date, '%Y-%m')
        ORDER BY month
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    finally:
        cursor.close()
        connection.close()


def plot_monthly_expenses():
    df = get_monthly_expenses()

    if df.empty:
        print("No expense data available.")
        return

    plt.figure(figsize=(10, 5))
    plt.bar(df["month"], df["monthly_expense"])

    plt.title("Monthly Fuel Expenses")
    plt.xlabel("Month")
    plt.ylabel("Total Expense")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("static/images/monthly_expenses.png")
    plt.close()

def get_fuel_consumption_data():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            v.vehicle_name,
            SUM(f.fuel_litres) AS total_litres
        FROM vehicles v
        JOIN fuel_entries f
            ON v.vehicle_id = f.vehicle_id
        GROUP BY v.vehicle_id, v.vehicle_name
        ORDER BY v.vehicle_name
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    finally:
        cursor.close()
        connection.close()


def plot_fuel_consumption():
    df = get_fuel_consumption_data()

    if df.empty:
        print("No fuel consumption data available.")
        return

    plt.figure(figsize=(10, 5))
    plt.bar(df["vehicle_name"], df["total_litres"])

    plt.title("Total Fuel Consumption by Vehicle")
    plt.xlabel("Vehicle Name")
    plt.ylabel("Total Fuel Consumed (Litres)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("static/images/fuel_consumption.png")
    plt.close()


def plot_vehicle_performance():
    df = get_mileage_data()

    if df.empty:
        print("No mileage data available.")
        return

    df = df.sort_values(
        by="average_mileage",
        ascending=False
    )

    plt.figure(figsize=(10, 5))
    plt.bar(
        df["vehicle_name"],
        df["average_mileage"]
    )

    plt.title("Vehicle Fuel Efficiency Performance")
    plt.xlabel("Vehicle Name")
    plt.ylabel("Average Mileage (km/litre)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("static/images/vehicle_performance.png")
    plt.close()

if __name__ == "__main__":
    print("Fuel Consumption Analysis System")
    print("1. Mileage Comparison")
    print("2. Monthly Fuel Expenses")
    print("3. Fuel Consumption")
    print("4. Vehicle Performance")

    choice = input("Choose a chart (1-4): ")

    if choice == "1":
        plot_mileage_comparison()
    elif choice == "2":
        plot_monthly_expenses()
    elif choice == "3":
        plot_fuel_consumption()
    elif choice == "4":
        plot_vehicle_performance()
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
>>>>>>> 102b27e849c4841cc4289906dff949b513489f10
