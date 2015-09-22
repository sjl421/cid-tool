#!/bin/bash

if ! test -e bin/citool; then
    echo "Invoke from CITool project root!"
    exit 1
fi

echo "Python 3"
nosetests3 \
    tests/citool_git_test.py:Test_CITool_Git \
    tests/citool_hg_test.py:Test_CITool_Hg \
    tests/citool_svn_test.py:Test_CITool_SVN

echo "Python 2.x"
nosetests \
    tests/citool_git_test.py:Test_CITool_Git \
    tests/citool_hg_test.py:Test_CITool_Hg \
    tests/citool_svn_test.py:Test_CITool_SVN
