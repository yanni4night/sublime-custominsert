#Custominsert.py
#
#author yanni4night@gmail.com
#datetime 2013-11-15 14:22:57
#version 0.0.1

import sublime, sublime_plugin
import re,datetime,os

class CustominsertCommand(sublime_plugin.TextCommand):
    def get_predefined_param(self,match):
        '''{%%}'''
        key=match.group(1)
        if key=='file_name':
            return os.path.basename(self.view.file_name() or '')
        elif key=='datetime':
            t=datetime.datetime.today()  
            return t.strftime(self.settings.get('__datetime_format__','%Y-%m-%d %H:%M:%S'))
        return match.group(1)
    def get_defined_param(self,match):
        '''{{}} '''
        key=match.group(1)
        return self.settings.get(key,"")
    def run(self, edit):
        v=self.view
        settings_name = 'Custominsert'
        settings =sublime.load_settings(settings_name + '.sublime-settings')
        #save settings
        self.settings=settings
        content=settings.get('__content__','__content__ NOT DEFINED')
        #replace {%%}
        p=re.compile('\{%\s*?([\w]+)\s*?%\}')
        content=re.sub(p,self.get_predefined_param,content)
        #replace {{}}
        p=re.compile('\{\{\s*?([\w]+)\s*?\}\}')
        content=re.sub(p,self.get_defined_param,content)
        #insert position
        if 'start'==settings.get('__position__','start'):
            v.insert(edit, 0, content)
        else:
            v.insert(edit,v.sel()[0].begin(), content)