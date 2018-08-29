# -*- coding: utf-8 -*-
x = 50

def func():
    # global을 통해 x가 전역 변수임을 선언
    # 이후로, x에 값을 대입하면 메인 블록의 x 값 또한 변경됨
    global x

    print 'x is', x
    x = 2 # func함수 밖의 x도 2로 값 변경됨
    print 'Changed global x to', x

func()
print 'Value of x is', x

