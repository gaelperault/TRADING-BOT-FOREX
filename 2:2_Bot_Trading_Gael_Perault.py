import pandas as pd
import json
import csv
import time
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
import os
import numpy as np
import talib
from pathlib import Path
from oandapyV20 import API
from oandapyV20.contrib.requests import (MarketOrderRequest, TrailingStopLossDetails,StopLossOrderRequest,TakeProfitOrderRequest )
import time
import datetime
path = str(os.path.abspath(os.getcwd()))
fx_pairs="AUDJPY CADJPY CHFJPY EURJPY NZDJPY USDJPY GBPJPY AUDUSD EURUSD GBPUSD NZDUSD USDCAD USDCHF AUDCAD CADCHF EURCAD GBPCAD NZDCAD AUDCHF EURCHF GBPCHF NZDCHF EURAUD EURGBP EURNZD GBPNZD GBPAUD AUDNZD"
fx_pairs=fx_pairs.replace(' ','')
logs = []
logs1 = []




####################################### DATA COMPILATION ##########################################################


while True :
    print(' checking for available pair .....')
    fx_pairs="AUDJPY CADJPY CHFJPY EURJPY NZDJPY USDJPY GBPJPY AUDUSD EURUSD GBPUSD NZDUSD USDCAD USDCHF AUDCAD CADCHF EURCAD GBPCAD NZDCAD AUDCHF EURCHF GBPCHF NZDCHF EURAUD EURGBP EURNZD GBPNZD GBPAUD AUDNZD"
    fx_pairs=fx_pairs.replace(' ','')
    client = oandapyV20.API(access_token = '60b61afd407c002be3b45984d46a2641-05ed7396fe447ebc7d4ca061a5df5b4c')
    accountID = '101-004-16009898-001'
    
    r = positions.OpenPositions(accountID = accountID)
    pos = client.request(r)
    
        
    if pos['positions'] == '[]':

        counter1=(len(fx_pairs)/6)
        print("lancement de l'algorithme")

    else:



        parsed_json = (json.loads(json.dumps(r.response, indent=4)))
        k = len(parsed_json['positions']) - 1
        while k >= 0 :

            m = parsed_json['positions'][k]['instrument']

            logs.append(m)
            k = k -1


        else:
            for pair in logs:

                q = pair.replace("_",'')
                logs1.append(q)


            for s in logs1:
                fx_pairs = fx_pairs.replace(s,"")


            counter1=(len(fx_pairs)/6)
            print(str(counter1)+ ' pair over 28 actually available ')
            

    print('\n')
    print(str(logs)+' : ' )
    print('\n')
    print(str(len(logs)) + ' Pairs are already in trade.')
    print('\n')
    
    while counter1>0:
        
        print(counter1)

        print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

        string=fx_pairs[-6:]
        fx_pairs=fx_pairs[0:-6]
        counter1=counter1-1
        df = pd.read_csv(path+'/WinPython/Forex Trading Bot/Forex OHLC/'+string+'.csv')
        df=df.drop('Unnamed: 0', 1)
        df=df.drop('complete', 1)
        df=df.drop('time', 1)
        df=df.drop('volume', 1)
        print('========================')
        print('========================')
        print('            Last News About : '+ string)
        print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
        print('========================')
        print(df.head(1))
        print(df.tail(1))
####################################### START RSI COMPUTING ##########################################################


        MA_ARRAY_13=talib.EMA(np.array(df.close), timeperiod=13)
        RSI_ARRAY_13=talib.RSI(MA_ARRAY_13, timeperiod=13) # measuring the velocity and magnitude of price movements
        MA_RSI_OMA_21=talib.EMA(RSI_ARRAY_13, timeperiod=21)
        MA_RSI_OMA_137=talib.EMA(RSI_ARRAY_13, timeperiod=137)
        print('========================')
        print('========================')
        print('RSI Computing from '+ string +" Data : ")
        print('========================')
        print(RSI_ARRAY_13[-10:])
        print(MA_RSI_OMA_21[-10:])
        print(MA_RSI_OMA_137[-10:])
        #time.sleep(5)
        ##### Trade conditions###
        current_price=df.tail(1)
        #print(klines.tail(1))
        current_price=current_price.close
        current_price=current_price.tolist()
        #print(current_price)
        current_price=current_price[-1]
        print('========================')
        print('========================')
        print('current price is : ',current_price)
        print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

####################################### END RSI COMPUTING ##########################################################


####################################### CONDITIONS ACCORDING TO PAIR ##########################################################

        if 'JPY' in string:

            rounding=3
            Long_SL=current_price-0.12
            Long_TP=current_price+0.18
            Short_SL=current_price+0.12
            Short_TP=current_price-0.20

        else:


            rounding=5
            Long_SL=current_price-0.0009
            Long_TP=current_price+0.0020
            Short_SL=current_price+0.0009
            Short_TP=current_price-0.0020



        print('===========================================================')

        print('===========================================================')

        print('===========================================================')




