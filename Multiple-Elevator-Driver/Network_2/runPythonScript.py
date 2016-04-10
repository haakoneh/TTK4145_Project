
import subprocess
import os

#remember .py file ending
def runPythonScript(filename):

	commandString = "gnome-terminal -e 'python " + filename + "'"
	os.system(commandString)

#runPythonScript("phoenix.py")
#works on ubuntu, not windows