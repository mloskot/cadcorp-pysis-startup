"""
Custom functions for Python in Cadcorp SIS Desktop (PySIS) 8.0 or later.

Author: Mateusz Loskot <mateusz@loskot.net>

This is free and unencumbered software released into the public domain.
For more information, please refer to <http://unlicense.org>
"""
if '__file__' in globals():
    print('|- importing module', __file__)
from cadcorp import sis
import random

def replace_help(namespace):
    def _help(*args, **kwds):
        # because of how the console works. we need our own help() pager func.
        # replace the bold function because it adds crazy chars
        import pydoc
        pydoc.getpager = lambda: pydoc.plainpager
        pydoc.Helper.getline = lambda self, prompt: None
        pydoc.TextDoc.use_bold = lambda self, text: text

        pydoc.help(*args, **kwds)

    namespace["help"] = _help

replace_help(globals())

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
            sis_api = sis.GisLink  # SISpy
        except AttributeError:
            sis_api = sis  # PySIS

        if not needle and output == 'list':
            methods = sorted([m for m in sis_api.__dict__.items()])
        else:
            methods = sorted(
                [m for m in sis_api.__dict__.items()
                 if (needle.lower()
                     if isinstance(needle, str) else needle.__name__.lower())
                 in m[0].lower()], key=lambda m: m[0])

        for (name, method) in methods:
            if output == 'list':
                print(name)
            else:
                help(method)
                print('-' * 50)


def find_crs(needle):
    """Searches for any Coordinate Reference System with name matching given string.
    Examples:
        >>> find_crs('pseudo-mercator')
        WGS 84.Pseudo-Mercator (EPSG:3857)
    """
    prjs = sis.NolCatalog("APrj", False).split('\t')
    for prj in prjs:
        if needle.lower() in prj.lower():
            epsg = 0
            try:
                epsg = sis.GetPrjCode(prj)
            except sis.GisLinkError:
                pass
            print(prj, "(EPSG:%d)" % epsg)

def random_points_mm(count, xmm, ymm, zmm):
    """xmm, ymm, zmm -  pairs of min and max values for X, Y and Z

    TODO: sis.Process will be much faster
    """
    print('"Generating', count, '"random points within X={}, Y={}, Z={}'.format(xmm, ymm, zmm))
    for _ in range(0, count):
        x = random.uniform(xmm[0], xmm[1])
        y = random.uniform(ymm[0], ymm[1])
        z = random.randint(zmm[0], zmm[1])
        sis.CreatePoint(x, y, z, 'Star', 1, 1)

def random_points(count):
    """Generate random points in range of the current view extent.
    """
    ext = view_extent()
    random_points_mm(count, (ext[0], ext[3]), (ext[1], ext[4]), (int(ext[2]), int(ext[5])))

def split_extent(csv_ext):
    """Splits '1,2,3,4,5,6' string to six separate values:
    x1, y1, z1, x2, y2, z2 = SplitExtent('1,2,3,4,5,6')
    """
    return [float(x) for x in csv_ext.split(',')]

def view_extent():
    """Return current view extent via `sis.GetViewExtent`.
    """
    return split_extent(sis.GetViewExtent())

#
# Selection
#
def selection_ids():
    """Returns IDs of all selected items.
    Dictionary mapping source dataset to selected items.
    """
    sis.CreateListFromSelection("selected")
    details = sis.GetListDetails("selected").split(":")
    sis.EmptyList("selected")
    if not details or not details[0]:
        #    raise RuntimeError("no items selected")
        return {}
    assert details and len(details) % 2 == 0
    ids = {}
    for i in range(0, len(details), 2):
        ids[int(details[i])] = [int(x) for x in details[i + 1].split(",")]
    assert ids
    return ids

#
# Properties
#
def prop(name, find_item_id = None):
    """name - name of property to be fetched from currently selected item(s)
    """
    ids = selection_ids()
    values = []
    for (ds_id, item_ids) in ids.items():
        for item_id in item_ids:
            sis.OpenExistingDatasetItem(ds_id, item_id)
            value = sis.GetProperty(sis.SIS_OT_CURITEM, 0, name)
            sis.CloseItem()
            if find_item_id and find_item_id == item_id:
                return value
            else:
                values.append(value)
    return values

#
# Geometry Representation
#
def _gr(cmd, fmt, fmt_plus=False):
    ids = selection_ids()
    grs = []
    if fmt_plus:
        fmt += 100
    for (ds_id, item_ids) in ids.items():
        crs = sis.GetProperty(sis.SIS_OT_DATASET, ds_id, '_crs$')
        for item_id in item_ids:
            sis.OpenExistingDatasetItem(ds_id, item_id)
            grs.append(cmd(crs, fmt, 0))
            sis.CloseItem()
    return grs

def hexwkb(fmt_plus=False):
    return _gr(sis.GetBlob, sis.SIS_BLOB_OGIS_HEXWKB, fmt_plus)

def wkb(fmt_plus=False):
    return _gr(sis.GetBlobB, sis.SIS_BLOB_OGIS_WKB, fmt_plus)

def wkt(fmt_plus=False):
    return _gr(sis.GetBlob, sis.SIS_BLOB_OGIS_WKT, fmt_plus)

def gj(fmt_plus=False):
    return _gr(sis.GetBlob, sis.SIS_BLOB_GEOJSON, fmt_plus)
