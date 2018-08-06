#! /bin/bash

# ps에서 -q 옵션에 대해 찾아보기
if ps -ef | grep svd | grep -q python; then # svd 프로세스를 찾고 그 목록 중에서 다시 python이 들어간 프로세스 찾음
  echo Please shutdown supervisor service
  echo "Please run '"${MAUM_ROOT}"/bin/svctl shutdown'"
  exit 1
fi

GROUP_NAME=`/usr/bin/id -ng` # 유저의 그룹을 찾는 명령