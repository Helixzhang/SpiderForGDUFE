import pandas as pd
import datetime
data = pd.read_csv('class.csv',names = ['week','day','num','class','teacher','weeks','room','class_num'])
new = data.groupby('week').apply(lambda x: x.sort_values('day', ascending=True)).set_index('week')

start = datetime.datetime.strptime('2021-3-8', '%Y-%m-%d')
day = datetime.timedelta(days=1)
week = datetime.timedelta(weeks=1)
new = new.reset_index()
csvfile = pd.DataFrame(columns=['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location','Private'])
class_start = {1:'08:00',2:'10:00',3:'14:10',4:'16:10',5:'18:40',6:'20:30'}
class_end = {1:'09:40',2:'11:40',3:'15:50',4:'17:50',5:'20:20',6:'21:15'}
for i,_class in new.iterrows():
    class_tmp = {'Subject':'','Start Date':'','Start Time':'','End Date':'','End Time':'','All Day Event':False,'Description':'','Location':'','Private':True}
    class_tmp['Subject'] = _class['class']
    class_tmp['Start Date'] = start +(_class['week']-1)*week +(_class['day']-1)*day
    class_tmp['End Date'] = start +(_class['week']-1)*week +(_class['day']-1)*day
    class_tmp['Start Time'] = class_start[_class['num']]
    class_tmp['End Time'] = class_end[_class['num']]
    class_tmp['Description'] = _class['teacher']+'\n'+_class['weeks']+'\n'+_class['class_num']
    class_tmp['Location'] = _class['room']
    csvfile = csvfile.append(class_tmp,ignore_index=True)
csvfile.to_csv('calendar.csv')