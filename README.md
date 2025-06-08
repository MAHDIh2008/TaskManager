# 📋 Task Manager (PyQt6 GUI)

This is a multi-tab personal productivity tool built with **Python** and **PyQt6**, designed to help you manage tasks, track daily/weekly progress, document learning, and visualize activity via charts.

---

## 🧩 Tabs Overview

### 1. **To-Do List**

A daily checklist to track and mark off your current tasks.

* ✅ Add/Delete tasks
* ✅ Save today’s tasks
* ✅ Load default/custom tasks
* ✅ Goal Date lock: disables editing before your target date

### 2. **Progress**

Track your progress weekly.

* ✅ 13 weekly checkboxes (Week 1 - Week 13)
* ✅ Save your weekly check status
* ✅ Goal Date sync

### 3. **Learning Path**

Track learning-focused tasks separately.

* ✅ Add new learning goals
* ✅ Delete selected goals
* ✅ Progress bar shown as percentage
* ✅ Persistent save via `learning_tasks.txt`

### 4. **Daily Log**

Log what you learned each day.

* 🗓 Enter date + topic
* 🧠 Write key takeaways
* ❓ Questions or problems you had
* 🪞 Personal reflection
* ✅ Save to `daily_<date>.txt`

### 5. **Weekly Review**

Summarize your week.

* 📅 Enter week number (1-52)
* ✍️ Write progress summary, challenges, and next week’s plan
* ✅ Saved as `weekly_<year>-W<week>.txt`

### 6. **Chart**

View visual progress from saved data.

* 📈 Daily scores (based on tasks completed)
* 📊 Weekly progress (based on weekly checkboxes)
* ✅ Data source: `task_score.csv`

### 7. **History**

Review past entries.

* 🕓 Daily Logs (last 10 entries)
* 📅 Weekly Reviews (last 5 entries)
* ✅ Read-only, auto-loaded

---

## 📁 Data Files

All data is saved under the `market_data/` directory:

* `todo_<date>.txt`: Daily to-do tasks
* `learning_tasks.txt`: Learning task status
* `progress.txt`: Weekly checkbox state
* `daily_<date>.txt`: Daily log entries
* `weekly_<year>-W<week>.txt`: Weekly reviews
* `task_score.csv`: Scores for charting
* `goal_date.txt`: Selected lock/unlock date

---

## 🚀 How to Run

1. Install dependencies:

```bash
pip install PyQt6 matplotlib
```

2. Run the app:

```bash
python TaskManager.py
```

---

## 🔒 Goal Date Lock System

You can set a **Goal Date** in multiple tabs. Until the selected date arrives:

* Learning Path, Daily Log, and Weekly Review tabs will be disabled.
* Helpful for structured planning or challenge-based tracking.

---

## 💡 Tips

* ✅ Use `Reset to Default` to reload original task templates
* 📦 App is self-contained with minimal dependencies
* 🧠 Great for habit tracking, studying, or learning sprints

---

## 👨‍💻 Author

**Mahdi**
Python Developer & Trader
GitHub: [github.com/MAHDIh2008](https://github.com/MAHDIh2008)
