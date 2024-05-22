import pandas as pd
import streamlit as st
import shioaji as sj
from datetime import datetime


edwardMargin=150000
ellisMargin=150000
jinerMargin=150000
jkkenMargin=150000

accountApiDict={"edward":["王伯涵","6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
            "ellis":["張育哲","7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
            "jiner":["黃宣璟","9hc8z9MSiT1YYaKXwgAMod28f5kA471fPmUuabNVMFbm","ECnwFfA1be6d675dSWCCpE223p2MMeoy4An3x4fTfdwh"],
            "jkken":["鄭旭智","9eHupB3zmvwVcMJtAueVSQ5pbW4qwtgMNEUXK677zk1b","3HDvRocNpgpiKuiVVyFdDEQDdTUK3dFTYmtco6YgNX3n"]}

accountMarginDict={"edward":["王伯涵",edwardMargin,"6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
            "ellis":["張育哲",ellisMargin,"7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
            "jiner":["黃宣璟",jinerMargin,"9hc8z9MSiT1YYaKXwgAMod28f5kA471fPmUuabNVMFbm","ECnwFfA1be6d675dSWCCpE223p2MMeoy4An3x4fTfdwh"],
            "jkken":["鄭旭智",jkkenMargin,"9eHupB3zmvwVcMJtAueVSQ5pbW4qwtgMNEUXK677zk1b","3HDvRocNpgpiKuiVVyFdDEQDdTUK3dFTYmtco6YgNX3n"]}



def query_profit():
    
    api=None
    nameList=[]
    profitList=[]
    receiveList=[]
    
    for key,value in accountMarginDict.items():

        api = sj.Shioaji(simulation=False) #模擬模式
        api.login(
            api_key=value[2], 
            secret_key=value[3])

        profitloss = api.margin(api.futopt_account)

        nameList.append(value[0])
        profitList.append(profitloss.equity_amount-value[1])

        if key=="edward":
            receiveList.append(0)
        else:
            receiveList.append((profitloss.equity_amount-value[1])*0.4)
		
        api.logout()
    
    df = pd.DataFrame(
        {
            "姓名": nameList,
            "損益": profitList,
            "預期應收": receiveList,
        }
    )

    profitSum=0
    receiveSum=0
    
    for idx,data in enumerate(profitList):
        if idx!=0:
            profitSum+=data

    for idx,data in enumerate(receiveList):
        if idx!=0:
            receiveSum+=data
            
    st.dataframe(df,hide_index=True)
    st.write("總獲利 : {0}".format(profitSum))
    st.write("預期總應收 : {0}".format(receiveSum))
    st.write("edward總應收 : {0}".format(receiveSum*0.3))
    st.write("york總應收 : {0}".format(receiveSum*0.3))
    st.write("cd總應收 : {0}".format(receiveSum*0.4))
    
def query_position():
	
    api=None
    nameList=[]
    commodityList=[]
    directionList=[]
    contractList=[]
    priceList=[]
    pnlList=[]
    
    for key,value in accountApiDict.items():

        api = sj.Shioaji(simulation=False) #模擬模式
        
        api.login(
            api_key=value[1], 
            secret_key=value[2])
        
        
        positions = api.list_positions(api.futopt_account)
        
        for data in positions:

            nameList.append(value[0])
            commodityList.append(data.code)
            directionList.append(data.direction.value)
            contractList.append(data.quantity)
            priceList.append(data.price)
            pnlList.append(data.pnl)
		            
        api.logout()
    
    if not (nameList and commodityList and directionList and contractList and priceList and pnlList):
        st.write("沒有部位")
    else:
        df = pd.DataFrame(
            {
                "姓名": nameList,
                "商品": commodityList,
                "方向": directionList,
                "口數": contractList,
                "價格": priceList,
                "損益": pnlList,
            }
        )
    
        st.dataframe(df,hide_index=True)

def customer_equity():

    api=None
    nameList=[]
    equityList=[]
    
    for key,value in accountApiDict.items():

        api = sj.Shioaji(simulation=False) #模擬模式
        api.login(
            api_key=value[1], 
            secret_key=value[2])

        equityData = api.margin(api.futopt_account)

        nameList.append(value[0])
        equityList.append(equityData.equity_amount)

        api.logout()
    
    df = pd.DataFrame(
        {
            "姓名": nameList,
            "權益總值": equityList,
        }
    )
    
st.title('客戶期貨查詢')
st.button('客戶部位', on_click=query_position)
st.button('客戶獲利', on_click=query_profit)
st.button('客戶權益總值', on_click=customer_equity)
