# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-03-04 12:45:55
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-03 01:51:40
# FilePath: \WoxPluginBase_Query\Query.py
# ----------------------------------------------------------------
# Copyright (c) 2023 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

# -*- coding: utf-8 -*-
import os
import win32con
import win32clipboard
from enum import Enum
import json

current = os.path.dirname(os.path.realpath(__file__))

class Launchers(Enum):
    Wox=0,
    FlowLauncher = 1

if 'wox' in current:
    from wox import Wox as LauncherBase
    LauncherType = Launchers.Wox
    LauncherName = 'Wox'
elif 'FlowLauncher' in current:
    from flowlauncher import FlowLauncher as LauncherBase
    LauncherType = Launchers.FlowLauncher
    LauncherName = 'Flow.Launcher'

class Launcher(LauncherBase):
    class API(Enum):
        ChangeQuery = 0, # change launcher query
        RestartApp = 1, # restart Launcher
        SaveAppAllSettings = 2, #save all Launcher settings
        CheckForNewUpdate = 3, # check for new Launcher update
        ShellRun = 4, # run shell commands
        CloseApp = 5, # close launcher
        HideApp = 6, # hide launcher
        ShowApp = 7, # show launcher
        ShowMsg = 8, # show messagebox
        GetTranslation = 9, # get translation of current language
        OpenSettingDialog = 10, # open setting dialog
        GetAllPlugins = 11, # get all loaded plugins
        StartLoadingBar = 12, # start loading animation in launcher
        StopLoadingBar = 13, # stop loading animation in launcher
        ReloadAllPluginData = 14, # reload all launcher plugins

    @staticmethod
    def GetActionKeyword(plugInID:int):
        with(
        open(Query.SettingPath,'r') as settingJson
        ):
            return json.load(settingJson)['PluginSettings']['Plugins'][plugInID]['ActionKeywords'][0]

    @staticmethod
    def GetSettingPath(PathName:str, isPortableMode:bool = False):
        mode = 'Roaming' if isPortableMode else 'Local'
        return os.environ['localAppData'.upper()] + '/../' + mode +'/' + PathName + '/Settings/Settings.json'

    @staticmethod
    def GetAPIName(api:API):
        return Launcher.Name + '.' + api.name
    
    Name = LauncherName

    SettingPath = GetSettingPath(LauncherType.name)
    if not os.path.isfile(SettingPath):
        SettingPath = GetSettingPath(LauncherType.name, True)

class Query(Launcher):
# class Query():
    @classmethod
    def copyData(cls, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
        win32clipboard.CloseClipboard()
    
    @classmethod
    def getCopyDataResult(cls, type, titleData, iconPath) -> dict:
        title = type + ": " + titleData
        subTitle = 'Press Enter to Copy ' + type
        return QueryResult(title, subTitle, iconPath, None, cls.copyData.__name__, True, titleData).toDict()
    
    def query(self, queryString:str):
        return [QueryResult('WoxPluginBase_Query is installed.',None,None,None,None,False).toDict()]

class QueryResult:
    def __init__(self, title:str, subtitle:str, icon:str, context , method:str, hideAfterAction:bool, *args) -> None:
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.method = method
        self.parameters = args
        self.context = context
        self.hideAfterAction = hideAfterAction
    
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
    Query()