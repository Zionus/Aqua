from . import main
from .forms import PseudoForm
from flask import Flask,request,redirect,url_for,render_template,flash,jsonify,session
from flask import send_from_directory
from flask import current_app,make_response
from flask_login import login_required,current_user
from flask_uploads import UploadSet,DOCUMENTS
from apps.celo.tasks import send_async_email,snitching
import os
from pandas import DataFrame
#import celery


from apps.ticks.utilities import  *    
class Aqua:#should be singlton
    def __init__(self,config):
        self.cfg = config
                
                

    def prepare(self):     
        releases = self.cfg['RELEASES_DICT']
        name = self.cfg['NAME']  
        comps = self.cfg['comps']
        hwlist= self.cfg['HW_LIST']
        name = self.cfg['NAME']
        catch = self.cfg['CATCH']
        labels = self.cfg['LABELS']
        #uncheck(os.path.join(base_path,name,today +'.csv')) 
        #data = obtainii(releases,NAME)
        data = marker(obtainer(releases,name,catch),comps,hwlist)
        data = wrapper(data,name)
        path = r'D:\aqua\apps\static\downloads'
        output = os.path.join(path,name,today +'_pv.csv')
        data = accounter(data,labels)
        if check(output):
            data.to_csv(output,index = False,encoding='utf-8')
        return data
        

    def work(self):
        data = self.prepare()
        labels = self.cfg['LABELS']
        pan = reporter(data,labels)
        #data.to_csv(base_path + '//'+ name + '_src.csv', index = False)
        return pan


#mark for change

#from utilities import self.cfg

def tickor(config)  :
    return  Aqua(config).prepare()
def ticker(config):
    aqua = Aqua(config) 
    return  aqua.work()

from apps.ticks.utilities import  block_cfg,purely_cfg,meta

@main.route('/downloads/<path:filename>')
def download_file(filename):
    response = make_response()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    #return response
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
    #        filename,as_attachment= True)
    return response

@main.route('/index')
def index():
    return render_template('index.html')
	
@main.route('/project')
def project():
    name  = request.args.get('name', None)
    return render_template('main/project.html',name = name)


@main.route('/demo')
def demo():
    name  = request.args.get('name', None)
    return render_template('main/demo.html',name=name)
                                                 

@main.route('/catcha')
def catcha():
    #use passing data to generate tab
    #print('timer is ticking,',timer)
    name  = request.args.get('name', None)
    funz  = request.args.get('funz', '')
    label  = request.args.get('label', None)
    tab =  request.args.get('tab', None)
    is_all =  request.args.get('is_all', None)
    
    
    if request.is_xhr:
        cfg = name+'_cfg'
        data = tickor(eval(cfg))
        #target = data[ tab == label and'Function'== funz ] && Function == @funz
        print('query  columns ' ,label ,' in  table ', tab,'with function',funz)    #check for none functions 
        if is_all == 'false' :
            if label != 'All':
                target = data[(data[tab]== label ) & (data['Function']== funz) ]
            else :
                target = data[ data['Function']== funz ]
        else:
            target = data[ data[tab]== label  ]
        col =  ['Bug ID', 'Product', 'Hardware', 'Severity', 'Function', 'Owner']
        result = {'target':DataFrame(target,columns= col).to_dict(orient='records')}
        #print('data size:',len(data))
        #result.update({'cols' : [item  for item in list(data.columns)   if   item not in rows  ] })
        return jsonify(result)
        
    return render_template('main/project.html', name  = name)


@main.route('/fetcha')
def fetcha():
    #use passing data to generate tab
    #print('timer is ticking,',timer)
    name  = request.args.get('name', None)
    if request.is_xhr:
        cfg = name+'_cfg'
        data = tickor(eval(cfg))[:8]
        col =  ['Bug ID', 'Product', 'Hardware', 'Severity', 'Function', 'Owner']
        result = {'src':DataFrame(data,columns= col).to_dict(orient='records')}
        result.update({'cols' : col}) 
        print('data size:',len(data))
        #result.update({'cols' : [item  for item in list(data.columns)   if   item not in rows  ] })
        print('with  cols are  :', result['cols'])
        '''
        label = list(data.columns)
        print('label is:', label)
        #print('result [cols ] is ',result['cols'])
        '''
        return jsonify(result)
        
    return render_template('main/demo.html',name = name)
 
         
