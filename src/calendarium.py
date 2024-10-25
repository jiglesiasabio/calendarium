import argparse
from datetime import datetime, timedelta
import webbrowser
import os

parser = argparse.ArgumentParser(
                    prog='cal-maker',
                    description='A simple command line calendar maker',
                    epilog='simple calendar maker',)

parser.add_argument('from_date', help='Start date of the calendar (dd/mm/yyyy)') 
parser.add_argument('to_date', help='End date of the calendar (dd/mm/yyyy)') 
parser.add_argument('filename', help='The name of the file to save the calendar') 

args = parser.parse_args()

try:
    from_date = datetime.strptime(args.from_date, '%d/%m/%Y')
    print(f"Parsed from_date: {from_date}")
except ValueError as e:
    print(f"Error parsing from date: {e}")
    exit(1)

try:
    to_date = datetime.strptime(args.to_date, '%d/%m/%Y')
    print(f"Parsed to_date: {to_date}")
except ValueError as e:
    print(f"Error parsing to_date: {e}")
    exit(1)

if from_date >= to_date:
    print("from_date cannot be greater than or equal to to_date")
    exit(1)

script_location = os.path.dirname(os.path.abspath(__file__))
with open(f'{script_location}/templates/base/page-template.html', 'r') as file:
    html = file.read()

with open(f'{script_location}/templates/base/day-block-template.html', 'r') as file:
    day_block_template = file.read()

day_blocks = ''
for i in range((to_date - from_date).days + 1):
    day_block = day_block_template
    day_block = day_block.replace('##DAY-NUMBER##', (from_date + timedelta(days=i)).strftime('%d'))
    day_block = day_block.replace('##DAY-NAME##', (from_date + timedelta(days=i)).strftime('%A')[:3].upper())
    day_block = day_block.replace('##MONTH-NAME##', (from_date + timedelta(days=i)).strftime('%B')[:3].upper())
    if (i+1) % 7 == 0:
        day_block += '''
        <div class="bottom-box-item"><h4>notes</h4></div>
        <div style = "display:block; clear:both; page-break-after:always;"></div>
        
        '''
    day_blocks += day_block

html = html.replace('##DAY-BLOCKS##', day_blocks)

html_path = f"{args.filename}.html"
with open(html_path, 'w') as file:
    file.write(html)
  
webbrowser.open_new_tab(html_path) 