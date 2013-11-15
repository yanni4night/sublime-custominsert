sublime-custominsert
====================

A sublime 2 plugin that can easily insert custom content.

configuration
===========
_Custominsert.sublime-keymap:_

    {	
    	/*Default data*/
        "data":{},
        
        /*Default content*/
        "content":"Nohting to insert",
        
        /*Default date_format*/
        "date_format":"%Y-%m-%d[%H:%M:%S]",
        
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
        			"author":"yanni4night@gmail.com",
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
 - {%var%}:pre-defined vars
 - {{var}}:custom defined vars in _data_ dict
 
pre-defined vars
===========
 - file_name
 - file_path
 - datetime
 - platform
 - arch
 
changelog
===========
 - 2013-11-15:{{}} syntax supported;position custom define supported;multiple actions&position insert supported.
 - 2013-11-15:{%%} syntax supported.

