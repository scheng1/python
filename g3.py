import easygui as g
import os

file_path = g.fileopenbox(default='*')

with open(file_path,'r+') as f:
    title = os.path.basename(file_path)
    msg = 'file %s content as follow:' % title
    text = f.read()
    a=g.textbox(msg,title,text)

    f.seek(0,0)
    f.write(a)
    #print(type(a))