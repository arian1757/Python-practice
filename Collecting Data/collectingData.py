import datetime as dt
import requests
import pandas as pd
import json
import threading
import queue
import asyncio
# from insert_DB  import SaveToDB



        



def fetch_data (url,parameter,event,data_queue, column_name):

    response = requests.get(url, params=parameter)
    
    data = json.loads(response.text)
    
    data = pd.DataFrame(data)
    
    data.columns = column_name
    
   
    data_queue.put(data)
    event.set()


def concat_data(data_queue,param,column_order):
    all_data = data_queue.get()

    for _ in range(data_queue.qsize()):
        data = data_queue.get()
        if 'symbol' in data.columns:
            data.drop('symbol',axis=1, inplace = True)

        
        all_data = all_data.merge(data, on='timestamp', how='left', suffixes=('_left', '_right'))
    
    
    # Reorder columns based on the specified order
    param['startTime'] = all_data['timestamp'].iloc[-1]
    all_data = all_data[column_order]
    all_data.to_csv('dataa.csv')
    # all_data = all_data.reindex(columns=column_order)
    
    
    return all_data,param
i = 0  
def save_data_to_DB(data):
    global i
    data.to_csv(f'data{i}.csv')
    i+=1
    # if insert_db.save_to_database('trading_metrics',data):
    #     print('done!')
    
def collecting_data(data:dict,param:dict):
    start_time = param['startTime']
    period = list(param.items())[3][1]
    
    if int((dt.datetime.now()).timestamp() * 1000) - start_time < int(period[:-1]) * 60 * 1000:
        return print('done')
    
    
    end_time = start_time+int(period[:-1])*60*1000*(int(param['limit']))
  
    param['endTime'] = end_time
    
    
    urls = [data[i]['Endpoints'] for i in list(data.keys())[:-1]]
 
    threads = []
    data_queue = queue.Queue()
    events = [threading.Event() for _ in range(len(data.keys())-1)]
    columns_names =[data[i]['columns'] for i in list(data.keys())[:-1]]
    for  url, event, column_name in zip( urls, events,columns_names ):
        
        thread = threading.Thread(target=fetch_data, args=(url, param, event, data_queue, column_name))
        threads.append(thread)
        thread.start()
    for event in events:
        event.wait()
    
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # final_event = asyncio.Event()
    # loop.run_until_complete(concat_data(data_queue, final_event))
    (all_data, param) = concat_data(data_queue,param,data['column_order'])

    save_data_to_DB(all_data)
    
    return collecting_data(data,param)
   
    
if __name__ == "__main__":
    insert_db = SaveToDB()
    insert_db.initialize_database()
    
    trading_metrics(APIs['Binance'],params['trading_metrics'])
    
    insert_db.close_database()
