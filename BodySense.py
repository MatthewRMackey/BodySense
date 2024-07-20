from tkinter import *
from tkinter import messagebox
from datetime import date
from datetime import datetime
from EntryDatabase import EntryDatabase
from PrintDatesWindow import PrintDatesWindow
from ReportPrinter import ReportPrinter
from LogPrinter import LogPrinter

import os
import subprocess


TYPE_GLU = "glu"
TYPE_KET = "ket"
TYPE_BP = "bp"
TYPE_WT = "wt"
ID_WIDTH = 11
DATE_WIDTH = 15
TYPE_WIDTH = 19
LEADING_SPACE = 15

# Enter button function
def enter_command(glu_entry: Entry, ket_entry: Entry, bp_hi_entry: Entry, bp_low_entry: Entry, wt_entry: Entry,
                listbox_list: list, is_morning: bool, day_entry: Entry, month_entry: Entry, year_entry: Entry):
    new_entries = [glu_entry, ket_entry, (bp_hi_entry, bp_low_entry), wt_entry]
    types_list = [TYPE_GLU, TYPE_KET, TYPE_BP, TYPE_WT]
    try:
        float(glu_entry.get())
        float(ket_entry.get())
        int(bp_hi_entry.get())
        int(bp_low_entry.get())
        float(wt_entry.get())
        for indx, type in enumerate(types_list):
            if type != TYPE_BP and new_entries[indx].get() != "":
                entry_date = date(year=int(year_entry.get()), month=int(month_entry.get()), day=int(day_entry.get()))
                entry_db.insert_db_entry(type, entry_date, is_morning, new_entries[indx].get())
                new_entries[indx].delete(0, END)
            elif type == TYPE_BP and new_entries[indx][0].get() != "" and new_entries[indx][1].get() != "":
                entry_date = date(year=int(year_entry.get()), month=int(month_entry.get()), day=int(day_entry.get()))
                entry_db.insert_db_entry(type, entry_date, is_morning, (new_entries[indx][0].get(), new_entries[indx][1].get()))
                new_entries[indx][0].delete(0, END)
                new_entries[indx][1].delete(0, END)

        update_listboxes(listbox_list)

    except ValueError as e:
        # Create and print out the input error
        log = LogPrinter()
        log.log_output(e, [glu_entry.get(), ket_entry.get(), (bp_low_entry.get(), bp_low_entry.get()), wt_entry.get()])

        # Create a popup window
        root = Tk()
        root.title("Input Error")

        # Center and size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 300
        window_height = 100
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
    
        # Add widgets
        warning_text = Label(root, text=f"Error processing inputs, check their formats. \nIf this problem persists, please call your local Matthew.")
        warning_text.pack()
        confirm_button = Button(root, text="OK", command=lambda: root.destroy())
        confirm_button.pack()


# Delete button callback
def delete_command(listbox_list: list):
    lbox_list = listbox_list
    val_names = ["Glucose", "Ketones", "BP", "Weight"]
    types_list = [TYPE_GLU, TYPE_KET, TYPE_BP, TYPE_WT]

    for indx, lbox in enumerate(lbox_list):
        selected_indx = lbox.curselection()
        if selected_indx == (0,):
            return
        elif len(selected_indx) >= 1:
            strip_text = lbox.get(selected_indx[0]).strip()
            text = strip_text[1:list(strip_text).index("|",1)].strip()
            if messagebox.askokcancel("Confirmation", "Are you sure you want to delete "+val_names[indx]+" ID: " + str(text)):
                entry_db.delete_db_entry(types_list[indx], text)

    update_listboxes(listbox_list)


