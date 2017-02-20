import json 
import os
import sys
import urllib2
from shutil import rmtree

# ConvPy-Module "Conversion.py"
import Conversion
# ConvPy-Module "Converter.py"
from Converter import Saxon, Call


def clean_tmp (file_path):
    """
    cleans all temporary files and folders being created during convPY working 
    * path: path of tmp-file to be deleted inkl. it's parent directory 
    """
    try:
        rmtree(os.path.dirname(file_path))
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


def convert (flow, convpy):
    """
    main conversion routine which creates Conversion-Instances and call the Converter-Instances

    TO-DO:
    - decouple Conversion from Converter
    - "pathify" Saxon-Class (Converter.py) -> and make the Classes smooth ... they are a mess right now
    - make Conversion-Class smooth !
    """
    for step in flow:
        conversion = Conversion.Conversion()
        conversion.scenarioise(step, convpy.scripts)
        #conversion.info()
        
        if conversion.type == 'xslt':
            Saxon(convpy.engines['Saxon'], conversion.script).xslt()
        elif conversion.type == 'xquery':
            Saxon(convpy.engines['Saxon'], conversion.script).xquery()
        else:
            Call(conversion.language, conversion.script).run()


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
    opens files and reads it in with params 
    * path: path of file being opened 
    """
    try:
        with open(path, 'r') as out:
            output = out.read()
        return output
    except:
        print ('[convPY:ERROR] Failed in reading in file "' + path +'". Exit!')
        sys.exit(1)


def preset (data, tmp_file):
    """
    starts convPY's workflow by creating the essential file-system for temporary file
    """

    def create_tmp_essentials (tmp_file, data):
        os.makedirs( os.path.dirname( tmp_file ) )
        create_file( tmp_file, data )

    tmp_file = tmp_file
    tmp_dir = os.path.dirname( tmp_file )
    try:
        if not os.path.exists( tmp_dir ):
            create_tmp_essentials(tmp_file, data)
        else:
            clean_tmp(tmp_file)
            create_tmp_essentials(tmp_file, data)
    except:
        print ('[convPY:ERROR] Failed in creating essential file "' + path +'". Exit!')
        sys.exit(1)


def read_JSON_file (json_file):
    return json.load(open_file(json_file))


def retrieve (path):
    """
    input handler which loads the input data and decides if File or URL and returns the data
    * path: file-path or url which should be read in
    """
    try:
        if os.path.exists(path) and os.path.isfile(path):
            return open_file(path)
        elif path.startswith('http'):
            return request(path)
    except:
        print ('[convPY:ERROR] Failed in reading inpu-data "' + path +'". Exit!')    
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



    
