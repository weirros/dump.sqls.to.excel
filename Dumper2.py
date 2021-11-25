# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 13:28:48 2021

@author: David
"""

import PySimpleGUI as sg
import sys
import pickle
import base64
import json
import pandas as pd
import time,datetime
import sqlalchemy

sg.theme('LightBlue')

tipofdb = '''
填写一个字典，用{}括号包裹；
'EOPKH800':'mssql+pymssql://sa:Compass2008@192.168.118.85:1433/EOPKH800'
如果有多条记录，用逗号分隔；
分别是数据库连接名，可以自定义，方便判断和识别；
数据库连接字符串，带有驱动+用户名密码+服务器地址+端口+库名字；目前在MSSQL测试通过
'''
tipofsql = '''
SQL字符串，用#日期参数S1#代替日期变量，目前设置有两个变量可用；
分别是#日期参数S1#，#日期参数S2#
运行时会用S1，S2参数迭代；
'''



def get_settings():
    
    try:
    
        with open ("Dumper.ini", 'rb') as f:
            bs = pickle.load(f)
            bbs = str(base64.b64decode(bs), "utf-8")
            settings=json.loads(bbs)
    except:
        
        pass
    
    return settings

settings=get_settings()

def loadingdefault(settings,window):
    
    if settings['D1']==True:
        window['_z1_'].update(visible=True)
        window['_frd_'].update(visible=True)
        window['_z3_'].update(visible=True)
    if settings['D1']==False:
        window['_z1_'].update(visible=False)
        window['_frd_'].update(visible=False)
        window['_z3_'].update(visible=False)
    if settings['D2']==True:
        window['_z4_'].update(visible=True)
        window['_tod_'].update(visible=True)
        window['_z2_'].update(visible=True)    
    
    if settings['D2']==False:
        window['_z4_'].update(visible=False)
        window['_tod_'].update(visible=False)
        window['_z2_'].update(visible=False) 
        
    
def getdb(values):

    if  len(values['_db_'])<10:
        print('数据库设置有误~请检查数据库设计')
    else:
        
        v1=eval(values['_db_'])
        
        #db=json.loads(v1)
        #print(v1)
        # for i in v1:
        #     print(i,v1[i])
        
        return v1  #数据库集合
    
def dbrun(db,dburl,sql):
    
    try:
        
        intime= time.strftime("%Y-%m-%d %H:%M:%S")
        engine = sqlalchemy.create_engine(dburl)
        data_sql=pd.read_sql(sql,engine)
        
        print (db,data_sql.shape[0],' 行s ',intime,' >> ',time.strftime("%Y-%m-%d %H:%M:%S"))
        return True,data_sql
    
    except:
        
        print(db,'连接失败~')
        return False,None
        

    
        


menu_def = [['系统', ['设置', '关于' ]]]

layout_tout = [
    
    [sg.Menu(menu_def, tearoff=False, pad=(20,1))],
     
    [sg.Text('选择要保存的文件夹，输入要保存的文件名，例如A001.xlsx') ], 
    
    [sg.Input(settings['file'],size=(10,1),key='_sk0_',text_color='black',font='Any 18'),sg.Text('在'),
     
      sg.Input(settings['path'],size=(30,1),key='_sk1_',text_color='black',font='Any 18'),sg.FolderBrowse('选择'),sg.Button('保存为默认',key='_save2_')],
    
    [sg.Text('自(含)',key='_z1_'),
     #sg.Input('-',size=(20, 1),text_color='black',readonly=True,key='_frd_', justification='c',enable_events=True),
     sg.In('-',readonly=True, size=(20, 1),key='_frd_',enable_events=True, justification='c', text_color='#0000CD'),  
     
     sg.CalendarButton('S1', size=(10, 1),key='_z3_')],
     [sg.Text('至(含)',key='_z4_'),
      sg.In('-',readonly=True, size=(20, 1),key='_tod_',enable_events=True, justification='c', text_color='#0000CD'),
     sg.CalendarButton('S2', size=(10, 1),key='_z2_')],
    
  
    [sg.Text('')],

    
    [ sg.B('跑路',size=(200,2),button_color=('white', 'red'), key='-Run-')],
    
     [sg.Text('以下是日志输出，如有必要请复制到剪贴板') ], 
    
    [sg.Output(size=(100, 40))],
    
    ]


layout_setting = [[sg.Text('以下设置数据库连接'),sg.Button('测试连接',key='_checkdb_')],
                  [sg.Multiline(settings['DB'],size=(100,20),key='_db_',tooltip=tipofdb) ],
                  
                  [sg.Text('以下设置在每个库里执行的SQL语句'),
                   sg.Checkbox('日期参数S1', default=settings['D1'],key='_enableDate1_',size=(11,1),background_color='#FFCC33',text_color='#000000',enable_events=True),
                   sg.Checkbox('日期参数S2', default=settings['D2'],key='_enableDate2_',size=(11,1),background_color='#FFCC33',text_color='#000000',enable_events=True),
                   sg.Button('带参数预览SQL',key='_budsql_',size=(15,1),button_color=('black', '#FFCC33'))
                   ],
                  
                  
                  [sg.Multiline(settings['Sqlstrings'],size=(100,20),key='_sqlstring_',tooltip=tipofsql) ],
                  
                  [sg.Text('以下设置解锁码')],
                  [sg.Input(settings['lockkey'],size=(30,1),key='_lock_') ],
                  [sg.Button('保存并加锁',key='_savelock_',size=(100,2),button_color=('white', 'red'))],
                  
                  
                  
                  ]

tabgrp = [[sg.TabGroup([[sg.Tab('运行', layout_tout,key='_M_'),
                         sg.Tab('设置', layout_setting,visible=False,key='_S_')
                         
                             ]], 
                           

                           enable_events=True,

                           
                           border_width=0
                           
                           )           
               ]] 


 
window =sg.Window("Dumper",tabgrp, location=(400, 60),size=(700,900), finalize=True)

loadingdefault(settings,window)

def main():
    
    while True:
        event, values = window.Read()       
            
        if event == '退出' or event == sg.WIN_CLOSED:
    
            window.close()
            sys.exit(0)
            
        else:
            #print(event,values)
            if event=='设置':                
                text1 = sg.popup_get_text('请输入解锁码',password_char='*')
                print(text1)
                if text1== settings['lockkey'] or text1== 'aaaaaaaa':                  #万能密码8个a
                    window['_S_'].update(visible=True)
                    #window['_S_'].update(disabled=False)
                    window['_S_'].select()
                   
                    
                    
            if event=='关于':
                

                text = '''Dumper
                垃圾车，专门把SQL在每个数据库执行并导出的工具；
                
                
                '''
                sg.PopupScrolled(text,size=(10,10),title='关于',auto_close=True,auto_close_duration=3)
                
            if event=='_savelock_' or event=='_save2_':
                
                settings1 = {
                    
                    "D1":values['_enableDate1_'],
                    "D2":values['_enableDate2_'],
                    
                    "file":values['_sk0_'],
                    "path":values['_sk1_'],

                    "DB":values['_db_'],
                    "Sqlstrings":values['_sqlstring_'],
                    
                    "lockkey":values['_lock_']
                    
                    
                    }
                
                settings2 = json.dumps(settings1)
                settings3 = base64.b64encode(settings2.encode("utf-8")) 
                
                
                with open ("Dumper.ini", 'wb') as f:
    
                    pickle.dump(settings3, f)
            
                sg.popup_ok('已保存~')
                
            if event=='_enableDate1_':
                
                settings['D1']=values['_enableDate1_']
                loadingdefault(settings,window)
            
            if event=='_enableDate2_':
                
                settings['D2']=values['_enableDate2_']
                loadingdefault(settings,window)
            
            if event == '_checkdb_':
                
                db = getdb(values)
                sql= 'select 1'
                for i in db:
                    dbrun(i,db[i],sql)
                
                sg.PopupTimed('一检测，请查看日志窗口',auto_close=True,auto_close_duration=3)
                
                window['_M_'].select() 
                
            if event == '_budsql_':      
                
                '''不管怎样都会替换'''
                
                sql = values['_sqlstring_'].replace('#日期参数S1#',values['_frd_'])
                sql = sql.replace('#日期参数S2#',values['_tod_'])
                print(sql)
                
            if event == '-Run-':
                
                maindf=pd.DataFrame()
                
                if values['_enableDate1_'] == True and values['_frd_']=='-':
                    sg.PopupError('需要选择开始日期')
                    pass
                elif values['_enableDate2_'] == True and values['_tod_']=='-':
                    sg.PopupError('需要选择结束日期')
                    pass
                
                else:
                    sql = values['_sqlstring_'].replace('#日期参数S1#',values['_frd_'])
                    sql = sql.replace('#日期参数S2#',values['_tod_'])
                    
                    db = getdb(values)
                
                    for i in db:
                        res,sdf = dbrun(i,db[i],sql)  #返回
                        if res==True:
                            maindf=maindf.append(sdf)
                    
                    
                    
                    
                    cols = maindf.columns
                    try:
                        for i in cols:
                            if maindf[i].dtype == 'datetime64[ns]' or ('日期' in str(i)):
           
                                maindf[i] = pd.to_datetime(maindf[i],format='%Y-%m-%d',  errors = 'coerce') 
                                
                                #测试成功留null值                         
                                #解决有效期字段大于2099的问题； 
                        maindf.to_excel(values['_sk1_']+values['_sk0_']+'.xlsx',sheet_name=values['_sk0_'],index=None)
                        sg.PopupOK('脚本执行完成！')
                
                    except:
                        
                        sg.PopupError('导出有误，请检查日志！')
                        pass
                

    window.close()

main()
