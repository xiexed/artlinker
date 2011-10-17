#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 or version 3 of the License
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#     Contributor(s):
#       Nickl Mitropolsky <lkuka@mail.ru> (original author)

import os
import sys
import pickle
import json
from pyutils import Event


class Article(object):
    def __init__(self, name = "", origname = "", tags = [], descr = ""):
        self.name = name
        self.origname = origname
        self.tags = tags
        self.descr = descr         
    
    def getTagsString(self):
        return ", ".join(self.tags)
    
    def setTagsString(self,tstr):
        self.tags =[unicode(s).strip() for s in tstr.split(",")]
   
class ArticleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Article):
            return {"name":obj.name, "orig":obj.origname, "tags":obj.tags, "descr":obj.descr }
        return json.JSONEncoder.default(self, obj)     


def loadArticleStoreFromFolder(folder):
    store = ArticleStore()
    store._loadFromFolder(folder)
    return store


filename = "pickle.tags"
jsonfilename = "json.tags"
class ArticleStore(object):
    def __init__(self):
        self.event_dataChanged = Event()
        self.event_tagsChanged = Event()
      
    def saveAndReload(self):
        self.savedata()
        self._loadFromFolder(self.folder)
        self.event_dataChanged()
        self.event_tagsChanged()  

    def _loadFromFolder(self, folder):
        self.folder=folder

        pickled = dict()
#       
        if os.path.isfile(self.folder+os.sep+jsonfilename):     
            def as_Artilce(dct):
                if 'tags' in dct:                    
                    return Article(dct["name"], dct["orig"], dct["tags"], dct["descr"])
                return dct
            
            f = open(self.folder+os.sep+jsonfilename, "rt")
            pickled = json.load(f, encoding="UTF8",  object_hook=as_Artilce)
            f.close()
        elif os.path.isfile(self.folder+os.sep+filename):
            f = open(self.folder+os.sep+filename, "rb")
            pickled = pickle.load(f)
            f.close()     

        fromdir = set()
        for e in os.listdir(folder):
            # @type e str
            r = e 
            
            if not r.endswith(".tags"):
                fromdir.add(r)

        # @type pickled dict
        for orig in pickled.keys():
            if orig not in fromdir:
                print orig," not in dir"
                del pickled[orig]

        for orig in fromdir:
            if orig not in pickled.keys():
                print orig," not in picled, new item created"
                pickled[orig] = Article("",orig,[],"")
       
        self.articles = pickled
        self.__buildtags()

    def savedata(self):        
        file = open(self.folder+os.sep+jsonfilename, "wt")
        json.dump(self.articles, file, ensure_ascii = False,cls = ArticleEncoder,indent = 3)
        file.close()           
    
    def __buildtags(self):
        self.tags = set()
        for article in self.articles.values():
            for tag in article.tags:
                self.tags.add(tag)

