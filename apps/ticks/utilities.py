import sys,os,shutil
sys.path.append('..')
sys.path.append(os.path.dirname(sys.path[0]))

import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame 
from datetime import datetime
from pandas import Panel

#variables
today = str(datetime.today()).replace('-','')[:8]
#auth 
auth = {}
auth['login'] = os.environ.get('USERNAME')+'@lenovo.com'
auth['password'] =os.environ.get('PASSWORD')

#utils
#dfuncmarker =lambda x : ''.join((METAFUNCTION[METAFUNCTION['Product'].str.contains('/'+x+'/')] ['Function']).tolist())

funcmarker =lambda x,meta : ''.join((meta[meta['Product'].str.contains('/'+x+'/')] ['Function']).tolist())
ownermarker = lambda x,meta : ''.join((meta[meta['Function'] == x ] ['Owner']).tolist()) if x == x  else ''

trimbrace = lambda x: x  if( x.find('(') == -1) else x[ :x.find('(') - 1 ]  
listtrimbrace = lambda x :  [trimbrace(item) for item in x]
flat=lambda L: sum(map(flat,L),[]) if isinstance(L,list) else [L]

def timeconvert(timez):
    times_index = pd.Index( pd.to_datetime(timez))
    times_index = (times_index.tz_localize('UTC').tz_convert('Asia/Shanghai'))
    return    pd.DatetimeIndex([i.replace(tzinfo=None) for i in times_index])




#base config
base_path = 'D:\\Aqua\\apps\\ticks'
cfg_path = os.path.join(base_path,'config\\')
getconfig = lambda filename,header= 0: DataFrame(pd.read_csv(cfg_path + filename,header = 0))

cfg_fields = getconfig('cfg_Field.csv').set_index('Server')
CLIENTCOLUMNS = getconfig('cfg_Field.csv')['Client'].tolist()
SERVERCOLUMNS = cfg_fields.index.tolist()
FIELDS_DICT = cfg_fields.to_dict()['Client']

block_cfg = dict(
RELEASES_DICT = dict( {'17B': ['17B_Block']  }),
#assume I have same source format,else define another FIELD_DICT instead
comps = None,
HW_LIST = None,
NAME = 'block',
CATCH = list(('Closed','Limitation')),
LABELS =  ['Sev1N2MS','Sev3N4MS','Statistics','OverAge','TestBlocker'] #mark account
)
#'Purley SR530 (Constantine)', 'Purley SR550 (Carnage)', 'Purley ST550 (Odin)','Purley SD530 (Stark)','Purley SR630 (Cable)'
#'Purley SD650 (OceanCat)', 'Purley SN550 (Ventura)', 'Purley SN850 (Winterfell)','Purley SR570 (Cosmo)', 'Purley SR590 (Callisto)','Purley SR650 (Cyborg)', 'Purley SR850 (Electron)', 'Purley SR860 (Neutron)', 'Purley SR950 (Proton)', 
#old 'purely_OOD' :['PurleyGA','Purley_Development_Internal','Purley_Electron','purley_ga','Purley_InitialGA','Purley_LXCA','Purley_Neutron','Purley_OceanCat','Purley_PostGA','Purley_Proton','Purley_Stark','Purley_Stark_ESP','Purley_Stark_GPU+DaisyChain','Purley_TDM_Post_GA','Purley_Ventura','Purley_Winterfell'] 
rows = ['Bug ID','Status','Risk Level','Product','Hardware','Limitation Status','Opened','Deadline','Release','Platform Affected','Phase Found','Component','Tip Pointer','Tip Status','Severity','Defect is Blocking','External ID','Resolution','Changed','Build Fixed','Classification','Duplicate ID','Target Release','Customer Impact','Probability','Summary','Answer','Priority','keywords', 'Action','Project','Suffix','Scope','Owner','Function']		
stscols = {
    'HighLight': ['Translation','inschedule','risky','Budding','Pending','OverMS'],
    'Statistics':['Closed','Rejected','Verify','Limitation','Fixed','Open','Working','LmtCandidate'],
    'Milestones':['Irevelent','Ahalf','Between','DuedExit','Deadliness'],
    "Sev1N2MS": ['Serv_1Meet1stCK','Serv_1Meet2ndCK', 'Serv_1OverMS', 'Serv_1NoDeadline','Serv_2Meet1stCK','Serv_2Meet2ndCK', 'Serv_2OverMS', 'Serv_2NoDeadline'],
    "Sev3N4MS": ['Serv_3Meet1stCK','Serv_3Meet2ndCK', 'Serv_3OverMS', 'Serv_3NoDeadline','Serv_4Meet1stCK','Serv_4Meet2ndCK', 'Serv_4OverMS', 'Serv_4NoDeadline'],
    "OverAge": ['Overdue','3day_open','20d_work','30d_work','50d_work'],
    "TestBlocker": ['Blocking'],
    'OutStanding':['Serv_1Active','Serv_1Fixed','Serv_1Verify','Serv_1Reject', 'Serv_2Active','Serv_2Fixed','Serv_2Verify','Serv_2Reject', 'Serv34_Active','Serv34_Fixed','Serv34_Verify','Serv34_Reject'],
    'General':  ['Limdup','Limcandi','LimApv', 'Lev1','Lev3','Lev4','Lev6','Lev5et' ,'duedAt5','duedAt6dl','duedAt6','dueFixed','dueFixnodl','overMS']
    
  
    }
