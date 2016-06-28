#Custominsert.py
#
#author yanni4night@gmail.com
#datetime 2013-11-15[14:22:57]
#update   2014-09-13[17:41:53]
#update   2016-06-28[11:46:05]
#version 1.4.0

import sublime, sublime_plugin
import re, datetime, os, socket, json

PLUGIN_NAME = 'Custominsert'

DIRNAME = os.path.dirname(os.path.realpath(__file__));

def get_settings():
    '''
    read sublime-settings file
    '''
    global SETTINGS
    global PLUGIN_NAME
    return sublime.load_settings(PLUGIN_NAME + '.sublime-settings')

def plugin_loaded():
    '''
    This function should be called when plugin loaded.
    It generate context menus and commands automatically.
    '''
    global PLUGIN_NAME
    SETTINGS = get_settings()
    actions = SETTINGS.get('actions') or {}
    action_keys = actions.keys() or []

    if SETTINGS.get('auto_generate_context_menus'):
        menus = []
        for action in action_keys:
            if action is not '':
                menus.append({"id": "custominsert_" + action,"command": "custominsert","args": {"action": action},"caption": "InsertCustom " + action.capitalize()})
        print(json.dumps(menus))
        #update menu profile safely
        try:
            try:
                menuHandle = open(DIRNAME + '/Context.sublime-menu', 'w')
                menuHandle.write(json.dumps(menus, indent = 4))
            finally:
                menuHandle.close()
        except:
            pass

    if SETTINGS.get('auto_generate_commands'):
        commands = []
        for action in action_keys:
            if action is not '':
                commands.append({"caption": "InsertCustom  " + action.capitalize(), "command": "custominsert","args":{"action": action} })
        #update commands profile safely
        try:
            try:
                cmdHandle = open(DIRNAME + '/' + PLUGIN_NAME + '.sublime-commands','w')
                cmdHandle.write(json.dumps(commands, indent = 4))
            finally:
                cmdHandle.close()
        except:
            pass

#load at first
plugin_loaded()

def get_local_ip():
    '''Stupid way to get IP address'''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('w3.org', 80))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'

def get_ext(filename):
    ext = os.path.splitext(filename or '')[1]
    #remove . at start position
    p = re.compile('^\.')
    return re.sub(p, '', ext)

class CustominsertCommand(sublime_plugin.TextCommand):

    def get_settings_param(self, chains = [], default = ''):
        '''get params in dict chains'''
        obj = self.settings
        for e in chains:
            obj = obj.get(e)
            if not obj:
                return default
        return obj

    def get_predefined_param(self, match):
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
        elif key == 'user':
            user = os.getlogin() if 'windows' != sublime.platform() else ''
            if user:
                return user
                #windows?
            user = os.popen('whoami').read()
            p = re.compile('[\r\n]', re.M)
            return re.sub(p, '', user)
        elif key == 'ext':
            return get_ext(self.view.file_name())
        elif key == 'year':
            t = datetime.datetime.today()
            return t.strftime('%Y')
        elif key == 'datetime':
            t = datetime.datetime.today()
            return t.strftime(self.get_action_param('datetime_format', '%Y-%m-%d %H:%M:%S'))
        return match.group(1)

    def get_defined_param(self ,match):
        '''{{}} '''
        key = match.group(1)
        return self.get_settings_param(['actions', self.action, 'data', key], self.get_settings_param(['data', key]))

    def get_action_param(self, key, default = ''):
        '''get params of actions'''
        return self.get_settings_param(['actions', self.action, key], self.get_settings_param([key]))

    def run(self, edit, action = ''):
        global SETTINGS
        v = self.view
        #save settings
        self.settings = get_settings()
        #save action
        self.action = action;
        content = self.get_action_param('content')

        if isinstance(content, dict):
            fext = get_ext(self.view.file_name())
            default_content = content.get('default')
            for ext in content:
                if ext == fext:
                    default_content = content.get(ext) or default_content
                    break
            content = default_content
        #replace {%%}
        p = re.compile('\{%\s*?([\w]+)\s*?%\}', re.LOCALE | re.MULTILINE)
        content = re.sub(p, self.get_predefined_param, content)
        #replace {{}}
        p = re.compile('\{\{\s*?([\w]+)\s*?\}\}', re.LOCALE | re.MULTILINE)
        content = re.sub(p, self.get_defined_param, content)
        #insert position
        if 'start' == self.get_action_param('position'):
            v.insert(edit, 0, content)
        else:
            for sel in v.sel():
                v.insert(edit,sel.begin(), content)
