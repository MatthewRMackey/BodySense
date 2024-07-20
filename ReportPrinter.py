from EntryDatabase import EntryDatabase
from datetime import datetime
from fpdf import FPDF

AM_PM_MAP = {1:"AM", 0:"PM"}
WIDTH_MAP = {"max":74, "date":13, "time":12, "glucose":12, "ketones":12, "bp":15, "weight":10}

class ReportPrinter:
    def __init__(self, from_date: datetime, to_date: datetime):
        self.from_date = from_date
        self.to_date = to_date
        self.entry_db = EntryDatabase()
        self.output_list = self.buildOutputList()


    # Builds a list storing output rows.
    # TODO Refactor this into separate
    def buildOutputList(self):
        data_tables = list(self.entry_db.get_all_database_entries())
        key_dict = {}
        output_table = []
        table_names = ["glucose", "ketones", "bp", "wt"]

        # Join data by (date, time)
        for t_indx, table in enumerate(data_tables):            
            for row in table:
                for name in table_names:
                    key = (row[1], row[2])
                if key not in key_dict:
                    key_dict[key] = {}
                if table_names[t_indx] not in key_dict[key]:
                    key_dict[key][table_names[t_indx]] = []
                if t_indx == 2:
                    key_dict[key][table_names[t_indx]].append(str(row[3])+" / "+str(row[4]))
                else:    
                    key_dict[key][table_names[t_indx]].append(f"{row[3]:.1f}")
    
        # Build output list
        sorted_dates = sorted([date for date in key_dict.keys()], key=self.getDate, reverse=True)
        current_day = "" 
        for key in sorted_dates:
            if datetime.strptime(key[0], "%Y-%m-%d") >= self.from_date and datetime.strptime(key[0], "%Y-%m-%d") <= self.to_date:
                for name in table_names:
                    if name not in key_dict[key]:
                        key_dict[key][name] = []   
                new_day = True if key[0] != current_day else False
                current_day = key[0] if key[0] != current_day else current_day
                max_length = max([len(key_dict[key]['glucose']),len(key_dict[key]['ketones']),len(key_dict[key]['bp']),len(key_dict[key]['wt'])])
                for i in range(max_length):
                    output_table.append([])
                    if new_day:
                        output_table[-1].append(key[0])
                        output_table[-1].append(AM_PM_MAP[key[1]])
                        new_day = False
                    else:
                        output_table[-1].append("-  -  -")
                        output_table[-1].append(AM_PM_MAP[key[1]])
                    for name in table_names:
                        if len(key_dict[key][name])-1 >= i:
                                output_table[-1].append(key_dict[key][name][i])
                        else:
                            output_table[-1].append("-")

        return output_table


    def buildReport(self):
        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()

        # Define header information
        headers = ["Date", "AM/PM", " Gluc.", " Ket.", "B.P.(HI/LO)", "Weight"]

        # Calculate total available space and margins
        total_width = pdf.w
        margin = 10

        # Calculate usable width for data table
        usable_width = total_width - 2 * margin

        # Define column width based on usable space
        col_width = usable_width / len(headers)

        # Print header line with empty cell before and after
        pdf.set_font("Courier", "B", 12)
        for i, header in enumerate(headers):
            # Center text within column
            pdf.cell(col_width, 10, header, 0, 0, 'C')
        pdf.cell(margin, 10, '', 0, 1)  # Empty cell for right margin

        # Print data
        pdf.set_font("Courier", "", 10)
        cur_date = self.output_list[0][0]
        for row in self.output_list:
            if row[0] != cur_date and row[0] != "-  -  -":
                printable_width = pdf.w - 2 * margin
                num_chars = int(printable_width / pdf.get_string_width("_"))               
                cell_width = pdf.get_string_width("_") 
                pdf.cell(cell_width, 0, "_" * num_chars, ln=0)
                pdf.cell(pdf.w, 5, "", 0, 1)
                pdf.cell(margin, 2, '', 0, 1) 
                pdf.cell(pdf.w, 8, "\n"*3,0, 1)

            for value in row:
                pdf.cell(col_width, 8, str(value), 0, 0, 'C')
            pdf.cell(margin, 8, '', 0, 1)  # Empty cell for right margin
            
        # Save the PDF
        return pdf

    def getDate(self, date_str):
        date_obj = datetime.strptime(date_str[0], "%Y-%m-%d")
        return date_obj
