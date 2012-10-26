import os
import sys

from urllib.parse import parse_qs

from config import *
from requestparser import RequestParser

def application(environ, start_response):
    try:
        query_body_size = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(query_body_size).decode('utf-8')
        
    except (ValueError):
        query_body_size = 0
        body = '{"requestType":100,"contentType":100,"requestData":{"productId":1,"user_email":"miha@miha8","user_password":"test_test88"}}'
    
    status = '200 OK'
    
    print (body)
    if len(body) > 0:
        plugin_response = RequestParser(body)
        plugin_response.distribute()
        output = plugin_response.output().encode('utf-8')
    else:
        output = "Empty result".encode('utf-8')
    
    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]


