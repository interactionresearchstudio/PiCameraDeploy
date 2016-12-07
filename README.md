# PiCameraDeploy
A script that converts a Mac / Linux OpenCV Python script to one that can be deployed on the ProbeTools PiCamera.

## Input files
In your input file, make sure you use the right comments to "mark" the sections that will be replaced. FYI, the PiCameraDeploy script works with regular expressions to replace chunks of code with their Raspberry Pi equivalents. So if your input file isn't right, I'm afraid your output file won't work. 

Have a look at `tests/BlankExample.py` to see what a correct input file looks like. You can just go ahead and use that file as your starting point when you're creating a new script!

## Usage
Place PiCameraDeploy in a sensible place, such as your home directory. From there, call it with Python, and give it the path to the file you'd like to deploy.

	python PiCameraDeploy.py /path/to/script
	
The script will process the file, adding appropriate camera settings and library imports, and will create a new file in the same input file directory, adding -pi at the end of the file name. Transfer that over to the Pi, and Bob's your uncle.