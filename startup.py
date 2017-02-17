# Startup script for Python in Cadcorp SIS Desktop (PySIS) 8.0 or later 
#
# Developed by Mateusz Loskot <mateusz@loskot.net>
#
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <http://unlicense.org>
from cadcorp import sis

def sis_version():
    """Returns string with SIS version and build numbers."""
    return "%s %s (%s)" % (sis.__version__, sis.__build_type__, sis.__build_date__)

# Print startup info banner
print("Startup script for Python in Cadcorp SIS", sis_version())
