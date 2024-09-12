# -*- coding: UTF-8 -*-
import requests
import re
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_data(neo_type, neo_category, neo_page):
    if neo_type not in ['wishlist', 'progress', 'complete']:
        raise ValueError('Invalid type parameter. Must be wishlist, progress, or complete')
    
    if neo_category not in ['book', 'movie', 'tv', 'music', 'game', 'podcast'] and neo_category != '':
        raise ValueError('Invalid category parameter. Must be book, movie, tv, music, game, podcast, or an empty string')

    base_url = f'https://neodb.social/api/me/shelf/{neo_type}?page={neo_page}'
    if neo_category:
        url = f'{base_url}&category={neo_category}'
    else:
        url = base_url

    headers = {
        'Authorization': 'Bearer ' + os.environ.get('AUTHORIZATION'),
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    return json.loads(response.text)
class Handler(BaseHTTPRequestHandler): 
    def do_GET(self):
        path = self.path
        neo_type = re.findall(r'type=([^&]*)', path)[0]
        neo_category = re.findall(r'category=([^&]*)', path)[0]
        neo_page_str = re.findall(r'page=([^&]*)', path)
        neo_page = int(neo_page_str[0]) if neo_page_str else 1
        if neo_page <= 0:
            raise ValueError('Page number must be a positive integer')
        try:    
            data = get_data(neo_type, neo_category, neo_page) 
        except Exception as e:  
            self.send_error(500, str(e))
            return
       
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return
    
# def run(server_class=HTTPServer, handler_class=Handler, port=8080):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print(f'Starting server on port {port}')
#     httpd.serve_forever()

# if __name__ == '__main__':
#     run()