prefix = ['Project','Owner','Function']
purely_cfg = dict(
    RELEASES_DICT = dict( {    
        'Purely' : ['Purley_MS','Purley_Odin','Purley_Value'],
        'purely_OOD' :['Purley_Electron','purley_ga','Purley_Neutron','Purley_Proton','Purley_Stark','Purley_Stark_ESP']
        }),
    #assume I have same source format,else define another FIELD_DICT instead
    comps =  getconfig('purely_mapping.csv')['Component'].values.tolist(),
    HW_LIST =  ['Purley SR530','Purley SR630','Purley SR550','Purley SR650','Purley ST550'],
    NAME = 'purely',
    CATCH = None,
    LABELS = ['HighLight','Statistics']
)

hs_cfg = dict(
    RELEASES_DICT = dict( { 'HS_USI' : ['SR630X-SR650X ESP_Tencent', 'SR630X-SR650X ESP_Yahoo','SR630X-SR650X Baidu','_Solution_Defect']    }),
    #assume I have same source format,else define another FIELD_DICT instead
    comps =  None,
    HW_LIST =  ['HS-SR630X', 'HS-SR650X'  ],
    NAME = 'hs',
    CATCH = list(('Closed','Limitation')),
    LABELS = ['Statistics', 'OutStanding','General']
)


getcfg = lambda filename,**kwargs: DataFrame(pd.read_csv(cfg_path + filename,**kwargs))
meta = getcfg('project_meta.csv')
def wrapper(data,*args):
    #use certain rules to group defects  
    NAME= args[0]

    '''change for nothing,works for free.  
    todo add field for purely selection     '''
    FUNC_MATA = getconfig(NAME + '_mapping.csv')#else cfg_function
    #FUNC_MATA['Product'] = FUNC_MATA['Product'].str.([1:-1])split('/')     
    data.loc[:,'Suffix'] = ''
    if NAME != 'hs':
        if NAME == 'block':
            f1 = lambda x: funcmarker(x,FUNC_MATA)
            f2 = lambda x: ownermarker(x,FUNC_MATA)
            data.loc[:,'Function'] = data['Product'].apply(f1)
            data.loc[:,'Owner'] = data['Function'].apply(f2)
        if NAME == 'purely':
            data = pd.merge(data, FUNC_MATA, on='Component', how='outer')        
        
        data.loc[data['Function'].isin(['UNKNOWN']),'Function'] =  data['Component'].apply(lambda comp : 'IMM' if comp.__contains__('imm') else 'UEFI'  )
        data.loc[data['Function'].isin(['UEFI','IMM']),'Suffix'] = data['Component'].apply(lambda comp : '_Platform' if comp.__contains__('.hv') else '_Core'  )
        data.loc[data['Function'].isin(['UEFI','IMM']),'Function']= data['Function'].__iadd__(data['Suffix'])
        data.loc[(data['Function'] == 'Application') & ((data['Product'] == 'SCOM') | (data['Product'] == 'SCCM') ),'Function'] =  data['Component'].apply(lambda comp : 'Application' if comp.__contains__('_SW_Plug_in') else ''  )   
    else:
        data = pd.merge(data, FUNC_MATA, on='Component', how='outer') 
        data = data[data['Function'].notnull()]
    return  data[data['Bug ID'].notnull()]

    
