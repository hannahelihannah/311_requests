# Import packages
import codecs
import json
import io
from typing import Callable, Coroutine, List
import concurrent
from concurrent.futures import ThreadPoolExecutor
import asyncio
import math
import os.path
import random
from os import path

import aiohttp
import numpy as np
from tqdm import tqdm
import time
import pandas as pd
from datetime import datetime
import requests
import multiprocessing
from multiprocessing import Pool, Manager, cpu_count
from functools import partial

#### DEFINE FUNCTIONS

def get_api_url(lat, long):
    return f'https://geocoding.geo.census.gov/geocoder/geographies/coordinates?' \
                          f'x={long}&y={lat}&' \
                          f'benchmark=Public_AR_Census2020&vintage=Census2020_Census2020&' \
                          f'layers=10&format=json'

##### TESTING OUT THE THREADED FUNCTION HERE
async def http_get(session: aiohttp.ClientSession, url: str) -> Coroutine:
    UTF8DECODER = codecs.getincrementaldecoder('utf-8')(errors='strict')
    r = await session.get(url)
    stream = r.content
    while not stream.at_eof():
        data = await stream.read()
        T = json.loads(UTF8DECODER.decode(data))
        try:
            tract = T['result']['geographies']['Census Blocks'][0]['TRACT']
        except:
            tract = np.nan
        # ['result']['addressMatches'][0]['geographies']['Census Blocks'][0]
        # https://stackoverflow.com/questions/35036921/asyncio-decode-utf-8-with-streamreader
        # tract = res

        return tract

async def fetch_tracts_async(url_column: List, inner: Callable):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_column:
            tasks.append(
                inner(
                    session,
                    url
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions = True)
        return responses


def get_tracts(df, url_col):
    urls = df[url_col]
    responses = asyncio.get_event_loop().run_until_complete(fetch_tracts_async(urls, http_get))
    return responses


    # Get the content from the request
    # https://towardsdatascience.com/part-1-defining-and-timing-an-api-function-with-python-b0849775e961
    # https://towardsdatascience.com/python-requests-api-70a555fecc97

# https://dmort-ca.medium.com/part-4-async-api-requests-with-python-and-httpx-9dcd630bc9b5

def main():
    ## Get tract API urls
  return 'Not quite done'


if __name__ == '__main__':
    start_time = datetime.now()
    print(f'Started at: {start_time}')

    #### IMPORT DATA

    # Import Census Tract Files
    cens_2010 = pd.read_csv(r'Census_Tracts_in_2010.csv') \
        .drop(columns=['CREATOR', 'EDITOR', 'CREATED', 'EDITED', 'SHAPEAREA', 'SHAPELEN'])
    print('Finished importing Census Tract files.')

    # Import ACS Data Files
    acs_ward_demo = pd.read_csv('ACS_Demographic_Characteristics_DC_Ward.csv')
    acs_ward_soc = pd.read_csv('ACS_Social_Characteristics_DC_Ward.csv')
    acs_trc_econ = pd.read_csv('ACS_Economic_Characteristics_DC_Census_Tract.csv')
    acs_trc_hous = pd.read_csv('ACS_Housing_Characteristics_DC_Census_Tract.csv')
    print('Finished importing ACS files by ward and tract.')

    # Import 311 Service Request Files
    fields = ['OBJECTID', 'SERVICECODE', 'SERVICECODEDESCRIPTION', 'SERVICETYPECODEDESCRIPTION',
              'ORGANIZATIONACRONYM', 'ADDDATE', 'RESOLUTIONDATE', 'SERVICEORDERSTATUS', 'PRIORITY',
              'STREETADDRESS', 'LATITUDE', 'LONGITUDE', 'WARD', 'CITY', 'STATE', 'ZIPCODE']

    if path.exists('all_311.csv'):
        print('311 file exists and data already joined.')
        all_311 = pd.read_csv('all_311.csv')

    else:
        req_2020 = pd.read_csv(r'311_City_Service_Requests_in_2020.csv', usecols=fields)
        req_2019 = pd.read_csv(r'311_City_Service_Requests_in_2019.csv', usecols=fields)
        req_2018 = pd.read_csv(r'311_City_Service_Requests_in_2018.csv', usecols=fields)
        req_2017 = pd.read_csv(r'311_City_Service_Requests_in_2017.csv', usecols=fields)
        req_2016 = pd.read_csv(r'311_City_Service_Requests_in_2016.csv', usecols=fields)
        print('Finished importing 311 Request Files.')

        # Join all 311 dataframes together
        all_311 = pd.DataFrame().append([req_2020, req_2019, req_2018, req_2017, req_2016], ignore_index=True)
        all_311.to_csv('all_311.csv', index=False)
        print('Joined 311 dataframes.')

        print(f'Finished importing all data files in {(datetime.now()-start_time).total_seconds()} seconds.')

    # Get all tract URLs
    tract_url_time = datetime.now()
    print(f'Starting process to get 311 urls at {tract_url_time}.')
    tract_time = datetime.now()
    if 'tract_url' in all_311.columns:
        print(f'Starting process to get 311 multiprocess at {tract_url_time}.')
        all_311['tract'] = get_tracts(all_311, 'tract_url')
    else:
        all_311['tract_url'] = all_311.apply(lambda x: get_api_url(x['LATITUDE'], x['LONGITUDE']), axis=1)
        print(f'Retrieved all tract URLs in {(datetime.now() - tract_url_time).total_seconds()} seconds.') ## Currently taking about 2 mins
        print('Starting to retrieve all tracts...')
        all_311.to_csv('all_311.csv')
        all_311_splits = []
        # Split dataframe into chunks and retrieve tracts
        for x in np.array_split(all_311, 50, axis=0):
            print(f'Retrieving tracs for slice {x}...')
            x['tract'] = get_tracts(x, 'tract_url')
            all_311_splits.append(x)
        print('Finished retrieving tracts.')
        all_311_splits = pd.concat(all_311_splits)
        all_311_splits.to_csv('all_311_tracts.csv', index=False)


    print(f'Retrieved tracts in {(datetime.now()-tract_time).total_seconds()} seconds.')



print('Finished ')

## Article for items: https://arxiv.org/pdf/1710.02452.pdf


### CODE GRAVEYARD
# from urllib3 import request

# import urllib3
# import certifi
# http = urllib3.PoolManager(
#        cert_reqs='CERT_REQUIRED',
#        ca_certs=certifi.where())
# Would've used data prior to 2016 but was not consistent
# Access all data using DCDATA API
# TODO re-attempt API calls to avoid 1000 row limit
# Census tract data: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
# Census geocoding how to : https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
#2020 docs: https://dcdatahub.maps.arcgis.com/sharing/rest/content/items/82b33f4833284e07997da71d1ca7b1ba/info/metadata/metadata.xml?format=default&output=html
# url2020 = 'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/' \
#           'ServiceRequests/MapServer/11/query?outFields=*&outSR=4326&f=json'
#
# x_2020 = http.request('GET', url2020)
# y_2020 = json.loads(x_2020.data.decode('utf-8'))]
# d2020 = pd.json_normalize(y_2020, 'features')
