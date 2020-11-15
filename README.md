![Screenshot](.img/image1.png)
## about anch-db
This is a tool to scan anime characters along with a little information. 
This is the result of scraping from website <a href="animecharactetsdatabase.com">here</a>

*because the api server from the default web has limited requests even though it can be 
handled with the express js module here with python can be free without limitations.
## Example Result
![Screenshot](.img/image2.png)

web based ? <a href="wbzncode.herokuapp.com/AnimeCharactersDatabase">wibuzone.code</a><br>
You can use it as a module in lib/ moduled.py if you can't compose it for your website. 

^ from modulename import anch_db 
^ anchdb.getinfo(your query)<br>

with a return as below
![Screenshot](.img/yo.png)
## module needed
* pip3 install requests
  