@main.route('/gotcha')
def gotcha():
    #use passing data to generate tab
    #print('timer is ticking,',timer)
    name  = request.args.get('name', None)
    if request.is_xhr:
        cfg = name+'_cfg'
        panel= ticker(eval(cfg))
        indexs = list(panel.axes[0])
        #indexs.remove('src')
        result = dict(labels=indexs)
        col =  ['Bug ID', 'Product', 'Hardware', 'Severity', 'Function', 'Owner']
        result.update({'cols' : col}) 
        #result = {'src':DataFrame(panel['src'],columns= rows +indexs).to_dict(orient='records')}
        #print(result['src'][:3])
        
        for ini in indexs:
            #print(stscols[ini])
            df =  DataFrame(panel[ini],columns= prefix + stscols[ini] + ['All'] ).fillna('').query('Project != "" ')
            #df.to_csv(r'D:\Aqua\apps\ticks\B_' + ini + '.csv',index= False)
            result.update({ini : df.to_dict('records') })
            
            result[ini + '_cols'] =  stscols[ini] 
            #print('tab label as : ',stscols[ini] )
            #print(result[ini][:3])
        return jsonify(result)
        
    return render_template('project.html',name = name)
    
@main.route('/push')
def push():
    #use passing data to generate tab
    return render_template('main/demo.html')
     


@main.route('/chart')
def chart():
    #assume to get the tag from request
    #use passing data to generate tab,or just get the function names
    print( current_app.config['UPLOAD_FOLDER'] )
    chartpath =os.path.join( current_app.config['UPLOAD_FOLDER'] ,'purely\\functions')
    flash(chartpath)
    #source_list = os.listdir(chartpath)
    return render_template('main/charter.html')
    
    
@main.route('/upload',methods = ['POST','GET'])
def upload():
    '''
    '''
    form = PseudoForm()
    if form.validate_on_submit():
        docs = UploadSet('docs',DOCUMENTS)
        
        #filename = secure_filename(form.pseudo.data.filename)
        filename = docs.save(form.pseudo.data)
        #docs.url(filename)
        flash('You have save file',filename)
    else:
        filename = None
    return render_template('upload.html',form = form,filename= filename)


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
       
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')
'''
import gevent
from gevent import monkey
monkey.patch_all()

from flask_mail import Message
@main.route('/mails', methods=['GET', 'POST'])
def mails():
    if request.method == 'GET':
        return render_template('test.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email
    app = current_app._get_current_object()
    to = email
    subject = app.config['MAIL_SUBJECT_PREFIX'] + 'Hello from Flask' 
    sender = app.config['DEFAULT_MAIL_SENDER']
    msg = Message(subject =subject ,sender = sender, recipients = to)

    # send the email DEFAULT_MAIL_SENDER
    
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(msg )
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('main.mails'))
   task_id=task.id)}	
@main.route('/longshot', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('snitching',
 
     
@main.route('/rindex')
def rindex():
    source_list = os.listdir(current_app.config['UPLOADS_DEFAULT_DEST'])[-5:]#change it to tick/[project]
    return render_template('index.html',source_list = source_list)


@main.route('/tabling/<name>')
def tabling(name):
    if request.is_xhr:
        #cfg = name+'_cfg'
        cfg = meta.loc[meta['NAME']== name]
        labels = eval(cfg['LABELS'].values.tolist()[0])
        data = {'tabs': labels}
        data.update(src= rows+labels)
        data.update(stscols)
        print("Tabling",data.keys())
        return jsonify(data)
    return render_template('project.html',name)
	
''''''
import gevent
from gevent import monkey
monkey.patch_all()

from flask_mail import Message
@main.route('/mails', methods=['GET', 'POST'])
def mails():
    if request.method == 'GET':
        return render_template('test.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email
    app = current_app._get_current_object()
    to = email
    subject = app.config['MAIL_SUBJECT_PREFIX'] + 'Hello from Flask' 
    sender = app.config['DEFAULT_MAIL_SENDER']
    msg = Message(subject =subject ,sender = sender, recipients = to)

    # send the email DEFAULT_MAIL_SENDER
    
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(msg )
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('main.mails'))
   task_id=task.id)}	
@main.route('/longshot', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('snitching',
 
     
@main.route('/rindex')
def rindex():
    source_list = os.listdir(current_app.config['UPLOADS_DEFAULT_DEST'])[-5:]#change it to tick/[project]
    return render_template('index.html',source_list = source_list)


@main.route('/tabling/<name>')
def tabling(name):
    if request.is_xhr:
        #cfg = name+'_cfg'
        cfg = meta.loc[meta['NAME']== name]
        labels = eval(cfg['LABELS'].values.tolist()[0])
        data = {'tabs': labels}
        data.update(src= rows+labels)
        data.update(stscols)
        print("Tabling",data.keys())
        return jsonify(data)
    return render_template('project.html',name)
	
'''