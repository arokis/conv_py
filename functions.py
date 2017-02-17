import json 
import os
import sys
import urllib2

def clean_tmp (file_path):
    """
    cleans all temporary files and folders being created during convPY working 
    * path: path of tmp-file to be deleted inkl. it's parent directory 
    """
    try:
        os.remove(file_path)
        os.rmdir(os.path.dirname(file_path))
    except:
        print ('[convPY:WARNING] Could not clean up tmp-file "' + path +'". Maybe you should clean it manually!')
        sys.exit(0)


def create_file (path, content, option='w+'):
    """
    creates files with params 
    * path: path of file being created
    * content: content being writen in file
    * options (optional): writing mode (no string-controll!), default: 'w+' 
    """
    try:
        fo = open( path, option ) 
        fo.write( content ) 
        fo.close()
    except:
        print ('[convPY:ERROR] Failed while creating File "' + path +'". Exit!')
        sys.exit(1)


def finish (tmp_file, output_file=False, clean=True):
    """
    convPY's result:  
    * return last conversion's output from tmp-file and clean-up
    * save last conversion's output from tmp-file in user-defined output-folder (under construction!)
    """
    output = open_file (tmp_file)
    if output_file != False:
        create_file(output_file, output)
    print(output)
    if clean == True:
        clean_tmp(tmp_file)
    sys.exit(0)


def open_file (path):
    """
    opens files with params 
    * path: path of file being opened 
    """
    try:
        with open(path, 'r') as out:
            output = out.read()
        return output
    except:
        print ('[convPY:ERROR] Failed in opening file "' + path +'". Exit!')
        sys.exit(1)


def preset (data, tmp_file):
    """
    starts convPY's workflow by creating the essential file-system for temporary file
    """
    try:
        if not os.path.exists( os.path.dirname( tmp_file ) ):
            os.makedirs( os.path.dirname( tmp_file ) )
            create_file( tmp_file, data )
    except:
        print ('[convPY:ERROR] Failed in creating essential file "' + path +'". Exit!')
        sys.exit(1)


def request (url):
    """
    requests data from url 
    * url: url whose data is going do be responded (well ... when server resonds)
    """
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        return data
    except:
        print ('[convPY:ERROR] Failed retrieving data from url "' + url +'" Exit!')
        sys.exit(1)



    
