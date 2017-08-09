# -*- coding: utf-8 -*-
"""
Created on Mon May 22 17:36:50 2017

@author: wangsy29
"""

import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame 
import sys,os,shutil
from datetime import datetime

#variables
today = str(datetime.today()).replace('-','')[:8]
todaydetail = datetime.today()
#auth 
auth = {}
auth['login'] = os.environ.get('USERNAME')+'@lenovo.com'
auth['password'] =os.environ.get('PASSWORD')

#utils
funcmarker =lambda x,meta : ''.join((meta[meta['Product'].str.contains('/'+x+'/')] ['Function']).tolist())
ownermarker = lambda x,meta : ''.join((meta[meta['Function'] == x ] ['Owner']).tolist()) if x == x  else ''

trimbrace = lambda x: x  if( x.find('(') == -1) else x[ :x.find('(') - 1 ]  
listtrimbrace = lambda x :  [trimbrace(item) for item in x]
flat=lambda L: sum(map(flat,L),[]) if isinstance(L,list) else [L]
getconfig = lambda filename,header= 0: DataFrame(pd.read_csv(cfg_path + filename,header = 0))
duedwork = lambda deadline:  True if (deadline == deadline)  and (  pd.Timestamp(todaydetail) - pd.Timestamp(deadline)).days > 2 else False
duedfinish =  lambda deadline:  True if (deadline == deadline)  and ( pd.Timestamp(deadline) -  pd.Timestamp(todaydetail) ).days > 2 else False
def timeconvert(timez):
    times_index = pd.Index( pd.to_datetime(timez))
    times_index = (times_index.tz_localize('UTC').tz_convert('Asia/Shanghai'))
    return    pd.DatetimeIndex([i.replace(tzinfo=None) for i in times_index])


#base config
base_path = 'D:\\Aqua\\apps\\ticks'
cfg_path = os.path.join(base_path,'config\\')    
dest_prefix = 'tick_'
dump_file = dest_prefix + today +'.csv'
dest_path = os.path.join(base_path,'dump\\') + dump_file
cfg_fields = getconfig('cfg_Field.csv').set_index('Server')
CLIENTCOLUMNS = getconfig('cfg_Field.csv')['Client'].tolist()
SERVERCOLUMNS = cfg_fields.index.tolist()
FIELDS_DICT = cfg_fields.to_dict()['Client']

block_cfg = """dump_prefix =  'block_',
RELEASES_DICT =dict( {'17B': ['17B_Block',]  }),
#assume I have same source format,else define another FIELD_DICT instead
COMP_DICT = None,
HW_LIST = None,
FUNC_MATA = getconfig('block_products.csv'),#works for MARKER
ACCOUNTER_TAG ="Serverity", #mark account
ORDER_TAB = "Overall"

    """
code = """
releases = RELEASES_DICT[0],#wierd for get tuple instead of dict?
#print('type for refers 1',type(releases[0])),
rel = releases[0]
#obtainer(rel).to_csv(base_path+'//accounted.csv')
data = obtainer(rel)
#data = wrapper(obtainer(rel),COMP_DICT,HW_LIST),
#print('length for wrapper data is',len(data))

#for test,just simplify marker,later rewise
data.loc[:,'Function'] = data['Product'].apply(funcmarker,args =(FUNC_MATA))
data.loc[:,'Owner'] = data['Function'].apply(ownermarker,args = (FUNC_MATA))
data = serve_accounter (data)
#for snitcher
data.to_csv(base_path+'//accounted.csv')
res = pivoter(data,ACCOUNTER_TAG[0],ORDER_TAB)
res.to_csv(base_path+'//accounter.csv')
res.to_json(base_path+'//acjason.json')
    """


#whatever pivot 
def pivoter(data,*args):#could insert an list of tab names,or just the simple overall tab
    ACCOUNTER_TAG, orderTab = args[0],args[1]
    if ACCOUNTER_TAG == "Serverity": 
        stscols = ['Closed','VrfORRjt','Limitation','LimReq','LimTipRew','LimTipApv','Fixed','Limcandi','Limdupl','SevLev1','SevLev2','SevLev3','SevLev4','DuedLine','DuedSeverity','DuedFixLine','DueFixed']    
    if orderTab == "Overall":#['Project','Owner','Function']
        #traverse the list to fill sts dictionary,
        #try this cfg['tabs']['result'] to store the data failed.reason is competable data.
        #columns = stscols if tabs['col']== "['stscolumns',]" else eval(tabs['col'])
        prefix = [    ]
        result=unitpivot(data,prefix,'stsdued',stscols)              
        
    return result
        
