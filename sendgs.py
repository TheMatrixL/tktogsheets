import json
import pandas as pd
import pygsheets
import gspread
from gspread_formatting import set_frozen
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from alg import find_tk
from pytz import timezone    

import os

all_in_one_key = os.environ['all_in_one_key']
jsonFileFromGoogle = os.environ['jsonFileFromGoogle']

def send_to_gs(link, worksheet_name):
  now = datetime.now(timezone('Europe/London'))
  today_now = now.strftime("%d/%m/%Y %H:%M:%S")
  
  df = pd.json_normalize(find_tk(link, worksheet_name))
  
  # Create the Client
  client = pygsheets.authorize(service_account_env_var = "jsonFileFromGoogle")
  # opens a spreadsheet by key
  spreadsht = client.open_by_key(all_in_one_key)
  
  try:
      #Creaete worksheet
      spreadsht.add_worksheet(worksheet_name)
  except:
      print("worksheet already exist, delete and create a new one")
      
      # opens exist worksheet by its name/title
      worksht = spreadsht.worksheet("title", worksheet_name)
      
      #delete exist worksheet
      spreadsht.del_worksheet(worksht)
      
      #Creaete worksheet
      spreadsht.add_worksheet(worksheet_name)
  finally:
      # opens a worksheet by its name/title
      worksht = spreadsht.worksheet("title", worksheet_name)
  #upload df to googlesheet
  worksht.set_dataframe(df,(1,1), copy_index=True)
  
  
  #format text by gspread
  scope = ['https://spreadsheets.google.com/feeds',
           'https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_dict(
      json.loads(jsonFileFromGoogle), scope)
  gc = gspread.authorize(credentials)
  
  sh = gc.open_by_key(all_in_one_key)
  worksheet = sh.worksheet(worksheet_name)
  
  #format text color
  worksheet.format('A', {'textFormat': {'fontSize': 100}})
  worksheet.format('E', {"textFormat": {"foregroundColor": {"red": 1.0,}}})
  
  set_frozen(worksheet, rows=1)
  
  worksht.sort_range(start=(2,1), end=(5000, 12), basecolumnindex=1, sortorder='ASCENDING')
  worksht.update_col(13, [f"Last update: {today_now}"])

if __name__ == "__main__":
  send_to_gs()