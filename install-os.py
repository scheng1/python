#!/usr/bin/python
# -*- coding: utf-8

# 此脚本基于python3编写；所以需要在执行脚本的机器上安装Python3.*
#pip3 会伴随Python3.* 安装
# tar -xvf Python-3.4.4.tgz && ./configure --prefix=/user/local/python34 && “make && make install”
# 如果出错是因为一些依赖没有安装：yum install -y gcc && yum install openssl-devel（for pip3）
# 为 python3；pip3 配置 软连接

import sys
import os
import subprocess
import re
import pexpect    # need install by pip ("pip3 install pexpect")

def judge_retcode(n,name_log):
    if n == 0:
        print('***'+name_log+': Success')
        return 0
    else:
        str_storage = '******'+name_log+': Installation log'+'******'
        print(str_storage)
        with open('/tmp/'+name_log+'.log', 'r') as f:
            for line in f.readlines():
                print('####',line.strip()) # delete'\n'
        print('*'*len(str_storage))
        raise Exception('shell executing error')
        #print('shell executing error')
def replace_os_repo(repo):
    if os.path.exists(centos_paas_repo) == True:
        os.rename(centos_paas_repo,centos_paas_repo+'.bak')
    files=os.listdir(an_location+'/roles/openshift_repos/files/origin/repos/')
    for file in files:
        if file.endswith(".repo"):
            os.remove(an_location+"/roles/openshift_repos/files/origin/repos/"+file)
    cmd = 'cp '+centos_base_repo+' '+repo
    judge_retcode(subprocess.call(cmd,shell=True),'Replace Repo ')
    #since os only recognize openshift-ansible-centos-paas-sig.repo
    cmd = 'mv '+repo+' '+centos_paas_repo
    judge_retcode(subprocess.call(cmd,shell=True),'Rename ')

def clean_and_makecahe():
    cmd = 'yum clean all && yum makecache'
    judge_retcode(subprocess.call(cmd,shell=True),'Yum makecache')

def glb_vars():
    arr_vars=['host_location','an_location','centos_paas_repo','centos_base_repo']
    for var in arr_vars:
        var_bool = var in dir()
        if var_bool == False:
            if var == 'host_location':
                global host_location
                host_location = input('please input the hosts file location(Absolute address like /aa/bb): ').strip()         
            elif var == 'an_location':
                global an_location
                print('\n',use_style('Please confirm the current branch of openshift-ansible !!!',fore = 'blue'))
                an_location = input('please input the openshift-ansible directory location(Absolute address like /aa/openshift-ansible): ').strip()               
            elif var == 'centos_paas_repo':
                global centos_paas_repo
                centos_paas_repo = an_location+'/roles/openshift_repos/files/origin/repos/openshift-ansible-centos-paas-sig.repo'               
            else:
                global centos_base_repo    
                centos_base_repo = '/etc/yum.repos.d/CentOS-Base.repo'                
            #global var
        else:
            return
def use_style(string, mode='', fore='', back=''):
    STYLE = {
        'fore': {
                'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
                'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
        },
        'back': {
                'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
                'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
        },
        'mode': {
                'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
        },
        'default': {
                'end': 0,
        }
    }

    mode = '%s' % STYLE['mode'][mode] if STYLE['mode'].__contains__(mode) else '1'
    fore = '%s' % STYLE['fore'][fore] if STYLE['fore'].__contains__(fore) else '31'
    back = '%s' % STYLE['back'][back] if STYLE['back'].__contains__(back) else '40'
    style = ';'.join([s for s in [mode, fore, back] if s])
    style = '\033[%sm' % style if style else ''
    end = '\033[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end) 