def unitpivot(df,prefix ,keys,columns ):
    dfi = DataFrame(df)
    tab = dfi.pivot_table(values = 'Bug ID',index= prefix,columns = keys,aggfunc = np.count_nonzero,margins= True)
    '''for multiindex ,not working well
    for each in prefix:
        df[each] = tab.index.get_level_values(each) 
    '''
    tab =tab.reset_index(prefix)
    tabo = DataFrame(tab,columns =prefix + columns)
    return tabo

def serve_accounter(data):
        statusmarker  = lambda sts :  {'Closed':'Closed','Rejected':'VrfORRjt','Verify':'VrfORRjt','Limitation':'Limitation','Fixed':'Fixed','Open':'OpenORWork','Working':'OpenORWork'}.get(sts, None) 
        data['Opened'] = timeconvert(data['Opened'])
        data['stsoval'] = data['Status'].apply(statusmarker)
         
        data.loc[(data['stsoval']== 'Limitation') &  (data['Limitation Status'] .isin(['Permanent with Tip','Temporary with Tip'])), 'stsoval'] ='LimReq'
              
        #Tips Review: Tips Pointer= Tips ID & Tips Status= Rejected or Review or Draft;              
        data.loc[(data['stsoval']== 'LimReq') & ((data['Tip Status'].isin(['Draft','Rejected','Review']))  & (data['Tip Pointer'].str.isnumeric())),'stsoval'] = 'LimTipRew'
              
        #: col LimTipReq. tips Pointer=Error+BLANK
        data.loc[(data['stsoval']== 'LimReq') & ( data['Tip Pointer'].str.isnumeric()) ,'stsoval'] = 'LimTipApv'

        #weird expression
        data.loc[ :,'stswithlv']= data['stsoval'].map(lambda x: x if x != 'OpenORWork' else 'unknownlev')
        
        #lmtduplicate
        data.loc[(data['stswithlv' ]== 'unknownlev') &  (data['Answer']== 'Duplicate'), 'stswithlv'] ='Limdupl'
        
        data.loc[(data['stswithlv' ]== 'unknownlev') &  (data['Limitation Status'] .isin(['Limitation Candidate'])), 'stswithlv'] ='Limcandi'
        data.loc[(data['stswithlv' ]== 'unknownlev') &  (data['Limitation Status'] .isin(['Permanment no Tip','Permanment with Tip','Temporary with Tip','Temporary no Tip'])), 'stswithlv'] ='LimApv'
        
        data.loc[data['stswithlv' ]=='unknownlev','stswithlv']  =  data['Severity'].apply(lambda levx:  {'Emergency':'SevLev1','High':'SevLev2','Medium':'SevLev3','Low':'SevLev4'}.get(levx,'SevNone'))     
        #print('data[Opened] is :',type(data['Tip Pointer']))
        #wait(200)
        
        

        #this is for dued item 
        data.loc[:,'stsdued'] =  data['stswithlv'] 
        data.loc[(data['stsdued'].str.contains('Sev')) & (data['Deadline'].isnull()),'stsdued'] = 'DuedLine'
        data.loc[(data['stsdued'].str.contains('Sev')) & data['Deadline'].notnull() & data['Deadline'].apply(duedwork) ,'stsdued'] = 'DuedSeverity'
        #fix for weekend 
        #data.loc[(data['stsdued'].isin(['duedAt6',])) & (data['Opened'].dt.weekday > 4),'stsdued']= 'duedAt6' 
        data.loc[(data['stsdued'] == 'Fixed') & data['Deadline'].notnull() &  data['Deadline'].apply(duedwork),'stsdued']= 'DueFixed'
        data.loc[(data['stsdued'] == 'Fixed') & (data['Deadline'].isnull()),'stsdued']= 'DuedFixLine' 
        return  data
        

