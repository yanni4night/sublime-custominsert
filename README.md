sublime-custominsert
====================

A [sublime 2](http://www.sublimetext.com/) plugin that can easily insert custom content.

configuration
===========
_Custominsert.sublime-keymap:_

    {	
    	/*Default data*/
        "data":{},
        
        /*Default content*/
        "content":"Nohting to insert",
        
        /*Default date_format*/
        "date_format":"%Y-%m-%d %H:%M:%S",
        
        /*Default insert position*/
        "position":"cursor",
        
        /*custom actions you can define*/
        "actions":{
        	"datetime":{
        		"content":"{%datetime%}"
        	},
        	"copyright":{
        		"content":"/**\n  * {%file_name%}\n  *\n  * @author {{author}}\n  * @datetime {%datetime%}\n  * @version {{version}}\n  */\n",
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
 - encoding : file encoding(may be Undefined)
 - user : name of the user logged in
 
changelog
===========
 - 2013-11-15:{{}} syntax supported;position custom define supported;multiple actions&position insert supported,more pre-defined supported.
 - 2013-11-14:{%%} syntax supported.

