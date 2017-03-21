import subprocess
import os 

def run_command(command,is_print = False):
	print command
	p = subprocess.Popen(command,shell = True, stdout = subprocess.PIPE)
	o = p.communicate() 
	if is_print:
		print o[0]


