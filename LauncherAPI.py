# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-04-09 11:15:27
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-09 11:16:40
# FilePath: \FlowLauncher\Plugins\WoxBasePluginQuery\LauncherAPI.py
# ----------------------------------------------------------------
# Copyright (c) 2023 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

import os
from enum import Enum
from Launcher import *
from QueryPlugin import *

pluginDir = os.path.dirname(os.path.realpath(__file__))

class LauncherAPI(Enum):
    ChangeQuery = 100 # Change Launcher query
    RestartApp = 101 # Restart Launcher
    SaveAppAllSettings = 102 # Save all Launcher settings
    CheckForNewUpdate = 103 # Check for new Launcher update
    ShellRun = 104 # Run shell commands
    CloseApp = 105 # Close Launcher
    HideApp = 106 # Hide Launcher
    ShowApp = 107 # Show Launcher
    ShowMsg = 108 # Show messagebox
    GetTranslation = 109 # get translation of current language
    OpenSettingDialog = 110 # Open setting dialog
    GetAllPlugins = 111 # get all loaded plugins
    StartLoadingBar = 112 # Start loading animation in Launcher
    StopLoadingBar = 113 # Stop loading animation in Launcher
    ReloadAllPluginData = 114 # Reload all Launcher plugins

    __apiDict__ = None

    @property
    def API_name(self) -> str:
        # API.CloseApp might not working sometimes while the launcher is run as Administrator, in which the launcher might just hide launcher instead
        # some other API is with the same problem, which need to be fixed if it's needed in use, plz check
        match self:
            case LauncherAPI.CloseApp:
                return QueryPlugin.close_launcher.__name__
        return self.name

    @property
    def name(self) -> str:
        return f'{Launcher.name}.{super().name}'
    
    @classmethod
    @property
    def all(cls):
        if cls.__apiDict__:
            return cls.__apiDict__
        cls.__apiDict__ = dict[LauncherAPI, dict[Language, str]]()
        for api in LauncherAPI:
            cls.__apiDict__[api] = dict[Language, str]()
        for language in Language:
            languageJSON = Launcher.geti18n(language)
            for api in LauncherAPI:
                key = str(api)
                if key not in languageJSON.keys():
                    languageJSON[key] = api
                cls.__apiDict__[api][language] = languageJSON[key].format(Launcher.name)
        return cls.__apiDict__

    def getDescription(self, language:Language=Language.en_us) -> str:
        return LauncherAPI.all[self][language]