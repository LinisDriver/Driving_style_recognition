import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
datain=pd.read_csv('./lankershim_data_rectify_20220322.csv')
data=datain[['Vehicle_ID','Frame_ID','v_Vel','v_Acc','Space_Headway','Time_Headway']]
data=data.sort_values(by=["Vehicle_ID","Frame_ID"],ascending=True)
# data=data.drop_duplicates(subset=['Global_Time'], keep='first', inplace=False)
Vehicle_id=data['Vehicle_ID'].unique()
data_visiable=data
data_visiable['brake']=data_visiable['v_Vel'].shift(1)
data_visiable['start']=data_visiable['v_Vel'].shift(-1)
# pd.set_option('display.max_columns', None)
data_visiable['start']=data_visiable['start']-data_visiable['v_Vel']
data_visiable['brake']=data_visiable['brake']-data_visiable['v_Vel']#错位相减
data_s = data_visiable.fillna(0)#
print(data_s)#遍历增加各车辆的启动和制动信息

change_df_start = pd.DataFrame(columns=['ID','start','end'])
change_df_brake = pd.DataFrame(columns=['ID','start','end'])

c=datain.columns #['Vehicle_ID','Frame_ID','v_Vel','v_Acc','Space_Headway','Time_Headway']
select_data_start=pd.DataFrame(columns=c)
select_data_brake=pd.DataFrame(columns=c)
select_data_start['time']=[]
select_data_brake['time']=[]

# print(select_data)

for id in Vehicle_id:
    print(id)
    data_vehicle=data_s[data_s['Vehicle_ID']==id]
    time_change_start=data_vehicle[(data_vehicle['v_Vel']==0) & (data_vehicle['start']>0)]
    time_change_brake=data_vehicle[(data_vehicle['v_Vel'] == 0) & (data_vehicle['brake']>0)]

    array_start=time_change_start['Frame_ID'].unique()
    array_brake=time_change_brake['Frame_ID'].unique()

    array_time=data_vehicle['Frame_ID'].unique()

    for i in array_start:
        a=i+37
        b=i
        if np.any(array_time == a):
            a = a
        else:
            a =np.max(array_time)

        change_df_start= change_df_start.append({'ID':id,'start':b,'end':a},ignore_index=True)
    for i in array_brake:
        a = i - 37
        b = i
        if np.any(array_time == a):
            a = a
        else:
            a = np.min(array_time)

        change_df_brake = change_df_brake.append({'ID': id, 'start': a, 'end': b}, ignore_index=True)


start_id=change_df_start['ID'].unique()
for id in start_id:
    start_vehicle_data=datain[datain['Vehicle_ID']==id]
    num=change_df_start[change_df_start['ID']==id]
    print(id)
    for p in range(0, len(num)):
        s=num.iloc[p]['start']
        e=num.iloc[p]['end']
        data_select=start_vehicle_data[(start_vehicle_data['Frame_ID']>=s) & (start_vehicle_data['Frame_ID']<=e)].copy()
        data_select['time'] = s
        select_data_start=select_data_start.append(data_select)

brake_id=change_df_start['ID'].unique()
for id in brake_id:
    brake_vehicle_data=datain[datain['Vehicle_ID']==id]
    num=change_df_brake[change_df_brake['ID']==id]
    print(id)
    for p in range(0, len(num)):
        s=num.iloc[p]['start']
        e=num.iloc[p]['end']
        data_select=brake_vehicle_data[(brake_vehicle_data['Frame_ID']>=s) & (brake_vehicle_data['Frame_ID']<=e)].copy()
        data_select['time'] = s
        select_data_brake=select_data_brake.append(data_select)



select_data_start.to_csv('./select_data_start.csv')
select_data_brake.to_csv('./select_data_brake.csv')
