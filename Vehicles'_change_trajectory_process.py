import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
datain=pd.read_csv('./lankershim_data_rectify_20220322.csv')
data=datain[['Vehicle_ID','Frame_ID','v_Vel','v_Acc','Space_Headway','Time_Headway','Lane_ID']]
data=data.sort_values(by=["Vehicle_ID","Frame_ID"],ascending=True)
# data=data.drop_duplicates(subset=['Global_Time'], keep='first', inplace=False)
Vehicle_id=data['Vehicle_ID'].unique()
data_visiable=data
data_visiable['Lane change']=data_visiable['Lane_ID'].shift(1)
# pd.set_option('display.max_columns', None)
data_visiable['Lane change']=data_visiable['Lane change']-data_visiable['Lane_ID']#错位相减
data_s = data_visiable.fillna(0)#
print(data_s)#遍历增加各车辆的变道信息
change_df = pd.DataFrame(columns=['ID','start','end'])
c=datain.columns
select_data=pd.DataFrame(columns=c)
select_data['time']=[]
print(select_data)
for id in Vehicle_id:
    print(id)
    data_vehicle=data_s[data_s['Vehicle_ID']==id]
    time_change=data_vehicle[data_vehicle['Lane change']!=0]
    array=time_change['Frame_ID'].unique()
    array_time=data_vehicle['Frame_ID'].unique()
    for i in array:
        a=i-50
        b=i+50
        if np.any(array_time == a):
            a = a
        else:
            a =np.min(array_time)
        if np.any(array_time == b):
            b = b
        else:
            b =np.max(array_time)
        change_df= change_df.append({'ID':id,'start':a,'end':b},ignore_index=True)

change_id=change_df['ID'].unique()
for id in change_id:
    change_vehicle_data=datain[datain['Vehicle_ID']==id]
    num=change_df[change_df['ID']==id]
    print(id)
    for p in range(0, len(num)):
        s=num.iloc[p]['start']
        e=num.iloc[p]['end']
        data_select=change_vehicle_data[(change_vehicle_data['Frame_ID']>=s) & (change_vehicle_data['Frame_ID']<=e)].copy()
        data_select['time'] = s
        select_data=select_data.append(data_select)

select_data.to_csv('./vehicle_change_trajectory_data20220322.csv')