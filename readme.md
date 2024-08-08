# BodySense
BodySense python based desktop application that allows the tracking and reporting of self-monitored health readings. The GUI is build using the TK library, and the data is stored using a sqlite3 database.

## Values 
Current values that can be stored are:
- Glucose
- Ketones
- Blood Pressure
- Weight. 

There can be multiple entries a day, and there indicators of morning or evening readings; the idea being many diabetics check their glucose multiple times a day. 

## Reports
The user is asked to enter a date range 

## Examples
### GUI
![User Interface](/media/gui1.png)

### Bad Inputs
![Some Input Validation](/media/input_valid1.png)
![More Input Validation](/media/input_valid2.png)

### Choose Report Dates
![Report Dates](/media/report_date_window.png)

### Reports
![Report](/media/report.png)