# mb-excelexport-2csv

This simple command line tool can be used to take an `.xls` file (that is actually formatted in xml), and output it as a csv. The main use case in mind here is to convert excel files downloaded from ManageBac and upload them to Google Sheets, without having to open Excel.

This tool provides the exact same output if the xls file was opened in Excel, copied, and then pasted into Google Sheets, but without requiring Excel.

## Getting Started

Requires Python 3.6.1 or above. Install Python 3 at python.org. Installing Python also installs a package manager (called pip) that can install the command `mb_excelexport_2csv` into your command line environment.

`pip3 install mb_excelexport_2csv`

Then, open the mini app using this command:

`mb_excelexport_2csv gui`

For those who want the command line, use: 

`mb_excelexport_2csv cmd`

See "Command Line" below for more info

### Upgrade

Should you need to update to the latest version, you can do:

`pip install --upgrade mb_excelexport_2csv`


## Command Line

After pip install worked, it is now installed on your path, and the command mb_excelexport_2csv is now available:

`mb_excelexport_2csv cmd ~/path/to/xml.xls ~/path/to/output.csv`

You can then import the csv file into Google Sheets. The delimiter used is a comma.

Alternatively, on Mac, you can skip the step of saving the csv file, and just run the following fancy command line, and it'll be on your clipboard.

`mb_excelexport_2csv cmd ~/path/to/xml.xls - | pbcopy`

Just paste into "A1" cell of your Google Sheet, Data -> Split Text into Columns.