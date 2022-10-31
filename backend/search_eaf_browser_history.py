#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 Andy Stewart
# 
# Author:     Andy Stewart <lazycat.manatee@gmail.com>
# Maintainer: <lazycat.manatee@gmail.com> <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import threading
import os
import traceback
import sexpdata
import re

from core.utils import get_command_result, get_emacs_var, get_emacs_vars, message_emacs, eval_in_emacs, logger    # type: ignore
from core.search import Search    # type: ignore


class SearchEAFBrowserHistory(Search):
    
    def __init__(self, backend_name, message_queue) -> None:
        Search.__init__(self, backend_name, message_queue)
        
    def search_match(self, prefix):
        if len(prefix.split()) > 0:
            eaf_config_path = get_emacs_var("eaf-config-location")
            if type(eaf_config_path) is str and eaf_config_path != "":
                eaf_browser_history_path = os.path.join(eaf_config_path, "browser", "history", "log.txt")
                if os.path.exists(eaf_browser_history_path):
                    histories = []
                    with open(eaf_browser_history_path) as f:
                        histories = f.read().splitlines()
                    
                    match_histories = []
                    prefix_regexp = re.compile(".*" + ".*".join(prefix.split()))
                    for history in histories:
                        history_infos = history.split("ᛡ")[0].split("ᛝ")
                        if prefix_regexp.match(history_infos[0].lower()) or prefix_regexp.match(history_infos[1].lower()):
                            match_histories.append(" ".join(history_infos))
                            
                    return match_histories
                
        return []
                        
