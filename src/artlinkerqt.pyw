#! /usr/bin/python
# -*- coding: utf-8 -*-

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
from mainwndview import open_settings

__author__ = "nickl"
__date__ = "$03.09.2009 19:56:40$"

import sys;

reload(sys);
sys.setdefaultencoding("utf8")

from datastore import Article
from datastore import loadArticleStoreFromFolder
from operator import ipow
import sys
from PyQt4 import QtCore, QtGui, Qt
from datastore import *

from artGridModel import *
from mainwndview import Ui_MainWnd
from filesView import FilesView


class ArtLinker(Ui_MainWnd):
    def __init__(self, path, parent=None):
        Ui_MainWnd.__init__(self, parent)

        self.store = loadArticleStoreFromFolder(path)
        settings = open_settings()
        history = settings.value("history", type='QStringList')
        history.prepend(path)
        settings.setValue("history", history[0:5])
        settings.sync()
        del settings

        self.filesView = FilesView(self.store, self)

        self.artList = ArtTagList(self)

        self.setupUI()

        self.genTagsDockWiew()
        self.genArticleDockWiew()



        #dock = self.genArticleDockView()
        #self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)  

        self.createMenus()
        self.setWindowTitle(self.tr("ArtLinker"))


    def genTagsDockWiew(self):
        def andorstateschanged(val):
            self.filesView.artmodel.setOrMode(val == Qt.Qt.Checked)
            self.filesView.artmodel.filter(self.artList.getSeletedTags())

        self.connect(self.andorbutton, QtCore.SIGNAL("stateChanged (int)"), andorstateschanged)
        artTagModel = ArtTagModel(self, self.store)
        self.artList.addTagSelectionListener(self.filesView.artmodel.filter)
        self.artList.setModel(artTagModel)


    def saveCurArticleData(self):
        if self.articleView.curarticle is not None:
            self.articleView.curarticle.name = unicode(self.articleView.nameLineEdit.text())
            self.articleView.curarticle.setTagsString(self.articleView.tagsLineEdit.text())
            self.articleView.curarticle.descr = unicode(self.articleView.descrTextEdit.toPlainText())


    def genArticleDockWiew(self):
        def setArticleData(article):
            self.articleView.nameLineEdit.setText(article.name)
            self.articleView.tagsLineEdit.setText(article.getTagsString())
            self.articleView.descrTextEdit.setPlainText(article.descr)

        def refreshArticleData():
            setArticleData(self.articleView.curarticle)

        def onSelectionChanged(article):
            self.saveCurArticleData()

            self.articleView.curarticle = article
            setArticleData(article)

        self.filesView.event_articleselected.subscribe(onSelectionChanged)

        self.articleView.tagsLineEdit.setCompletationList(self.store.tags)

        def tagschanged():
            self.articleView.tagsLineEdit.setCompletationList(self.store.tags)

        self.store.event_tagsChanged.subscribe(tagschanged)

        self.connect(self.filesView.artmodel,
            QtCore.SIGNAL("dataChanged ( const QModelIndex & , const QModelIndex & )"), refreshArticleData)


    def savedata(self):
        self.saveCurArticleData()
        self.store.savedata()

    def reloaddata(self):
        self.saveCurArticleData()
        self.store.saveAndReload()

    def createMenus(self):
        self.openAct.triggered.connect(self.open)
        self.connect(self.saveAct, QtCore.SIGNAL("triggered()"), self.savedata)
        self.connect(self.reloadAct, QtCore.SIGNAL("triggered()"), self.reloaddata)

    def open(self):
        fd = QtGui.QFileDialog(self)
        fd.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        if fd.exec_():
            pathToOpen = fd.selectedFiles()[0]
            new_wnd = ArtLinker(pathToOpen)
            self.close()
            new_wnd.show()


    def closeEvent(self, event):
        Ui_MainWnd.closeEvent(self, event)
        if self.autosaveAct.isChecked():
            self.savedata()


if __name__ == "__main__":
    pathToOpen = None
    if len(sys.argv) > 1:
        pathToOpen = unicode(sys.argv[1].decode(sys.getfilesystemencoding() or sys.getdefaultencoding()))

    if pathToOpen is None:
        settings = open_settings()
        print settings.fileName()
        prev = settings.value("history", type='QStringList')
        if len(prev) > 0:
            pathToOpen = prev[0]

    app = QtGui.QApplication(sys.argv)

    if pathToOpen is None:
        fd = QtGui.QFileDialog()
        fd.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        if fd.exec_():
            pathToOpen = fd.selectedFiles()[0]
        fd.destroy()

    if pathToOpen is None:
        print("no files selected")
        exit(1)


    imageViewer = ArtLinker(pathToOpen)
    imageViewer.show()
    sys.exit(app.exec_())

#    mainwnd = QtGui.QMainWindow()
#    Ui_MainWindow().setupUi(mainwnd)
#    mainwnd.show()


    