def marker(data,*args):
        #use marks to filter data
        """for 4R1T do nothing,for transfered ,check in Platform,
        other param hwlist,dict
        """
        comps,hwlist = args[0],args[1] #'All','Purley All'
        trimbrace = lambda x: x  if( x.find('(') == -1) else x[ :x.find('(') - 1 ]  
        listtrimbrace = lambda x :  [trimbrace(item) for item in x]
        if  comps != None  :
            if hwlist  != None:
                hwlist +=  ['All','Purley All']
            #hwlist = purely_hardware #all & other are excluded.

            #also move into a decorator
            #data['Suffix'] = data['Project'].apply(lambda  mark :False if  mark 'purely_OOD' else True )
            data['Suffix'] =np.where(data['Project'].isin(['purely_OOD','purely_OOD+']),False,True)
        
            data ['Platform Affected']  = data['Platform Affected'].apply(str)
            data['Platform Affected'] = data['Platform Affected'].apply(eval) 
            data['Platform Affected'] = (data['Platform Affected']).apply(listtrimbrace)
            #print('processing ' ,len(data.loc[data['Suffix'] == False]))
            data.loc[data['Suffix'] == False ,'Suffix'] = data['Platform Affected'].apply( lambda x:True if [val for val in hwlist if val in x]  else False )
            #print('revelent data size ',len(data))
            data = data[data['Suffix']== True]
            data.loc[:,'Scope'] = np.where(data['Component'].isin(comps), "Develop" , "Others")
            return data
        else: 
            data.loc[:,'Scope'] = 'GE'
            if hwlist != None:
                #hyperscale filter ,'Other'
                print( hwlist )
                hwlist +=  ['All']
                data ['Platform Affected']  = data['Platform Affected'].apply(str)
                data['Platform Affected'] = data['Platform Affected'].apply(eval) 
                data['Platform Affected'] = (data['Platform Affected']).apply(listtrimbrace)
                data['Suffix'] = data['Platform Affected'].apply( lambda x:True if [val for val in hwlist if val in x]  else False )
                data = data[data['Suffix']== True]
                print('length for filted  data is ',len(data))
        return data
    
def check(path):
        return  not(  os.path.exists( path ) and os.path.getsize( path ) )
def uncheck(path):
    #os.path.remove(path)
    try:
        os.remove(path)
    except OSError:
        pass


from time import time
import asyncio,aiohttp
from multidict import MultiDict


