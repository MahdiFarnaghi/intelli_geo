# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IntelliGeoDockWidget
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

/**************************************************************************

IntelliGeoDockWidget

This module contains the IntelliGeoDockWidget class, which is a custom
QDockWidget used within IntelliGeo. The widget provides an interface for
displaying, updating, and managing conversation cards, which include
information like titles, descriptions, metadata, and actions for editing,
deleting, and opening conversations.

Classes:
    IntelliGeoDockWidget: A QDockWidget subclass for managing conversation
                          cards in a QGIS plugin interface.

Usage:
    - Initialize the IntelliGeoDockWidget with an optional parent widget.
    - Use displayConversationCard to populate the widget with conversation
      cards based on the data provided by a dataloader.
    - Update or remove conversation cards using the provided methods.
    - Handle user input and events through the event filter and predefined
      slots.

Dependencies:
    - QGIS
    - datetime
    - utils (local module)
***************************************************************************/

"""

import os
from datetime import datetime

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

from qgis.PyQt.QtCore import QEvent, Qt
from qgis.PyQt.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QPushButton, QSizePolicy, QSpacerItem,
                                 QScrollArea, QWidget)
from qgis.PyQt.QtGui import QFont

from .utils import handleNoneConversation, unpack, formatDescription, show_variable_popup

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'intelli_geo_dockwidget_base.ui'))


class IntelliGeoDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()
    enterPressed = pyqtSignal(str)
    searchPressed = pyqtSignal(str)
    switchClearMode = pyqtSignal(str)

    def __init__(self, parent=None):
        """Constructor."""
        super(IntelliGeoDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.conversationCards = {}
        self.scrollAreaWidget, self.scrollAreaLayout = None, None

        self.conversationCardSearchMode = False

        self.setupUi(self)

        # create listener for plainTextEditor 'ptMessage'
        self.ptMessage.installEventFilter(self)
        self.ptSearchConversationCard.installEventFilter(self)

        # TODO: to be removed in version v0.0.2
        for index in reversed(range(self.twTabs.count())):
            tab = self.twTabs.widget(index)
            if tab.objectName() in ["tbContext", "tabModels"]:
                self.twTabs.removeTab(index)


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def displayConversationCard(self, dataloader, slotsFunctions,
                                searchFilter=lambda x: True,
                                highlightRule=lambda x: x):
        # Tricky Argument Passed Here!
        # the argument 'onConversationLoad' is a function (method) defined in class IntelliGeo

        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaWidget = QWidget()
        self.saConversationCard.setWidget(self.scrollAreaWidget)
        self.scrollAreaWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        metaTable = dataloader.selectConversationInfo()
        metaTable.sort(key=lambda info: datetime.strptime(info['modified'], "%m %d %Y %H:%M:%S"))

        for metaInfo in metaTable:
            if searchFilter(metaInfo):
                self.addConversationCard(metaInfo, slotsFunctions, highlight=highlightRule)
            else:
                continue

        self.scrollAreaWidget.setLayout(self.scrollAreaLayout)

    def updateConversationCard(self, conversationMetaInfo, slotsFunctions):
        """
        Find the conversation card, remove it and add a new one.
        """
        conversationID = conversationMetaInfo['ID']
        self.removeConversationCard(conversationID)
        self.addConversationCard(conversationMetaInfo, slotsFunctions)

    def addConversationCard(self, metaInfo, slotsFunctions, order=0, highlight=lambda x: x):
        onConversationLoad, onConversationDeleted, onConversationEdited = slotsFunctions
        conversationCard = QGroupBox()
        cardLayout = QVBoxLayout()

        # "ID", "llmID", "title", "description", "created", "modified", "messageCount", "workflowCount", "userID"
        (conversationID,
         llmID,
         title,
         description,
         created,
         lastEdit,
         messageCount,
         workflowCount,
         userID) = unpack(metaInfo, "conversation")

        titleLabel = QLabel(highlight(title))
        font = QFont()
        font.setBold(True)  # Set the font to bold
        titleLabel.setFont(font)

        desLabel = QLabel(highlight(description))
        desLabel.setWordWrap(True)

        verticalSpacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        metadata = f"Created: {created} | LLM: {llmID} \n Messages: {messageCount} | Workflow: {workflowCount} "
        metadataLabel = QLabel(metadata)
        metadataLabel.setAlignment(Qt.AlignRight)

        horizontalLayout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        pbEdit = QPushButton("Edit")
        pbEdit.setStyleSheet("""
            QPushButton {
                background-color: #9DDE8B;
            }
        """)
        pbEdit.clicked.connect(lambda: onConversationEdited(conversationID))

        pbDelete = QPushButton("Delete")
        pbDelete.setStyleSheet("""
            QPushButton {
                background-color: #FA7070;
            }
        """)
        pbDelete.clicked.connect(lambda: onConversationDeleted(conversationID))

        pbOpen = QPushButton("Open")
        pbOpen.clicked.connect(lambda: onConversationLoad(conversationID))

        horizontalLayout.addSpacerItem(spacer)
        horizontalLayout.addWidget(pbEdit)
        horizontalLayout.addWidget(pbDelete)
        horizontalLayout.addWidget(pbOpen)

        cardLayout.addWidget(titleLabel)
        cardLayout.addWidget(desLabel)
        cardLayout.addSpacerItem(verticalSpacer)
        cardLayout.addWidget(metadataLabel)
        cardLayout.addLayout(horizontalLayout)
        conversationCard.setLayout(cardLayout)

        self.scrollAreaLayout.insertWidget(order, conversationCard)
        self.conversationCards[conversationID] = conversationCard

    def removeConversationCard(self, conversationID):
        """
        Remove the Conversation Card only in the 'Conversations' Browser.

        """
        if conversationID in self.conversationCards:
            card = self.conversationCards[conversationID]
            self.scrollAreaLayout.removeWidget(card)
            card.deleteLater()
            del self.conversationCards[conversationID]

    @handleNoneConversation
    def updateGeneralInfo(self, conversation) -> None:
        """
        Update general information dock under "Messages" tab.
        """
        self.lbTitle.setText(conversation.title)
        self.lbDescription.setText(formatDescription(conversation.description))

        metadata = conversation.getMetadata()
        self.lbMetadata.setText(metadata)

    @handleNoneConversation
    def updateConversation(self, conversation) -> None:
        """
        Update chat log under "Messages" tab.
        """
        # get updated log
        log = conversation.fetch()
        self.txHistory.setPlainText(log)

        # set text browser read only
        self.txHistory.setReadOnly(True)

        # always show the bottom of streaming conversation
        self.txHistory.verticalScrollBar().setValue(self.txHistory.verticalScrollBar().maximum())

    def eventFilter(self, QTObject, event):
        if event.type() == QEvent.KeyPress:
            if QTObject is self.ptMessage and self.ptMessage.hasFocus():
                if event.key() == Qt.Key_Return:
                    self.enterPressed.emit(self.ptMessage.toPlainText())
                    return True

            elif QTObject is self.ptSearchConversationCard and self.ptSearchConversationCard.hasFocus():
                if event.key() == Qt.Key_Return:
                    self.searchPressed.emit(self.ptSearchConversationCard.toPlainText())
                    return True
                elif self.pbSearchConversationCard.text() == "Clear":
                    self.switchClearMode.emit(self.ptSearchConversationCard.toPlainText())

        return super().eventFilter(QTObject, event)