# Prints the entries to PDF
def print_report_command(root):
    os.makedirs(entry_db.get_path_root()+"\\Reports", exist_ok=True)
    dates_win = PrintDatesWindow(root)
    if dates_win.ok_clicked:
        report_printer = ReportPrinter(dates_win.from_date, dates_win.to_date)
        report = report_printer.buildReport()
        report_name = "report_"+report_printer.from_date.strftime("%m-%d-%y")+"_to_"+report_printer.to_date.strftime("%m-%d-%y")+".pdf"
        report.output(entry_db.get_path_root()+"\\Reports\\"+report_name, "F")        
        try:
            subprocess.Popen(["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "/p", entry_db.get_path_root()+"\\Reports\\"+report_name])
        except FileNotFoundError:
            file = entry_db.get_path_root()+"\\Reports\\"+report_name
            print(f"Error: PDF file not found: {file}")
    

# Updates listbox entries
def update_listboxes(list_boxlist: list):
    bp_data_indx = 2
    data_table_names = ['GLUCOSE', 'KETONES', ('BP HIGH', 'BP LOW'), 'WEIGHT']
    data_tables = list(entry_db.get_all_database_entries())
    lboxes = list_boxlist
    
    for indx, lbox in enumerate(lboxes):
        lbox.delete(0, END)
        if indx != bp_data_indx:
            lbox.insert(0, f"| {'ID':^{ID_WIDTH+1}} | {'DATE':^{DATE_WIDTH+4}} | {'AM/PM':^{TYPE_WIDTH-4}} | {data_table_names[indx]:^{TYPE_WIDTH-6}} |")
            lbox.insert(1, f'{"-"*65:^{55}}')
            sorted_data = sorted(data_tables[indx], key=get_date)
            for item in sorted_data:
                am_pm = "AM" if item[2] == 1 else "PM"
                id = str(item[0])
                date = datetime.strptime(item[1], "%Y-%m-%d").strftime("%m-%d-%Y")
                glu = f"{item[3]:.1f}".zfill(5)
                while len(id) < 3:
                    id = "0"+id
                lbox.insert(2, f"| {id:^{ID_WIDTH}} | {date:^{DATE_WIDTH}} | {am_pm:^{TYPE_WIDTH}} | {glu:^{TYPE_WIDTH}} |")

        else:
            lbox.insert(0, f"| {'ID':^{ID_WIDTH+1}} | {'DATE':^{DATE_WIDTH+4}} | {'AM/PM':^{TYPE_WIDTH-4}} | {data_table_names[indx][0]:^{TYPE_WIDTH-5}} | {data_table_names[indx][1]:^{TYPE_WIDTH-5}} |")
            lbox.insert(1, f'{"-"*75:^{65}}')
            sorted_data = sorted(data_tables[indx], key=get_date)
            for item in sorted_data:
                am_pm = "AM" if item[2] == 1 else "PM"
                id = str(item[0])
                date = datetime.strptime(item[1], "%Y-%m-%d").strftime("%m-%d-%Y")
                high = f"{item[3]:.0f}".zfill(3)
                low = f"{item[4]:.0f}".zfill(2)
                while len(id) < 3:
                    id = "0"+id
                lbox.insert(2, f"| {id:^{ID_WIDTH}} | {date:^{DATE_WIDTH}} | {am_pm:^{TYPE_WIDTH}} | {high:^{TYPE_WIDTH}} | {low:^{TYPE_WIDTH}} |")

# Obvious
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
    glu_listbox = Listbox(window, width=49, height=30)
    glu_scrollbar = Scrollbar(window, orient=VERTICAL, command=glu_listbox.yview)
    glu_listbox.config(yscrollcommand=glu_scrollbar.set)
    
    ket_listbox = Listbox(window, width=49, height=30)
    ket_scrollbar = Scrollbar(window, orient=VERTICAL, command=ket_listbox.yview)
    ket_listbox.config(yscrollcommand=ket_scrollbar.set)

    bp_listbox = Listbox(window, width=61, height=30)
    bp_scrollbar = Scrollbar(window, orient=VERTICAL, command=bp_listbox.yview)
    bp_listbox.config(yscrollcommand=bp_scrollbar.set)

    wt_listbox = Listbox(window, width=49, height=30)
    wt_scrollbar = Scrollbar(window, orient=VERTICAL, command=wt_listbox.yview)
    wt_listbox.config(yscrollcommand=wt_scrollbar.set)

    listbox_list = [glu_listbox, ket_listbox, bp_listbox, wt_listbox]
    update_listboxes(listbox_list)

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
    enter_button = Button(button_frame, text="Enter", command=lambda: enter_command(glu_entry, ket_entry, bp_high_entry, bp_low_entry, wt_entry,
                                                                                    listbox_list, is_morning, day_entry, mon_entry, year_entry))
    delete_button = Button(button_frame, text="Delete", command=lambda: delete_command(listbox_list))
    print_report_button = Button(button_frame, text="Print Report", command=lambda: print_report_command(window))
    make_backup_button = Button(button_frame, text="Backup", command=lambda: entry_db.backup_database())

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


# Create database object
entry_db = EntryDatabase()


if __name__ == "__main__":
    # Create the main window
    window = Tk()
    
    # Build window
    generate_window(window)
    
    # Start the event loop to display the window
    window.mainloop()