def obtainer(refers,name,catch=None):
    #fetch data in placepython
    path = r'D:\aqua\apps\static\downloads'
    output = os.path.join(path,name,today +'_src.csv')
    if check(output):
        authparams = auth
        srccolumns = SERVERCOLUMNS
        fieldmap = FIELDS_DICT
        queryparams = MultiDict({'include_fields': ','.join(srccolumns)})
        queryparams.update(authparams)
        baseurl = 'https://bz.labs.lenovo.com/rest'
        queryurl = baseurl +'/bug'


        #this area data encapsulate within config file
        #mark column list in config file,including Release info
        data   = None

        async def getty(val):
            watching =     ['Rejected','Verify','Fixed','Open','Working']
            null = ''
            true = True
            [queryparams.add('version', vi) for vi in val]
            if catch != None:
                watching += catch
                print (type(watching))
                #[queryparams.add('status', vi) for vi in catch]
            [queryparams.add('status', vi) for vi in watching]
            
            #queryparams['version'] =str( val)
            print('using release vals :',val )   
            conn = aiohttp.TCPConnector(verify_ssl=False)
            async with aiohttp.ClientSession(connector=conn) as session:
                async with session.get(queryurl,params= queryparams) as response:
                    txt =  await response.text()
                    return   list(eval(txt).values())[0]                 

        async def fetch():               
            tasks = [ asyncio.Task(getty(value)) for (key,value) in refers.items() ]
            buffer  =  await asyncio.gather( *tasks )
            # list(eval(response.text()).values())[0]
            buff = flat(buffer)
            print('length for data is: ',len(buff))
            #print('data is: ',buff[:1])    
            nonlocal data            
            data = DataFrame(buff,columns = srccolumns)
            return data                
            
        #make async tasks,new_event_loop 
        loop = asyncio.new_event_loop ()
        asyncio.set_event_loop(loop)
        #loop.get/submit tasks asyncio.open_connection?
        start = time()
        loop.run_until_complete(fetch())
        loop.close()
        end = time()

        print ('Cost {} seconds'.format((end - start) / 5))
            
        #rename columns    
        for each in fieldmap.items():
            #purely_OOD(type(each))
            data.rename(columns = {each[0]:each[1]} ,inplace = True )
        data.to_csv(output,index = False,encoding='utf-8')
    else:
         data = pd.read_csv(output,encoding='utf-8')
         print('roaming  data lenth are ',len(data))
    data['Project']= data['Release'].apply( lambda rel :list( {  key:value  for (key,value) in refers.items()   if value.__contains__(rel) }.keys() ) [0] )
    return data
    