def step1():

    print('\n',use_style('-'*18+'Step 1 Setting the repo file'+'-'*18,fore = 'yellow'))

    glb_vars()
    flag = True
    while flag:
        print('if U choose 163 repo, it will replace the OS default repo!')
        arg1=input('Do u want to use 163 repo?(y/n): ');
        arg1 = arg1.strip().lower()
        if arg1 == 'y' or arg1 == 'yes':
            if os.path.exists(centos_base_repo) == True:
                #cmd = 'mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak'
                #judge_retcode(subprocess.call(cmd,shell=True))
                os.rename(centos_base_repo,centos_base_repo+'.bak')
            name_log = 'Repo'
            cmd = 'wget http://mirrors.163.com/.help/CentOS6-Base-163.repo -O /etc/yum.repos.d/CentOS-Base.repo > /tmp/'+name_log+'.log 2>&1'
            judge_retcode(subprocess.call(cmd,shell=True),name_log)
            file_ob = open('/etc/yum.repos.d/CentOS-Base.repo','a')
            seq = ['\n[paas]\n','name=CentOS-$releasever - Paas- 163.com\n'\
            'baseurl=http://mirrors.163.com/centos/$releasever/paas/$basearch/openshift-origin/\n',\
            'gpgcheck=0\n', 'enabled=1\n','gpgkey=http://mirrors.163.com/centos/RPM-GPG-KEY-CentOS-7\n']
            file_ob.writelines( seq )
            file_ob.close()
            centos_163_repo = an_location+'/roles/openshift_repos/files/origin/repos/openshift-ansible-163-paas-sig.repo'
            #if os.path.exists(centos_paas_repo) == True:
            #    os.rename(centos_paas_repo,centos_paas_repo+'.bak')
            #cmd = 'cp '+centos_base_repo+' '+centos_163_repo
            #judge_retcode(subprocess.call(cmd,shell=True),'163 repo replace')
            replace_os_repo(centos_163_repo)
            clean_and_makecahe()
            flag=False
        elif arg1 == 'n'or arg1 == 'no':
            arg2=input('Do u want to use U own repo?(y/n): ')
            arg2 = arg2.strip().lower()
            if arg2 == 'y'or arg2 == 'yes':
                centos_own_repo = an_location+'/roles/openshift_repos/files/origin/repos/openshift-ansible-own-paas-sig.repo'
                repo_location=input('The Repo file location(Absolute address like "/aa/bb.repo"): ').strip()
                if os.path.exists(repo_location) == True:
                    if os.path.exists(centos_base_repo) == True:
                        if repo_location == centos_base_repo:
                            replace_os_repo(centos_own_repo)
                            print('The repo file is ready')
                            clean_and_makecahe()
                            break
                        os.rename(centos_base_repo,centos_base_repo+'.bak')
                    cmd = 'cp '+repo_location+' '+centos_base_repo
                    name_log = 'Repo'
                    judge_retcode(subprocess.call(cmd,shell=True),name_log)
                    replace_os_repo(centos_own_repo)
                    clean_and_makecahe()
                else:
                    #print('The repo does not exit !!!')
                    raise Exception('The repo does not exit !!!')
            else:
                print('We will use the local repo file!' )
            flag=False

        else:
            print('Illegal Input!!!')
    print()

def step2():

    print('\n',use_style('-'*18+'Step 2 Check the components '+'-'*18,fore = 'yellow'),'\n')
    print(use_style("You'd better have carried out the step1 before perfrom this step2",fore = 'blue'))
    args1=['ansible','pyOpenSSL','python2-cryptography','python-lxml']
    for arg3 in args1:
            cmd ='rpm -qa | grep '+arg3+' >/dev/null'
            #judge_retcode(retcode = subprocess.call(cmd,shell=True),arg3)
            retcode = subprocess.call(cmd,shell=True)
            if retcode == 0:
                print(use_style(arg3+': '+'Already installed',fore = 'green'))
            else:
                    print(use_style(arg3+': '+'Not installed'))
                    print(use_style('##### Installing '+arg3+' #####',fore = 'green'),'\n' )
                    cmd = 'yum install -y '+arg3+ ' >/tmp/'+arg3+'.log 2>&1'
                    retcode = subprocess.call(cmd,shell=True)
                    if retcode == 0:
                        print(use_style(arg3+': Already installed',fore = 'green'))
                    else:
                        str_storage = '*'*22+arg3+': Installation log'+'*'*22
                        print(use_style(str_storage),)
                        with open('/tmp/'+arg3+'.log', 'r') as f:
                            for line in f.readlines():
                                print('####',line.strip()) # '\n'
                        print(use_style('*'*len(str_storage)))
    	
    print()

