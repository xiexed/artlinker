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

from PyQt4 import QtCore, QtGui, Qt

class AutoLE(QtGui.QLineEdit):
    def __init__(self, parent = None):
        QtGui.QLineEdit.__init__(self, parent)
        self.cl =QtCore.QStringList([])
        self._AutoLE__lastmatched = ""

    def _AutoLE__getUnselected(self):
        ct = self.text()
        if self.selectedText():
            ct.replace(self.selectionStart(), len(self.selectedText()), "")
        
        return ct


    def _AutoLE__completeWith(self, t, startposition, match):
        compl = match[len(t):]
        finishposition = startposition + len(compl)
        self.setText(self._AutoLE__getUnselected() + compl)
        self.setCursorPosition(startposition)
        self.setSelection(startposition, finishposition)


    def _AutoLE__getTextToComplete(self):
        ct = self._AutoLE__getUnselected()
        t = ct.split(',')[-1].trimmed()
        startposition = len(ct)
        return t, startposition

    
    def _AutoLE__getMatchingComletations(self, st):
        if not st:
            return [] 
#        for x in self.cl:            
#            if x.startsWith(st):
#                print x, "starts with ", st
#            else:
#                print x, "dosnt start with ", st  
        return [x for x in self.cl if x.startsWith(st)]  
    
        
    
    def keyPressEvent(self, event ):
        QtGui.QLineEdit.keyPressEvent(self, event)
        
        if QtCore.QRegExp("\w").exactMatch(event.text()):
            #print "event.text()=",event.text()
            t, startposition = self._AutoLE__getTextToComplete()
            #print "t=",t
            matches = self._AutoLE__getMatchingComletations(t)            
            #print "matches=",matches
            if matches:
                self._AutoLE__lastmatched = matches[0]                
                self._AutoLE__completeWith(t, startposition, matches[0])
                
        elif event.key()==Qt.Qt.Key_Return and self.selectedText():
            self.setCursorPosition(self.selectionStart()+len(self.selectedText()))
            
        elif event.key()==Qt.Qt.Key_Down or event.key()==Qt.Qt.Key_Up:
            t, startposition = self._AutoLE__getTextToComplete()
            matches = self._AutoLE__getMatchingComletations(t)            
            if matches and (self._AutoLE__lastmatched in matches):
                i = matches.index(self._AutoLE__lastmatched)
                if event.key()==Qt.Qt.Key_Down:
                    i=i+1
                if event.key()==Qt.Qt.Key_Up:
                    i=i-1                
                if i>=len(matches):
                    i=0
                if i<0:
                    i=len(matches)-1                         
                self._AutoLE__lastmatched = matches[i]
                self._AutoLE__completeWith(t, startposition, matches[i])                                           
                
            
                
        
            
    def setCompletationList(self, cl):
        self.cl =QtCore.QStringList([x for x in cl])
            
        
        
        
        
        

        