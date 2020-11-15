#!/usr/bin/python3
#natsuya (https://github.com/nolepeople)
#created with depression <3

 
import os
import sys
import re
import requests
import bs4
import time
from  multiprocessing import Pool


BASE_URL = "https://www.animecharactersdatabase.com/"
headers = {
                "Host":"www.animecharactersdatabase.com",
                "Referer":"https://www.animecharactersdatabase.com/searches.php",
                "User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                }


class anch_db(object):

    def __init__(self,query):
        global BASE_URL,headers
        self.query,self.headers = query,headers
        self.url = "{}searches.php?s={}".format(BASE_URL,self.query)

    def go(url):
        return requests.get(url,headers=headers).text


    def getinfo(self):
        self.result = []
        self.r = requests.get(self.url,headers=self.headers).text

        for r2 in [r1 for r1 in re.findall(r'<A(.*?)</A>',self.r)]:
            if None if not re.sub(" ","",r2).startswith("HREF") else True:
                if 'style=""' in r2:
                    pass
                else:
                    self.result.append({
                            "name":re.findall(r'TITLE="(.*?)"',r2)[0],
                             "image":re.findall(r'SRC="(.*?)"',r2)[0],
                            "page_id":re.findall(r'(\d+)',r2)[0],
                            }
                            )

        self._r = []


        self.nexturl = []
        for link in self.result:
            try:
                self.nexturl.append(BASE_URL + "characters.php?id={}".format(link["page_id"]))
            except:pass


        pool = Pool(processes=5)
        page_sc = pool.map(anch_db.go,[u for u in self.nexturl])
        self.oke =[]
        self.inter = 0
        for self.su in page_sc:
            self.match = [
                    re.findall('<td>(\d{1,})</td>',self.su)[0],
                    re.findall('<A href="source.*?id=\d{1,}">(.*?)</',self.su)[0],
                    re.findall('<th>\w{5}\s\w{4}</th>\s{1,}<td>(.*?)</td>',self.su)[0],
                    re.findall('.\s{1,}<BR>\s{1,}(.*?)\s{1,}</P>',self.su)[0],
                    re.findall('<A href="animebyyear.php.*?>(.*?)</A>',self.su)[0],
                    ]

            #voiced by if possible list
            self.vmi = [x for x in re.findall(r'<td><a href="va.php.*?va_id=\d{1,}">(.*?)</',self.su)]
            #relations if possible list
            self.rifl = [r for r in re.findall(r'<li><span.*?</a>',self.su)]
            self._r.append({
                "name":self.result[self.inter]["name"],
                "image":self.result[self.inter]["image"],
                "Id":self.match[0],
                "From_Anime":self.match[1],
                "Media_Type":self.match[2],
                "Voiced_By":self.vmi if len(self.vmi) >= 1 else None,
                "Profile":re.sub(r'<.*?>','',self.match[3]),
                'Relations':[re.sub(r'<.*?>','',self.rf_) for self.rf_ in self.rifl] if len(self.rifl) >= 1 else None,
                "Year_Release":self.match[4],})
            self.inter += 1 
            self.oke += self._r

        self.list = []
        for data in self.oke:
            if data not in self.list:
               try:
                 if len(data["Relations"]) >= 1:
                    data["Relations"] = ", ".join(data["Relations"])
               except:pass
               try:
                  if data["Voiced_By"] and None:
                     pass
                  else:
                     data["Voiced_By"] = data["Voiced_By"][0]
               except:pass

               self.list.append(data)

        self.list.append({"r_count":"result found {} of {} ".format(len(self.result),self.query)}) if len(self.result) >= 1 else \
                self.list.append({"r_count":"result not found for {}".format(self.query)})

        return self.list




