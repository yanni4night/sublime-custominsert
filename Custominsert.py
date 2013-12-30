#Custominsert.py
#
#author yanni4night@gmail.com
#datetime 2013-11-15 14:22:57
#version 0.0.1

import sublime, sublime_plugin
import re,datetime,os,socket


def get_local_ip():
    '''Stupid way to get IP address'''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('w3.org',80))
        return s.getsockname()[0]
    except Exception, e:
        return '127.0.0.1'


class CustominsertCommand(sublime_plugin.TextCommand):

    def get_settings_param(self,chains = [],default = ''):
        '''get params in dict chains'''
        obj = self.settings
        for e in chains:
            obj = obj.get(e)
            if not obj:
                return default
        return obj

    def get_predefined_param(self,match):
        '''{%%}'''
        key = match.group(1)
        if key == 'filename':
            return os.path.basename(self.view.file_name() or '')
        elif key == 'filepath':
            return self.view.file_name() or ''
        elif key == 'dirname':
            return os.path.dirname(self.view.file_name() or '')
        elif key == 'platform':
            return sublime.platform()
        elif key == 'arch':
            return sublime.arch()
        elif key == 'encoding':
            encoding = self.view.encoding()
            return encoding if 'Undefined' != encoding else self.settings.get('default_encoding')
        elif key == 'ip':
            return get_local_ip()
            ipaddrlist = socket.gethostbyname_ex(socket.gethostname())
            ips = ''
            for e in ipaddrlist:
                if isinstance(e,list):
                    for k in e:
                        ips += " "+k
                else:
                    ips += e
            return ips
        elif key == 'user':
            user = os.getlogin() if 'windows' != sublime.platform() else ''
            if user:
                return user
                #windows?
            user = os.popen('whoami').read()
            p = re.compile('[\r\n]',re.M)
            return re.sub(p,'',user)
        elif key == 'ext':
            ext = os.path.splitext(self.view.file_name() or '')[1]
            #remove . at start position
            p = re.compile('^\.')
            return re.sub(p,'',ext)
        elif key == 'datetime':
            t = datetime.datetime.today()  
            return t.strftime(self.get_action_param('datetime_format','%Y-%m-%d %H:%M:%S'))
        return match.group(1)

    def get_defined_param(self,match):
        '''{{}} '''
        key = match.group(1)
        return self.get_settings_param(['actions',self.action,'data',key],self.get_settings_param(['data',key]))

    def get_action_param(self,key,default = ''):
        '''get params of actions'''
        return self.get_settings_param(['actions',self.action,key],self.get_settings_param([key]))

    def run(self, edit,action = ''):
        v = self.view
        settings_name = 'Custominsert'
        settings =sublime.load_settings(settings_name + '.sublime-settings') or {}
        #save settings
        self.settings = settings
        #save action
        self.action = action;
        content = self.get_action_param('content')
        #replace {%%}
        p = re.compile('\{%\s*?([\w]+)\s*?%\}',re.LOCALE|re.MULTILINE)
        content = re.sub(p,self.get_predefined_param,content)
        #replace {{}}
        p = re.compile('\{\{\s*?([\w]+)\s*?\}\}',re.LOCALE|re.MULTILINE)
        content = re.sub(p,self.get_defined_param,content)
        #insert position
        if 'start' == self.get_action_param('position'):
            v.insert(edit, 0, content)
        else:
            for sel in v.sel():
                v.insert(edit,sel.begin(), content)
