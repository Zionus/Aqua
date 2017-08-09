# -*- coding: utf-8 -*-
"""
Created on Fri May 26 10:05:38 2017

@author: wangsy29
"""
from utilities import *
s =  ['Overdue','3day_open','20d_work','30d_work','50d_work']
def formator(s):
	pre = '<th data-field="'
	suf='</th>'
	st = [ pre + ''+ item + '">' + item + suf  for item in s]
	[print(it) for it in st]

'''


var $table = $('#table').bootstrapTable({
    data: data
});

$table.on('click', 'tbody > tr > td', function (e){
    var table = $table.data('bootstrap.table'),
        $element = $(this),
        $tr = $element.parent(),
        row = table.data[$tr.data('index')],
        cellIndex = $element[0].cellIndex,
        $headerCell = table.$header.find('th:eq(' + cellIndex + ')'),
        field = $headerCell.data('field'),
        value = row[field];
    
    table.$el.trigger($.Event('click-cell.bs.table'), [value, row, $element]);
});

$table.on('click-cell.bs.table', function(e, value, row, $element){
		 alert('row: '+  JSON.stringify(row )  ); //row dict
    alert( JSON.stringify($element[0].cellIndex )  ); //col index
	var rowIndex = $element.parents("tr:first")[0].rowIndex; //row index 
    alert('row: '+JSON.stringify( $element.attr('data-index') ) );
});


todo :
fixnodl
duedatlev6

Kiri Logs
#schedule task
chart_src = load()#say /static/dump/chart_src.csv /json,then transport
#just for  all_sts 
all_sts = None
all_sts = pd.concat([None,panel['Statistics'].loc[panel['Statistics']['Project']== 'All']])

first get data  as transported.,then append today data 


#pv_Statistics > tbody > tr:nth-child(10) > td:nth-child(2)

small 318 215
large 760 430
'''

from utilities import *
dt ={'HW_LIST':list, 'LABELS':list, 'comps':bool, 'NAME':str, 'CATCH':list, 'RELEASES_DICT':dict}
getcfg = lambda filename,**kwargs: DataFrame(pd.read_csv(cfg_path + filename,**kwargs))
meta = getcfg('project_meta.csv',dtype = dt)
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame 
'''Creating our own class with values to pass in as parameters to our
chart.'''
import pygal
class ge_cfg(pygal.config.Config):
    width = 520
    height = 300
    title= 'overall'
    y_title = 'Defects Acount'
    x_title = 'By Date'
    #show_x_labels = True
    tooltip_font_size = 30
    title_font_size = 25
    no_data_text = 'Unable to load data'

	
all2 = pd.read_csv(r'D:\aqua\apps\static\svg\tabs\dummy.csv')#should I set index
sts = ['Closed','Rejected','Verify','Limitation','Fixed','Open','Working','LmtCandidate']
all2['Fields'] = all2[['All','Closed','Rejected','Verify','Limitation','Fixed','Open','Working','LmtCandidate']].values.tolist()
from datetime import datetime, timedelta
date_chart = pygal.Line(ge_cfg)
date_chart.x_labels = map(str,all2['Date'].values.tolist() )
print(all2['Closed'].values.tolist() )
[ date_chart.add( each ,all2[each].values.tolist()   )  for each in sts]
date_chart.render_to_file(r'D:\aqua\apps\static\svg\overall.svg') 
#date_chart.render_to_png(r'D:\aqua\apps\static\closing.png') 


class sub_cfg(pygal.config.Config):
    width = 310
    height = 200
    y_title = 'Defects'
    x_title = 'Date'
    #show_x_labels = True
    tooltip_font_size = 10
    title_font_size = 8
    no_data_text = 'Unable to load data'
today =  20170617
'''data loader '''
now_pv = pd.read_csv(r'D:\aqua\apps\static\svg\tabs\daily_pv.csv')#assume get from schedulor.
functions = {}.fromkeys(all_sts['Function'].values.tolist()).keys()
now_pv['Date']  = today
all_sts = pd.read_csv(r'D:\aqua\apps\static\svg\tabs\repo.csv') #remove all,or use pannel 
all_sts  = pd.concat([all_sts,now_pv])
#iterate the functions to generate table

def drawing(tags,src):
    for tag in tags:
        #print('using tag',tag)
        suf_src = src.query('Function == @tag')
        #print(suf_src)
        sub_chart = pygal.Line(sub_cfg)
        sub_chart.x_labels = map(str,suf_src['Date'].values.tolist() )
        #print(tag_src['Closed'].values.tolist() )
        [ sub_chart.add( each ,suf_src[each].values.tolist()   )  for each in sts]
        sub_chart.title= 'Funtion_'+ tag
        print(tag)
        name =''.join([  each for each in  filter(str.isalpha,tag)  ])
        try:
            sub_chart.render_to_file(r'D:\aqua\apps\static\downloads\block\functions\suf_'+ name + '.svg') 
        except Exception:
            pass

drawing(functions,all_sts)

