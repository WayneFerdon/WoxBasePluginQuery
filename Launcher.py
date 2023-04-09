# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-04-05 02:56:19
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-09 11:09:31
# FilePath: \FlowLauncher\Plugins\WoxPluginBase_Query\Launcher.py
# ----------------------------------------------------------------
# Copyright (c) 2023 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

import os
import json
from enum import Enum

pluginDir = os.path.dirname(os.path.realpath(__file__))

class Language(Enum):
    en_us = 0,
    zh_cn = 1

    @property
    def json(self) -> dict[str, str]:
        try:
            jsonFile = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))) , f'language\\{self.name}.json') 
            with open(jsonFile, 'r', encoding='utf-8`') as f:
                data = json.load(f)
            return data
        except Exception:
            return dict[str, str]()

class Launcher():
    __definitions__ = None
    __launcherName__ = None
    __settings__ = None
    __language__ = None
    __distribution__ = None
    
    class Distribution(Enum):
        Wox = 0
        FlowLauncher = 1

        __all__ = None

        @classmethod
        @property
        def all(cls):
            if cls.__all__:
                return cls.__all__
            cls.__all__ =  {
                Launcher.Distribution.Wox:{
                    cls.dir: 'wox',
                    cls.name: 'wox'
                },
                Launcher.Distribution.FlowLauncher:{
                    cls.dir: 'FlowLauncher',
                    cls.name: 'Flow.Launcher'
                }
            }
            return cls.__all__

        @property
        def name(self):
            return Launcher.Distribution.all[self][Launcher.Distribution.name]
        
        @property
        def dir(self):
            return Launcher.Distribution.all[self][Launcher.Distribution.dir]

    @classmethod
    @property
    def distribution(cls) -> Distribution:
        if cls.__distribution__:
            return cls.__distribution__
        for distribution in Launcher.Distribution.all:
            if distribution.dir in pluginDir:
                cls.__distribution__ = distribution
                break
        return cls.__distribution__

    @classmethod
    @property
    def name(cls) -> str:
        return cls.distribution.name
    
    @classmethod
    @property
    def icon(cls):
        return os.path.relpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Images\\Icon_{}.png'.format(cls.name)),os.path.abspath('./'))

    @classmethod
    @property
    def settings(cls) -> dict:
        if cls.__settings__:
            return cls.__settings__
        
        # 1. portable/non-portable mode, and WoxPluginBase_Query is in the build-in plugin folder
        buildin = f'../UserData/'
        # 2. non-portable mode, and WoxPluginBase_Query is in %appdata%{dirName}
        roaming = os.path.join(os.getenv('appData'), f'./{cls.name}/')
        # 3. portable mode, and WoxPluginBase_Query is in the user plugin folder
        portable = f'../../'

        modes = [roaming, buildin, portable]
        relative = './Settings/Settings.json'

        for mode in modes:
            current = os.path.join(mode, relative)
            if os.path.isfile(current):
                path = current
                break
        with(open(path, 'r') as f):
            cls.__settings__ = json.load(f)
        return cls.__settings__
        
    @classmethod
    @property
    def language(cls) -> Language:
        if cls.__language__:
            return cls.__language__
        langName = str(cls.settings['Language']).replace('-', '_')
        cls.__language__ = Language[langName]
        return cls.__language__

    @staticmethod
    def close_launcher():
        try:
            os.popen(f'taskkill /f /im {Launcher.name}.exe')
        except Exception:
            pass
    
    @staticmethod
    def geti18n(language:Language) -> dict[str, str]:
        languages = [language, Launcher.language, Language.en_us]
        jsons = list(lang.json for lang in languages)
        jsons.reverse()
        i18n = dict[str, str]()
        for json in jsons:
            i18n.update(json)
        return i18n

match Launcher.distribution:
    case Launcher.Distribution.Wox:
        from wox import Wox as PluginBase
    case Launcher.Distribution.FlowLauncher:
        from flowlauncher import FlowLauncher as PluginBase
    case _:
        raise ValueError(f'Unknown Launcher {Launcher.distribution}')