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

class Event(object):
    def __init__(self):
        self.handlers = set()

    def subscribe(self, handler):
        self.handlers.add(handler)
        return self

    def unsubscribe(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unsubscribe it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = subscribe
    __isub__ = unsubscribe
    __call__ = fire
    __len__  = getHandlerCount
    
def createAction(parent, name, action, shortcut = None):    
        act = QtGui.QAction(name, parent)        
        act.connect(act, QtCore.SIGNAL("triggered()"), action)
        return act

def createActionSlot(parent, name, target,slot, shortcut = None):    
        act = QtGui.QAction(name, parent)        
        act.connect(act, QtCore.SIGNAL("triggered()"), target, slot)
        return act
