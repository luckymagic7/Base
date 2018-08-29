# -*- coding: utf-8 -*-
while True:
    s = raw_input('Enter something: ')
    if s == 'quit':
        break
    if len(s) < 3:
        print 'Too small'
        # 3보다 작으면 continue가 실행되어
        # 다음 loop로 넘어가는데, 다음 루프가 없으므로
        # 다시 while의 첫 부분으로 넘어간다
        continue 
    print 'input is of sufficient length'

