# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-03-04 12:45:55
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-04 22:38:59
# FilePath: \Plugins\WoxPluginBase_Query\Query.py
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


class LauncherEnum(Enum):
    Wox = 0,
    FlowLauncher = 1

    @staticmethod
    def GetDefinitions():
        return {
            LauncherEnum.Wox:{
                'dir': 'wox',
                'name': 'wox'
            },
            LauncherEnum.FlowLauncher:{
                'dir': 'FlowLauncher',
                'name': 'Flow.Launcher'
            }
        }

class Language(Enum):
    en_us = 0,
    zh_cn = 1

pluginDir = os.path.dirname(os.path.realpath(__file__))

LAUNCHER_DEFINITIONS = LauncherEnum.GetDefinitions()

for definition in LAUNCHER_DEFINITIONS:
    if LAUNCHER_DEFINITIONS[definition]['dir'] not in pluginDir:
        continue
    LAUNCHER_TYPE = definition
    match definition:
        case LauncherEnum.Wox:
            from wox import Wox as LauncherBase
        case LauncherEnum.FlowLauncher:
            from flowlauncher import FlowLauncher as LauncherBase
        case _:
            raise ValueError(f'Unknown Launcher Type{LauncherEnum(definition).name}')

class Launcher(LauncherBase):
    class API(Enum):
        ChangeQuery = 0, # Change Launcher query
        RestartApp = 1, # Restart Launcher
        SaveAppAllSettings = 2, # Save all Launcher settings
        CheckForNewUpdate = 3, # Check for new Launcher update
        ShellRun = 4, # Run shell commands
        CloseApp = 5, # Close Launcher
        HideApp = 6, # Hide Launcher
        ShowApp = 7, # Show Launcher
        ShowMsg = 8, # Show messagebox
        GetTranslation = 9, # Get translation of current language
        OpenSettingDialog = 10, # Open setting dialog
        GetAllPlugins = 11, # Get all loaded plugins
        StartLoadingBar = 12, # Start loading animation in Launcher
        StopLoadingBar = 13, # Stop loading animation in Launcher
        ReloadAllPluginData = 14, # Reload all Launcher plugins

    @staticmethod
    def LoadLanguageJson(language:Language) -> dict[str, str]:
        languageData = None
        try:
            jsonFIle = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))) , f'language\\{language.name}.json') 
            with open(jsonFIle, 'r', encoding='utf-8`') as f:
                try:    
                    languageData = json.load(f)
                except Exception:
                    pass
        except Exception:
            if language != Language.en_us:
                languageData = Launcher.LoadLanguageJson(Language.en_us)
        return languageData

    @staticmethod
    def GetSettings():
        if not Launcher.__settings__:
            with(open(Launcher.GetSettingPath(),'r') as f):
                Launcher.__settings__ = json.load(f)
        return Launcher.__settings__

    @staticmethod
    def GetActionKeyword(plugInID:int):
        return Launcher.GetSettings()['PluginSettings']['Plugins'][plugInID]['ActionKeywords'][0]

    @staticmethod
    def GetSettingPath():
        dirName = Launcher.GetName()
        appdata = os.path.join(os.environ['localAppData'.upper()],'../')
        
        roaming = os.path.join(appdata, f'./Roaming/{dirName}/')
        local = os.path.join(appdata, f'./Loacl/{dirName}/UserData/')
        portable = f'../../../'
        portableLocal = f'../../UserData/'

        relative = './Settings/Settings.json'
        modes = [roaming, local, portable, portableLocal]
        for mode in modes:
            path = os.path.join(mode, relative)
            if os.path.isfile(path):
                return path
        return os.path.join(os.path.realpath(__file__), '../../../Settings/Settings.json')

    @staticmethod
    def GetAPI(api:API):
        return f'{Launcher.__launcherName__}.{api.name}'
    
    @staticmethod
    def GetAPIName(api:API, language:Language=Language.en_us):
        return Launcher.GetAPIs()[api][language]
    
    @staticmethod
    def GetName():
        if not Launcher.__launcherName__:
            Launcher.__launcherName__ = LAUNCHER_DEFINITIONS[LAUNCHER_TYPE]['name']
        return Launcher.__launcherName__

    __launcherName__ = None
    __settingPath__ = None 
    __settings__ = None
    __apis__ = None
    __language = None

    @staticmethod
    def GetLanguage():
        if not Launcher.__language:
            langName = str(Launcher.GetSettings()['Language']).replace('-', '_')
            Launcher.__language = Language[langName]
        return Launcher.__language

    @staticmethod
    def GetLanguageJson(language:Language):
        languageJSON = Launcher.LoadLanguageJson(language)
        if languageJSON:
            return languageJSON
        if language is not Language.en_us:
            languageJSON = Launcher.LoadLanguageJson(Language.en_us)
        currentLanguage = Launcher.GetLanguage()
        if language is not currentLanguage:
            languageJSON = Launcher.LoadLanguageJson(currentLanguage)
        if languageJSON:
            return languageJSON
        languageJSON = dict[str, str]()
        for api in Launcher.API:
            languageJSON[str(api)] = f'Launcher.{api}'
        return languageJSON

    @staticmethod
    def GetAPIs():
        if not Launcher.__apis__:
            Launcher.__apis__ = dict[Launcher.API, dict[Language, str]]()
            for api in Launcher.API:
                Launcher.__apis__[api] = dict[Language, str]()
            for language in Language:
                languageJSON = Launcher.GetLanguageJson(language)
                for api in Launcher.API:
                    Launcher.__apis__[api][language] = languageJSON[str(api)].format(Launcher.GetName())
        return Launcher.__apis__


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
    
    class InstallationCheck(Launcher):
        def PluginName(self) -> str:
            return 'WoxPluginBase_Query'

        def query(self, queryString:str):
            return [QueryResult(f'{self.PluginName()} is installed.',None,None,None,None,False).toDict()]

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
    Query.InstallationCheck()