'''
Created on Apr 3, 2013

@author: tunnelshade
'''
import urllib.request
import urllib.parse
import gzip
from lib.parser import Google_Results_Parser
import time


class Search_Google():
    def __init__(self, domain, search_words,  limit, proxy, proxy_username='', proxy_password=''):
        self.domain = domain
        proxy_handler = urllib.request.ProxyHandler(proxy)
        proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        proxy_auth_handler.add_password(None, 'https://www.google.com/', proxy_username, proxy_password)
        self.opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
        self.opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0'),
                                  ('Accept-Encoding','gzip')]
        self.url = 'https://www.google.com/search?hl=en&meta=&output=search&q=site:' + domain
        for keyword in search_words:
            self.url = self.url + '%20' + urllib.parse.quote(keyword,safe=':')
        self.limit = limit
        self.url_list = []
                   
    def search(self, start):
        for start in range(0,self.limit,10):
            self.url += '&start=' + str(start)
            try:
                data = self.opener.open(self.url)
                data = gzip.decompress(data.readall())
                data = data.decode('ascii','ignore')
                temp_list = Google_Results_Parser(data)
                if len(temp_list) != 0:
                    self.url_list += temp_list
                else:
                    break
            except urllib.error.HTTPError as e:
                if e == 'HTTP Error 503: Service Unavailable':
                    print("[!] Going to sleep for 1 minute to prevent lockout")
                    time.sleep(60)
                    
            except urllib.error.URLError as e:
                print("[!] Proxy server  ^ "+" appears down")
        return self.url_list