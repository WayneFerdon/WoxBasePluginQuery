# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-03-04 12:45:55
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-11 05:26:28
# FilePath: \FlowLauncher\Plugins\WoxPluginBase_Query\QueryPlugin.py
# ----------------------------------------------------------------
# Copyright (c) 2023 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

# -*- coding: utf-8 -*-
import win32con
import win32clipboard
import json
from Launcher import *

class Plugin(PluginBase):
    with open('./plugin.json','r') as f:
        pluginJson = json.load(f)
    plugName = pluginJson['Name']
    id = pluginJson['ID']
    defaultIcon = pluginJson['IcoPath']
    actionKeyword = Launcher.settings['PluginSettings']['Plugins'][id]['ActionKeywords'][0]

    def close_launcher(self):
        Launcher.close_launcher()

    @staticmethod
    def setPlatformAsPluginIcon():
        launcherIcon = Launcher.icon
        if Plugin.defaultIcon == launcherIcon:
            return
        Plugin.defaultIcon = Launcher.icon
        Plugin.pluginJson['IcoPath'] = Plugin.defaultIcon
        with open('./plugin.json','w') as f:
            f.write(json.dumps(Plugin.pluginJson))

    def __init__(self):
        super().__init__()
    
    def context_menu(self, data) -> list:
        return super().context_menu(data)

    def debug(self, msg: str):
        return super().debug(msg)

    def query(self, param: str = '') -> list:
        return super().query(param)

class QueryPlugin(Plugin):
    def copyData(self, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
        win32clipboard.CloseClipboard()
    
    def getCopyDataResult(self, type, titleData, iconPath) -> dict:
        title = type + ": " + titleData
        subTitle = 'Press Enter to Copy ' + type
        return QueryResult(title, subTitle, iconPath, None, self.copyData.__name__, True, titleData).toDict()
    
    def getTitleOnlyResult(self, title:str):
        return QueryResult(title,None,self.defaultIcon,None,None,False).toDict()

    def getExceptionResult(self, traceback:str) -> dict:
        return self.getTitleOnlyResult(traceback)
    
    def context_menu(self, data) -> list:
        return super().context_menu(data)

    def debug(self, msg: str):
        return super().debug(msg)

    def query(self, param: str = '') -> list:
        return super().query(param)
    
class InstallationCheck(Plugin):
    def query(self, _:str):
        if 'WoxPluginBase_Query' == Plugin.plugName:
            Plugin.setPlatformAsPluginIcon()
        msg = f'{Plugin.plugName} is installed.'
        self.debug(msg=msg)
        return [QueryResult(msg,None,Plugin.defaultIcon,None,None,False).toDict()]

class QueryResult:
    def __init__(self, title:str, subtitle:str, icon:str, context, method:str, hideAfterAction:bool, *args) -> None:
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.context = context
        self.method = method
        self.hideAfterAction = hideAfterAction
        self.parameters = args
    
    def toDict(self):
        jsonResult = {
            'Title': self.title, 
            'SubTitle': self.subtitle, 
            'IcoPath': self.icon, 
            'ContextData': self.context
        }
        if self.method is not None:
            jsonResult['JsonRPCAction'] = {
                'method': self.method, 
                'parameters': self.parameters, 
                "doNotHideAfterAction".replace('oNo', 'on'): (not self.hideAfterAction), 
            }
        return jsonResult

if __name__ == "__main__":
    InstallationCheck()