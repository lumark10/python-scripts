import tkinter as tk
import json
from datetime import datetime

#----- Configs
DATA_FILE = 'time_widget_data.json'  #store widget data

class TimeWidget:
    """
    A desktop time widget that displays current time and saves detailed time data to JSON.
    Features: draggable, always on top, semi-transparent, double-click to close.
    """
    
    def __init__(self):
        self.root = self.create_window()
        self.label = self.create_label()
        self.setup_interactions()
        self.start_update_loop()
    
    def create_window(self):
        """Creates and configures the main window."""
        root = tk.Tk()
        root.title("Time Widget")
        root.geometry("300x100")
        root.attributes("-topmost", True)  # on top 
        root.overrideredirect(True)        # no borders
        root.configure(bg='black')
        root.attributes('-alpha', 0.8)     # transparency
        return root
    
    def create_label(self):
        """Creates and configures the time display label."""
        label = tk.Label(
            self.root,
            text=self.get_current_time(),
            font=("Segoe UI", 24, "bold"),
            fg="#FFD369",  # Gold 
            bg="#222831"   # Dark gray bg
        )
        label.pack(expand=True, fill="both")
        return label
    
    def setup_interactions(self):
        """Sets up mouse interactions for the widget."""
        # draggable
        self.label.bind("<B1-Motion>", self.move_window)
        
        # Close ->double-click
        self.label.bind("<Double-Button-1>", lambda e: self.root.destroy())
    
    def move_window(self, event):
        """Moves the window when dragged."""
        self.root.geometry(f"+{event.x_root}+{event.y_root}")
    
    def get_current_time(self):
        """Returns current time in HH:MM:SS format."""
        return datetime.now().strftime("%H:%M:%S")
    
    def get_current_date(self):
        """Returns current date in YYYY-MM-DD format."""
        return datetime.now().strftime("%Y-%m-%d")
    
    def create_widget_data(self):
        """Creates comprehensive time data structure."""
        now = datetime.now()
        
        return {
            'widget_type': 'time',
            'time': self.get_current_time(),
            'date': self.get_current_date(),
            'timezone': str(now.astimezone().tzinfo),
            'timestamp': now.timestamp(),
            
            # Time format info
            'is_24_hour_format': True,
            'is_am_pm_format': False,
            
            # Day/week info
            'weekday': now.strftime("%A"),
            'weekday_number': now.weekday(),
            'is_weekend': now.weekday() >= 5,
            'is_working_day': now.weekday() < 5,
            
            # Time of day categories
            'is_morning': 6 <= now.hour < 12,
            'is_afternoon': 12 <= now.hour < 18,
            'is_evening': 18 <= now.hour < 22,
            'is_night': now.hour >= 22 or now.hour < 6,
            
            # Special times
            'is_midnight': now.hour == 0,
            'is_noon': now.hour == 12,
            
            # Day halves
            'is_first_half_of_day': now.hour < 12,
            'is_second_half_of_day': now.hour >= 12,
            
            # Year quarters
            'quarter': (now.month - 1) // 3 + 1,
            'is_first_quarter': now.month in [1, 2, 3],
            'is_second_quarter': now.month in [4, 5, 6],
            'is_third_quarter': now.month in [7, 8, 9],
            'is_fourth_quarter': now.month in [10, 11, 12],
            
            # Year info
            'year': now.year,
            'month': now.month,
            'month_name': now.strftime("%B"),
            'day': now.day,
            'is_leap_year': (now.year % 4 == 0 and now.year % 100 != 0) or (now.year % 400 == 0),
            
            # Daylight saving time
            'is_daylight_saving': bool(now.astimezone().dst()),
            'is_dst': now.astimezone().dst() is not None,
            
            # Placeholder for holiday detection (can be extended)
            'is_holiday': False,
            
            # Last updated
            'last_updated': now.isoformat()
        }
    
    def update_display_and_data(self):
        current_time = self.get_current_time()
        self.label.config(text=current_time)
        
        widget_data = self.create_widget_data()
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(widget_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save widget data: {e}")
        
        self.root.after(1000, self.update_display_and_data)
    
    def start_update_loop(self):
        self.update_display_and_data()
    
    def run(self):
        print("Time widget started!")
        print("- Drag to move the widget")
        print("- Double-click to close")
        print(f"- Time data saved to: {DATA_FILE}")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\nWidget closed by user.")
        finally:
            print("Time widget stopped.")


def main():
    widget = TimeWidget()
    widget.run()


if __name__ == "__main__":
    main()
