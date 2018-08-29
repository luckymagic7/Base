number = 23
guess = int(raw_input('Enter an integer : '))

if guess == number:
    # New block start here
    print 'Congratulations, you guessed it.'
    print '(but you do not win any prizes!)'
    # New block ends here
elif guess < number:
    # Another block
    print 'No, it is a little higher than that'
    # You can do whatever you want in a block
else:
    print 'No, it is a little lower than that'

print 'Done'