####################################### CONDITIONS ACCORDING TO RSI ##########################################################


        if MA_RSI_OMA_21[-1] < 15:# low velocity of prices so should  buying
            

            if MA_RSI_OMA_21[-1] > RSI_ARRAY_13[-1] and MA_RSI_OMA_137[-1] > RSI_ARRAY_13[-1]:#LONG
                signal='OP_BUY'
                SL=Long_SL
                TP=Long_TP
                place_order = pd.DataFrame({'': [string+','+signal+','+str(SL)+','+str(TP)]})
                
                place_order = place_order.to_csv(path+'/WinPython/Forex Trading Bot/Forex OHLC/Files/LastSignal.csv', header=None, index=None, mode='w', sep=' ',quoting=csv.QUOTE_NONE, quotechar="-",  escapechar="-")
                print('===============================')
                print(string+' pair has opened Long Position')
                print('===============================')
                #time.sleep(5)
                
                

                
                
########################################'LONG POSITION ORDER PLACING'##############################################
                
                
                
                
                MO = MarketOrderRequest(instrument=string[0:3]+'_'+string[3:6], units=10000)
                #print(json.dumps(MO.data, indent=4))
                client = oandapyV20.API(access_token = '60b61afd407c002be3b45984d46a2641-05ed7396fe447ebc7d4ca061a5df5b4c')
                accountID = '101-004-16009898-001'
                r = orders.OrderCreate(accountID, data = MO.data)
                rv = client.request(r)
                print(json.dumps(rv, indent=4))
              


                {
                "timeInForce": "GTC",
                "distance": "0.00500"
                }

                parsed_json = (json.loads(json.dumps(rv, indent=4)))
                k = json.dumps(parsed_json,indent = 4,sort_keys = True)
                data = json.loads(k)
                tradeID = data['orderFillTransaction']['tradeOpened']['tradeID']



                ############################ START STOP Loss ###############################
                ordr_SL = StopLossOrderRequest(tradeID, Long_SL)
                print(json.dumps(ordr_SL.data, indent=4))
                p = orders.OrderCreate(accountID, data=ordr_SL.data)
                rp = client.request(p)
                ############################# END STOP LOSS #################################


            
                ############################ START TAKE PROFIT ###############################
                ordr_TP = TakeProfitOrderRequest(tradeID, (Long_TP))
                print(json.dumps(ordr_TP.data, indent=4))
                o = orders.OrderCreate(accountID, data=ordr_TP.data)
                ro = client.request(o)
                ############################# END TAKE PROFIT #################################

                




###################################### END LONG POSITION ORDER PLACING ###########################################

            else:
                print(string+' does not valid conditions to make trade')




        elif MA_RSI_OMA_21[-1] > 85: # high velocity of prices so should selling

            

            if MA_RSI_OMA_21[-1] < RSI_ARRAY_13[-1] and MA_RSI_OMA_137[-1] < RSI_ARRAY_13[-1]:
                #SHORT:

                signal='OP_SELL'
                SL=Short_SL
                TP=Short_TP
                place_order = pd.DataFrame({'': [string+','+signal+','+str(SL)+','+str(TP),',,,']})
                
                place_order = place_order.to_csv(path+'/WinPython/Forex Trading Bot/Forex OHLC/Files/LastSignal.csv', header=None, index=None, mode='w', sep=' ',quoting=csv.QUOTE_NONE, quotechar="-",  escapechar="-")
                print('===============================')
                print(string+' pair has opened Short Position')

                print('===============================')
                


#########################################'SHORT POSITION ORDER PLACING'############################################



                MO = MarketOrderRequest(instrument=string[0:3]+'_'+string[3:6], units=-100000)
                
                
                client = oandapyV20.API(access_token = '60b61afd407c002be3b45984d46a2641-05ed7396fe447ebc7d4ca061a5df5b4c')
                accountID = '101-004-16009898-001'


                {
                "timeInForce": "GTC",
                "distance": "0.00500"
                }
                #print(json.dumps(MO.data, indent=4))
                t = orders.OrderCreate(accountID, data = MO.data)
                rt = client.request(t)
                print(json.dumps(rt,indent=4))

                parsed_json = (json.loads(json.dumps(rt, indent=4)))
                k = json.dumps(parsed_json,indent = 4 , sort_keys = True)
                data = json.loads(k)
                tradeID = data['orderFillTransaction']['tradeOpened']['tradeID']



                ############################ START STOP Loss ###############################
                ordr_SL = StopLossOrderRequest(tradeID, Short_SL)
                print(json.dumps(ordr_SL.data, indent=4))
                w = orders.OrderCreate(accountID, data=ordr_SL.data)
                rw = client.request(w)
                ############################# END STOP LOSS #################################



                ############################ START TAKE PROFIT ###############################
                ordr_TP = TakeProfitOrderRequest(tradeID, Short_TP)
                print(json.dumps(ordr_TP.data, indent=4))
                q = orders.OrderCreate(accountID, data=ordr_TP.data)
                rq = client.request(q)
                ############################# END TAKE PROFIT #################################

                #---------------------------------------------------------------------------#
                #---------------------------------------------------------------------------#
                #---------------------------------------------------------------------------#




#########################################'END SHORT POSITION ORDER PLACING'############################################

                
            else:
                print(string+' does not valid conditions to make trade')


        else:
            print('-------------------------------')
            print('-------------------------------')
            print(string+' does not valid conditions to make trade')
            print('-------------------------------')
            print('-------------------------------')



    else:
        
        print('all the pair respecting our RSI conditions have been placed ')
        print('\n')
        sec = 2100
        print("Algorithme stop for " + str(sec) + ' secondes')
        time.sleep(sec)
        logs=[]
        logs1=[]
        
        








