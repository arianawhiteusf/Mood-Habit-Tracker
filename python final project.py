#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import datetime
import os
from statistics import mean

class DayEntry:
    def __init__(self, date, mood, sleep_hours, gym, ate_meals):
        self.date = date
        self.mood = int(mood)
        self.sleep_hours = float(sleep_hours)
        self.gym = gym.lower() == "true"
        self.ate_meals = ate_meals.lower() == "true"

    def to_list(self):
        return [self.date, self.mood, self.sleep_hours, self.gym, self.ate_meals]

class Tracker:
    def __init__(self, filename):
        self.filename = filename
        self.entries = self.load_entries()

    def load_entries(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  
            return [DayEntry(*row) for row in reader]

    def add_entry(self, entry):
        self.entries.append(entry)
        with open(self.filename, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if os.stat(self.filename).st_size == 0:
                writer.writerow(["Date", "Mood", "Sleep Hours", "Gym", "Ate Meals"])
            writer.writerow(entry.to_list())

    def analyze(self):
        if not self.entries:
            return "No data to analyze."

        mood_scores = [e.mood for e in self.entries]
        sleep_hours = [e.sleep_hours for e in self.entries]
        gym_days = sum(e.gym for e in self.entries)
        meal_days = sum(e.ate_meals for e in self.entries)

        avg_mood = mean(mood_scores)
        avg_sleep = mean(sleep_hours)

        return {
            "Average Mood": round(avg_mood, 2),
            "Average Sleep Hours": round(avg_sleep, 2),
            "Gym Days": gym_days,
            "Days Ate 3 Meals": meal_days,
            "Total Days Tracked": len(self.entries)
        }

#
if __name__ == "__main__":
    DATA_FILE = "mood_tracker_data.csv"

    tracker = Tracker(DATA_FILE)
    summary = tracker.analyze()
    print("Your Weekly Summary:")
    for k, v in summary.items():
        print(f"{k}: {v}")


# In[ ]:




