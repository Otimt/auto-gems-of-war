#!/usr/bin/env python
#coding=utf-8
#author:naiveloafer
#date:2012-06-07
 
from flup.server.fcgi import WSGIServer
import json
 
def get_environ_param(environ):
    rquest_method = environ["REQUEST_METHOD"]
    str = "rquest_method:" + rquest_method + "\r\n"
    query_string = environ["QUERY_STRING"]
    str += ",query_string:" + query_string + "\r\n"
    #script_filename = environ["SCRIPT_FILENAME"]
    #str += ",script_filename:" + script_filename + "\r\n"
    #script_name = environ["SCRIPT_NAME"]
    #str += ",script_name:" + script_name + "\r\n"
    #rquest_uri = environ["REQUEST_URI"]
    #str += ", rquest_uri:" + rquest_uri + "\r\n"
    #remote_addr = environ["REMOTE_ADDR"]
    #str += ",remote_addr:" + remote_addr + "\r\n"
    #remote_port = environ["REMOTE_PORT"]
    #str += ",remote_port:" + remote_port + "\r\n"
    #
    #data = environ["wsgi.input"].read()
    #str += ", data:" + data + "\r\n"
    print(query_string)
    obj = dict([x.split('=',1) for x in query_string.split('&')])
    return obj
 
def naiveloafer_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    param_dict = get_environ_param(environ)
    res = json.dumps(param_dict)
    return [res]
 


    
if __name__  == '__main__':
    WSGIServer(naiveloafer_app,bindAddress=('127.0.0.1',8090)).run()