'''

todo:HS
DC5200 ?


odoo
https://www.zhiyunerp.com/blog/2/post/odoo-12
say daily_pv store the statstics pivot data
and repo.csv store the historical data,mark with Filed Date (yyyymmdd)
today =  20170617
now_pv = pd.read_csv(r'D:\aqua\apps\static\svg\tabs\daily_pv.csv')
now_pv['Date']  = today
all_sts = pd.read_csv(r'D:\aqua\apps\static\svg\tabs\repo.csv') #remove all,or use pannel 
all_sts  = pd.concat([all_sts,now_pv])
#all_sts.to_csv(r'D:\aqua\apps\static\svg\tabs\repo.csv')  #update history data
tag = 'BB'
tag_src = all_sts[all_sts['Function'] == 'BB']
print(tag_src)

all_sts.set_index('State')
#merge multiple cols
all_dict = all_sts.to_dict('records')
#print(all_sts[:2])
#all_sts.plot.hist()

first get a list of query,
try to transport 
and convert to records
then draw the map.

sv1 =  ['Serv_1Meet1stCK','Serv_1Meet2ndCK', 'Serv_1OverMS', 'Serv_1NoDeadline','Serv_2Meet1stCK','Serv_2Meet2ndCK', 'Serv_2OverMS', 'Serv_2NoDeadline']
sv2 =     ['Serv_3Meet1stCK','Serv_3Meet2ndCK', 'Serv_3OverMS', 'Serv_3NoDeadline','Serv_4Meet1stCK','Serv_4Meet2ndCK', 'Serv_4OverMS', 'Serv_4NoDeadline']
    statusmarker  = lambda sts :  {'Closed':'Closed','Rejected':'VrfORRjt','Verify':'VrfORRjt','Limitation':'Limitation','Fixed':'Fixed','Open':'OpenORWork','Working':'OpenORWork'}.get(sts, None) 
    data['Opened'] = timeconvert(data['Opened'])
    data['Tip Status'] =  data['Tip Status'].astype(str)
    print(data.dtypes)
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


    severy =     lambda sts : {'Emergency':'Serv_1', 'Medium':'Serv_3', 'Low':'Serv_4', 'High':'Serv_2'}.get(sts, None)
    data['Severity'] = data['Severity'].astype(str)    
    data.loc[ :,'Suffix']  = data['Severity'].apply(severy)#Severity Medium
    data['Opened'] = timeconvert(data['Opened'])#adding filter for open/working/fixed
    data['Deadline'] =  data['Deadline'].fillna('')
    duedcheck = lambda deadline,ref,mark: mark if (deadline == deadline)  and (  pd.Timestamp(deadline) - pd.Timestamp(ref)  ).days  < 0  else None#deadline < ref
    dueincheck = lambda deadline,ref,mark: mark if (deadline == deadline)  and (  pd.Timestamp(deadline) - pd.Timestamp(ref)  ).days  > 0  else None #deadline > ref
    duedin = lambda deadline,init,ends:  True if (deadline != None)  and (  pd.Timestamp(init) - pd.Timestamp(deadline)).days <= 0 and (  pd.Timestamp(ends) - pd.Timestamp(deadline)).days > 0  else False
    def de_accounter(data,label):
        #print('using label',label,len(data))
        if label == "Milestones" or   label == "Sev1N2MS"  or  label == "Sev3N4MS" :   #['Irevelent','Ahalf','Between','DuedExit','Deadliness','Irevelent']          
            mid = datetime(2017, 6, 12, 12, 0, 0, 2606)
            exits = datetime(2017, 6, 26, 12, 0, 0, 2606)
            data.loc[:,'Milestones'] = np.where(data['Deadline'].values != '',None, 'NoDeadline' )  
            #postexit  =  lambda deadline,mark:duedcheck(deadline,exits,mark)
            #postmid = lambda deadline,mark:duedcheck(deadline,mid,mark)

            df = data.loc[  data['Deadline'].values != '' ]
            #df.to_csv(base_path+'\\dummu.csv',index= False)
            df.loc[ :,'Milestones'] = df['Deadline'].apply(duedcheck,args=[mid,'Meet1stCK']) 
            df.loc[  df['Milestones'].isnull(),'Milestones'] =  df['Deadline'].apply(duedcheck,args=[ exits,'Meet2ndCK']) 
            df.loc[  df['Milestones'].isnull(),'Milestones'] = 'OverMS'
            
            data =  pd.concat([df,data.loc[data['Milestones'].values == 'NoDeadline']])
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
           

			InSchedule	DEADLINE < TODAY			
			Translation	- Translation | Documentation | Limitation Candidates			
			Risky	6/2 < DEADLINE <=6/5 			
			Budding	NO DEADLINE AND ACTIVE<=3			
			Pending	6/5 < DEADLINE <= 6/15+ NO DEADLINE AND ACTIVE>3			
			over_MS	6/15 < DEADLINE


            #translation
            return data
            
    for label in labels:
        data = de_accounter(data,label)
        print(label,len(data))
    return data

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
    return accountero(data,labels)
dat = blocks()
'''