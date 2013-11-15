import sublime, sublime_plugin
import re,datetime,os

class CustominsertCommand(sublime_plugin.TextCommand):
    def get_predefined_param(self,match):
        '''get_predefined_param'''
        key=match.group(1)
        if key=='file_name':
            return os.path.basename(self.view.file_name() or '')
        elif key=='datetime':
            t=datetime.datetime.today()  
            return t.strftime('%Y-%m-%d %H:%M:%S')
        return match.group(1)
    def get_defined_param(self,match):
        ''' '''
        key=match.group(1)
        return self.settings.get(key,"")
    def run(self, edit):
        v=self.view
        settings_name = 'Custominsert'
        settings =sublime.load_settings(settings_name + '.sublime-settings')
        self.settings=settings
        content=settings.get('__content__','')
        p=re.compile('\{%\s*?([\w]+)\s*?%\}')
        content=re.sub(p,self.get_predefined_param,content)
        p=re.compile('\{\{\s*?([\w]+)\s*?\}\}')
        content=re.sub(p,self.get_defined_param,content)
        if 'start'==settings.get('__position__'):
            v.insert(edit, 0, content)
        else:
            v.insert(edit,v.sel()[0].begin(), content)