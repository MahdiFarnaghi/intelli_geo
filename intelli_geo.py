# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IntelliGeo
                                 A QGIS plugin
 IntelliGeo is QGIS plugin that facilitates interaction with Large Language Models in QGIS environment
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2024 by GIP Department, Faculty ITC, University of Twente
        email                : m.farnaghi@utwente.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# from PyQt5.QtWebEngineWidgets import QWebEngineView
import subprocess
import sys
import os
import asyncio

try:
    import langchain_cohere, langchain_openai, langchain
    import requests, psutil
    from bs4 import BeautifulSoup
except:
    # Path to your requirements.txt file
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    requirementsPath = os.path.join(scriptDir, 'requirements.txt')
    # Run the pip install command
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirementsPath])

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QThread, QTimer, pyqtSignal
from qgis.PyQt.QtGui import QIcon, QTextCursor, QClipboard
from qgis.PyQt.QtWidgets import QAction, QDialog, QPushButton, QWidget, QPlainTextEdit, QDockWidget, QApplication
from qgis.utils import iface

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .intelli_geo_dockwidget import IntelliGeoDockWidget
import os.path
import re
from qasync import QEventLoop

# https://github.com/qgis/QGIS/tree/master/python/console
# import 'console' folder in QGIS python package
import console
# import 'processing' folder in QGIS pytho package
from processing.modeler.ModelerDialog import ModelerDialog

# Import code for edit dialog
from .digNewEditConversation import NewEditConversationDialog

# Import plugin utilities
from .dataloader import Dataloader
from .conversation import Conversation
from .utils import generateUniqueID, getCurrentTimeStamp, pack, show_variable_popup, extractCode, getVersion
from .retrievalVectorbase import RetrievalVectorbase
from .debugDialog import DebugDialog

from .environment import QgisEnvironment


