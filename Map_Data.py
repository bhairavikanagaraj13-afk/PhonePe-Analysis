import os
import pandas as pd
import json 
## Map- Transaction Data
path="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\map\\transaction\\hover\\country\\india\\state\\"
map_state_list_T=os.listdir(path)
map_state_list_T

## Extract data's to a dataframe
mtd={'State':[],'Year':[],'Quarter':[],'District_name_T':[],'DIS_T_count':[],'DIS_T_amount':[]}
for i in map_state_list_T:
    p_i=path+i+"\\" ## i is first iteration which is state
    map_yr_T=os.listdir(p_i)
    for j in map_yr_T:
        p_j=p_i+j+"\\" ## j is second iteration which is adding year after state
        map_Qtr_T=os.listdir(p_j)
        for k in map_Qtr_T:
            p_k=p_j+k  ## this points the final data
            Data=open(p_k,'r')
            MT=json.load(Data)
            for z in MT['data']['hoverDataList']:
                Name=z['name']
                count=z['metric'][0]['count']
                amount=z['metric'][0]['amount']
                mtd['District_name_T'].append(Name)
                mtd['DIS_T_count'].append(count)
                mtd['DIS_T_amount'].append(amount)
                mtd['State'].append(i)
                mtd['Year'].append(j)
                mtd['Quarter'].append(int(k.strip('.json')))
## Convert into dataframes
Map_Trans=pd.DataFrame(mtd)
Map_Trans.to_csv("Map_transaction.csv",index=False)

##Map- User Data
path1="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\map\\user\\hover\\country\\india\\state\\"
Map_state_list_U=os.listdir(path1)
Map_state_list_U
## Extract data's to a dataframe
mtd1={'State':[],'Year':[],'Quarter':[],'User_district':[],'registered_users':[],'Appopens_U':[]}
for i in Map_state_list_U:
    p_i1=path1+i+"\\" ## i is first iteration which is state
    map_yr_U=os.listdir(p_i1)
    for j in map_yr_U:
        p_j1=p_i1+j+"\\" ## j is second iteration which is adding year after state
        map_Qtr_U=os.listdir(p_j1)
        for k in map_Qtr_U:
            p_k1=p_j1+k  ## this points the final data
            Data1=open(p_k1,'r')
            MU=json.load(Data1)
            for z,v in MU['data'].get('hoverData').items():
                Dis_name=z
                Res_User=v['registeredUsers']
                Appopen=v['appOpens']
                mtd1['User_district'].append(Dis_name)
                mtd1['registered_users'].append(Res_User)
                mtd1['Appopens_U'].append(Appopen)
                mtd1['State'].append(i)
                mtd1['Year'].append(j)
                mtd1['Quarter'].append(int(k.strip('.json')))
## Convert into dataframes
Map_User=pd.DataFrame(mtd1)
Map_User.to_csv("Map_user.csv",index=False)


##Map - Insurance Data

path2="C:\\Users\\Bhairavi\\OneDrive\\GUVI- DSA\\Projects\\Project 1 - Phonepe\\ExtractedDATA\\data\\map\\insurance\\hover\\country\\india\\state\\"
Map_state_list_I=os.listdir(path2)
Map_state_list_I
## Extract data's to a dataframe
mtd2={'State':[],'Year':[],'Quarter':[],'Ins_Dis_name_M':[],'Ins_count_M':[],'Ins_amount_M':[]}
for i in Map_state_list_I:
    p_i2=path2+i+"\\" ## i is first iteration which is state
    map_yr_I=os.listdir(p_i2)
    for j in map_yr_I:
        p_j2=p_i2+j+"\\" ## j is second iteration which is adding year after state
        map_Qtr_I=os.listdir(p_j2)
        for k in map_Qtr_I:
            p_k2=p_j2+k  ## this points the final data
            Data2=open(p_k2,'r')
            MI=json.load(Data2)
            for z in MI['data']['hoverDataList']:
                Name=z['name']
                count=z['metric'][0]['count']
                amount=z['metric'][0]['amount']
                mtd2['Ins_Dis_name_M'].append(Name)
                mtd2['Ins_count_M'].append(count)
                mtd2['Ins_amount_M'].append(amount)
                mtd2['State'].append(i)
                mtd2['Year'].append(j)
                mtd2['Quarter'].append(int(k.strip('.json')))
## Convert into dataframes
Map_Insurance=pd.DataFrame(mtd2)
Map_Insurance.to_csv("Map_Insurance.csv",index=False)
