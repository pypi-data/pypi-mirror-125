# excel2csv

This simple command line tool can be used to take an `.xls` file (that is actually formatted in xml), and output it as a csv. The main use case in mind here is to convert excel files downloaded from ManageBac and upload them to Google Sheets, without having to open Excel.

This tool provides the exact same output if the xls file was opened in Excel, copied, and then pasted into Google Sheets, but without requiring Excel.

## Getting Started

Requires Python 3.9 or above. Install Python at python.org. Installing Python also installs a package manager (called pip) that can install the command asc2mb into your command line enviornment.

`pip install excel2csv`

If for some reason the pip command doesn't work, you can manually install it by following the relevant instructions for your system.

### Upgrade

Should you need to update to the latest version, you can do:

`pip install --upgrade excel2csv`


## Use

After pip install worked, it is now installed on your path, and the command excel2csv is now available:

`excel2csv ~/path/to/xml.xls ~/path/to/output.csv`

You can then import the csv file into Google Sheets. The delimiter used is a tab.

Alternatively, on Mac, you can skip the step of saving the csv file, and just run the following fancy command line, and it'll be on your clipboard.

`excel2csv ~/path/to/xml.xls - | pbcopy`

Just paste into "A1" cell of your Google Sheet.