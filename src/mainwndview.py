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

from artList import ArtTagList, ArtTagModel
import re
from filesView import FilesView
from autocmplLE import AutoLE

class Ui_MainWnd(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)



    
    def setupUI(self):
        
        self._Ui_MainWnd__createFilesView() 
        self._Ui_MainWnd__createTagsDockView()
        self._Ui_MainWnd__genArticleDockView()
        
        self._Ui_MainWnd__createMenu()
        
        self._Ui_MainWnd__readSettings() 
        
    def _Ui_MainWnd__createMenu(self):
        self.reloadAct = QtGui.QAction(self.tr("&Reload"), self)
        self.reloadAct.setShortcut(self.tr("Ctrl+R"))
        
        self.autosaveAct = QtGui.QAction(self.tr("&Auto Save On Exit"), self)
        self.autosaveAct.setCheckable(True)
        self.autosaveAct.setChecked(True)
                 
        
        self.saveAct = QtGui.QAction(self.tr("&Save"), self)
        self.saveAct.setShortcut(self.tr("Ctrl+S"))        
        self.exitAct = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.fileMenu.addAction(self.reloadAct)
        self.fileMenu.addAction(self.autosaveAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        
        
        viewMenu = QtGui.QMenu(self.tr("&View"), self)
        
        
        
        def createShow(name, dock):
            action = QtGui.QAction(self.tr(name), self)
            action.setCheckable(True)
            
            def onShowTagsClick():
                if action.isChecked():                
                    dock.show()
                else:
                    dock.hide()             
            self.connect(action, QtCore.SIGNAL("triggered()"), onShowTagsClick)
            self.connect(dock, QtCore.SIGNAL("visibilityChanged ( bool )"),
                          action, QtCore.SLOT("setChecked( bool )"))
            return action
        
        viewMenu.addAction(createShow("&Show Tags",self._Ui_MainWnd__tagsdock)) 
        viewMenu.addAction(createShow("&ShowArticles",self._Ui_MainWnd__articlesdock)) 
         
        self.helpMenu = QtGui.QMenu(self.tr("&Help"), self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(viewMenu)
        self.menuBar().addMenu(self.helpMenu)
        
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("close()"))
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"), self.about)
        self.connect(self.aboutQtAct, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("aboutQt()"))



    def _Ui_MainWnd__createTagsDockView(self):
        self._Ui_MainWnd__tagsdock = QtGui.QDockWidget(self.tr("Tags"), self)
        self._Ui_MainWnd__tagsdock.setObjectName("TagsDock")
        self._Ui_MainWnd__tagsdock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        dockpanellayout = QtGui.QVBoxLayout()
        dockpanellayout.setContentsMargins(0, 0, 0, 0)
        ttagswidget = QtGui.QWidget()        
        self.andorbutton = QtGui.QCheckBox(self.tr("\"or\" mode"))
        dockpanellayout.addWidget(self.andorbutton)
        dockpanellayout.addWidget(self.artList)
        ttagswidget.setLayout(dockpanellayout)
        self._Ui_MainWnd__tagsdock.setWidget(ttagswidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._Ui_MainWnd__tagsdock)
        
    def _Ui_MainWnd__genArticleDockView(self):
        self._Ui_MainWnd__articlesdock = QtGui.QDockWidget(self.tr("Article"), self)
        self._Ui_MainWnd__articlesdock.setObjectName("ArticlesDock")
        self._Ui_MainWnd__articlesdock.setFeatures(QtGui.QDockWidget.DockWidgetClosable |QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)        
        self.articleView = QtGui.QWidget()
        self.articleView.curarticle = None             
        dockpanellayout = QtGui.QVBoxLayout()
        dockpanellayout.setMargin(0)        
        formLayout = QtGui.QFormLayout()        
        self.articleView.nameLineEdit = QtGui.QLineEdit()        
        formLayout.addRow(self.tr("name"),self.articleView.nameLineEdit)
        self.articleView.tagsLineEdit = AutoLE()       
        formLayout.addRow(self.tr("tags"),self.articleView.tagsLineEdit)
        dockpanellayout.addLayout(formLayout)
        label = QtGui.QLabel("Description")        
        dockpanellayout.addWidget(label)
        self.articleView.descrTextEdit = QtGui.QPlainTextEdit()        
        dockpanellayout.addWidget(self.articleView.descrTextEdit)
        
        
        self.articleView.setLayout(dockpanellayout)
        self._Ui_MainWnd__articlesdock.setWidget(self.articleView)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self._Ui_MainWnd__articlesdock)
    
    
    def _Ui_MainWnd__readSettings(self):
        settings = QtCore.QSettings("Nickl", "ArtLinker")
        pos = settings.value("pos", QtCore.QVariant(QtCore.QPoint(200, 200))).toPoint()
        size = settings.value("size", QtCore.QVariant(QtCore.QSize(800, 400))).toSize()                      
        self.restoreState(settings.value("mainwnd").toByteArray ())
        self.resize(size)
        self.move(pos)
        self.autosaveAct.setChecked(settings.value("autosave", QtCore.QVariant(True)).toBool())  
        self.setWindowState(Qt.Qt.WindowState(settings.value("wndstate",QtCore.QVariant(0)).toInt()[0]))      
        self.filesView.header().restoreState(settings.value("grid/headerstate").toByteArray ())

    def _Ui_MainWnd__writeSettings(self):
        settings = QtCore.QSettings("Nickl", "ArtLinker")
        if not self.isMaximized():
            settings.setValue("pos", QtCore.QVariant(self.pos()))
            settings.setValue("size", QtCore.QVariant(self.size()))
        settings.setValue("autosave", QtCore.QVariant(self.autosaveAct.isChecked())) 
        settings.setValue("wndstate", QtCore.QVariant(int(self.windowState()))) 
        settings.setValue("mainwnd", QtCore.QVariant(self.saveState ())) 
        settings.setValue("grid/headerstate", QtCore.QVariant(self.filesView.header().saveState ()))    
        
    def _Ui_MainWnd__createFilesView(self):        
        self.setCentralWidget(self.filesView)

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About ArtLinker"), self.tr("""                                                                          
ArtLinker provides simple Crossplatform GUI to organize files by tags in single directory

It is a simple file-tagging program, written in PyQt. I\'ve created it to organize scientific articles in my research work. But it obviously could be used with any file type.
Nicolay Mitropolsky <lkuka@mail.ru>
"""))


    def maybeSave(self):
        return True
        
    def closeEvent(self, event):
        if self.maybeSave():
            self._Ui_MainWnd__writeSettings()
            event.accept()
        else:
            event.ignore()
        