def step3():

    print('\n',use_style('-'*18+' Step 3 Free password login '+'-'*18,fore = 'yellow'))

    print(use_style('User "root" would allow ssh based auth without requiring a password!!!',fore = 'blue'))
    flag = True
    while flag: 
        node_ips = input(use_style('The machines IPS splited with ";"(like 1.1.1.1;2.2.2.2 or 1.1.1.[1-9]): ', fore = 'green'))
        print()
        node_ips_list = node_ips.strip().split(';')
        pattern = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        fg = True
        for ip in node_ips_list:
            ip = ip.strip()
            if pattern.match(ip):
                if fg == True:
                    flag = False
            else:
                print(use_style(ip+': Invalid IP Address!!!'))
                fg = False
                flag = True
                continue
    if os.path.exists('/root/.ssh/id_rsa') == False:
        #os.remove('/root/.ssh/id_rsa')
        #os.remove('/root/.ssh/id_rsa.pub')
        cmd = 'ssh-keygen -t rsa'
        print(use_style('******** U can entry [Enter key] to choose default option *******',fore = 'yellow'))
        subprocess.call(cmd,shell=True)
    elif os.path.exists('/root/.ssh/id_rsa.pub') == False:
        os.remove('/root/.ssh/id_rsa')
        print(use_style('*** U can entry [Enter key] to choose default option ***', fore = 'yellow'))
        cmd = 'ssh-keygen -t rsa'
        subprocess.call(cmd,shell=True)
    for ip in node_ips_list:
        ip = ip.strip()
        cmd = 'ssh root@'+ip
        child = pexpect.spawn(cmd)
        try:
            ret = child.expect(['[Pp]assword:','continue connecting (yes/no)?','[$#]'],timeout=5)
            if ret == 0:
                child.close()
                cmd = 'ssh-copy-id -i  /root/.ssh/id_rsa.pub root@'+ip
                #child = pexpect.spawn(cmd)
                retcode = subprocess.call(cmd,shell=True)
                if retcode == 0:
                    print(use_style("***** U can login "+ip+" without passwd *****",fore = 'green'),'\n')
                else:
                    raise Exception(use_style('The \"'+cmd+'\" command execution failed  !!!'))
            elif ret == 1:
                child.sendline('yes')
                child.expect('password:')
                child.close()
                cmd = 'ssh-copy-id -i  /root/.ssh/id_rsa.pub root@'+ip
                #child = pexpect.spawn(cmd)
                retcode = subprocess.call(cmd,shell=True)
                if retcode == 0:
                    print(use_style("***** U can login "+ip+" without passwd *****",fore = 'green'),'\n')
                else:
                    raise Exception(use_style('The \"'+cmd+'\" command execution failed  !!!'))
            elif ret == 2:
                child.sendline('exit')
                ret = child.expect(['closed'],timeout=5)
                if ret == 0:
                    print(use_style("***** U are already able to login "+ip+" without passwd *****",fore = 'green'),'\n')
                    child.close()
                else:
                    child.close()
                    raise Exception(use_style('##### Something Wrong !!! #####'))

        except pexpect.EOF:
            print(use_style("EOF"))
            child.close()
            sys.exit(0)
        except pexpect.TIMEOUT:
            print(use_style('TIMEOUT: Can not connect to '+ip))
            child.close()
            sys.exit(0)

#        retcode = subprocess.call(cmd,shell=True)
#        if retcode == 0:
#            print(use_style("***** U are already able to login "+ip+" without passwd *****",fore = 'green'),'\n')
#        else:
#            cmd = 'ssh-copy-id -i  /root/.ssh/id_rsa.pub root@'+ip
#            retcode = subprocess.call(cmd,shell=True)
#            if retcode == 0:
#                print(use_style("***** U can login "+ip+" without passwd *****",fore = 'green'),'\n')
#            else:
#                raise Exception(use_style('The \"'+cmd+'\" command execution failed  !!!'))

    print()

def step4():
    print('\n',use_style('-'*18+' Step 4 Advanced install OS ORIGIN by ansible '+'-'*18,fore = 'yellow'))
    

#-----------------------------------------------------------------------------------------
try:
    print('\033[1;33;40m')
    print('**************************************************')
    print('* exit: 0                                        *')
    print('* Step 1 Setting the repo file                   *')
    print('* Step 2 Check the components                    *')
    print('* Step 3 Free password login                     *')
    print('* Step 4 Advanced install OS ORIGIN by ansible   *')
    print('**************************************************')
    print('\033[0m')

    flag = True
    while flag:
        ch_steps = input(use_style('which steps do U want to execute?(like 1,2): ',fore = 'green'))
        steps_list = ch_steps.strip().split(',')
        fg = True
        for m in steps_list:
            m = m.strip()
            if re.match(r'^[0-4]$', m):
                if fg == True:
                    flag = False
            else:    
                print(use_style(m+': Invalid Input!!!'))
                fg = False
                flag = True
                continue

    for n in steps_list:
        n = n.strip()
        if n == '0':
            exit()
        if n == '1':
            step1()
        if n == '2':
            step2() 
        if n == '3':
            step3()
        if n == '4':
            print('\n',use_style('Perform  Step4, U  have to make sure that Step1,2,3 have been performed.\n \
If not, please input "no" to exit !!! ', fore = 'blue'))
            flag_4 = True
            while flag_4:
                confirm = input(use_style('Do U have performed Step1,2,3?(like yes/no): ',fore = 'green'))
                confirm = confirm.strip().lower()
                if confirm == 'yes' or confirm == 'y':
                    flag_4 = False
                    step4()
                elif confirm == 'no' or confirm == 'n':
                    flag_4 = True
                    sys.exit(0)
                else:
                    print(use_style(confirm+': Invalid Input!!!'))

except KeyboardInterrupt:
    print('\n','\n',use_style('##### Ctrl+C:Forced exit #####',fore = 'purple'))
    
finally:    
    print('\n',use_style('*'*30+'end'+'*'*30,fore = 'yellow'))

