#!/usr/bin/python3
#coded by natsuya (https://github.com/nolepeople)

import os
import sys
import re
import logging
import requests
import bs4
import time

logging.basicConfig(format="%(message)s",level=logging.INFO)

BASE_URL = "https://www.animecharactersdatabase.com/"
headers = {
                "Host":"www.animecharactersdatabase.com",
                "Referer":"https://www.animecharactersdatabase.com/searches.php",
                "User-Agent":"Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                }
def banner():
    logging.info("""\033[92m
.-. . . .-. . .   .-.  .-.
|-| |\| |   |-| - |  ) |-)
` ' ' ` `-' ' `   `-'  `-' [@wibuzone_id]\033[97m
anime charaters database
            """)

class anch_db(object):

    def __init__(self,query):
        global BASE_URL,headers
        self.query,self.headers = query,headers
        self.url = "{}searches.php?s={}".format(BASE_URL,self.query)

    def getbasicinfo(self):
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
                            "page_id":re.findall(r'HREF="(.*?)"',r2)[0],
                            }
                            )

        self._r = self.result
        self._r.append({"r_count":len(self.result)}) if len(self.result) >= 1 else \
                self._r.append({"r_count":None})


        if self._r:
            for x in self._r[::-1]:
                if x["r_count"] == None:
                    self._r[0]["r_count"] = "result not found for {}".format(self.query)
                    return self._r
                return self._r

class getotherinfo(anch_db):
    def __init__(self):
        pass

    def find_info(self,page_id):
        self.result = []
        self.url = BASE_URL + page_id
        with requests.Session() as r:
            self.r = r.get(self.url,headers=self.headers).text
            self.pattern = [
                    '<td>(\d{1,})</td>','<A href="source.*?id=\d{1,}">(.*?)</',
                    '<th>\w{5}\s\w{4}</th>\s{1,}<td>(.*?)</td>',
                    '.\s{1,}<BR>\s{1,}(.*?)\s{1,}</P>',
                    '<A href="animebyyear.php.*?>(.*?)</A>',
                    ]

            self.match = []
            for q in self.pattern:
                self.match += re.findall(q,self.r)

            if list(set(self.match)):
                #voiced by if possible list
                self.vmi = [x for x in re.findall(r'<td><a href="va.php.*?va_id=\d{1,}">(.*?)</',self.r)]
                #relations if possible list
                self.rifl = [r for r in re.findall(r'<li><span.*?</a>',self.r)]
                self.result.append({"Id":self.match[0],"From Anime":self.match[1],
                    "Media Type":self.match[3],
                    "Voiced By":self.vmi if len(self.vmi) >= 1 else None,
                    "Profile":re.sub(r'<.*?>','',self.match[4]),
                    'Relations':[re.sub(r'<.*?>','',self.rf_) for self.rf_ in self.rifl] if len(self.rifl) >= 1 else None,
                    "Year Release":self.match[5],
                   })

            return self.result

    def display_for_cli(self,rlist):
        self.rl_ = rlist[0]
        try:
            if self.rl_["Voiced By"] and None:
                pass
            else:
                self.rl_["Voiced By"] = self.rl_["Voiced By"][0]
            if self.rl_["Relations"] and None:
                pass
            else:
                self.rl_["Relations"] = self.rl_["Relations"][0]
        except:pass

        printf = """
[ID] {}
    - from anime   : {} 
    - media type   : {}
    - voiced by    : {}
    - year release : {}
    - relations    : {}
    - profile      : {}     """.format(
            self.rl_["Id"],self.rl_['From Anime'],self.rl_['Media Type'],
            self.rl_["Voiced By"],self.rl_["Year Release"],
            self.rl_["Relations"],self.rl_["Profile"]
             )
        return printf


class main(object):
    banner()

    def __init__(self,query):
        anch_db.__init__(self,query)
        self.result = anch_db(query).getbasicinfo();del self.result[-1]
        if len(self.result) >= 1:
            logging.info("[INFO] {} found result of {} \n".format(len(self.result),query))
            time.sleep(1)
        else:
            sys.exit(logging.info("[INFO] result not found of {}".format(self.query)))
        i = 0
        for select in self.result:
            print ("[{}]".format(i),select["name"]);i+=1
        self.ns = input("{}\n[-] Which one are you curious, buddy? ".format("-"*20))
        self.rlist = getotherinfo.find_info(self,self.result.pop(int(self.ns))['page_id'])
        print (getotherinfo.display_for_cli(self,self.rlist))


if __name__=="__main__":
   try:
      main(sys.argv[1])
   except IndexError:
        sys.exit("usage: .py <query>\nwhat is the name on your mind?\n")





