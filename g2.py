import easygui as g

msg = 'Please input personal information'
title = 'Account Center'
fieldnames = ['*User name','*Real name','Fixed telephone','*telephone number','  QQ','E-mail']
fieldvalues = []
fieldvalues = g.multenterbox(msg,title,fieldnames)

while 1:
    if fieldvalues == None:
        break
    errmsg = ''
    for i in range(len(fieldvalues)):
        option = fieldnames[i].strip()
        if fieldvalues[i] == '' and option[0] == '*':
            errmsg += ('%s is Required Field. \n \n' % option)
            print(errmsg)
    if errmsg == '':
        break
    fieldvalues = g.multenterbox(msg,title,fieldnames)
        
print('user profiles as follow: %s' % str(fieldvalues))