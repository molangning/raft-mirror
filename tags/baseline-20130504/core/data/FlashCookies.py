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

from pyamf import sol
import os
import platform

class FlashCookies:
    def __init__(self, framework):
        self.framework = framework
        self.detected_platform = False

    def detect_platform(self):
        if self.detected_platform:
            return
        attempt = 0
        while attempt < 3:
            try:
                system_platform = platform.system()
                self.is_mac = False
                self.is_windows = False
                self.is_linux = False
                if 'Darwin' == system_platform:
                    self.is_mac = True
                elif 'Windows' == system_platform:
                    self.is_windows = True
                else:
                    # assume linux or similar
                    self.is_linux = True
                self.detected_platform = True
                break
            except IOError:
                attempt += 1

    def visit_flashcookies_files(self, obj, dirname, entries):
        for entry in entries:
            if not obj.has_key('randomized'):
                if entry not in ('.','..'):
                    obj['randomized'] = entry
            if entry.endswith('.sol'):
                self.flashcookies_files.append((dirname, entry, obj['randomized']))

    def add_path_if_exists(self, base_paths, base_path):
        if os.path.exists(base_path):
            base_paths.add(base_path)

    def get_base_paths(self):
        base_paths = set()
        self.detect_platform()
        if self.is_mac:
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), 'Library/Preferences/Macromedia/Flash Player/#SharedObjects/'))
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), 'Library/Application Support/Google/Chrome/Default/Pepper Data/Shockwave Flash/WritableRoot/#SharedObjects/'))
        elif self.is_windows:
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), 'Application Data\\Macromedia\\Flash Player\\#SharedObjects\\'))
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), 'AppData\\Local\\Macromedia\\Flash Player\\#SharedObjects\\'))
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), 'AppData\\Remote\\Macromedia\\Flash Player\\#SharedObjects\\'))
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), 'AppData\\Local\\Google\\Chrome\\User Data\\Default\\Pepper Data\\Shockwave Flash\\WritableRoot\\#SharedObjects\\'))
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), 'AppData\\Remote\\Google\\Chrome\\User Data\\Default\\Pepper Data\\Shockwave Flash\\WritableRoot\\#SharedObjects\\'))
        else:
            # assume linux or similar
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), '.macromedia/Flash_Player/#SharedObjects/'))
            self.add_path_if_exists(base_paths, os.path.join(self.framework.get_user_home_dir(), '.config/google-chrome/Default/Pepper Data/Shockwave Flash/WritableRoot/#SharedObjects/'))

        return list(base_paths)

    def read_flashcookies(self):
        self.flashcookies_files = []
        for base_path in self.get_base_paths():
            user_dir = {}
            os.path.walk(base_path, self.visit_flashcookies_files, user_dir)

        self.flashcookies = {}
        for item in self.flashcookies_files:
            try:
                dirname, entry, randomized = item
                filename = os.path.join(dirname, entry)
                print(filename)
                n = dirname.find(randomized)
                if n > -1:
                    domain = dirname[n+len(randomized)+1:]
                    n = domain.find(os.path.sep)
                    if n > -1:
                        domain = domain[:n]
                    if not self.flashcookies.has_key(domain):
                        self.flashcookies[domain] = []
                    lso = sol.load(filename)
                    self.flashcookies[domain].append(lso)
            except Exception, error:
                self.framework.report_exception(error)
        
        return self.flashcookies
            


