#!/bin/bash

# Define Variables and make *.in files list
# sed를 이용한 문자열 자르기 찾기
VERSION_NAME=`${MAUM_ROOT}/bin/m2u-itfd -v | sed 's/m2u-itfd version //'`
# null device 사용법 찾기
IN_FILES=`bin/setup list 2> /dev/null`

# 변수를 이용한 for loop
for in_file in ${IN_FILES}
do
    cp ${MAUM_ROOT}/${in_file} ${MAUM_ROOT}/${VERSION_NAME}.backups/
    diff -u ./${in_file} $MAUM_ROOT/${in_file} >> ${VERSION_NAME}.diff
done

# if -s 옵션은 파일이 존재하고 크기가 0이상인지 검사한다.
if [ -s ${VERSION_NAME}.diff ]; then
    echo "Please check the "${VERSION_NAME}".diff file and run './m2u-reinstall.sh'"
else
    echo "No Changes at in_files!! Please run './m2u-reinstall.sh'"
fi