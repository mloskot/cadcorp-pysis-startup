if '__file__' in globals():
    print('|- importing module', __file__)
import os
from cadcorp import sis

def create_from_gr(str_or_filename, zoom=True, proj='*APrjPC', run_test=False, stop_test_on_failure=False):
    '''Creates new item(s) from textual geometry representation.
    The input text can be passed directly or read from lines in given file.
    '''
    def create_item(item_text, proj):
        # Plus formats by default
        fmt = sis.SIS_BLOB_OGIS_WKT + 100
        if item_text[:2] == '0x':
            fmt = sis.SIS_BLOB_OGIS_HEXWKB + 100
        elif item_text[:2] == '00' or item_text[:2] == '01':
            fmt = sis.SIS_BLOB_OGIS_WKB + 100
        elif item_text[0] == '{' or  item_text[-1] == '}':
            fmt = sis.SIS_BLOB_GEOJSON + 100

        if fmt in (sis.SIS_BLOB_OGIS_WKB, sis.SIS_BLOB_OGIS_WKB + 100):
            sis.CreateItemB(bytearray.fromhex(item_text), proj, fmt)
        else:
            sis.CreateItem(item_text, proj, fmt)

    test_result = 'FAIL'
    tests_count = { 'RUN': 0, 'PASS': 0, 'FAIL': 0 }
    lines = []
    if os.path.exists(str_or_filename):
        with open(str_or_filename, 'r') as f:
            lines = f.readlines()
    else:
        assert type(str_or_filename) == str
        lines = [ str_or_filename ]

    for line in lines:
        item_text = line.strip()
        test_expect_fail = False
        if item_text[0] == '!':
            test_expect_fail = True
            item_text = item_text[1:]
        if not item_text or item_text[0] == '#':
            continue # skip comment

        tests_count['RUN'] += 1
        if run_test:
            print('Test {0:>3} {1}'.format(tests_count['RUN'], item_text[:100]))

        try:
            create_item(item_text, proj)

            test_result = 'FAIL' if test_expect_fail else 'PASS'
        except:
            if run_test:
                test_result = 'PASS' if test_expect_fail else 'FAIL'
            else:
                print(item_text[:100])
                raise

        if run_test:
            print('{0:>8} {1}'.format(test_result, '(failed as expected)' if test_expect_fail else ''))
            if test_result == 'FAIL' and stop_test_on_failure:
                raise RuntimeError('stop test on failure')
            assert test_result
            tests_count[test_result] += 1

    if zoom:
        try:
            sis.ZoomExtent()
        except:
            pass

    if run_test:
        print('Tests summary:')
        for k,v in tests_count.items():
            print('{0: >4}: {1}'.format(k, v))
