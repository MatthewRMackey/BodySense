import random
import sqlite3
import datetime

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('C:\\Users\\matth\\BodySense\\readings.db')
c = conn.cursor()

# Define a function to generate random dates starting from June 1, 2024
def generate_date(start_date="2024-06-01"):
  days_to_add = random.randint(0, 30)
  date_delta = datetime.timedelta(days=days_to_add)
  start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
  return (start_date_obj + date_delta).strftime("%Y-%m-%d")

# Generate random data for each table
glucose_data = []
ketones_data = []
bloodpressure_data = []
weight_data = []
for i in range(30):
  date = generate_date()
  morning = random.randint(0, 1)  # Boolean for morning (0 or 1)
  glucose = round(random.uniform(70, 140),2)  # Random glucose value
  ketones = round(random.uniform(0, 1.5), 2)  # Random ketones value
  bloodpressure_high = random.randint(90, 140)
  bloodpressure_low = random.randint(60, 90)  # Ensure low is lower than high
  weight = random.uniform(150, 200)  # Random weight value
  glucose_data.append((date, morning, glucose))
  ketones_data.append((date, morning, ketones))
  bloodpressure_data.append((date, morning, bloodpressure_high, bloodpressure_low))
  weight_data.append((date, morning, weight))

# Insert data into tables (replace table names if different)
c.executemany("INSERT INTO glucose (date, morning, glucose) VALUES (?, ?, ?)", glucose_data)
c.executemany("INSERT INTO ketones (date, morning, ketones) VALUES (?, ?, ?)", ketones_data)
c.executemany("INSERT INTO bloodpressure (date, morning, high, low) VALUES (?, ?, ?, ?)", bloodpressure_data)
c.executemany("INSERT INTO weight (date, morning, weight) VALUES (?, ?, ?)", weight_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("30 random entries inserted into each table!")