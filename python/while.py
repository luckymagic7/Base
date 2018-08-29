number = 23
running = True

while running:
    guess = int(raw_input('Enter an integer: '))

    if guess == number:
        print 'You guessed it'
        # this causes the while loop to stop
        running = False
    elif guess < number:
        print 'No'
    else:
        print 'No'
else:
    print 'The while loop is over'

print 'Done'
