#
# Implements a standard web page that has user interaction
#
# Author: Gregory Fleischer (gfleischer@gmail.com)
#
# Copyright (c) 2011 RAFT Team
#
# This file is part of RAFT.
#
# RAFT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# RAFT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RAFT.  If not, see <http://www.gnu.org/licenses/>.
#

import PyQt4
from PyQt4 import QtWebKit, QtNetwork
from PyQt4.QtCore import *

from core.web.BaseWebPage import BaseWebPage

class StandardWebPage(BaseWebPage):
    def __init__(self, framework, parent = None):
        BaseWebPage.__init__(self, framework, parent)
        self.framework = framework
        self.loadFinished.connect(self.handle_loadFinished)
        self.contentsChanged.connect(self.handle_contentsChanged)

    def set_page_settings(self, settings):
        # common settings handled by base
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows, True)
            
    def javaScriptConsoleMessage(self, message, lineNumber, sourceID):
        self.framework.console_log('console log from [%s / %s]: %s' % (lineNumber, sourceID, message))

    def userAgentForUrl(self, url):
        return self.framework.useragent()

    def handle_loadFinished(self, ok):
        self.mainFrame().addToJavaScriptWindowObject("__RAFT__", self)

    def handle_contentsChanged(self):
        pass

    def acceptNavigationRequest(self, frame, request, navigationType):
        return True
