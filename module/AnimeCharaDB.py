# recode? malu bang sama umur 
# ~ natsuya (hero)

import os,sys,re
import requests

class search:

    def __init__(self,query):
        self.query = query
        self.url = "https://www.animecharactersdatabase.com/searches.php?s={}".format(self.query)
        self.headers = {
                "Host":"www.animecharactersdatabase.com",
                "Referer":"https://www.animecharactersdatabase.com/searches.php",
                "User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                }

    def getcontent(self):
        self.bingo,self.zleb = [],[]
        self.req = requests.get(self.url,headers=self.headers).text
        self.rtodict = re.findall(r'<A(.*?)</A>',self.req)
        for s in self.rtodict:
            if 'style=""' in s:
                pass
            else:
                s = re.sub(' ','',s)
                if s.startswith("HREF"):
                   self.bingo.append(s)


        for retag in self.bingo:
            page_id,name,image = \
                    re.findall(r'HREF="(.*?)"',retag)[0],re.findall('TITLE="(.*?)"',retag)[0],re.findall('SRC="(.*?)"',retag)[0]
            self.zleb.append({"name":name,"image":image,"page_id":page_id})

        return self.zleb



