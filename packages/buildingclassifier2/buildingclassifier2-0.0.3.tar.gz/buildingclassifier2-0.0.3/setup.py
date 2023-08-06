from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Rule-based building classifier package'
LONG_DESCRIPTION = 'A package containing previously developed buildingclassifier function for intaking addresses and classify the corresponding building types for those addresses'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="buildingclassifier2", 
        version=VERSION,
        author="Emeric Szaboky",
        author_email="<emeric.szaboky@rakuten.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['jaconv', "os", "datetime", "time", "re", "dask", "dask.dataframe", "dsdtools"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

import pandas as pd
import numpy as np
import os
import datetime
import time
import jaconv
import re
import dask
import dask.dataframe as dd
from dask import delayed
from dsdtools import build_hiveserver2_session
