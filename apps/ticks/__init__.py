# -*- coding: utf-8 -*-
"""something was wrong with return value,so keep working on.
Created on Mon May 22 17:36:50 2017

@author: wangsy29
"""
from utilities import *
class Aqua:
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
        data = accounter(data,labels)
        return data
        
    def work(self):
        data = self.prepare()
        pan = reporter(data,labels)
        #data.to_csv(base_path + '//'+ name + '_src.csv', index = False)
        return pan

        


#mark for change

#from utilities import self.cfg

#block_cfg  
def tickor(config)  :
    return  Aqua(config).prepare()
def ticker(config):
    aqua = Aqua(config) 
    return  aqua.work()

if __name__ == '__main__':
    #aqua( cmd)
    #tick(block_cfg)
    test()
    
    