def wrapper(data,*args):
        #use marks to filter data
        """for 4R1T do nothing,for transfered ,check in Platform,
        other param hwlist,dict
        """
        comp_dict,hwlist = args[0],args[1]
        print('args 0 is',type(comp_dict))
        if  comp_dict[0] == None  :
            #hwlist = purely_hardware #all & other are excluded.
            trimbrace = lambda x: x  if( x.find('(') == -1) else x[ :x.find('(') - 1 ]  
            listtrimbrace = lambda x :  [trimbrace(item) for item in x]
            #also move into a decorator
            data['revelent'] = data['Project'].apply(lambda  mark :True if  mark == 'selected'else False )
            data ['Platform Affected']  = data['Platform Affected'].apply(str)
            data['Platform Affected'] = data['Platform Affected'].apply(eval) 
            data['Platform Affected'] = (data['Platform Affected']).apply(listtrimbrace)
            
            data.loc[data['revelent'] == False,'revelent'] = data['Platform Affected'].apply( lambda x:True if [val for val in hwlist if val in x]  else False )
            data = data[data['revelent']== True] 
            print('after first filter,remaining data is ',len(data))
            # data.to_csv(base_path+'//filtered.csv')
            #mark component
            #data['scope']= data['Component'].apply( lambda comp:'Develop' if comp_dict.keys().__contains__(comp) else 'Others' )
            data.loc[:,'scope'] = np.where(data['Component'].isin(comp_dict), "Develop" , "Others")
            #data['Component'].apply( lambda comp:'Develop' if comp_dict.keys().__contains__(comp) else 'Others' )
            return data
        else: 
            return data
    
def check():
        return  not(  os.path.exists( dest_path ) and os.path.getsize( dest_path ) )
    
def obtainer(refers):
    #fetch data in place
    if check():
        authparams = auth
        srccolumns = SERVERCOLUMNS
        fieldmap = FIELDS_DICT
        queryparams = {'include_fields': srccolumns}
        queryparams.update(authparams)
        baseurl = 'https://bz.labs.lenovo.com/rest'
        queryurl = baseurl +'/bug'
        output = dest_path

        #this area data encapsulate within config file
        #mark column list in config file,including Release info
        
        from requests import Request, Session
        session = Session()
        data = raw_json = raw_df = None
        null = ''
        true = True
        #initrequest = Request('GET',queryurl,params= queryparams)
        for (key,value) in refers.items():
            print('value type is ', type(value))    
            queryparams['version'] = value
            #the overflow machanism add here.
            initrequest = Request('GET',queryurl,params= queryparams)
            prepare  = session.prepare_request(initrequest)
            response = session.send( prepare,verify = False)
            raw_json=  list (eval(response.text).values())[0]
            print('lenth of raw data for release ',len(raw_json))                
            #transform data into dict                
            raw_df = DataFrame(raw_json,columns = srccolumns)
            raw_df['Project'] = key
            data = pd.concat([raw_df,data])
            
        #rename columns    
        for each in fieldmap.items():
            #print(type(each))
            data.rename(columns = {each[0]:each[1]} ,inplace = True )
        data.to_csv(output,index = False,encoding='utf-8')
 
        return data
    else:
         data = pd.read_csv(dest_path,encoding='utf-8')
         print('after loading,remaining data is ',len(data))
    
    return data
    


    def serve_accounter(data):
        statusmarker  = lambda sts :  {'Closed':'Closed','Rejected':'VrfORRjt','Verify':'VrfORRjt','Limitation':'Limitation','Fixed':'Fixed','Open':'OpenORWork','Working':'OpenORWork'}.get(sts, None) 
        data['Opened'] = timeconvert(data['Opened'])
        data['stsoval'] = data['Status'].apply(statusmarker)
         
        data.loc[(data['stsoval']== 'Limitation') &  (data['Limitation Status'] .isin(['Permanent with Tip','Temporary with Tip'])), 'stsoval'] ='LimReq'
              
        #Tips Review: Tips Pointer= Tips ID & Tips Status= Rejected or Review or Draft;              
        data.loc[(data['stsoval']== 'LimReq') & ((data['Tip Status'].isin(['Draft','Rejected','Review']))  & (data['Tip Pointer'].str.isnumeric())),'stsoval'] = 'LimTipRew'
              
        #: col LimTipReq. tips Pointer=Error+BLANK
        data.loc[(data['stsoval']== 'LimReq') & ( data['Tip Pointer'].str.isnumeric()) ,'stsoval'] = 'LimTipApv'

        #weird expression
        data.loc[ :,'stswithlv']= data['stsoval'].map(lambda x: x if x != 'OpenORWork' else 'unknownlev')
        
        #lmtduplicate
        data.loc[(data['stswithlv' ]== 'unknownlev') &  (data['Answer']== 'Duplicate'), 'stswithlv'] ='Limdupl'
        
        data.loc[(data['stswithlv' ]== 'unknownlev') &  (data['Limitation Status'] .isin(['Limitation Candidate'])), 'stswithlv'] ='Limcandi'
        data.loc[(data['stswithlv' ]== 'unknownlev') &  (data['Limitation Status'] .isin(['Permanment no Tip','Permanment with Tip','Temporary with Tip','Temporary no Tip'])), 'stswithlv'] ='LimApv'
        
        data.loc[data['stswithlv' ]=='unknownlev','stswithlv']  =  data['Severity'].apply(lambda levx:  {'Emergency':'SevLev1','High':'SevLev2','Medium':'SevLev3','Low':'SevLev4'}.get(levx,'SevNone'))     
        #print('data[Opened] is :',type(data['Tip Pointer']))
        #wait(200)
        
        

        #this is for dued item 
        data.loc[:,'stsdued'] =  data['stswithlv'] 
        data.loc[(data['stsdued'].str.contains('Sev')) & (data['Deadline'].isnull()),'stsdued'] = 'DuedLine'
        data.loc[(data['stsdued'].str.contains('Sev')) & data['Deadline'].notnull() & data['Deadline'].apply(duedwork) ,'stsdued'] = 'DuedSeverity'
        #fix for weekend 
        #data.loc[(data['stsdued'].isin(['duedAt6',])) & (data['Opened'].dt.weekday > 4),'stsdued']= 'duedAt6' 
        data.loc[(data['stsdued'] == 'Fixed') & data['Deadline'].notnull() &  data['Deadline'].apply(duedwork),'stsdued']= 'DueFixed'
        data.loc[(data['stsdued'] == 'Fixed') & (data['Deadline'].isnull()),'stsdued']= 'DuedFixLine' 
        return  data
