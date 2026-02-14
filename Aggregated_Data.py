import os
import pandas as pd
import json 
## Aggregated- Transaction Data
path="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\aggregated\\transaction\\country\\india\\state\\"
Agg_state_list_T=os.listdir(path)
Agg_state_list_T

## Extract data's to a dataframe
clm={'State':[],'Year':[],'Quarter':[],'Transaction_type':[],'Transaction_count':[],'Transaction_amount':[]}
for i in Agg_state_list_T:
    p_i=path+i+"\\" ## i is first iteration which is state
    Agg_yr_T=os.listdir(p_i)
    for j in Agg_yr_T:
        p_j=p_i+j+"\\" ## j is second iteration which is adding year after state
        Agg_Qtr_T=os.listdir(p_j)
        for k in Agg_Qtr_T:
            p_k=p_j+k  ## this points the final data
            Data=open(p_k,'r')
            DT=json.load(Data)
            try:
             for z in DT['data']['transactionData']:
                Name=z['name']
                count=z['paymentInstruments'][0]['count']
                amount=z['paymentInstruments'][0]['amount']
                clm['Transaction_type'].append(Name)
                clm['Transaction_count'].append(count)
                clm['Transaction_amount'].append(amount)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quarter'].append(int(k.strip('.json')))
            except:
                pass
## Convert into dataframes
Agg_Transaction=pd.DataFrame(clm)
Agg_Transaction.to_csv("Agg_Transaction.csv", index=False)

##Aggregated- User Data
path1="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\aggregated\\user\\country\\india\\state\\"
Agg_state_list_U=os.listdir(path1)
Agg_state_list_U
## Extract data's to a dataframe
clm1={'State':[],'Year':[],'Quarter':[],'User_Brand':[],'User_count':[],'Device_perc':[]}
for i in Agg_state_list_U:
    p_i1=path1+i+"\\" ## i is first iteration which is state
    Agg_yr_U=os.listdir(p_i1)
    for j in Agg_yr_U:
        p_j1=p_i1+j+"\\" ## j is second iteration which is adding year after state
        Agg_Qtr_U=os.listdir(p_j1)
        for k in Agg_Qtr_U:
            p_k1=p_j1+k  ## this points the final data
            Data1=open(p_k1,'r')
            DU=json.load(Data1)
            try:
             for z in DU['data'].get('usersByDevice') or []:
                Brand=z['brand']
                count=z['count']
                Percentage=z['percentage']
                clm1['User_Brand'].append(Brand)
                clm1['User_count'].append(count)
                clm1['Device_perc'].append(Percentage)
                clm1['State'].append(i)
                clm1['Year'].append(j)
                clm1['Quarter'].append(int(k.strip('.json')))
            except:
               pass
## Convert into dataframes
Agg_User=pd.DataFrame(clm1)
Agg_User.to_csv("Aggregated_User.csv",index=False)

##Aggregated - Insurance Data

path2="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\aggregated\\insurance\\country\\india\\state\\"
Agg_state_list_I=os.listdir(path2)
Agg_state_list_I
## Extract data's to a dataframe
clm2={'State':[],'Year':[],'Quarter':[],'Ins_Name':[],'Ins_count':[],'Ins_amount':[]}
for i in Agg_state_list_I:
    p_i2=path2+i+"\\" ## i is first iteration which is state
    Agg_yr_I=os.listdir(p_i2)
    for j in Agg_yr_I:
        p_j2=p_i2+j+"\\" ## j is second iteration which is adding year after state
        Agg_Qtr_I=os.listdir(p_j2)
        for k in Agg_Qtr_I:
            p_k2=p_j2+k  ## this points the final data
            Data2=open(p_k2,'r')
            DI=json.load(Data2)
            try:
             for z in DI['data']['transactionData']:
                Name=z['name']
                count=z['paymentInstruments'][0]['count']
                amount=z['paymentInstruments'][0]['amount']
                clm2['Ins_Name'].append(Name)
                clm2['Ins_count'].append(count)
                clm2['Ins_amount'].append(amount)
                clm2['State'].append(i)
                clm2['Year'].append(j)
                clm2['Quarter'].append(int(k.strip('.json')))
            except:
               pass
## Convert into dataframes
Agg_Insurance=pd.DataFrame(clm2)
Agg_Insurance.to_csv("Aggregated_Insurance.csv",index=False)





