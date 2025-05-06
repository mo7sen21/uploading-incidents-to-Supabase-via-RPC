# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:53:16 2022

@author: Ahmed Mohsen

"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime,date , timedelta
import os
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import json
import os
from supabase import create_client, Client
import requests

#reading the sqlite and loading to a dataframe
con = sqlite3.connect('******.db')
test_db = sqlite3.connect('(******.db')

print('Loading Sqlite incedints')

df = pd.read_sql_query("SELECT * FROM ******", test_db)

df['type'] = np.where(df['risk_level'] == 2, 'Minor','Major')


"""
#loading the config info , this would run we are sure about the config files

with open('global_config.json', 'r') as config_file:
    config_data = json.load(config_file)
current_jetson_dev_id = int(config_data['device_id'])
current_jetson_secret_id = str(config_data['secret_id'])
"""


# loading the supabase devices table to get secret for each id

supabase_url = "https://******.supabase.co"
supabase_key = '******.******.******-******'
mail = '******@gmail.com'
mail_pass = '******'

supa_df = create_client(supabase_url, supabase_key)
supa_user = supa_df.auth.sign_in(
    email=mail,
    password=mail_pass)

print('Loading Devices info from supabase')

devices_df = supa_df.table('devices').select('*').execute()
dev_json = json.loads(devices_df.json())
dev_df = pd.json_normalize(dev_json['data'])



#Turning Devices info to dicts , to use as refrence

dev_vdict = dev_df.drop(['type', 'company_id', 'created_at', 'secret'],axis =1).set_index(['id'])
dev_vdict = dev_vdict.to_dict()['vehicle_id']

dev_cdict = dev_df.drop(['type', 'vehicle_id', 'created_at', 'secret'],axis =1).set_index(['id'])
dev_cdict = dev_cdict.to_dict()['company_id']

dev_sdict = dev_df.drop(['type', 'company_id', 'vehicle_id', 'created_at'],axis =1).set_index(['id'])
dev_sdict = dev_sdict.to_dict()['secret']

df['vehicle_id'] = df['id']
df['company_id'] = df['id']
df['device_id'] = df['id']

df['vehicle_id'] = df['vehicle_id'].map(dev_vdict)
df['company_id'] = df['company_id'].map(dev_cdict)
df['device_id'] = df['device_id'].map(dev_sdict)

print('Restructuring Data')

final = pd.DataFrame()
final['device_id'] = df['id']
final['secret'] = df['device_id']

""" to Use the Config file for id and secret , unlook the following two lines"""

#final['device_id'] = current_jetson_dev_id
#final['secret'] = current_jetson_secret_id

final['incident_type'] = df['type']
final['location'] = 300
final['video_url'] = "http://localhost/video.mpg"
final['notes'] = 'time_test_notes_with_delete'
final['created_at'] = df['incident_time']
final['maxVelocity'] = df['max_relative_speed_of_person'].astype(float)
final['noPedestrians'] = df['number_of_persons'].astype(int)


test_supa_json = final.to_dict(orient='records')


print(f'Establishing connection and uploading incidents :{len(final.index)}')

""" on real data, unlook line 108 , and disable line 107"""

for x in range(0,12):
#for x in range(0 , len(test_supa_json) ):
    url = 'https://******.supabase.co/rest/v1/rpc/add_incident'



    headers_e = {'Content-Type': 'application/json',
                'Authorization' : 'Bearer ******.******.******-******',
                 'apikey': f'{supabase_key}'
              }

    supa_json = json.dumps(test_supa_json[x])
    req = requests.post(url, headers=headers_e,  data=supa_json)
    print(f'Uploading inscident number {x+1}')
    print('respnose code :' +  str(req.status_code))
    if req.status_code == 200:
        print('Accepted Response , Device recognized')
    if req.status_code == 400:
        print('Rejected Response , Device not recognized')

""" Following is the option to delete all the rows from the sqlite
 and another option to delete only rows that we loaded based on incident_time"""

# Option 1 delete all data :

"""
c = con.cursor()

# delete all rows from table
c.execute('DELETE FROM incidents;',);

print('Have deleted', c.rowcount, 'records from the table.')

"""

# Option 2 delete row by row
"""
incidents_supa = supa_df.table('incidents').select('*').execute()
incidents_json = json.loads(incidents_supa.json())
incidents_df = pd.json_normalize(incidents_json['data'])

for x in incidents_df['created_at'].unique():
    print(f'record with incedint_time :{x}')
    cursor = con.cursor()
    # Deleting single record now
    sql_delete_query = "DELETE from incidents where incident_time=?"
    cursor.execute(sql_delete_query, (x,))
    con.commit()
    print("Record deleted successfully ")


con.close()
"""
