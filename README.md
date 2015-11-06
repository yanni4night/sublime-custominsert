sublime-custominsert
====================

A [Sublime](http://www.sublimetext.com/) plugin that can easily insert custom content.It can insert 'copyright',code template,signature,date time or anything else as you want.

Now `Sublime 3` is supported.


install
===========

 - You can use [Package Control](https://sublime.wbond.net) to install.

configuration
===========
_Custominsert.sublime-keymap:_

    {	
    	/*Default data*/
        "data":{},
        
        /*Default content*/
        "content":"Nohting to insert",
        
        /*Default date_format,see https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior*/
        "date_format":"%Y-%m-%d %H:%M:%S",
        
        /*Default insert position*/
        "position":"cursor",
        
        /*custom actions you can define*/
        "actions":{
        	"datetime":{
        		"content":"{%datetime%}"
        	},
        	"copyright":{
        		"content": {
                    "default": "/*{{author}}*/",
                    "php": "<?php{{author}}?>",
                    "py": "#php{{author}}",
                },
        		"data":{
        			"author":"yanni4night",
        			"version":"0.0.1"
        		}
        	}
        }
    }
    
_Default (OSX).sublime-keymap:_

	[
		{ "keys": ["ctrl+c"], "command": "custominsert", "args": {"action":"copyright"} },
		{ "keys": ["ctrl+t"], "command": "custominsert", "args": {"action":"datetime"} }
	]
	
syntax
===========
 - {%var%}:[pre-defined variables](#pre-defined-vars).
 - {{var}}:custom defined variables in _data_ dict.
 
pre-defined vars
===========
 - filename : file name with ext
 - dirname : absolute directory path
 - filepath : absolute file path
 - datetime : date&time
 - platform : 'osx','linux' or 'windows'
 - arch : 'x32' or 'x64'
 - ext : file ext(without '.',may be empty)
 - ip : IP address(may be 'localhost')
 - encoding : file encoding(may be Undefined),you can use 'default_encoding' to override Undefined value
 - user : name of the user logged in
 
changelog
===========
 - 2015-11-06:content by file ext is supported
 - 2015-01-12:sublime 3 is supported
 - 2014-09-13:generate menus&commands automatically
 - 2014-06-21:modified settings
 - 2013-12-30:default_encoding supported
 - 2013-11-19:menus supported.
 - 2013-11-15:{{}} syntax supported;position custom define supported;multiple actions&position insert supported,more pre-defined supported.
 - 2013-11-14:{%%} syntax supported.

