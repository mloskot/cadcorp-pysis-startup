"""
Startup script for Python in Cadcorp SIS Desktop (PySIS) 8.0 or later.

Author: Mateusz Loskot <mateusz@loskot.net>

This is free and unencumbered software released into the public domain.
For more information, please refer to <http://unlicense.org>
"""
import os
import sys

print('Executing startup script', __file__)
sys.path.append(os.path.dirname(__file__))

# Import module(s) by name to make them reloadable with `imp.reload`
import sis_functions
# Bind all public names from the module(s) in the local namespace for the current scope.
from sis_functions import *

# Print startup info banner
print("Python in Cadcorp SIS", sis_version())
