from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import date
from datetime import datetime
import os
from pathlib import Path
import shutil

TYPE_GLU = "glu"
TYPE_KET = "ket"
TYPE_BP = "bp"
TYPE_WT = "wt"
ID_WIDTH = 7
DATE_WIDTH = 13
TYPE_WIDTH = 17
LEADING_SPACE = 15

# Determine the root up to the current user's home directory (Windows only)
def get_path_root():
    cwd = os.getcwd()
    slashes = 0
    index = 0
    root_path = ""
    while slashes < 3:
        root_path += cwd[index]
        if cwd[index] == "\\":
            slashes += 1
        index += 1
    return root_path

# Generates Database
def create_database(db_file):
    """Creates a new SQLite database with a table for entries."""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Create table (if it doesn't exist)
    c.execute("CREATE TABLE IF NOT EXISTS "+"glucose "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, glucose real)")
    conn.commit()
    c.execute("CREATE TABLE IF NOT EXISTS "+"ketones "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, ketones real)")
    conn.commit()
    c.execute("CREATE TABLE IF NOT EXISTS "+"bloodpressure "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, high real, low real)")
    conn.commit()
    c.execute("CREATE TABLE IF NOT EXISTS "+"weight "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, weight real)")
    conn.commit()

    conn.close()

# Inserts into Database
def insert_db_entry(type, date, morning, value):
    """Inserts a new entry into the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if type == TYPE_GLU:
        create_str = "INSERT INTO "+"glucose "+"(date, morning, glucose) VALUES (?, ?, ?)" 
        c.execute(create_str, (date, morning.get(), value))
    elif type == TYPE_KET:
        create_str = "INSERT INTO "+"ketones "+"(date, morning, ketones) VALUES (?, ?, ?)"
        c.execute(create_str, (date, morning.get(), value))
    elif type == TYPE_BP:
        create_str = "INSERT INTO "+"bloodpressure "+"(date, morning, high, low) VALUES (?, ?, ?, ?)"
        c.execute(create_str, (date, morning.get(), value[0], value[1]))
    elif type == TYPE_WT:
        create_str = "INSERT INTO "+"weight "+"(date, morning, weight) VALUES (?, ?, ?)"
        c.execute(create_str, (date, morning.get(), value))

    
    conn.commit()
    conn.close()

# Deletes from the Database
def delete_db_entry(type, entry_id):
    """Deletes an entry from the database based on its ID."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if type == TYPE_GLU:
        create_str = "DELETE FROM "+"glucose "+"WHERE id = ?" 
    elif type == TYPE_KET:
        create_str = "DELETE FROM "+"ketones "+"WHERE id = ?" 
    elif type == TYPE_BP:
        create_str = "DELETE FROM "+"bloodpressure "+"WHERE id = ?" 
    elif type == TYPE_WT:
        create_str = "DELETE FROM "+"weight "+"WHERE id = ?" 

    # Delete entry
    c.execute(create_str, (entry_id,))
    conn.commit()
    conn.close()

# Get all database entries from both tables
def get_database_entries():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    tables = []
    c.execute("SELECT * FROM glucose")
    tables.append(c.fetchall())
    c.execute("SELECT * FROM ketones")
    tables.append(c.fetchall())
    c.execute("SELECT * FROM bloodpressure")
    tables.append(c.fetchall())
    c.execute("SELECT * FROM weight")
    tables.append(c.fetchall())

    return (t for t in tables)

# Backup database keeping the ten most recent backups
##TODO Need to fix the ordering of backups to delete the oldest one when there are 10
def backup_database():
    os.makedirs(get_path_root()+"\\BodySense\\backups", exist_ok=True)
    backups = [f for f in Path(db_path[0:db_path.rindex("\\")]+"\\backups").iterdir() if f.is_file()]
    backup_count = len(backups)
    shutil.copy2(db_path, db_path[0:-11]+"\\backups\\backup_"+str(backup_count)+"_On_"+str(date.today())+".db")

# Save button callback
def enter_command(glu_entry: Entry, ket_entry: Entry, bp_hi_entry: Entry, bp_low_entry: Entry, wt_entry: Entry,
                 glu_listbox: Listbox, ket_listbox: Listbox, bp_listbox: Listbox, wt_listbox: Listbox, is_morning: bool,
                 day_entry: Entry, month_entry: Entry, year_entry: Entry):
    glucose = glu_entry.get()
    ketones = ket_entry.get()
    bp_high = bp_hi_entry.get()
    bp_low = bp_low_entry.get()
    weight = wt_entry.get()

    if glucose != "":
        insert_db_entry(TYPE_GLU, date(year=int(year_entry.get()), month=int(month_entry.get()), day=int(day_entry.get())), is_morning, glucose)
        glu_entry.delete(0, END)

    if ketones != "":
        insert_db_entry(TYPE_KET, date(year=int(year_entry.get()), month=int(month_entry.get()), day=int(day_entry.get())), is_morning, ketones)
        ket_entry.delete(0, END)
    
    if bp_high != "" or bp_low != "":
        insert_db_entry(TYPE_BP, date(year=int(year_entry.get()), month=int(month_entry.get()), day=int(day_entry.get())), is_morning, (bp_high, bp_low))
        bp_hi_entry.delete(0, END)
        bp_low_entry.delete(0, END)
    
    if weight != "":
        insert_db_entry(TYPE_WT, date(year=int(year_entry.get()), month=int(month_entry.get()), day=int(day_entry.get())), is_morning, weight)
        wt_entry.delete(0, END)

    update_listboxes(glu_listbox, ket_listbox, bp_listbox, wt_listbox)
    
# Delete button callback
def delete_command(glu_listbox: Listbox, ket_listbox: Listbox, bp_listbox: Listbox, wt_listbox: Listbox):
    selected_indices1 = glu_listbox.curselection()
    selected_indices2 = ket_listbox.curselection()
    selected_indices3 = bp_listbox.curselection()
    selected_indices4 = wt_listbox.curselection()
    
    if selected_indices1 == (0,) or selected_indices2 == (0,) or selected_indices3 == (0,) or selected_indices4 == (0,):
        return
    elif selected_indices1 != ():
        strip_text = glu_listbox.get(selected_indices1[0]).strip()
        text = strip_text[0:list(strip_text).index(" ")]
        if messagebox.askokcancel("Confirmation", "Are you sure you want to delete Glucose ID: " + str(text)):
            delete_db_entry(TYPE_GLU, text)
    elif selected_indices2 != ():
        strip_text = ket_listbox.get(selected_indices2[0]).strip()
        text = strip_text[0:list(strip_text).index(" ")]
        if messagebox.askokcancel("Confirmation", "Are you sure you want to delete Ketones ID: " + str(text)):
            delete_db_entry(TYPE_KET, text)
    elif selected_indices3 != ():
        strip_text = bp_listbox.get(selected_indices3[0]).strip()
        text = strip_text[0:list(strip_text).index(" ")]
        if messagebox.askokcancel("Confirmation", "Are you sure you want to delete BP ID: " + str(text)):
            delete_db_entry(TYPE_BP, text)
    elif selected_indices4 != ():
        strip_text = wt_listbox.get(selected_indices4[0]).strip()
        text = strip_text[0:list(strip_text).index(" ")]
        if messagebox.askokcancel("Confirmation", "Are you sure you want to delete Weight ID: " + str(text)):
            delete_db_entry(TYPE_WT, text)

    update_listboxes(glu_listbox, ket_listbox, bp_listbox, wt_listbox)

# Prints the entries to PDF
def print_report_command():
    return 

# Updates listbox entries
def update_listboxes(glu_listbox: Listbox, ket_listbox: Listbox, bp_listbox: Listbox, wt_listbox: Listbox):
    
    #Get data
    (glucose_data, ketones_data, bp_data, wt_data) = get_database_entries()

    # Sort data by most recent date
    glucose_data = sorted(glucose_data, key=get_date)
    ketones_data = sorted(ketones_data, key=get_date)
    bp_data = sorted(bp_data, key=get_date)
    wt_data = sorted(wt_data, key=get_date)

    # Delete listbox contents
    glu_listbox.delete(0, END)
    ket_listbox.delete(0, END)
    bp_listbox.delete(0, END)
    wt_listbox.delete(0, END)

    # Add headers to the listboxes
    glu_listbox.insert(0, f"{'ID':^{ID_WIDTH}} {'DATE':^{DATE_WIDTH}} {'AM/PM':^{TYPE_WIDTH}} {'GLUCOSE':^{TYPE_WIDTH}}")
    ket_listbox.insert(0, f"{'ID':^{ID_WIDTH}} {'DATE':^{DATE_WIDTH}} {'AM/PM':^{TYPE_WIDTH}} {'KETONES':^{TYPE_WIDTH}}")
    bp_listbox.insert(0, f"{'ID':^{ID_WIDTH}} {'DATE':^{DATE_WIDTH}} {'AM/PM':^{TYPE_WIDTH}} {'BP High':^{TYPE_WIDTH}} {'BP Low':^{TYPE_WIDTH}}")
    wt_listbox.insert(0, f"{'ID':^{ID_WIDTH}} {'DATE':^{DATE_WIDTH}} {'AM/PM':^{TYPE_WIDTH}} {'WEIGHT':^{TYPE_WIDTH}}")

    glu_listbox.insert(1, f'{"-"*49:^{55}}')
    ket_listbox.insert(1, f'{"-"*49:^{55}}')
    bp_listbox.insert(1, f'{"-"*58:^{65}}')
    wt_listbox.insert(1, f'{"-"*49:^{55}}')

    #Add data to listboxes
    for item in glucose_data:
        am_pm = "AM" if item[2] == 1 else "PM"
        id = str(item[0])
        date = datetime.strptime(item[1], "%Y-%m-%d").strftime("%m-%d-%Y")
        glu = f"{item[3]:.1f}".zfill(5)
        while len(id) < 3:
            id = "0"+id
        glu_listbox.insert(2, f"{id:^{ID_WIDTH}} {date:^{DATE_WIDTH}} {am_pm:^{TYPE_WIDTH}} {glu:^{TYPE_WIDTH+7}}")
    
    for item in ketones_data:
        am_pm = "AM" if item[2] == 1 else "PM"
        id = str(item[0])
        date = datetime.strptime(item[1], "%Y-%m-%d").strftime("%m-%d-%Y")
        ket = f"{item[3]:.2f}".zfill(3)
        while len(id) < 3:
            id = "0"+id
        ket_listbox.insert(2, f"{id:^{ID_WIDTH}} {date:^{DATE_WIDTH}} {am_pm:^{TYPE_WIDTH}} {ket:^{TYPE_WIDTH+7}}")

    for item in bp_data:
        am_pm = "AM" if item[2] == 1 else "PM"
        id = str(item[0])
        date = datetime.strptime(item[1], "%Y-%m-%d").strftime("%m-%d-%Y")
        high = f"{item[3]:.0f}".zfill(3)
        low = f"{item[4]:.0f}".zfill(2)
        while len(id) < 3:
            id = "0"+id
        bp_listbox.insert(2, f"{id:^{ID_WIDTH}} {date:^{DATE_WIDTH}} {am_pm:^{TYPE_WIDTH}} {high:^{TYPE_WIDTH+7}} {low:^{TYPE_WIDTH}}")

    for item in wt_data:
        am_pm = "AM" if item[2] == 1 else "PM"
        id = str(item[0])
        date = datetime.strptime(item[1], "%Y-%m-%d").strftime("%m-%d-%Y")
        wt = f"{item[3]:.1f}".zfill(5)
        while len(id) < 3:
            id = "0"+id
        wt_listbox.insert(2, f"{id:^{ID_WIDTH}} {date:^{DATE_WIDTH}} {am_pm:^{TYPE_WIDTH}} {wt:^{TYPE_WIDTH+7}}")

def get_date(element):
    date_str = element[1]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj

# Centers the window
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Builds window elements
def generate_window(window):
   
    window.title("BodySense: Readings")
    
    # Create labels for input boxes
    glu_label = Label(window, text="Glucose")
    ket_label = Label(window, text="Ketones")
    bp_high_label = Label(window, text="BP High")
    bp_low_label = Label(window, text="BP Low")
    wt_label = Label(window, text="Weight")
    
    # Create input boxes (Entry widgets)
    glu_entry = Entry(window)
    ket_entry = Entry(window)
    bp_high_entry = Entry(window)
    bp_low_entry = Entry(window)
    wt_entry = Entry(window)
     
    # Create listboxs and scrollbars
    glu_listbox = Listbox(window, width=45, height=30)
    glu_scrollbar = Scrollbar(window, orient=VERTICAL, command=glu_listbox.yview)
    glu_listbox.config(yscrollcommand=glu_scrollbar.set)
    
    ket_listbox = Listbox(window, width=45, height=30)
    ket_scrollbar = Scrollbar(window, orient=VERTICAL, command=ket_listbox.yview)
    ket_listbox.config(yscrollcommand=ket_scrollbar.set)

    bp_listbox = Listbox(window, width=55, height=30)
    bp_scrollbar = Scrollbar(window, orient=VERTICAL, command=bp_listbox.yview)
    bp_listbox.config(yscrollcommand=bp_scrollbar.set)

    wt_listbox = Listbox(window, width=45, height=30)
    wt_scrollbar = Scrollbar(window, orient=VERTICAL, command=wt_listbox.yview)
    wt_listbox.config(yscrollcommand=wt_scrollbar.set)
    
    update_listboxes(glu_listbox, ket_listbox, bp_listbox, wt_listbox)

    # Create RadioButtons
    is_morning = IntVar()
    is_morning.set(1)
    radio_frame = Frame(window)
    morning = Radiobutton(radio_frame, text="AM", variable=is_morning, value=1)
    evening = Radiobutton(radio_frame, text="PM", variable=is_morning, value=0)

    # Create Date Input Frame
    date_frame = Frame(window, pady=10)
    day_label = Label(date_frame, text="DD")
    mon_label = Label(date_frame, text="MM")
    year_label = Label(date_frame, text="YYYY")
    day_entry = Entry(date_frame, width=10)
    mon_entry = Entry(date_frame, width=10)
    year_entry = Entry(date_frame, width=10)
    today = str(date.today())
    
    # Default to today
    day_entry.insert(0, today[8:])
    mon_entry.insert(0, today[5:7])
    year_entry.insert(0, today[0:4])

    # Create the buttons
    button_frame = Frame(window)
    enter_button = Button(button_frame, text="Save", command=lambda: enter_command(glu_entry, ket_entry, bp_high_entry, bp_low_entry, wt_entry, 
                                                                           glu_listbox, ket_listbox, bp_listbox, wt_listbox, is_morning, day_entry, mon_entry, year_entry))
    delete_button = Button(button_frame, text="Delete", command=lambda: delete_command(glu_listbox, ket_listbox, bp_listbox, wt_listbox))
    print_report_button = Button(button_frame, text="Print Report", command=lambda: print_report_command())
    make_backup_button = Button(button_frame, text="Backup", command=lambda: backup_database())

    # Arrange the widgets in the window
    glu_label.grid(row=0, column=0)
    ket_label.grid(row=0, column=2)
    bp_high_label.grid(row=0, column=4)
    bp_low_label.grid(row=0, column=5)
    wt_label.grid(row=0, column=7)
    
    glu_entry.grid(row=1, column=0)
    ket_entry.grid(row=1, column=2)
    bp_high_entry.grid(row=1, column=4)
    bp_low_entry.grid(row=1, column=5)
    wt_entry.grid(row=1, column=7)
    
    glu_listbox.grid(row=2, column=0, columnspan=1)
    glu_scrollbar.grid(row=2, column=1, sticky=NS)
    
    ket_listbox.grid(row=2, column=2, columnspan=1)
    ket_scrollbar.grid(row=2, column=3, sticky=NS)

    bp_listbox.grid(row=2, column=4, columnspan=2)
    bp_scrollbar.grid(row=2, column=6, sticky=NS)

    wt_listbox.grid(row=2, column=7, columnspan=1)
    wt_scrollbar.grid(row=2, column=8, sticky=NS)
    
    # Date Frame
    mon_label.grid(row=0, column=0)
    day_label.grid(row=0, column=1)
    year_label.grid(row=0, column=2)
    mon_entry.grid(row=1, column=0)
    day_entry.grid(row=1, column=1)
    year_entry.grid(row=1, column=2)
    date_frame.grid(row=3, column=2)

    # Buttons
    enter_button.grid(row=0, column=0)
    delete_button.grid(row=0, column=1)
    print_report_button.grid(row=0, column=2)
    make_backup_button.grid(row=0, column=3)
    button_frame.grid(row=3, column=4)
    
    # Radio Button
    morning.grid(row=0, column=0)
    evening.grid(row=0, column=1)
    radio_frame.grid(row=3, column=5)

    # Center window
    center_window(window)

os.makedirs(get_path_root()+"\\BodySense", exist_ok=True)
db_path = get_path_root() + "BodySense\\readings.db"

if __name__ == "__main__":
    # Create Databases if don't exist
    create_database(db_path)
    
    # Create the main window
    window = Tk()
    
    # Build window
    generate_window(window)
    
    # Start the event loop to display the window
    window.mainloop()