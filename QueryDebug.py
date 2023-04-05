# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-04-02 12:21:06
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-05 23:44:20
# FilePath: \FlowLauncher\Plugins\WoxPluginBase_Query\QueryDebug.py
# ----------------------------------------------------------------
# Copyright (c) 2023 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

import traceback

class QueryDebug:
    # 静态变量
    Instance=None
    __flag__=False
    
    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.Instance is None:
            cls.Instance=super().__new__(cls)
        return cls.Instance
    
    @classmethod
    def __init__(cls):
        if cls.__flag__:
            return
        cls.__flag__=True

    Logs = list[str]()
    
    @classmethod
    def Log(cls, *info):
        cls.Instance.Logs.append([len(cls.Instance.Logs), str(list(info))[1:-1] + "\n" + "\n".join(traceback.format_stack())])