def accounter(data,labels):
    severy =     lambda sts : {'Emergency':'Serv_1', 'Medium':'Serv_3', 'Low':'Serv_4', 'High':'Serv_2'}.get(sts, None)
    data['Severity'] = data['Severity'].astype(str)    
    data['Opened'] = timeconvert(data['Opened'])#adding filter for open/working/fixed
    data['Changed'] = timeconvert(data['Changed'])
    data['Deadline'] =  data['Deadline'].fillna('')
    duedcheck = lambda deadline,ref,mark: mark if (deadline == deadline)  and (  pd.Timestamp(deadline) - pd.Timestamp(ref)  ).days  < 0  else None#deadline < ref
    dueincheck = lambda deadline,ref,mark: mark if (deadline == deadline)  and (  pd.Timestamp(deadline) - pd.Timestamp(ref)  ).days  > 0  else None #deadline > ref
    duedin = lambda deadline,init,ends:  True if (deadline != None)  and (  pd.Timestamp(init) - pd.Timestamp(deadline)).days <= 0 and (  pd.Timestamp(ends) - pd.Timestamp(deadline)).days > 0  else False
    def de_accounter(data,label):
        data.loc[ :,'Suffix']  = data['Severity'].apply(severy)#Severity Medium        
        #print('using label',label,len(data))
        if label == "Milestones" or   label == "Sev1N2MS" or label == "Sev3N4MS" :   #[O/W/F']          
            mid = datetime(2017, 8, 4, 12, 0, 0, 2606)
            exits = datetime(2017, 8, 18, 12, 0, 0, 2606)
            data.loc[:,'Milestones'] = np.where(data['Deadline'].values != '',None, 'NoDeadline' )  
            #postexit  =  lambda deadline,mark:duedcheck(deadline,exits,mark)
            #postmid = lambda deadline,mark:duedcheck(deadline,mid,mark)

            df = data.loc[ data['Deadline'].values != '' ]
            # df = data.loc[   data['Status'].isin(['Closed','Rejected','Verify','Limitation']) &  data['Deadline'].values != '' ]
            #df.to_csv(base_path+'\\dummu.csv',index= False)
            df.loc[ :,'Milestones'] = df['Deadline'].apply(duedcheck,args=[mid,'Meet1stCK']) 
            df.loc[  df['Milestones'].isnull(),'Milestones'] =  df['Deadline'].apply(duedcheck,args=[ exits,'Meet2ndCK']) 
            df.loc[  df['Milestones'].isnull(),'Milestones'] = 'OverMS'
            #exclude status except o/w/f
           
            
            data =  pd.concat([df,data.loc[data['Milestones'].values == 'NoDeadline']])
            data.loc[   data['Status'].isin(['Closed','Rejected','Verify','Limitation']) ,'Milestones' ]= None
            #data.loc[data['Severity'].isnull() | data['Status'].isin(['Limitaion','Closed','Verify','Rejected']),'Milestones'] = 'Irevelent' 
            if  label == "Sev1N2MS":
                data['Sev1N2MS'] = np.where(data['Suffix'].isin(['Serv_1','Serv_2']), data['Suffix'],None )
                data['Milestones'] = np.where(data['Suffix'].isin(['Serv_1','Serv_2']), data['Milestones'], None)
                #data.loc[data['Suffix'].isin(['Serv_1','Serv_2']), "Sev1N2MS"] = data['Suffix']
                data.loc[:, "Sev1N2MS"] = data['Sev1N2MS'].__iadd__(data['Milestones']) 
            elif  label == "Sev3N4MS":
                data['Sev3N4MS'] = np.where(data['Suffix'].isin(['Serv_3','Serv_4']), data['Suffix'],None )
                data['Milestones'] = np.where(data['Suffix'].isin(['Serv_3','Serv_4']),data['Milestones'] , None)
                data.loc[:, "Sev3N4MS"] = data['Sev3N4MS'].__iadd__(data['Milestones']) 
            return data
			
        if label == "OverAge":  #"": ['Overdue','3day_open','20d_work','30d_work','50d_work']
            df = data.loc[  data['Deadline'].values != '' ]
            #df.to_csv(base_path+'\\dummu.csv',index= False)
            data.loc[:,'Scope'] = data['Changed'].apply(lambda doa : ( pd.Timestamp(datetime.today() ) -  pd.Timestamp(doa) ).days  )
            data.loc[:,'OverAge'] = None
            df.loc[data['Status' ].isin(  ['Open','Working']) , 'OverAge'] = df['Deadline'].apply(dueincheck,args=[datetime.today() ,'Overdue']) 
            
            data.loc[data['Status' ].isin( ['Working']), 'OverAge'] =data['Scope'].apply(lambda val:  '50d_work'   if val >= 50 else '30d_work'  )
            data.loc[ ( data['Status'] == 'Working') & (data['OverAge'] == '30d_work' ), 'OverAge'] =data['Scope'].apply(lambda val:  '20d_work' if val <= 30 else '30d_work' ) 
            data.loc[data['Status' ].isin( ['Open']), 'OverAge'] =data['Scope'].apply(lambda val:  '3day_open'   if val >= 3 else None )
            data=  pd.concat([df,data[ data['Deadline'].values  == ''  ] ])            
            return data 
        
        if label == "TestBlocker": #"TestBlocker": ['Blocking']
            data.loc[:,'TestBlocker'] = np.where( data['Statistics' ].isin(['Open','Working','Fixed']) & (data['Defect is Blocking'].values != 'No') , 'Blocking',None )  
            return data 
            
        if label == "Statistics":
            statusmarker  = lambda sts :  {'Closed':'Closed','Rejected':'Rejected','Verify':'Verify','Limitation':'Limitation','Fixed':'Fixed','Open':'Open','Working':'Working'}.get(sts, None) 
            data.loc[:,'Statistics'] = data['Status'].apply(statusmarker)
            data.loc[data['Statistics' ].isin(  ['Open','Working']) &  (data['Limitation Status'] .isin(['Limitation Candidate'])), 'Statistics'] ='LmtCandidate'
            data.loc[data['Statistics' ].isin(['Open','Working']) &  (data['Limitation Status'] .isin(['Permanment no Tip','Permanment with Tip','Temporary with Tip','Temporary no Tip'])), 'Statistics'] ='LmtCandidate'
            return data 
            
        if label == "HighLight":
            from datetime import timedelta
            now = datetime.now()
            n_day = lambda n: timedelta(days = n)
            init= datetime(2017, 6,5, 12, 0, 0, 2606)
            exits = datetime(2017, 6, 15, 12, 0, 0, 2606)
            #duedcheck = lambda deadline,ref:  True if (deadline == deadline)  and (  pd.Timestamp(ref) - pd.Timestamp(deadline) ).days < 0  else False
            #split data
            data.loc[:,'HighLight'] =np.where(data['Deadline'].values != '',None, 'NoDeadline' ) 
            df = data.loc[  data['Deadline'].values != '' ]
            #df
            df.loc[ :,'HighLight']  = df['Deadline'].apply(dueincheck,args=[now,'Inschedule'])
            df.loc[ df['Deadline'].apply(duedin,args=[init+n_day(-3),init]),'HighLight'] = 'Risky'
            df.loc[df['Deadline'].apply(duedin,args=[init,exits]),'HighLight']  = 'Pending'
            df.loc[df['Status'].isin(['Open','Working']) ,'HighLight'] = df['Deadline'].apply(dueincheck,args=[exits,'OverMS'])        
            #so tidious
            data=  pd.concat([df,data[ data['Deadline'].values  == ''  ] ])            
            data['Suffix'] = np.where(data['Opened'].apply(duedcheck,args= [now+n_day(-3),'Pending']),'Pending','Budding')
            data.loc[data['Deadline'].values == '','HighLight'] = data['Suffix']
			
            data.loc[(data['Product'] == 'Translation') | data['Limitation Status'].isin(['Limitation Candidate']) ,'HighLight'] = 'Translation'
           
            '''
			InSchedule	DEADLINE < TODAY			
			Translation	- Translation | Documentation | Limitation Candidates			
			Risky	6/2 < DEADLINE <=6/5 			
			Budding	NO DEADLINE AND ACTIVE<=3			
			Pending	6/5 < DEADLINE <= 6/15+ NO DEADLINE AND ACTIVE>3			
			over_MS	6/15 < DEADLINE
			'''

            #translation
            return data
        if label == 'OutStanding'  :#  '':['Active','Fixed','Verify','Reject'],
            data.loc[:,'Scope'] = data['Status'].apply(lambda sts : {'Rejected':'Reject','Verify':'Verify','Fixed':'Fixed','Open':'Active','Working':'Active'}.get(sts, None) )
            #marking for severity
            data.loc[data['Scope'].isnull() ,'Suffix'] =  None
            data.loc[ data['Suffix'].isin(['Serv_3','Serv_4']) ,'Suffix'] = 'Serv34_'
            data["OutStanding"] = data['Suffix'].__iadd__(data['Scope']) 
            return data
        if label == 'General': #'General': ['Limdup','Limcandi','LimApv', ''Lev1','Lev3',,'Lev4','Lev6','Lev5et' ,'duedAt5','duedAt6dl','duedAt6','dueFixed','dueFixnodl','overMS']
            data.loc[: ,'General'] =  np.where(data['Status'].isin(['Open','Working']) ,'Active',None)
            data['Opened'] = timeconvert(data['Opened'])
            data.loc[(data['Status' ].isin(['Open','Working'])),'General']  =  data['Risk Level'].apply(lambda levx:  {'1-Need Help':'Lev1','3-Over Schedule':'Lev3','4-Arbitration':'Lev4','6-Schedule OK':'Lev6'}.get(levx,'Lev5et'))     
            #overdue
            data.loc[data['General'] == 'Lev5et','General'] =data['Opened'].apply(lambda opendate: 'duedAt5' if( (datetime.utcnow() - pd.Timestamp(opendate)).days > 3 ) else 'Lev5et' )
            #fix for weekend #fix for weekend 
            data.loc[(data['General'].isin(['duedAt5'])) & (data['Opened'].dt.weekday > 4),'General']= 'Lev5et'
            df = data.loc[  data['Deadline'].values != '' ]
            todaydetail = datetime.today()
            df.loc[(df['General'] == 'Lev6'),'General'] =df['Deadline'].apply(lambda deadline: 'duedAt6' if (deadline == deadline) and (pd.Timestamp(todaydetail) - pd.Timestamp(deadline)).days > 1  else 'Lev6' )
            #fix for weekend 
            #df.loc[(df['General'].isin(['duedAt6',])) & (df['Opened'].dt.weekday > 4),'General']= 'duedAt6' 
            df.loc[(df['Status'] == 'Fixed'),'General']= df['Deadline'].apply(lambda deadline: 'dueFixed' if (deadline == deadline) and (pd.Timestamp(todaydetail) - pd.Timestamp(deadline)).days > 1  else None )	
            data=  pd.concat([df,data[ data['Deadline'].values  == ''  ] ])   
            data.loc[(data['General'] == 'Lev6') & (data['Deadline'].values == '' ),'General'] ='duedAt6dl'
            data.loc[(data['Status'] == 'Fixed') & (data['Deadline'].values == '' ),'General']= 'dueFixnodl'
            #Limitation             
            data.loc[(data['Status' ].isin(['Open','Working'])) &  (data['Answer']== 'Duplicate'), 'General'] ='Limdup'
            data.loc[(data['Status' ].isin(['Open','Working']))  &  (data['Limitation Status'] .isin(['Limitation Candidate'])), 'General'] ='Limcandi'
            data.loc[(data['Status' ].isin(['Open','Working'])) &  (data['Limitation Status'] .isin(['Permanment no Tip','Permanment with Tip','Temporary with Tip','Temporary no Tip'])), 'General'] ='LimApv'
            return  data

            
    for label in labels:
        data = de_accounter(data,label)
        print(label,len(data))
    return data

