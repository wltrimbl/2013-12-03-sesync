#!/bin/sh
newdir='new_test_results'
olddir='test_results'
rm -rf $newdir
mkdir $newdir
python reformat_usaid_map.py test_data/BDKR4JFL.MAP $newdir/BDKR4JFL.CSV >$newdir/data1.stdout 2>$newdir/data1.stderr
python reformat_usaid_map.py test_data/nosuchfile $newdir/nosuchfile.results >$newdir/nosuchfile.stdout 2>$newdir/nosuchfile.stderr
python reformat_usaid_map.py test_data/BDKR4JFL.MAP no_such_dir/nosuchdir.results >$newdir/nosuchdir.stdout 2>$newdir/nosuchdir.stderr
diff -r test_results new_test_results
if [ "$?" == "0" ]; then
    echo "Tests succeeded"
    rm -rf new_test_results
else
    echo
    echo "!!! Tests failed !!!"
    echo
fi
