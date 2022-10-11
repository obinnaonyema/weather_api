#get the tar.gz file
import requests
response = requests.get('https://www.ncei.noaa.gov/data/gsom/archive/gsom-latest.tar.gz')
with open('gsom.tar.gz','wb') as f:
  f.write(response.content)

# importing the "tarfile" module
import tarfile
  
# open file
file = tarfile.open('gsom.tar.gz')
  
# extracting file
file.extractall('./gsom_folder')
  
file.close()

import pandas as pd
import os

path = './gsom_folder'
dfs = []
cnt=0
for file in os.listdir(path):
    _df = pd.read_csv(os.path.join(path,file))
    try:
      #get the columns needed for the task
      _df = _df[['STATION','DATE','LATITUDE','LONGITUDE','NAME','TAVG','TMAX','TMIN']]
      dfs.append(_df)
    except:
      pass
    cnt+=1
    print(cnt,end='--')
    
df = pd.concat(dfs,ignore_index=True)    
df.head()

df.shape

#keep a copy
df_ = df.copy()

#create year and month columns
df['YEAR'] = df.DATE.map(lambda x:x.split('-')[0])
df['YEAR'] = df['YEAR'].astype(int)

df['MONTH'] = df.DATE.map(lambda x:x.split('-')[1])
df['MONTH'] = df['MONTH'].astype(int)
df.tail()

def seasons(val):
  "map seasons"
  if val in (3,4,5):
    return 'Spring'
  elif val in (6,7,8):
    return 'Summer'
  elif val in (9,10,11):
    return 'Fall'
  else:
    return 'Winter'

#map seasons
df['SEASON'] = df.MONTH.map(lambda x: seasons(x))
df.head()

#save to single text file for further ingestion into database
#writing to db from pandas can be slower that using a different ETL tool
df.to_csv('station_data.txt',index=False)