"""
releases = block_cfg['RELEASES_DICT']
name= block_cfg['NAME']

"""
#whatever pivot 
       
def unitpivot(df,prefix ,keys,columns ):
    #df = DataFrame(df)
    tab = df.pivot_table(values = 'Bug ID',index= prefix,columns = keys,aggfunc = np.count_nonzero,margins= True).reset_index(prefix)
    '''for multiindex ,not working well
    for each in prefix:
        df[each] = tab.index.get_level_values(each) 
    '''
    return DataFrame(tab,columns =prefix + columns).fillna('')
     


def reporter(data,labels):                      
    #stscols['src'] = rows + labels
    dd = {}
    for label in labels:#unitpivot(data,prefix,label,stscols[label])     
        dd[label] =unitpivot(data,prefix,label,stscols[label] + ['All'] )
        #print(label,dd[label][:2])
    #dd['src']  = data
    pan = Panel(dd)
    #pan.to_excel(base_path+'\\panels.xls',index=False,cols = stscols)
    return pan

def blocks():
    releases = block_cfg['RELEASES_DICT']
    name = block_cfg['NAME']  
    comps = block_cfg['comps']
    hwlist= block_cfg['HW_LIST']
    name = block_cfg['NAME']
    catch = block_cfg['CATCH']
    labels = block_cfg['LABELS']
    #uncheck(os.path.join(base_path,name,today +'.csv')) 
    #data = obtainii(releases,NAME)
    data = marker(obtainer(releases,name,catch),comps,hwlist)
    data = wrapper(data,name)
    data = accounter(data,labels)
    pan = reporter(data,labels)
if __name__ == '__main__':
    blocks()    
    '''     
    releases = purely_cfg['RELEASES_DICT']
    name = purely_cfg['NAME']  
    comps = purely_cfg['comps']
    hwlist= purely_cfg['HW_LIST']
    name = purely_cfg['NAME']
    catch = purely_cfg['CATCH']
    labels = purely_cfg['LABELS']
    #uncheck(os.path.join(base_path,name,today +'.csv')) 
    #data = obtainii(releases,NAME)
    data = marker(obtainer(releases,name,catch),comps,hwlist)
    data = wrapper(data,name)
    data = accounter(data,labels)
    pan = reporter(data,labels)
    
        
    #[val for val in hwlist if val in x]
    #print(data[:3]) 
    #data.to_csv(base_path+'\\dum.csv',index=False)
    #pan.to_excel(base_path+'\\panels.xls',index=False)
    '''
    
 


