from tkinter import *
from datetime import date, datetime, timedelta


class PrintDatesWindow:
    def __init__(self, root):
        """Creates and displays a new window with an entry box, OK, and Cancel buttons."""
        self.from_date = datetime.today() - timedelta(days=30)
        self.to_date = datetime.today()
        self.ok_clicked = False
        
        self.new_window = Toplevel(root)  # Create a new window using Toplevel
        self.new_window.title("Input Window")
        self.new_window.geometry("320x150")  # Set the window size

        self.from_frame = Frame(self.new_window)
        self.from_from_label = Label(self.from_frame, text="Start Date").grid(column=0, row=0, columnspan=3)
        self.from_mon_label = Label(self.from_frame, text="MM").grid(row=1, column=0)
        self.from_day_label = Label(self.from_frame, text="DD").grid(row=1, column=1)
        self.from_year_label = Label(self.from_frame, text="YYYY").grid(row=1, column=2)

        self.to_frame = Frame(self.new_window)
        self.to_from_label = Label(self.to_frame, text="End Date").grid(column=0, row=0, columnspan=3)
        self.to_mon_label = Label(self.to_frame, text="MM").grid(row=1, column=0)
        self.to_day_label = Label(self.to_frame, text="DD").grid(row=1, column=1)
        self.to_year_label = Label(self.to_frame, text="YYYY").grid(row=1, column=2)

        self.from_mon_entry = Entry(self.from_frame, width=7)
        self.from_mon_entry.insert(0, self.from_date.month)
        self.from_mon_entry.grid(row=2, column=0)
        self.from_day_entry = Entry(self.from_frame, width=7)
        self.from_day_entry.insert(0, self.from_date.day)
        self.from_day_entry.grid(row=2, column=1)
        self.from_year_entry = Entry(self.from_frame, width=7)
        self.from_year_entry.insert(0, self.from_date.year)
        self.from_year_entry.grid(row=2, column=2)

        self.to_mon_entry = Entry(self.to_frame, width=7)
        self.to_mon_entry.insert(0, self.to_date.month)
        self.to_mon_entry.grid(row=2, column=0)
        self.to_day_entry = Entry(self.to_frame, width=7)
        self.to_day_entry.grid(row=2, column=1)
        self.to_day_entry.insert(0, self.to_date.day)
        self.to_year_entry = Entry(self.to_frame, width=7)
        self.to_year_entry.insert(0, self.to_date.year)
        self.to_year_entry.grid(row=2, column=2)

        self.button_frame = Frame(self.new_window)
        self.ok_button = Button(self.button_frame, text="OK", command=self.ok_button_clicked)
        self.ok_button.grid(row=0, column=0)
        self.cancel_button = Button(self.button_frame, text="Cancel", command=self.cancel_button_clicked)
        self.cancel_button.grid(row=1, column=0)

        self.button_frame.grid(row=1, column=0, pady=10, columnspan=3)
        self.from_frame.grid(row=0, column=0, padx=10)
        self.to_frame.grid(row=0, column=1, padx=10)

        self.center_window(self.new_window)

        while not self.ok_clicked and self.new_window.winfo_exists():
            root.update()

    def ok_button_clicked(self):
        """Gets the text from the entry box and closes the new window."""

        from_day = self.from_day_entry.get()
        from_mon = self.from_mon_entry.get()
        from_year = self.from_year_entry.get()

        to_day = self.to_day_entry.get()
        to_mon = self.to_mon_entry.get()
        to_year = self.to_year_entry.get()

        self.from_date = datetime.strptime(from_year+"-"+from_mon+"-"+from_day, "%Y-%m-%d")
        self.to_date = datetime.strptime(to_year+"-"+to_mon+"-"+to_day, "%Y-%m-%d")
        self.ok_clicked = True

        # Process the entered text here (e.g., print it, store it)
        self.new_window.destroy()  # Close the new window
    
    def cancel_button_clicked(self):
        """Simply closes the new window on Cancel button click."""
        self.new_window.destroy()

    # Centers the window
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")