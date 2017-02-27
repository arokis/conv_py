#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, argparse

def regex(in_file, out_file):

    #print tmp

    with open(in_file, 'r') as out:
        xml_data = out.read()
    

    transform = re.sub('\)@@\(', ' ', xml_data)
    transform = re.sub('\)@[\s]?', ' ', transform)
    transform = re.sub('[\s]?@\(', ' ', transform)
    transform = re.sub('([\s]?·[\s]?)|([\s]?·[\s]?)', ' ‧ ', transform)
   
    print(transform)
    
    
    file = open(out_file,"w+") 
    file.write(transform) 
    file.close()
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='cs_post', description='coptic scriptorium post processing.')
    parser.add_argument('-i', '--input', help='defines input directory or file')
    parser.add_argument('-o', '--output',  help="output")
    cmd_args = parser.parse_args()
    regex(cmd_args.input, cmd_args.output)

