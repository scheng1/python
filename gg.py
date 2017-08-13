asfdsgagasdgas
import random
import easygui as g

g.msgbox('Clike ok to begin',title='Hi,welcome to this game')
secret = random.randint(1,3)
msg = 'a number from 1 to 3'
title = 'number game'
guess = g.integerbox(msg,title,lowerbound = 1,upperbound = 3)

while True:
    if secret == guess:
        g.msgbox('holy shit U are right')
        g.msgbox('No reward')
        break

    else:
        if secret < guess:
            g.msgbox('too big')
        else:
            g.msgbox('too small')
        guess = g.integerbox(msg,title,lowerbound = 1,upperbound = 3)

g.msgbox('No more game')

print(secret)