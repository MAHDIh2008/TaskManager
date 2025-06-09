import sys
import os
import csv
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QScrollArea,
    QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates


class TaskManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 80, 800, 730)

        # Initialize variables
        self.goal_date = None
        self.data_dir = "task_data"  # Changed from market_data to task_data
        os.makedirs(self.data_dir, exist_ok=True)

        # Default tasks
        self.default_tasks = [
            "Review daily goals",
            "Complete priority tasks",
            "Learning session",
            "Exercise",
            "Plan next day"
        ]
        
        self.weekly_tasks = [f"Week {i + 1}" for i in range(13)]
        self.weekly_checkboxes = []
        self.todo_checkboxes = []
        self.learning_checkboxes = []

        self.initialize_data_files()
        self.create_main_widgets()
        self.load_initial_data()

    def initialize_data_files(self):
        """Create necessary data files if they don't exist with proper validation"""
        required_files = {
            "task_score.csv": "",
            "progress.txt": "",
            "custom_tasks.txt": "\n".join(self.default_tasks),
            "learning_tasks.txt": "\n".join(["Python Programming|0", 
                                           "Data Structures|0",
                                           "Algorithms|0"])
        }
        
        for file, default_content in required_files.items():
            path = os.path.join(self.data_dir, file)
            if not os.path.exists(path):
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(default_content)
                except Exception as e:
                    print(f"Error creating {file}: {e}")
                    QMessageBox.warning(self, "File Error", 
                                      f"Could not create {file}: {str(e)}")

    # بقیه متدها بدون تغییر می‌مانند...
    def create_main_widgets(self):
        """Create all main widgets and tabs"""
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create tabs
        self.tab_todo = QWidget()
        self.tab_progress = QWidget()
        self.tab_learning = QWidget()
        self.tab_daily = QWidget()
        self.tab_weekly = QWidget()
        self.tab_chart = QWidget()
        self.tab_history = QWidget()

        self.tab_widget.addTab(self.tab_todo, "To-Do List")
        self.tab_widget.addTab(self.tab_progress, "Progress")
        self.tab_widget.addTab(self.tab_learning, "Learning Path")
        self.tab_widget.addTab(self.tab_daily, "Daily Log")
        self.tab_widget.addTab(self.tab_weekly, "Weekly Review")
        self.tab_widget.addTab(self.tab_chart, "Chart")
        self.tab_widget.addTab(self.tab_history, "History")

        self.setup_todo_tab()
        self.setup_progress_tab()
        self.setup_learning_tab()
        self.setup_daily_tab()
        self.setup_weekly_tab()
        self.setup_chart_tab()
        self.setup_history_tab()

    def setup_todo_tab(self):
        """Setup to-do list tab"""
        layout = QVBoxLayout(self.tab_todo)

        # Goal date controls
        goal_frame = QFrame()
        goal_layout = QHBoxLayout(goal_frame)
        goal_layout.addWidget(QLabel("Goal Date (YYYY-MM-DD):"))

        self.goal_date_edit = QLineEdit()
        goal_layout.addWidget(self.goal_date_edit)

        set_goal_btn = QPushButton("Set Goal")
        set_goal_btn.clicked.connect(self.save_goal_date)
        goal_layout.addWidget(set_goal_btn)

        layout.addWidget(goal_frame)

        # Task entry
        self.todo_entry = QLineEdit()
        self.todo_entry.setPlaceholderText("Enter a new task")
        layout.addWidget(self.todo_entry)

        # Task list in scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.todo_container = QWidget()
        self.todo_layout = QVBoxLayout(self.todo_container)
        self.todo_layout.addStretch()
        scroll.setWidget(self.todo_container)
        layout.addWidget(scroll)

        # Buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)

        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self.add_task)
        btn_layout.addWidget(add_btn)

        del_btn = QPushButton("Delete Selected")
        del_btn.clicked.connect(self.delete_task)
        btn_layout.addWidget(del_btn)

        save_btn = QPushButton("Save Tasks")
        save_btn.clicked.connect(self.save_tasks)
        btn_layout.addWidget(save_btn)

        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_to_default_tasks)
        btn_layout.addWidget(reset_btn)

        layout.addWidget(btn_frame)

    def setup_progress_tab(self):
        """Setup progress tracking tab"""
        layout = QVBoxLayout(self.tab_progress)

        # Goal date controls
        goal_frame = QFrame()
        goal_layout = QHBoxLayout(goal_frame)
        goal_layout.addWidget(QLabel("Goal Date (YYYY-MM-DD):"))

        self.goal_date_edit_progress = QLineEdit()
        goal_layout.addWidget(self.goal_date_edit_progress)

        set_goal_btn = QPushButton("Set Goal")
        set_goal_btn.clicked.connect(self.save_goal_date)
        goal_layout.addWidget(set_goal_btn)

        layout.addWidget(goal_frame)

        # Progress checkboxes in scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.progress_container = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_container)

        for task in self.weekly_tasks:
            cb = QCheckBox(task)
            self.weekly_checkboxes.append(cb)
            self.progress_layout.addWidget(cb)

        self.progress_layout.addStretch()
        scroll.setWidget(self.progress_container)
        layout.addWidget(scroll)

        # Save button
        save_btn = QPushButton("Save Weekly Progress")
        save_btn.clicked.connect(self.save_progress)
        layout.addWidget(save_btn)

    def setup_learning_tab(self):
        """Setup learning path tab"""
        layout = QVBoxLayout(self.tab_learning)

        # Goal date controls
        goal_frame = QFrame()
        goal_layout = QHBoxLayout(goal_frame)
        goal_layout.addWidget(QLabel("Goal Date (YYYY-MM-DD):"))

        self.goal_date_edit_learning = QLineEdit()
        goal_layout.addWidget(self.goal_date_edit_learning)

        set_goal_btn = QPushButton("Set Goal")
        set_goal_btn.clicked.connect(self.save_goal_date)
        goal_layout.addWidget(set_goal_btn)

        layout.addWidget(goal_frame)

        # Task entry
        self.learning_entry = QLineEdit()
        self.learning_entry.setPlaceholderText("Enter new learning task")
        layout.addWidget(self.learning_entry)

        # Task list in scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.learning_container = QWidget()
        self.learning_layout = QVBoxLayout(self.learning_container)
        self.learning_layout.addStretch()
        scroll.setWidget(self.learning_container)
        layout.addWidget(scroll)

        # Buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)

        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self.add_learning_task)
        btn_layout.addWidget(add_btn)

        del_btn = QPushButton("Delete Selected")
        del_btn.clicked.connect(self.delete_learning_task)
        btn_layout.addWidget(del_btn)

        layout.addWidget(btn_frame)

        # Progress label
        self.learning_progress_label = QLabel()
        layout.addWidget(self.learning_progress_label)

    def setup_daily_tab(self):
        """Setup daily log tab"""
        layout = QVBoxLayout(self.tab_daily)

        # Goal date controls
        goal_frame = QFrame()
        goal_layout = QHBoxLayout(goal_frame)
        goal_layout.addWidget(QLabel("Goal Date (YYYY-MM-DD):"))

        self.goal_date_edit_daily = QLineEdit()
        goal_layout.addWidget(self.goal_date_edit_daily)

        set_goal_btn = QPushButton("Set Goal")
        set_goal_btn.clicked.connect(self.save_goal_date)
        goal_layout.addWidget(set_goal_btn)

        layout.addWidget(goal_frame)

        # Date entry
        self.daily_date_edit = QLineEdit()
        self.daily_date_edit.setPlaceholderText("Date (YYYY-MM-DD)")
        self.daily_date_edit.setText(QDate.currentDate().toString("yyyy-MM-dd"))
        layout.addWidget(self.daily_date_edit)

        # Topic entry
        self.topic_entry = QLineEdit()
        self.topic_entry.setPlaceholderText("Topic Covered")
        layout.addWidget(self.topic_entry)

        # Sections
        sections = [
            ("Key Takeaways:", "takeaway_entry"),
            ("Questions:", "question_entry"),
            ("Reflection:", "reflection_entry"),
        ]

        for title, attr_name in sections:
            layout.addWidget(QLabel(title))
            text_edit = QTextEdit()
            setattr(self, attr_name, text_edit)
            layout.addWidget(text_edit)

        # Save button
        save_btn = QPushButton("Save Daily Log")
        save_btn.clicked.connect(self.save_daily)
        layout.addWidget(save_btn)

    def setup_weekly_tab(self):
        """Setup weekly review tab"""
        layout = QVBoxLayout(self.tab_weekly)

        # Goal date controls
        goal_frame = QFrame()
        goal_layout = QHBoxLayout(goal_frame)
        goal_layout.addWidget(QLabel("Goal Date (YYYY-MM-DD):"))

        self.goal_date_edit_weekly = QLineEdit()
        goal_layout.addWidget(self.goal_date_edit_weekly)

        set_goal_btn = QPushButton("Set Goal")
        set_goal_btn.clicked.connect(self.save_goal_date)
        goal_layout.addWidget(set_goal_btn)

        layout.addWidget(goal_frame)

        # Week number entry
        self.week_number_edit = QLineEdit()
        self.week_number_edit.setPlaceholderText("Week Number (1-52)")
        layout.addWidget(self.week_number_edit)

        # Sections
        sections = [
            ("Progress Summary:", "week_summary"),
            ("Challenges Faced:", "week_challenges"),
            ("Next Week Plans:", "week_plans"),
        ]

        for title, attr_name in sections:
            layout.addWidget(QLabel(title))
            text_edit = QTextEdit()
            setattr(self, attr_name, text_edit)
            layout.addWidget(text_edit)

        # Save button
        save_btn = QPushButton("Save Weekly Review")
        save_btn.clicked.connect(self.save_weekly)
        layout.addWidget(save_btn)

    def setup_chart_tab(self):
        """Setup progress charts tab"""
        layout = QVBoxLayout(self.tab_chart)

        # Daily chart
        daily_chart_frame = QFrame()
        daily_layout = QVBoxLayout(daily_chart_frame)
        daily_layout.addWidget(QLabel("Daily Progress"))

        self.fig_daily = Figure(figsize=(6, 3), facecolor='#f0f0f0')
        self.ax_daily = self.fig_daily.add_subplot(111)
        self.canvas_daily = FigureCanvas(self.fig_daily)
        daily_layout.addWidget(self.canvas_daily)

        layout.addWidget(daily_chart_frame)

        # Weekly chart
        weekly_chart_frame = QFrame()
        weekly_layout = QVBoxLayout(weekly_chart_frame)
        weekly_layout.addWidget(QLabel("Weekly Progress"))

        self.fig_weekly = Figure(figsize=(6, 3), facecolor='#f0f0f0')
        self.ax_weekly = self.fig_weekly.add_subplot(111)
        self.canvas_weekly = FigureCanvas(self.fig_weekly)
        weekly_layout.addWidget(self.canvas_weekly)

        layout.addWidget(weekly_chart_frame)

    def setup_history_tab(self):
        """Setup history viewing tab"""
        layout = QVBoxLayout(self.tab_history)

        self.history_tabs = QTabWidget()
        layout.addWidget(self.history_tabs)

        # Daily history
        self.tab_daily_history = QWidget()
        self.daily_history_layout = QVBoxLayout(self.tab_daily_history)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.daily_scroll_content = QWidget()
        self.daily_scroll_layout = QVBoxLayout(self.daily_scroll_content)
        scroll.setWidget(self.daily_scroll_content)

        self.daily_history_layout.addWidget(scroll)
        self.history_tabs.addTab(self.tab_daily_history, "Daily Log History")

        # Weekly history
        self.tab_weekly_history = QWidget()
        self.weekly_history_layout = QVBoxLayout(self.tab_weekly_history)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.weekly_scroll_content = QWidget()
        self.weekly_scroll_layout = QVBoxLayout(self.weekly_scroll_content)
        scroll.setWidget(self.weekly_scroll_content)

        self.weekly_history_layout.addWidget(scroll)
        self.history_tabs.addTab(self.tab_weekly_history, "Weekly Review History")

    def load_initial_data(self):
        """Load all initial data"""
        self.load_goal_date()
        self.load_tasks()
        self.load_progress()
        self.load_learning_tasks()
        self.load_history()
        self.update_chart()

    def load_goal_date(self):
        """Load goal date from file"""
        path = os.path.join(self.data_dir, "goal_date.txt")
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    date_str = f.read().strip()
                    self.goal_date = QDate.fromString(date_str, "yyyy-MM-dd")

                    # Update all goal date entries
                    for widget in [self.goal_date_edit, self.goal_date_edit_progress,
                                 self.goal_date_edit_learning, self.goal_date_edit_daily,
                                 self.goal_date_edit_weekly]:
                        widget.setText(date_str)
            except Exception as e:
                print(f"Error reading goal date: {e}")
                self.goal_date = None

    def save_goal_date(self):
        """Save goal date with validation"""
        date_str = self.sender().parent().findChild(QLineEdit).text()
        try:
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if not date.isValid():
                raise ValueError

            if date < QDate.currentDate():
                QMessageBox.critical(self, "Invalid Date", "Goal date cannot be in the past")
                return

            with open(os.path.join(self.data_dir, "goal_date.txt"), "w") as f:
                f.write(date_str)
            self.goal_date = date

            # Update all goal date entries
            for widget in [self.goal_date_edit, self.goal_date_edit_progress,
                          self.goal_date_edit_learning, self.goal_date_edit_daily,
                          self.goal_date_edit_weekly]:
                widget.setText(date_str)

            QMessageBox.information(self, "Goal Set", f"Goal date set to {date_str}")
            self.apply_goal_lock()
        except ValueError:
            QMessageBox.critical(self, "Invalid Date", "Use YYYY-MM-DD format")

    def apply_goal_lock(self):
        """Lock or unlock tabs based on goal date"""
        if not self.goal_date:
            return

        locked = QDate.currentDate() < self.goal_date
        state = Qt.ItemFlag.ItemIsEnabled if not locked else Qt.ItemFlag.ItemIsSelectable

        # Lock/unlock relevant tabs
        for tab in [self.tab_daily, self.tab_weekly, self.tab_learning]:
            for widget in tab.findChildren(QWidget):
                if isinstance(widget, QLineEdit) and widget in [
                    self.goal_date_edit_daily, self.goal_date_edit_weekly,
                    self.goal_date_edit_learning
                ]:
                    continue
                widget.setEnabled(not locked)

    def load_tasks(self):
        """Load tasks from file"""
        today = QDate.currentDate().toString("yyyy-MM-dd")
        filepath = os.path.join(self.data_dir, f"todo_{today}.txt")

        # Clear existing checkboxes
        for i in reversed(range(self.todo_layout.count())):
            widget = self.todo_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.todo_checkboxes = []

        try:
            # First try to load today's tasks
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("|", 1)
                        if len(parts) == 2:
                            value, task = parts
                            self._create_task_checkbox(task, value == "1")
            else:
                # If no tasks for today, load from custom_tasks.txt or default
                custom_tasks_path = os.path.join(self.data_dir, "custom_tasks.txt")

                # Check if custom_tasks exists and has content
                if os.path.exists(custom_tasks_path) and os.path.getsize(custom_tasks_path) > 0:
                    with open(custom_tasks_path, "r", encoding="utf-8") as f:
                        tasks = [line.strip() for line in f if line.strip()]
                else:
                    tasks = self.default_tasks
                    # Save default tasks to custom_tasks for future use
                    with open(custom_tasks_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(tasks))

                # Create checkboxes for loaded tasks
                for task in tasks:
                    self._create_task_checkbox(task)

                # Save these tasks for today (all unchecked)
                self.save_tasks()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tasks: {str(e)}")

    def _create_task_checkbox(self, task, checked=False):
        """Helper to create a task checkbox"""
        cb = QCheckBox(task)
        cb.setChecked(checked)
        self.todo_checkboxes.append(cb)
        self.todo_layout.insertWidget(self.todo_layout.count() - 1, cb)

    def add_task(self):
        """Add a new task to the list"""
        task = self.todo_entry.text().strip()
        if task:
            self._create_task_checkbox(task)
            self.todo_entry.clear()
            self.save_tasks()

    def delete_task(self):
        """Delete selected tasks"""
        deleted = False
        remaining_checkboxes = []

        for cb in self.todo_checkboxes:
            if cb.isChecked():
                cb.deleteLater()
                deleted = True
            else:
                remaining_checkboxes.append(cb)

        if deleted:
            self.todo_checkboxes = remaining_checkboxes
            self.save_tasks()
        else:
            QMessageBox.information(self, "Info", "No tasks selected for deletion")

    def reset_to_default_tasks(self):
        """Reset tasks to default list"""
        # Clear existing checkboxes
        for i in reversed(range(self.todo_layout.count())):
            widget = self.todo_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.todo_checkboxes = []

        # Load default tasks
        for task in self.default_tasks:
            self._create_task_checkbox(task)

        # Save to custom tasks file
        custom_tasks_path = os.path.join(self.data_dir, "custom_tasks.txt")
        with open(custom_tasks_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.default_tasks))

        # Save to today's tasks
        self.save_tasks()
        QMessageBox.information(self, "Success", "Tasks reset to default successfully")

    def save_tasks(self):
        """Save tasks to file"""
        today = QDate.currentDate().toString("yyyy-MM-dd")
        score = sum(1 for cb in self.todo_checkboxes if cb.isChecked())

        try:
            # Save today's tasks
            with open(
                    os.path.join(self.data_dir, f"todo_{today}.txt"), "w", encoding="utf-8"
            ) as f:
                for cb in self.todo_checkboxes:
                    status = "1" if cb.isChecked() else "0"
                    f.write(f"{status}|{cb.text()}\n")

            # Update task score CSV
            task_score_path = os.path.join(self.data_dir, "task_score.csv")
            updated = False
            rows = []

            if os.path.exists(task_score_path):
                with open(task_score_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[0] == today:
                            row = [today, str(score)]
                            updated = True
                        if row:
                            rows.append(row)

            if not updated:
                rows.append([today, score])

            with open(task_score_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            # Update custom tasks file
            current_tasks = [cb.text() for cb in self.todo_checkboxes]
            custom_tasks_path = os.path.join(self.data_dir, "custom_tasks.txt")
            with open(custom_tasks_path, "w", encoding="utf-8") as f:
                f.write("\n".join(current_tasks))

            self.update_chart()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save tasks: {str(e)}")

    def save_daily(self):
        """Save daily log with date validation"""
        date_str = self.daily_date_edit.text()
        try:
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if not date.isValid():
                raise ValueError

            if date > QDate.currentDate():
                QMessageBox.critical(self, "Invalid Date", "Date cannot be in the future")
                return
        except ValueError:
            QMessageBox.critical(self, "Invalid Date", "Please use YYYY-MM-DD format")
            return

        try:
            with open(
                    os.path.join(self.data_dir, f"daily_{date_str}.txt"),
                    "w",
                    encoding="utf-8",
            ) as f:
                f.write(f"Date: {date_str}\n")
                f.write(f"Topic Covered: {self.topic_entry.text()}\n")
                f.write(f"Key Takeaways: {self.takeaway_entry.toPlainText()}\n")
                f.write(f"Questions: {self.question_entry.toPlainText()}\n")
                f.write(f"Reflection: {self.reflection_entry.toPlainText()}\n")

            self.topic_entry.clear()
            self.takeaway_entry.clear()
            self.question_entry.clear()
            self.reflection_entry.clear()

            self.load_history()
            QMessageBox.information(self, "Success", "Daily log saved successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save daily log: {str(e)}")

    def save_weekly(self):
        """Save weekly review with validation"""
        week_number = self.week_number_edit.text()
        try:
            week_num = int(week_number)
            if not 1 <= week_num <= 52:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Week number must be between 1-52")
            return

        year = QDate.currentDate().year()
        week_id = f"{year}-W{week_num:02d}"

        try:
            with open(
                    os.path.join(self.data_dir, f"weekly_{week_id}.txt"),
                    "w",
                    encoding="utf-8",
            ) as f:
                f.write(f"Week ID: {week_id}\n")
                f.write(f"Progress Summary: {self.week_summary.toPlainText()}\n")
                f.write(f"Challenges Faced: {self.week_challenges.toPlainText()}\n")
                f.write(f"Next Week Plans: {self.week_plans.toPlainText()}\n")

            self.week_number_edit.clear()
            self.week_summary.clear()
            self.week_challenges.clear()
            self.week_plans.clear()

            self.load_history()
            QMessageBox.information(self, "Success", "Weekly review saved successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save weekly review: {str(e)}")

    def save_progress(self):
        """Save weekly progress"""
        week = QDate.currentDate().weekNumber()
        year = QDate.currentDate().year()
        week_id = f"{year}-W{week:02d}"
        score = sum(1 for cb in self.weekly_checkboxes if cb.isChecked())

        try:
            with open(
                    os.path.join(self.data_dir, "progress.txt"), "w", encoding="utf-8"
            ) as f:
                for cb in self.weekly_checkboxes:
                    status = "1" if cb.isChecked() else "0"
                    f.write(f"{status}|{cb.text()}\n")

            task_score_path = os.path.join(self.data_dir, "task_score.csv")
            updated = False
            rows = []

            if os.path.exists(task_score_path):
                with open(task_score_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[0] == week_id:
                            row = [week_id, str(score)]
                            updated = True
                        if row:
                            rows.append(row)

            if not updated:
                rows.append([week_id, score])

            with open(task_score_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            self.update_chart()
            QMessageBox.information(self, "Success", "Weekly progress saved successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save progress: {str(e)}")

    def load_progress(self):
        """Load progress from file"""
        try:
            with open(
                    os.path.join(self.data_dir, "progress.txt"), "r", encoding="utf-8"
            ) as f:
                for line in f:
                    parts = line.strip().split("|", 1)
                    if len(parts) == 2:
                        value, task = parts
                        for cb in self.weekly_checkboxes:
                            if cb.text() == task:
                                cb.setChecked(value == "1")
                                break
        except FileNotFoundError:
            pass

    def load_learning_tasks(self):
        """Load learning tasks from file"""
        # Clear existing checkboxes
        for i in reversed(range(self.learning_layout.count())):
            widget = self.learning_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.learning_checkboxes = []

        try:
            if os.path.exists(os.path.join(self.data_dir, "learning_tasks.txt")):
                with open(os.path.join(self.data_dir, "learning_tasks.txt"), "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("|", 1)
                        if len(parts) == 2:
                            value, task = parts
                        else:
                            value, task = "0", line.strip()

                        cb = QCheckBox(task)
                        cb.setChecked(value == "1")
                        cb.stateChanged.connect(self.save_learning_tasks)
                        self.learning_checkboxes.append(cb)
                        self.learning_layout.insertWidget(self.learning_layout.count() - 1, cb)

            self.update_learning_progress()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load learning tasks: {str(e)}")

    def add_learning_task(self):
        """Add a new learning task"""
        task = self.learning_entry.text().strip()
        if task:
            cb = QCheckBox(task)
            cb.stateChanged.connect(self.save_learning_tasks)
            self.learning_checkboxes.append(cb)
            self.learning_layout.insertWidget(self.learning_layout.count() - 1, cb)
            self.learning_entry.clear()
            self.save_learning_tasks()

    def delete_learning_task(self):
        """Delete selected learning tasks"""
        deleted = False
        remaining_checkboxes = []

        for cb in self.learning_checkboxes:
            if cb.isChecked():
                cb.deleteLater()
                deleted = True
            else:
                remaining_checkboxes.append(cb)

        if deleted:
            self.learning_checkboxes = remaining_checkboxes
            self.save_learning_tasks()
        else:
            QMessageBox.information(self, "Info", "No tasks selected for deletion")

    def save_learning_tasks(self):
        """Save learning tasks to file"""
        try:
            with open(os.path.join(self.data_dir, "learning_tasks.txt"), "w", encoding="utf-8") as f:
                for cb in self.learning_checkboxes:
                    status = "1" if cb.isChecked() else "0"
                    f.write(f"{status}|{cb.text()}\n")

            self.update_learning_progress()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save learning tasks: {str(e)}")

    def update_learning_progress(self):
        """Update learning progress label"""
        total = len(self.learning_checkboxes)
        if total == 0:
            self.learning_progress_label.setText("No tasks available")
            return

        done = sum(1 for cb in self.learning_checkboxes if cb.isChecked())
        percent = (done / total) * 100 if total > 0 else 0
        self.learning_progress_label.setText(
            f"Progress: {done}/{total} tasks ({percent:.0f}%)"
        )

    def load_history(self):
        """Load history from files"""
        try:
            # Clear existing history
            for i in reversed(range(self.daily_scroll_layout.count())):
                widget = self.daily_scroll_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            for i in reversed(range(self.weekly_scroll_layout.count())):
                widget = self.weekly_scroll_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            # Load daily history
            daily_files = sorted(
                [f for f in os.listdir(self.data_dir) if f.startswith("daily_")],
                key=lambda x: datetime.datetime.strptime(x[6:-4], "%Y-%m-%d"),
                reverse=True,
            )

            for file in daily_files[:10]:
                filepath = os.path.join(self.data_dir, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                label = QLabel(file.replace("daily_", "").replace(".txt", ""))
                label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
                self.daily_scroll_layout.addWidget(label)

                text_edit = QTextEdit()
                text_edit.setPlainText(content)
                text_edit.setReadOnly(True)
                self.daily_scroll_layout.addWidget(text_edit)

            # Load weekly history
            weekly_files = sorted(
                [f for f in os.listdir(self.data_dir) if f.startswith("weekly_")],
                key=lambda x: x.replace("weekly_", "").replace(".txt", ""),
                reverse=True,
            )

            for file in weekly_files[:5]:
                filepath = os.path.join(self.data_dir, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                label = QLabel(file.replace("weekly_", "").replace(".txt", ""))
                label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
                self.weekly_scroll_layout.addWidget(label)

                text_edit = QTextEdit()
                text_edit.setPlainText(content)
                text_edit.setReadOnly(True)
                self.weekly_scroll_layout.addWidget(text_edit)

        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Error loading history: {str(e)}")

    def update_chart(self):
        """Update progress charts"""
        try:
            # Clear previous charts
            self.ax_daily.clear()
            self.ax_weekly.clear()

            # Load data from CSV
            daily_dates = []
            daily_scores = []
            weekly_data = {}

            try:
                with open(
                        os.path.join(self.data_dir, "task_score.csv"), "r", encoding="utf-8"
                ) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if not row or len(row) < 2:
                            continue

                        # Daily data
                        try:
                            date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
                            score = int(row[1])
                            daily_dates.append(date)
                            daily_scores.append(score)
                            continue
                        except ValueError:
                            pass

                        # Weekly data
                        try:
                            if row[0].count('-W') == 1:  # Format: YYYY-WNN
                                year, week = row[0].split('-W')
                                weekly_data[(int(year), int(week))] = int(row[1])
                        except (ValueError, IndexError):
                            continue

            except FileNotFoundError:
                # Show "No data" message if file doesn't exist
                self.ax_daily.text(0.5, 0.5, 'No daily data available',
                                  ha='center', va='center', fontsize=12)
                self.ax_weekly.text(0.5, 0.5, 'No weekly data available',
                                   ha='center', va='center', fontsize=12)
                self.canvas_daily.draw()
                self.canvas_weekly.draw()
                return

            # Update daily chart
            if daily_dates and daily_scores:
                self.ax_daily.plot(
                    daily_dates,
                    daily_scores,
                    marker="o",
                    color="cyan",
                    label="Daily Score",
                    linestyle="-",
                    linewidth=2,
                )
                self.ax_daily.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
                self.ax_daily.tick_params(axis="x", rotation=45)
                self.ax_daily.set_title("Daily Progress")
                self.ax_daily.set_ylabel("Score")
                self.ax_daily.legend(loc="upper left")
                self.ax_daily.grid(True, linestyle='--', alpha=0.7)
                self.fig_daily.tight_layout()
            else:
                self.ax_daily.text(0.5, 0.5, 'No daily data available',
                                 ha='center', va='center', fontsize=12)

            # Update weekly chart
            if weekly_data:
                sorted_weeks = sorted(weekly_data.keys())
                week_labels = [f"{year}-W{week:02d}" for year, week in sorted_weeks]
                week_scores = [weekly_data[(year, week)] for year, week in sorted_weeks]

                self.ax_weekly.plot(
                    week_labels,
                    week_scores,
                    marker="s",
                    color="orange",
                    label="Weekly Score",
                    linestyle="-",
                    linewidth=2,
                )
                self.ax_weekly.tick_params(axis="x", rotation=45)
                self.ax_weekly.set_title("Weekly Progress")
                self.ax_weekly.set_ylabel("Score")
                self.ax_weekly.legend(loc="upper left")
                self.ax_weekly.grid(True, linestyle='--', alpha=0.7)
                self.fig_weekly.tight_layout()
            else:
                self.ax_weekly.text(0.5, 0.5, 'No weekly data available',
                                   ha='center', va='center', fontsize=12)

            self.canvas_daily.draw()
            self.canvas_weekly.draw()

        except Exception as e:
            QMessageBox.critical(self, "Chart Error", f"Failed to update chart: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec())
