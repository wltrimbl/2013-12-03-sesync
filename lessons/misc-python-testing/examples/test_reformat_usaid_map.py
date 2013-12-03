from reformat_usaid_map import (reformat_spec_line,
                                reformat_block,
                                reformat_data,
                                generate_csv)
from StringIO import StringIO
from unittest import TestCase

data = """\
                                                   BDKR4JFL
                                                BDKR4JFL_DICT

                                           C:\exports\BDKR4JFL.DCF
                                    Last Modified:  10/23/2006  2:13:15 PM

--------------------------------------------------------------------------------------------------------------
Level Name                    Level Label                                                  Type            Rec
  Record Name                   Record Label                                              Value  Req  Max  Len
--------------------------------------------------------------------------------------------------------------
HOUSEHOLD                     HOUSEHOLD
  RECORD1                       RECORD1                                                          Yes    1 1590
Level: HOUSEHOLD                                       Record: RECORD1
--------------------------------------------------------------------------------------------------------------
                                                                                 Data Item            Dec Zero
Item Name              Item Label                                     Start  Len Type Type  Occ  Dec Char Fill
--------------------------------------------------------------------------------------------------------------
                         (record type)                                    0    0   AN    I    1    0   No   No
CASEID            (id) Case Identification                                1   15   AN    I    1    0   No   No
MIDX              (id) Index to birth history                            16    1    N    I    1    0   No   No
                               1:6  
V000                   Country code and phase                            17    3   AN    I    1    0   No   No
V001                   Cluster number                                    20    8    N    I    1    0   No   No
                               1:550  
V012                   Current age - respondent                          67    2    N    I    1    0   No   No
                               10:49  
                          (na)        NotAppl
V013                   Age 5-year groups                                 69    1    N    I    1    0   No   No
                               0  10-14
                               1  15-19
                               2  20-24
                               3  25-29
                               4  30-34
                               5  35-39
                               6  40-44
                               7  45-49
                          (na)    NotAppl
"""

for line in data.splitlines():
    if line.startswith('CASEID'):
        spec = line
        break

class ReformatTests(TestCase):

    def test_reformat_spec_line(self):
        self.assertEqual(
            reformat_spec_line(spec),
            ['CASEID', '(id) Case Identification',
                '1', '15', 'AN', 'I', '1', '0', 'No', 'No'])

    def test_reformat_block(self):
        self.assertEqual(
            reformat_block(spec, ['some', 'dummy', 'lines']),
                ['CASEID', '(id) Case Identification',
                    '1', '15', 'AN', 'I', '1', '0', 'No', 'No',
                    'some\ndummy\nlines']),

    def test_reformat_data(self):
        self.assertEqual(
            list(reformat_data(data.splitlines())), [
            ['CASEID', '(id) Case Identification',
                '1', '15', 'AN', 'I', '1', '0', 'No', 'No', ''],
            ['MIDX', '(id) Index to birth history',
                '16', '1', 'N', 'I', '1', '0', 'No', 'No', '1:6'],
            ['V000', 'Country code and phase',
                '17', '3', 'AN', 'I', '1', '0', 'No', 'No', ''],
            ['V001', 'Cluster number',
                '20', '8', 'N', 'I', '1', '0', 'No', 'No', '1:550'],
            ['V012', 'Current age - respondent',
                '67', '2', 'N', 'I', '1', '0', 'No', 'No',
                '10:49\n(na)        NotAppl'],
            ['V013', 'Age 5-year groups',
                '69', '1', 'N', 'I', '1', '0', 'No', 'No',
                ('0  10-14\n1  15-19\n2  20-24\n3  25-29\n4  30-34\n5  35-39\n6  40-44\n'
                 '7  45-49\n(na)    NotAppl')]
            ])

    maxDiff = None
    def test_generate_csv(self):
        inf = StringIO(data)
        inf.name = 'sample'
        outf = StringIO()
        generate_csv(inf, outf)
        self.assertEqual(outf.getvalue().splitlines(), [
            'Map_Name,Item_Name,Item_Label,Start,Len,Data_Type,Item_Type,Occ,Dec,Dec_Char,Zero_Fill,Values',
            'sample,CASEID,(id) Case Identification,1,15,AN,I,1,0,No,No,',
            'sample,MIDX,(id) Index to birth history,16,1,N,I,1,0,No,No,1:6',
            'sample,V000,Country code and phase,17,3,AN,I,1,0,No,No,',
            'sample,V001,Cluster number,20,8,N,I,1,0,No,No,1:550',
            'sample,V012,Current age - respondent,67,2,N,I,1,0,No,No,"10:49',
            '(na)        NotAppl"',
            'sample,V013,Age 5-year groups,69,1,N,I,1,0,No,No,"0  10-14',
            '1  15-19',
            '2  20-24',
            '3  25-29',
            '4  30-34',
            '5  35-39',
            '6  40-44',
            '7  45-49',
            '(na)    NotAppl"',
            ])
