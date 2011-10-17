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

from artList import ArtTagList, ArtTagModel

__author__="nickl"
__date__ ="$03.09.2009 19:56:40$"

from datastore import Article
from datastore import loadArticleStoreFromFolder
from operator import ipow
import sys
from PyQt4 import QtCore, QtGui, Qt
from datastore import *

from artGridModel import ArtGridModel
from pyutils import *



class UI_FilesView(QtGui.QTreeView):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self,parent)
          #        self.setStyleSheet("""
#         QTreeView::item {       border: 1px solid #d9d9d9;
#                                 border-top-color: transparent;
#                                 border-right-color: transparent;
#                                 border-left-color: transparent;
#                         }
#        """)      
#        class ItemDelegate(QtGui.QItemDelegate):
#            def __init__(self, parent = None):
#                QtGui.QItemDelegate.__init__(self, parent)
                 
#        id =  self.itemDelegate()
#        def sizeHint (option,index ):
#            print "called"
#            QtGui.QStyledItemDelegate.sizeHint(id,option,index )            
#            return QtCore.QSize(20,20); 
#        id.sizeHint = sizeHint
        self.setItemDelegate(MyItemDelegate(self))
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setColumnWidth(0, 260)
        self.setColumnWidth(1, 150)
        self.setUniformRowHeights(True)

        self.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked)
        self.setItemsExpandable(False)
    
class MyItemDelegate(QtGui.QStyledItemDelegate): 
    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self,parent)
    def sizeHint (self,option,index ):        
        oqs=QtGui.QStyledItemDelegate.sizeHint(self,option,index )            
        return QtCore.QSize(oqs.width(),20);  
    
    
 
class FilesView(UI_FilesView):
    def __init__(self, store, parent = None):
        UI_FilesView.__init__(self,parent)
        
        self.store = store
        
        self.artmodel = ArtGridModel(self, self.store)
        
        self._FilesView__proxyModel = QtGui.QSortFilterProxyModel()
        self._FilesView__proxyModel.setDynamicSortFilter(True)
        self._FilesView__proxyModel.setSourceModel(self.artmodel)
        
        
        self.setModel(self._FilesView__proxyModel)        
        self.doubleClicked.connect(self._FilesView__openfile)
        
        def keypressed(e):
            QtGui.QTreeView.keyPressEvent(self,e)            
            if e.key()==Qt.Qt.Key_Return:
                if not self.filesView.state() == QtGui.QAbstractItemView.EditingState:
                    sm = self.filesView.selectionModel()
                    if sm.hasSelection ():                                                
                        self._FilesView__openfile(sm.selectedRows()[0])
            
        self.keyPressEvent = keypressed
        self.event_articleselected = Event()        
        
        sm = self.selectionModel()        
              
        #self.connect(sm, QtCore.SIGNAL("selectionChanged ( const QItemSelection &, const QItemSelection &  )"), onSelectionChanged)                
        print("connecting")
        self.connect(sm, QtCore.SIGNAL("selectionChanged ( const QItemSelection &, const QItemSelection &  )"), self._FilesView__onSelectionChanged)
        print("connected")                
    
    
    def _FilesView__onSelectionChanged(self,s,ds):            
            if len(s)>0:
                index = self.selectedIndexes()[0]
                article = self.artmodel.getArticle(self._FilesView__proxyModel.mapToSource(index))
                self.event_articleselected(article)      
        
    def _FilesView__openfile(self, index):
        a = self.artmodel.getArticle(self._FilesView__proxyModel.mapToSource(index))
        #a = self.artmodel.getArticle(index)
        
        import os
        folder = self.store.folder
        filepath = folder+os.sep+ a.origname
        if os.name == 'nt':
            os.startfile(filepath)
        else:
            prog = u"xdg-open" 
            command = prog+u" \""+ filepath +u"\""
            print command.encode('utf8')
            os.system(command.encode('utf8')) 
        
             