class IntelliGeo:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'IntelliGeo_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&IntelliGeo')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'IntelliGeo')
        self.toolbar.setObjectName(u'IntelliGeo')

        #print "** INITIALIZING IntelliGeo"

        self.pluginIsActive = False
        self.dockwidget = None
        self.editdialog = None
        self.liveConversationID = None
        self.liveConversation = None

        # create sqlite database
        self.dataloader = Dataloader("IntelliGeo.db")

        version = getVersion()
        self.retrievalVectorbase = RetrievalVectorbase(version)

        self.consoleText = ""
        self.consoleTracker = QTimer()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('IntelliGeo', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/intelli_geo/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Open IntelliGeo'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING IntelliGeo"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False
        self.dataloader.close()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD IntelliGeo"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&IntelliGeo'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        # Initialization
        if not self.pluginIsActive:

            self.pluginIsActive = True

            # print "** STARTING IntelliGeo"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = IntelliGeoDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

            self.dataloader.connect()

            # connect push button send to onNewMessageSend action
            self.dockwidget.pbSend.clicked.connect(self.onNewMessageSend)
            self.dockwidget.enterPressed.connect(self.onNewMessageSend)

            # connect push button delete to onConversationDeleted action
            # self.dockwidget.pbDelete.clicked.connect(self.onConversationDeleted)

            # connect push button edit to onConversationEdited action
            # self.dockwidget.pbEdit.clicked.connect(self.onConversationEdited)

            # connect push button 'pbNew' to onConversationNewed action
            self.dockwidget.pbNew.clicked.connect(self.onConversationNewed)

            # connect push button 'pbSearchConversationCard' to onSearchConversationCard action
            self.dockwidget.pbSearchConversationCard.clicked.connect(self.onSearchConversationCard)
            self.dockwidget.searchPressed.connect(self.onSearchConversationCard)

            self.dockwidget.switchClearMode.connect(self.switchClearMode)

            # a bit functional?
            slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
            self.dockwidget.displayConversationCard(self.dataloader, slotsFunctions)

    def onNewMessageSend(self):
        message = self.dockwidget.ptMessage.toPlainText()
        if message == "":
            return

        # Conversation: If no live conversation then create one
        if self.liveConversation is None:
            self.onConversationNewed()

        # Dock Interface: Clear message plainTextEdit
        self.dockwidget.ptMessage.clear()

        # Dock Interface: Get response mode
        if self.dockwidget.rbtVisualModel.isChecked():
            responseType = "Visual mode"
        else:
            responseType = "Code"

        if self.liveConversation is not None:
            self.liveConversation.llmResponse.connect(self.onNewResponseReceived)
            self.liveConversation.updateUserPrompt(message, responseType)
            self.dockwidget.disableAllButtons()
            self.dockwidget.disableAllTextEdit()

    def onNewResponseReceived(self, response, workflow, modelPath):
        if self.liveConversation is not None:
            self.dockwidget.enableAllButtons()
            self.dockwidget.enableAllTextEdit()
            self.liveConversation.llmResponse.disconnect(self.onNewResponseReceived)
            # Python Console Interface: Load python code from response
            if workflow == "withCode":
                code = extractCode(response)
                self.consoleText = self.activateConsole(code, False)
                self.startConsoleTracker()

            # Graphic Modeler Interface: Load .model3 from storage
            if workflow == "withModel":
                self.activeGraphicDesigner(modelPath, False)

            # Dock Interface: Update log & general information
            self.dockwidget.updateConversation(self.liveConversation)
            self.dockwidget.updateGeneralInfo(self.liveConversation)

            # Dock Interface: Update conversation cards
            slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
            self.dockwidget.updateConversationCard(self.liveConversation.metaInfo, slotsFunctions)

            # Dataloader: Update meta-information
            self.dataloader.updateConversationInfo(self.liveConversation.metaInfo)

    def onConversationNewed(self):
        if self.editdialog is None or not self.editdialog.isVisible():
            self.editdialog = NewEditConversationDialog(self.dataloader.llmFullDict, self.dataloader.fetchAllConfig())
            self.editdialog.show()
            if self.editdialog.exec_() == QDialog.Accepted:
                # The dialog was accepted, handle the data if needed
                title, description, llmID, endpoint, apiKey = self.editdialog.onUpdateMetadata()
                created = getCurrentTimeStamp()
                modified = created
                sessionID, _ = self.dataloader.loadCredential()
                self.liveConversationID = f"{sessionID}_" + generateUniqueID()

                metaInfo = pack((self.liveConversationID, llmID, title, description,
                                 created, modified, 0, 0, f"{sessionID}"),
                                "conversation")

                # Dataloader: Create corresponding table in database & update apikey
                self.dataloader.createConversation(metaInfo)
                self.dataloader.updateAPIKey(apiKey, llmID)

                # Conversation: Update live conversation to new conversation
                self.liveConversation = Conversation(self.liveConversationID, self.dataloader, self.retrievalVectorbase)

                # update dock widget
                self.dockwidget.twTabs.setCurrentWidget(self.dockwidget.tbMessages)
                self.dockwidget.updateConversation(self.liveConversation)
                self.dockwidget.updateGeneralInfo(self.liveConversation)

                slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
                self.dockwidget.addConversationCard(metaInfo, slotsFunctions)

    def onConversationLoad(self, conversationID):
        # TODO: test, to be removed
        qgis = QgisEnvironment()
        qgis.refresh()
        info = qgis.getLayerAttributes()

        # Conversation: Load or create conversation
        self.liveConversationID = conversationID
        self.liveConversation = Conversation(conversationID, self.dataloader, self.retrievalVectorbase)
        self.liveConversation.lastEdit = getCurrentTimeStamp()

        # Dataloader: Sync meta-information to database
        self.dataloader.updateConversationInfo(self.liveConversation.metaInfo)

        # Dock Interface: Change the order of the Conversation Cards
        slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
        self.dockwidget.updateConversationCard(self.liveConversation.metaInfo, slotsFunctions)
        # Dock Interface: Switch to dock 'Conversations' & refresh the content
        self.dockwidget.twTabs.setCurrentWidget(self.dockwidget.tbMessages)
        self.dockwidget.updateConversation(self.liveConversation)
        self.dockwidget.updateGeneralInfo(self.liveConversation)

    def onConversationDeleted(self, conversationID: str) -> None:
        """
        Handle logic when a conversation is deleted.
        Drop table in database, and clear Interface in both 'Message' tab and 'Conversations' tab.
        """

        # Dataloader: Drop the rows in "conversation" and "interaction" table
        self.dataloader.deleteConversation(conversationID)

        if self.liveConversationID == conversationID:
            if self.liveConversation is not None:
                # Conversation: set live conversation to None if deleted
                self.liveConversation = None

            # Dock Interface: Clear 'Messages' Tab content
            self.dockwidget.txHistory.clear()
            self.dockwidget.lbTitle.clear()
            self.dockwidget.lbDescription.clear()
            self.dockwidget.lbMetadata.clear()
            # Dock Interface: Remove conversation card correlated with live conversation
            self.dockwidget.removeConversationCard(conversationID)

        else:
            # Dock Interface: Remove conversation card correlated with deleted conversation
            self.dockwidget.removeConversationCard(conversationID)

    def onConversationEdited(self, conversationID: str) -> None:

        # New/Edit Dialog Interface: If no dialog, create one
        if self.editdialog is None or not self.editdialog.isVisible():
            editConversation = Conversation(conversationID, self.dataloader, self.retrievalVectorbase)
            self.editdialog = NewEditConversationDialog(self.dataloader.llmFullDict,
                                                        self.dataloader.fetchAllConfig(),
                                                        editConversation.title,
                                                        editConversation.description,
                                                        editConversation.llmID)
            self.editdialog.show()

            if self.editdialog.exec_() == QDialog.Accepted:
                # Conversation: Dialog was accepted, update conversation meta-information
                editConversation.title, editConversation.description, llmID, _, apiKey = self.editdialog.onUpdateMetadata()
                editConversation.lastEdit = getCurrentTimeStamp()

                # the information don't have to be about liveConversation
                # so I let the argument unpacked and exposed for now

                # Dataloader: Update meta-information
                self.dataloader.updateConversationInfo(editConversation.metaInfo)
                self.dataloader.updateAPIKey(apiKey, llmID)

                # Dock Interface: If editing live conversation, update general information in 'Messages' Tab
                if conversationID == self.liveConversationID:
                    self.liveConversation = editConversation
                    self.dockwidget.updateGeneralInfo(self.liveConversation)

                # Dock Interface: Update corresponding conversation card
                slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
                self.dockwidget.updateConversationCard(editConversation.metaInfo, slotsFunctions)

    def onSearchConversationCard(self):
        searchText = self.dockwidget.ptSearchConversationCard.toPlainText()
        if searchText == "":
            return

        # Generate the filter function for search keyword
        def searchFilter(metaInfo, keyword=searchText):
            titleLower, descriptionLower = metaInfo['title'].lower(), metaInfo['description'].lower()
            keywordLower = keyword.lower()
            if titleLower.find(keywordLower) != -1 or descriptionLower.find(keywordLower) != -1:
                return True
            else:
                return False

        # Generate the highlight rule for content in conversation cards
        def highlight(fullText, keyword=searchText):
            pattern = re.compile(f'({re.escape(keyword)})', re.IGNORECASE)
            # Set the HTML formatted text to the label
            highlightedText = pattern.sub(r'<span style="background-color: yellow">\1</span>', fullText)
            return highlightedText

        # Dock Interface: Pass slots functions to buttons in conversation cards to display
        slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
        self.dockwidget.displayConversationCard(self.dataloader, slotsFunctions, searchFilter, highlight)

        # Dock Interface: Turn 'Search' button into 'Clear button'
        self.dockwidget.pbSearchConversationCard.clicked.disconnect(self.onSearchConversationCard)
        self.dockwidget.searchPressed.disconnect(self.onSearchConversationCard)

        self.dockwidget.pbSearchConversationCard.setText("Cancel")
        self.dockwidget.pbSearchConversationCard.clicked.connect(self.switchClearMode)

    def switchClearMode(self):
        slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
        self.dockwidget.displayConversationCard(self.dataloader, slotsFunctions)
        self.dockwidget.pbSearchConversationCard.clicked.connect(self.onSearchConversationCard)
        self.dockwidget.searchPressed.connect(self.onSearchConversationCard)

        self.dockwidget.pbSearchConversationCard.setText("Search")

    def activateConsole(self, code: str, run: bool) -> str:
        consoleWidget = iface.mainWindow().findChild(QDockWidget, "PythonConsole")
        if not consoleWidget or not consoleWidget.isVisible():
            iface.actionShowPythonDialog().trigger()
            consoleWidget = iface.mainWindow().findChild(QDockWidget, "PythonConsole")

        pythonConsole = consoleWidget.findChild(console.console.PythonConsoleWidget)
        editorWidget = pythonConsole.findChild(console.console_editor.Editor)

        if not editorWidget or not editorWidget.isVisible:
            pythonConsole.showEditorButton.trigger()

        shellOutputWidget = pythonConsole.findChild(console.console_output.ShellOutputScintilla)

        pythonConsole.tabEditorWidget.newTabEditor(tabName='IntelliGeo', filename=None)
        QApplication.clipboard().setText(code)
        pythonConsole.pasteEditor()

        return shellOutputWidget.text()

    def startConsoleTracker(self):
        self.consoleTracker.timeout.connect(self.comparePythonConsoleOutput)

        interval = 300
        self.consoleTracker.start(interval)

        # thread = QThread()
        # consoleTracker.moveToThread(thread)
        # thread.started.connect(lambda: consoleTracker.start(300))

    def comparePythonConsoleOutput(self):
        consoleWidget = iface.mainWindow().findChild(QDockWidget, "PythonConsole")
        if not consoleWidget or not consoleWidget.isVisible():
            self.consoleTracker.stop()
            return
        pythonConsole = consoleWidget.findChild(console.console.PythonConsoleWidget)
        editorWidget = pythonConsole.findChild(console.console_editor.Editor)

        if not editorWidget or not editorWidget.isVisible:
            self.consoleTracker.stop()
            return

        shellOutputWidget = pythonConsole.findChild(console.console_output.ShellOutputScintilla)
        currentFullLogMessage = shellOutputWidget.text()

        if (currentFullLogMessage != self.consoleText) and (self.consoleText in currentFullLogMessage):
            if currentFullLogMessage.find(self.consoleText) == 0:
                newLogText = currentFullLogMessage[len(self.consoleText):]
                self.consoleText = currentFullLogMessage
                show_variable_popup(newLogText)
                show_variable_popup(newLogText.count('\n'))
                if len(newLogText) == 0:
                    self.consoleTracker.stop()
                    return

                self.consoleTracker.stop()
                if newLogText.count('\n') >= 2:
                    self.activateDebugDialog(newLogText)

        return

    def activateDebugDialog(self, logMessage):
        dialog = DebugDialog()
        result = dialog.exec_()
        self.consoleTracker.stop()
        
        if result != QDialog.Accepted:
            return
        self.liveConversation.llmReflection.connect(self.onDebugReceived)
        self.liveConversation.updateReflection(logMessage, "code")
        self.dockwidget.disableAllButtons()
        self.dockwidget.disableAllTextEdit()

    def onDebugReceived(self, response, workflow, modelPath):
        self.liveConversation.llmReflection.disconnect(self.onDebugReceived)
        self.dockwidget.enableAllButtons()
        self.dockwidget.enableAllTextEdit()
        if response == "":
            return

        code = extractCode(response)
        show_variable_popup(code)
        self.consoleText = self.activateConsole(code, False)
        self.startConsoleTracker()

        # Dock Interface: Update log & general information
        self.dockwidget.updateConversation(self.liveConversation)
        self.dockwidget.updateGeneralInfo(self.liveConversation)

        # Dock Interface: Update conversation cards
        slotsFunctions = [self.onConversationLoad, self.onConversationDeleted, self.onConversationEdited]
        self.dockwidget.updateConversationCard(self.liveConversation.metaInfo, slotsFunctions)

        # Dataloader: Update meta-information
        self.dataloader.updateConversationInfo(self.liveConversation.metaInfo)

    def activeGraphicDesigner(self, modelPath, run):
        dialog = ModelerDialog()
        dialog.loadModel(modelPath)
        dialog.show()

        return None
