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

from datastore import Article
from datastore import loadArticleStoreFromFolder
from operator import ipow
import sys
from PyQt4 import QtCore, QtGui, Qt
from datastore import *



class ArtGridModel(QtCore.QAbstractTableModel):

    
    def setOrMode(self, b):
        self._ormode = b                        

    def getArticle(self, index):
        return self._store2D.getArticle(index.row())
    
    def filter(self, tags):
        self._filterTags = tags
        self._store2D.filterTags(tags, self._ormode)
        self.reset()
        #self.emit(QtCore.SIGNAL("dataChanged"), None, None)
        
    def _ArtGridModel__refresh(self):
        self._store2D = Store2D(self._store)
        self._store2D.filterTags(self._filterTags, self._ormode)
        self.reset()

    def __init__(self, parent, articleStore):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ["name","origname","tags"]
        self._store = articleStore
        self._store2D = Store2D(articleStore)
        self._ormode = False;
        self._filterTags = []
        self._store.event_dataChanged.subscribe(self._ArtGridModel__refresh)


    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headers[section])
        return QtCore.QVariant()
    def setData(self, index, value, role):
        if (index.isValid() and role == QtCore.Qt.EditRole):
            val = value.toString()
            self._store2D.set(index.row(), index.column(), val)            
            self.emit(QtCore.SIGNAL("dataChanged ( const QModelIndex & , const QModelIndex & )"), index, index)            
            return True
        return False
    def flags(self, index):
        sf = QtCore.QAbstractTableModel.flags(self,index)
        if(index.column()!=1):
            return sf | Qt.Qt.ItemIsEditable
        return sf

    def rowCount(self, parent):
        if parent.isValid(): 
            return 0
        return self._store2D.getcount()
    def columnCount(self,parent):
        if parent.isValid(): 
            return 0
        return 3
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return QtCore.QVariant(QtCore.QString(self._store2D.get(index.row(), index.column())))

        return QtCore.QVariant()
    
class Store2D(object):
    def __init__(self, articleStore):
        self._artdict = articleStore.articles
        self._filtredartdict = self._artdict           
        self.gettermap = {
        0: lambda a: a.name,
        1: lambda a: a.origname,
        2: lambda a: a.getTagsString(),
        }
    def get(self, x, y):
        article = self._filtredartdict.values()[x]
        return self.gettermap[y](article)
    def getArticle(self, x):
        return self._filtredartdict.values()[x]
    def getcount(self):
        return len (self._filtredartdict.values())
    def set(self, x,y, val):
        article = self._filtredartdict.values()[x]
        if y ==0:
            # @type article Article
            article.name = unicode(val)
        elif y == 2:
            # @type val str
            #article.tags =[unicode(s).strip() for s in val.split(",")]
            article.setTagsString(val)
    def filterTags(self, tags, orMode ):                       
        if tags != []:           
            def containsany(a,b):                
                for e in a:
                    if e in b:                        
                        return True                
                return False
            contf = lambda a,b: set(b).issubset(set(a))                
            if orMode:
                contf = containsany                    
                             
            self._filtredartdict =  dict( [ (item, self._artdict[item] ) for item in self._artdict if contf(self._artdict[item].tags, tags)])
        else:
            self._filtredartdict = self._artdict

