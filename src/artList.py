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

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt

class ArtTagModel(QtGui.QStringListModel):
    def __init__(self, parent, datastore):
        QtGui.QStringListModel.__init__(self,parent)
        
        self.datastore = datastore
        self.sl = []
                
        self.setStringList(sorted(self.datastore.tags))
        def tagschanged():
            self.setStringList(sorted(self.datastore.tags))
        self.datastore.event_tagsChanged.subscribe(tagschanged)
        
        
    def flags(self, index):
        sf = QtGui.QStringListModel.flags(self,index)
        
        #return sf
        return sf ^ Qt.Qt.ItemIsEditable
    
    def getTag(self, index):
        return unicode(self.data(index,Qt.Qt.EditRole).toString())
        
        


class ArtTagList(QtGui.QListView):
    def __init__(self, parent = None):
        QtGui.QListView.__init__(self,parent)
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.sl = []
    def addTagSelectionListener(self, listener):
        self.sl.append(listener)
        
    def getSeletedTags(self):        
        return [self.model().getTag(i) for i in self.selectedIndexes()]
    
    def selectionChanged (self, selected, deselected ):
        QtGui.QListView.selectionChanged(self,selected, deselected)
        stags = self.getSeletedTags()
        for l in self.sl:
            l(stags)
    
     
        
    
    