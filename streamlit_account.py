import pandas as pd
import streamlit as st
import shioaji as sj
from datetime import datetime

#accountDict={"edward":["6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
#            "edward_wife":["Gvd6pFwFncAHWZgg5jVNEFVBawS2EVEQPqrnwJQ7Jpeo","6nnNUWxuL66eCPR17MGxvgPB8djXPYjCsAENR1KgUycr"],
#            "ellis":["7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
#            "chun":["2oMvtudzAFkH1JeryThNNLYpGuGdG2QDuwuqrevdpXQz","48PtSPc9uJ3JzobmfqPwMsQxUGCuFzMApEJ3XjTpDWRf"],
#            "big":["3MKdCLdZoEq78zYbbRJziUSrzYdxYYGhqEDwGfbnAF3x","KUqwpdqqydh1BLAp4yo7dJdb9zciZzTRTuRok1KdwXd"]}


#accountDict={"edward":["6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
#            "edward_wife":["Gvd6pFwFncAHWZgg5jVNEFVBawS2EVEQPqrnwJQ7Jpeo","6nnNUWxuL66eCPR17MGxvgPB8djXPYjCsAENR1KgUycr"],
#            "ellis":["7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
#            "big":["3MKdCLdZoEq78zYbbRJziUSrzYdxYYGhqEDwGfbnAF3x","KUqwpdqqydh1BLAp4yo7dJdb9zciZzTRTuRok1KdwXd"]}

#accountDict={"edward":["6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
#            "edward_wife":["Gvd6pFwFncAHWZgg5jVNEFVBawS2EVEQPqrnwJQ7Jpeo","6nnNUWxuL66eCPR17MGxvgPB8djXPYjCsAENR1KgUycr"],
#            "ellis":["7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"]}

accountApiDict={"edward":["王伯涵","6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
            "ellis":["張育哲","7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
            "jiner":["黃宣璟","9hc8z9MSiT1YYaKXwgAMod28f5kA471fPmUuabNVMFbm","ECnwFfA1be6d675dSWCCpE223p2MMeoy4An3x4fTfdwh"],
            "jkken":["鄭旭智","9eHupB3zmvwVcMJtAueVSQ5pbW4qwtgMNEUXK677zk1b","3HDvRocNpgpiKuiVVyFdDEQDdTUK3dFTYmtco6YgNX3n"]}

accountMarginDict={"edward":["王伯涵",150000,"6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
            "ellis":["張育哲",150000,"7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
            "jiner":["黃宣璟",150000,"9hc8z9MSiT1YYaKXwgAMod28f5kA471fPmUuabNVMFbm","ECnwFfA1be6d675dSWCCpE223p2MMeoy4An3x4fTfdwh"],
            "jkken":["鄭旭智",150000,"9eHupB3zmvwVcMJtAueVSQ5pbW4qwtgMNEUXK677zk1b","3HDvRocNpgpiKuiVVyFdDEQDdTUK3dFTYmtco6YgNX3n"]}



def query_profit():
    
    api = sj.Shioaji(simulation=False) #模擬模式

    nameList=[]
    commodityList=[]
    quantityList=[]
    pnlList=[]
    
    for key,value in accountMarginDict.items():

        api.login(
            api_key=value[2], 
            secret_key=value[3])

        profitloss = api.margin(api.futopt_account)

        
        nameList.append(value[0])
        pnlList.append(profitloss.equity_amount-value[1])
    
        # api.logout()
    
    df = pd.DataFrame(
        {
            "姓名": nameList,
            "損益": pnlList,
        }
    )
    
    st.dataframe(df,hide_index=True)
     
    #st.write("aabbcc")
    
    
def query_position():

    api = sj.Shioaji(simulation=False) #模擬模式

    nameList=[]
    commodityList=[]
    directionList=[]
    contractList=[]
    priceList=[]
    pnlList=[]
    
    for key,value in accountApiDict.items():

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
		            
        # api.logout()
    
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

st.title('客戶期貨查詢')
st.button('客戶部位', on_click=query_position)
st.button('客戶獲利', on_click=query_profit)