def marker(data):
        '''
        none     '''
        data =data
        data.loc[:,'Function'] = data['Product'].apply(funcmarker)
        #change function OS deleting commponent without beijing key word
        data.loc[data['Function']=='OS','Function'] = data['Component'].apply(lambda comp: 'OS' if comp.__contains__('Beijing') else '')

        data.loc[data['Function'] == 'UNKNOWN','Function'] =  data['Component'].apply(lambda comp : 'IMM' if comp.__contains__('imm') else 'UEFI'  )
        data.loc[(data['Function'] == 'Application') & ((data['Product'] == 'SCOM') | (data['Product'] == 'SCCM') ),'Function'] =  data['Component'].apply(lambda comp : 'Application' if comp.__contains__('_SW_Plug_in') else ''  )
        data = data[data['Function'] !='']        
        data.loc[:,'Owner'] = data['Function'].apply(ownermarker)
        
        #differ Team FW deleting commponent with '.hv' key word into CORE/PLATFORM
        #add a new column naming suffix           
        data.loc[:,'Suffix'] = ''
        #data.loc[data['Owner']=='DB (FW)','Suffix'] = data['Component'].apply(lambda comp : '_PLAT' if comp.__contains__('.hv') else '_CORE'  )
        data.loc[data['Function'].isin(['IMM','UEFI']),'Suffix'] = data['Component'].apply(lambda comp : '_Platform' if comp.__contains__('.hv') else '_Core'  )
        #data.loc[data['Owner']=='DB (FW)''Function'] = data['Function']+  data['Suffix']
        data.loc[data['Owner']=='DB (FW)','Function']= data['Function'].__iadd__(data['Suffix'])
        data.loc[:,'Suffix'] =''

        return data        
def aqua(cfg):
    #works as a wrapper
    prev = locals()
    c = compile(cfg,'','exec') #compile into code object
    exec(c)
    afterw = locals()
   # diff  = afterw.keys() - prev.keys()
    #print(afterw)
    
    #cmd ="obtainer().to_csv(base_path+'//accounted.csv')"
    #exec(cmd,locals())
if __name__ == '__main__':
    aqua(block_cfg + code)
    
