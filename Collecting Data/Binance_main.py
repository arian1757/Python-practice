import datetime as dt
from collectingData import  collecting_data


params ={
    'trading_metrics':{'symbol':'ETHUSDT','startTime': int((dt.datetime.now() - dt.timedelta(days=3)).timestamp()* 1000),
                       'limit':500,'period':'5m','endTime':None },
    'K-line':{'symbol':'ETHUSDT','startTime':int((dt.datetime.now() - dt.timedelta(days=3)).timestamp() * 1000),
              'limit':1500,'interval':'5m','endTime':None, 'pair':'ETHUSDT'},
    'Funding_Rate_History':{'symbol':'ETHUSDT','startTime':int((dt.datetime.now() - dt.timedelta(days=3)).timestamp() * 1000),
              'limit':1000,'period':'480m','endTime':None,},

}
APIs = {
    'Binance':{
        
            'trading_metrics':{'openInterest':{'Endpoints':'https://fapi.binance.com/futures/data/openInterestHist','columns':['symbol','sumOpenInterest','sumOpenInterestValue','timestamp']},
                               'accountRatio':{'Endpoints':'https://fapi.binance.com/futures/data/topLongShortAccountRatio','columns':['symbol','longShortRatioA','longAccountA','shortAccountA','timestamp']},
                                'positionRatio':{'Endpoints':'https://fapi.binance.com/futures/data/topLongShortPositionRatio','columns':['symbol','longShortRatioP','longAccountP','shortAccountP','timestamp']},
                                'gaccountRatio':{'Endpoints':'https://fapi.binance.com/futures/data/globalLongShortAccountRatio','columns':['symbol','longShortRatioG','longAccountG','shortAccountG','timestamp']},
                                'longshortRatio':{'Endpoints':'https://fapi.binance.com/futures/data/takerlongshortRatio','columns':["buySellRatio", "buyVol", "sellVol",'timestamp']},
                                'column_order':["timestamp", "longShortRatioA", "longAccountA", "shortAccountA","longShortRatioP", "longAccountP", "shortAccountP", "longShortRatioG",
                                                "longAccountG", "shortAccountG", "buySellRatio", "sellVol", "buyVol","sumOpenInterest", "sumOpenInterestValue"]}
        ,
        'K-line':{'Candlestick Data':{'Endpoints':'https://fapi.binance.com/fapi/v1/klines','columns':[ 'timestamp','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_of_trades','Taker_buy_base_asset_volume','Taker_buy_quote_asset_volume',' Ignore']},
                  'Index Price Kline':{'Endpoints':'https://fapi.binance.com/fapi/v1/indexPriceKlines','columns':['timestamp','Open_IN','High_IN','Low_IN','Close_IN' ,'Ignore','Close_time_IN','Ignore','Ignore','Ignore','Ignore','Ignore']},
                  'Mark Price Kline':{'Endpoints':'https://fapi.binance.com/fapi/v1/markPriceKlines','columns':['timestamp', 'Open_market', 'High_market', 'Low_market', 'Close_market' , 'Ignore', 'Close_time_market', 'Ignore', 'Ignore', 'Ignore', 'Ignore', 'Ignore']},
                  'Premium Index Kline Data':{'Endpoints':'https://fapi.binance.com/fapi/v1/premiumIndexKlines','columns':['timestamp', 'Open_Premium', 'High_Premium', 'Low_Premium', 'Close_Premium', 'Ignore', 'Close_time_Premium', 'Ignore', 'Ignore', 'Ignore', 'Ignore', 'Ignore']},
                  'column_order':['timestamp','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_of_trades','Taker_buy_base_asset_volume','Taker_buy_quote_asset_volume',
                                  'Open_IN','High_IN','Low_IN','Close_IN',
                                  'Open_market', 'High_market', 'Low_market', 'Close_market' , 'Close_time_market',
                                  'Open_Premium', 'High_Premium', 'Low_Premium', 'Close_Premium', 'Close_time_Premium'
                                  ]}  ,              
        'Funding_Rate_History' :{'fundingRate':{'Endpoints':'https://fapi.binance.com/fapi/v1/fundingRate','columns':['symbol', 'timestamp', 'fundingRate', 'markPrice']} ,
                                 'column_order':  ['symbol', 'timestamp', 'fundingRate', 'markPrice']   
                
                
                }

    
    }
}

# for dataset in APIs['Binance'].keys():
#     collecting_data(APIs['Binance'][dataset],params[dataset])
    
collecting_data(APIs['Binance']['Funding_Rate_History'],params['Funding_Rate_History'])
# collecting_data(APIs['Binance']['K-line'],params['K-line'])
    # globals()[key] = DataSet(params(key),APIs['Binance'][key].keys(),)
 