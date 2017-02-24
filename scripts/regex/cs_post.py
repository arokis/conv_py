#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys

def regex(tmp):

    #print tmp

    with open(tmp, 'r') as out:
        xml_data = out.read()
    

    transform = re.sub('\)@@\(', ' ', xml_data)
    transform = re.sub('\)@[\s]?', ' ', transform)
    transform = re.sub('[\s]?@\(', ' ', transform)
    transform = re.sub('([\s]?·[\s]?)|([\s]?·[\s]?)', ' ‧ ', transform)
   
    print(transform)
    
    
    file = open(tmp,"w+") 
    file.write(transform) 
    file.close()
    

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        tmp = sys.argv[1]
    else:
        tmp = os.path.join(conv_py_home, 'tmp/tmp.xml')
    
    regex(tmp)

