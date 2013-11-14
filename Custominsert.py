import sublime, sublime_plugin
import re,datetime,os


#g_settings={};
#
#def settings_changed():
    #for window in sublime.windows():
        #for view in window.views():
            #reload_settings(view)
#
#def reload_settings(view):
    #'''Restores user settings.'''
    #settings_name = 'Custominsert'
    #settings = sublime.load_settings(settings_name + '.sublime-settings')
    #settings.clear_on_change(settings_name)
    #settings.add_on_change(settings_name, settings_changed)
    #g_settings=settings
#

class CustominsertCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view=view
        reload_settings(view)
    def get_predefine_param(self,match):
        '''get_predefine_param'''
        key=match.group(1)
        if key=='file_name':
            return os.path.basename(self.view.file_name())
        elif key=='datetime':
            t=datetime.datetime.today()  
            return t.strftime('%Y-%m-%d %H:%M:%S')
        return match.group(1)
    def run(self, edit):
        v=g_view=self.view
        settings_name = 'Custominsert'
        settings =sublime.load_settings(settings_name + '.sublime-settings')
        content=settings.get('content','')
        p=re.compile('\{%\s*?([\w]+)\s*?%\}')
        content=re.sub(p,self.get_predefine_param,content)
        v.insert(edit, v.sel()[0].begin(), content)
