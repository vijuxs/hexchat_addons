
__module_name__ = "ud"
__module_version__ = "1.0"
__module_description__ = "Gets the Urban Dictionary"

import hexchat
import requests
import re


#TODO add colors

data = None
full_data = None
url = 'http://api.urbandictionary.com/v0/define'
param_value = ''

def ud(word, word_eol, userdata):
	## /ud you do you
	## /ud --3 you do you
	## /ud --4

	idx = 0
	switch = '' 
	global data
	global full_data

	try:
		if '--' == word[1][:2]:
			switch = word[1][2:3]
			if switch.isdigit():
				idx = int(switch)
			
			if len(word) >  2: 
				param_value = word_eol[2]
			elif full_data != None:
				data = full_data[idx-1]
				hexchat.prnt('Urban Dictionary -> ' + data['word'] + ': ' + data['definition'])
				return hexchat.EAT_ALL
			else:
				hexchat.prnt("Urban Dictionary: I don't know what you are looking for, genius")
				return hexchat.EAT_ALL
		else:
			param_value = word_eol[1]
			
		try:
			r = requests.get(url, params={'term': param_value}) 
			data = r.json()['list'][idx-1]
			full_data = r.json()['list']
			hexchat.prnt('Urban Dictionary ' +str(idx+1)+'/'+ str(len(full_data)) +'::\n' + data['word'] + ': ' + data['definition'])
			data = None
		except Exception as e:
			hexchat.prnt('Urban Dictionary: ENGLISH, MOTHERFUCKER DO YOU SPEAK IT???' + str(e))	
	except Exception as e:
		hexchat.prnt("Outer exc " + str(e))

	return hexchat.EAT_ALL

hexchat.hook_command('ud', ud, help='UD <word>')
