import datetime as dt
import requests
import pandas as pd
import json
import threading
import queue
import asyncio
from insert_DB  import SaveToDB


params ={
    'symbol':'ETHUSDT',
    'trading_metrics':{'start_time': int((dt.datetime.now() - dt.timedelta(days=30)).timestamp() * 1000),
                       'limit':500,
                       'period':'5m'

    }

}

APIs = {
    'Binance':{
        'EndPoint': {
            'trading_metrics':{'openInterest':'https://fapi.binance.com/futures/data/openInterestHist',
                               'accountRatio':'https://fapi.binance.com/futures/data/topLongShortAccountRatio',
                                'positionRatio':'https://fapi.binance.com/futures/data/topLongShortPositionRatio',
                                'gaccountRatio':'https://fapi.binance.com/futures/data/globalLongShortAccountRatio',
                                'longshortRatio':'https://fapi.binance.com/futures/data/takerlongshortRatio'}
        }
    }
    

}
def openInterest(url,parameter,event,data_queue):
    response = requests.get(url, params=parameter)
    data = json.loads(response.text)
    data = pd.DataFrame(data)
    params['trading_metrics']['start_time'] = data.iloc[-1,3]
    
    data_queue.put(data)
    event.set()

def accountRatio(url,parameter,event,data_queue):
    response = requests.get(url, params=parameter)
    data = json.loads(response.text)
    data = pd.DataFrame(data)
    data.columns = ['symbol','longShortRatioA','longAccountA','shortAccountA','timestamp']
    
    data_queue.put(data)
    event.set()
    
def positionRatio(url,parameter,event,data_queue):
    response = requests.get(url, params=parameter)
    data = json.loads(response.text)
    data = pd.DataFrame(data)
    data.columns =['symbol','longShortRatioP','longAccountP','shortAccountP','timestamp']
    
    data_queue.put(data)
    event.set()
    
def gaccountRatio(url,parameter,event,data_queue):
    response = requests.get(url, params=parameter)
    data = json.loads(response.text)
    data = pd.DataFrame(data)
    data.columns = ['symbol','longShortRatioG','longAccountG','shortAccountG','timestamp']
    
    data_queue.put(data)
    event.set()
    
def longshortRatio(url,parameter,event,data_queue):
    response = requests.get(url, params=parameter)
    data = json.loads(response.text)
    data = pd.DataFrame(data)
    
    data_queue.put(data)
    event.set()

def concat_data(data_queue):
    all_data = data_queue.get()

    for _ in range(data_queue.qsize()):
        data = data_queue.get()
        if 'symbol' in data.columns:
            data.drop('symbol',axis=1, inplace = True)

        
        all_data = all_data.merge(data, on='timestamp', how='left', suffixes=('_left', '_right'))

    column_order = ["timestamp", "symbol", "longShortRatioA", "longAccountA", "shortAccountA",
                "longShortRatioP", "longAccountP", "shortAccountP", "longShortRatioG",
                "longAccountG", "shortAccountG", "buySellRatio", "sellVol", "buyVol",
                "sumOpenInterest", "sumOpenInterestValue"]
    # Reorder columns based on the specified order
    all_data = all_data.reindex(columns=column_order)
    
    return all_data
    
def save_data_to_DB(data):
    if insert_db.save_to_database('trading_metrics',data):
        print('done!')
    
def trading_metrics(data:dict,param:dict):
    start_time = param['start_time']
    
    if int((dt.datetime.now()).timestamp() * 1000) - start_time < 5 * 60 * 1000:
        return print('done')
    
    
    end_time = start_time+5*60*1000*(int(param['limit']))
    parameters = {'symbol':params['symbol'], 'startTime':start_time,'endTime':end_time, 'limit':param['limit'],
             'period':param['period'] }
    func_names = list(data['EndPoint']['trading_metrics'].keys())
    url =list(data['EndPoint']['trading_metrics'].values())
    threads = []
    data_queue = queue.Queue()
    events = [threading.Event() for _ in range(len(func_names))]
    for func_name, url, event in zip(func_names, url, events):
        thread = threading.Thread(target=globals()[func_name], args=(url, parameters, event, data_queue))
        threads.append(thread)
        thread.start()
    for event in events:
        event.wait()
    
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # final_event = asyncio.Event()
    # loop.run_until_complete(concat_data(data_queue, final_event))
    all_data = concat_data(data_queue)

    save_data_to_DB(all_data)
    
    return trading_metrics(data,param)
   
    
if __name__ == "__main__":
    insert_db = SaveToDB()
    insert_db.initialize_database()
    
    trading_metrics(APIs['Binance'],params['trading_metrics'])
    
    insert_db.close_database()
