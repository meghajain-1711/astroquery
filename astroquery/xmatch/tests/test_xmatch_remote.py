import os.path

import pytest
from astropy.tests.helper import remote_data

from ...xmatch import XMatch


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@pytest.fixture
def xmatch():
    return XMatch()


@remote_data
def test_xmatch_avail_tables(xmatch):
    tables = xmatch.get_available_tables('txt').splitlines()
    assert tables
    # those example tables are from
    # http://cdsxmatch.u-strasbg.fr/xmatch/doc/API-calls.html
    assert 'II/311/wise' in tables
    assert 'II/246/out' in tables


@remote_data
def test_xmatch_is_avail_table(xmatch):
    assert xmatch.is_available_table('II/311/wise')
    assert xmatch.is_available_table('II/246/out')
    assert not xmatch.is_available_table('vizier:II/311/wise')


@remote_data
def test_xmatch_query(xmatch):
    expected_csv_output = """angDist,ra,dec,2MASS,RAJ2000,DEJ2000,errHalfMaj,errHalfMin,errPosAng,Jmag,Hmag,Kmag,e_Jmag,e_Hmag,e_Kmag,Qfl,Rfl,X,MeasureJD
1.352044,267.22029,-20.35869,17485281-2021323,267.220049,-20.358990,0.150,0.110,16,9.931,8.822,7.550,0.239,0.241,,EEU,226,2,2450950.8609
1.578188,267.22029,-20.35869,17485288-2021328,267.220348,-20.359125,0.140,0.120,158,8.868,7.784,8.530,,,0.128,UUB,662,2,2450950.8609
3.699368,267.22029,-20.35869,17485264-2021294,267.219344,-20.358171,0.130,0.120,33,9.562,8.525,9.445,,,0.119,UUB,662,2,2450950.8609
3.822922,267.22029,-20.35869,17485299-2021279,267.220825,-20.357754,0.080,0.070,7,10.756,9.725,9.287,0.139,0.127,0.103,EBA,222,2,2450950.8609
4.576677,267.22029,-20.35869,17485255-2021326,267.218994,-20.359064,0.140,0.130,87,10.431,9.348,7.926,0.159,0.316,,CEU,226,2,2450950.8609
0.219609,274.83971,-25.42714,18192154-2525377,274.839773,-25.427162,0.060,0.060,90,9.368,8.431,7.919,0.024,0.044,0.036,AAA,211,0,2451407.5033
1.633225,275.92229,-30.36572,18234133-3021582,275.922233,-30.366171,0.080,0.080,55,12.947,12.334,12.145,0.156,0.221,0.127,EEE,222,2,2451021.7212
0.536998,283.26621,-8.70756,18530390-0842276,283.266284,-8.707690,0.060,0.060,45,12.182,11.534,11.380,0.057,0.071,0.063,AAA,222,0,2451301.7945
1.178542,306.01575,33.86756,20240382+3352021,306.015944,+33.867275,0.060,0.060,90,13.575,12.684,12.321,0.025,0.027,0.026,AAA,222,0,2450948.9708
0.853178,322.493,12.16703,21295836+1210007,322.493171,+12.166862,0.100,0.080,179,9.798,9.339,9.176,0.109,0.150,0.100,EEA,222,0,2451080.6935
4.503950,322.493,12.16703,21295861+1210023,322.494242,+12.167332,0.100,0.080,1,10.057,9.720,9.483,0.077,0.136,0.088,EEE,222,0,2451080.6935
"""
    with open(os.path.join(DATA_DIR, 'posList.csv')) as pos_list:
        res = xmatch.query(
            pos_list, 'vizier:II/246/out', 5, 'csv', 'ra', 'dec')
        assert res.text == expected_csv_output
