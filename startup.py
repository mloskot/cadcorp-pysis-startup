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

def sis_help(needle=None, output='help'):
    """Invokes the built-in help system with Cadcorp SIS API lookup enabled.

    Arguments:
    needle -- the subject to search for.
    If it is a string, then it is looked up as a name or part of a name.
    The name is matched in case-insensitive comparison.
    If it is an empty object, then complete help of the sis module is printed.
    If it is an empty object and output is 'list', then list of sis commands is printed.
    If it is any other kind of object, not limited to the Cadcorp SIS API scope,
    then a help page on the object is generated.
    output -- the output format
    If it is 'help', then a help page(s) about the subject(s) is displayed.
    If it is 'list', then only list of names of the matched subjects is displayed.

    The function tries to detect available Cadcorp SIS API and
    either looks for methods in the scope of sis.GisLink class (SISpy)
    or sis module (PySIS).

    Examples:
        >>> sis_help() # sis module help
        >>> sis_help(output='help') # same as above, module help
        >>> sis_help(output='list') # list of all commands
        >>> sis_help('GetViewPrj') # full command name match
        >>> sis_help('Prj', output='list') # partial command name match
        >>> sis_help(sis.GetViewPrj) # PySIS command help
        >>> sis_help(sis.GisLink.GetViewPrj) # SISpy command help
        >>> sis_help(list) # Python built-in type, object, or function help
    """
    if needle and not isinstance(needle, str):
        help(needle)
    elif not needle and output == 'help':
        help(sis)
    else:
        try:
            sis_api = sis.GisLink # SISpy
        except AttributeError:
            sis_api = sis # PySIS

        if not needle and output == 'list':
            methods = sorted([m for m in sis_api.__dict__.items()])
        else:
            methods = sorted([m for m in sis_api.__dict__.items() \
                if (needle.lower() \
                    if isinstance(needle, str) else needle.__name__.lower()) \
                in m[0].lower()], key=lambda m: m[0])

        for (name, method) in methods:
            if output is 'list':
                print(name)
            else:
                help(method)
                print('-' * 50)

# Print startup info banner
print("Startup script for Python in Cadcorp SIS", sis_version())
