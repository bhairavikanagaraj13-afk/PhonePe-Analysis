import os
import pandas as pd
import json 
## Top- Transaction Data
path="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\top\\transaction\\country\\india\\state\\"
top_state_list_T=os.listdir(path)
top_state_list_T

## Extract data's to a dataframe
ttd={'State':[],'Year':[],'Quarter':[],'Level_top_T':[],'Entity_name_top_T':[],'top_count_T':[],'top_amount_T':[]}
for i in top_state_list_T:
    p_i=path+i+"\\" ## i is first iteration which is state
    top_yr_T=os.listdir(p_i)
    for j in top_yr_T:
        p_j=p_i+j+"\\" ## j is second iteration which is adding year after state
        top_Qtr_T=os.listdir(p_j)
        for k in top_Qtr_T:
            p_k=p_j+k  ## this points the final data
            Data=open(p_k,'r')
            TT=json.load(Data)
            for z in TT['data'].get('states') or []:## for state
                ttd['Level_top_T'].append('states')
                ttd['Entity_name_top_T'].append(z['entityName'])
                ttd['top_count_T'].append(z['metric']['count'])
                ttd['top_amount_T'].append(z['metric']['amount'])
                ttd['State'].append(i)
                ttd['Year'].append(j)
                ttd['Quarter'].append(int(k.strip('.json')))
            for z in TT['data'].get('districts') or []: ## for districts
                ttd['State'].append(i)
                ttd['Year'].append(j)
                ttd['Quarter'].append(int(k.strip('.json')))
                ttd['Level_top_T'].append('district')
                ttd['Entity_name_top_T'].append(z['entityName'])
                ttd['top_count_T'].append(z['metric']['count'])
                ttd['top_amount_T'].append(z['metric']['amount'])
            for z in TT['data'].get('pincodes') or []: ## for pincode
                ttd['State'].append(i)
                ttd['Year'].append(j)
                ttd['Quarter'].append(int(k.strip('.json')))
                ttd['Level_top_T'].append('pincodes')
                ttd['Entity_name_top_T'].append(z['entityName'])
                ttd['top_count_T'].append(z['metric']['count'])
                ttd['top_amount_T'].append(z['metric']['amount'])
## Convert into dataframes
Top_Trans=pd.DataFrame(ttd)
Top_Trans.to_csv("Top_Transaction.csv",index=False)

##Top User Data
path1="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\top\\user\\country\\india\\state\\"
top_state_list_U=os.listdir(path1)
top_state_list_U
## Extract data's to a dataframe
ttd1={'State':[],'Year':[],'Quarter':[],'Level_top_U':[],'Entity_name_top_U':[],'registered_Users':[]}
for i in top_state_list_U:
    p_i1=path1+i+"\\" ## i is first iteration which is state
    top_yr_U=os.listdir(p_i1)
    for j in top_yr_U:
        p_j1=p_i1+j+"\\" ## j is second iteration which is adding year after state
        top_Qtr_U=os.listdir(p_j1)
        for k in top_Qtr_U:
            p_k1=p_j1+k  ## this points the final data
            Data1=open(p_k1,'r')
            TU=json.load(Data1)
            for z in TU['data'].get('states') or []:## for state
                ttd1['Level_top_U'].append('states')
                ttd1['Entity_name_top_U'].append(z['name'])
                ttd1['registered_Users'].append(z['registeredUsers'])
                ttd1['State'].append(i)
                ttd1['Year'].append(j)
                ttd1['Quarter'].append(int(k.strip('.json')))
            for z in TU['data'].get('districts') or []: ## for districts
                ttd1['State'].append(i)
                ttd1['Year'].append(j)
                ttd1['Quarter'].append(int(k.strip('.json')))
                ttd1['Level_top_U'].append('district')
                ttd1['Entity_name_top_U'].append(z['name'])
                ttd1['registered_Users'].append(z['registeredUsers'])
                
            for z in TU['data'].get('pincodes') or []: ## for pincode
                ttd1['State'].append(i)
                ttd1['Year'].append(j)
                ttd1['Quarter'].append(int(k.strip('.json')))
                ttd1['Level_top_U'].append('pincodes')
                ttd1['Entity_name_top_U'].append(z['name'])
                ttd1['registered_Users'].append(z['registeredUsers'])
## Convert into dataframes
Top_User=pd.DataFrame(ttd1)
Top_User.to_csv("Top_user.csv",index=False)

## Top_Insurance
path2="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\top\\insurance\\country\\india\\state\\"
top_state_list_I=os.listdir(path2)
top_state_list_I

## Extract data's to a dataframe
ttd2={'State':[],'Year':[],'Quarter':[],'Level_top_I':[],'Entity_name_top_I':[],'top_count_I':[],'top_amount_I':[]}
for i in top_state_list_I:
    p_i2=path2+i+"\\" ## i is first iteration which is state
    top_yr_I=os.listdir(p_i2)
    for j in top_yr_I:
        p_j2=p_i2+j+"\\" ## j is second iteration which is adding year after state
        top_Qtr_I=os.listdir(p_j2)
        for k in top_Qtr_I:
            p_k2=p_j2+k  ## this points the final data
            Data2=open(p_k2,'r')
            TI=json.load(Data2)
            for z in TI['data'].get('states') or []:## for state
                ttd2['Level_top_I'].append('states')
                ttd2['Entity_name_top_I'].append(z['entityName'])
                ttd2['top_count_I'].append(z['metric']['count'])
                ttd2['top_amount_I'].append(z['metric']['amount'])
                ttd2['State'].append(i)
                ttd2['Year'].append(j)
                ttd2['Quarter'].append(int(k.strip('.json')))
            for z in TI['data'].get('districts') or []: ## for districts
                ttd2['State'].append(i)
                ttd2['Year'].append(j)
                ttd2['Quarter'].append(int(k.strip('.json')))
                ttd2['Level_top_I'].append('district')
                ttd2['Entity_name_top_I'].append(z['entityName'])
                ttd2['top_count_I'].append(z['metric']['count'])
                ttd2['top_amount_I'].append(z['metric']['amount'])
            for z in TI['data'].get('pincodes') or []: ## for pincode
                ttd2['State'].append(i)
                ttd2['Year'].append(j)
                ttd2['Quarter'].append(int(k.strip('.json')))
                ttd2['Level_top_I'].append('pincodes')
                ttd2['Entity_name_top_I'].append(z['entityName'])
                ttd2['top_count_I'].append(z['metric']['count'])
                ttd2['top_amount_I'].append(z['metric']['amount'])
## Convert into dataframes
Top_Ins=pd.DataFrame(ttd2)
Top_Ins.to_csv("Top_insurance.csv",index=False)

