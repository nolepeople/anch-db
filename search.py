import sys
from module import AnimeCharaDB as animecdb

if __name__=="__main__":
   try:
     search = animecdb.search(sys.argv[1])
     result = search.getcontent()
     for s in result:
         print ("""!: name ({})\n!: image ({})\!:nother info (https://animecharacterdatabase.com/{})
            """.format(s['name'],s['image'],s['page_id']));print ("-"*25)

   except IndexError:
        sys.exit("!: search.py <query>\n!: @wibuzone_id")
