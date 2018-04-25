# NSL-feedback
Project 2 for Nonlinear Systems Lab

To run: 

> pipenv shell 
> python display.py

Potential working DSLR to Python:

> sudo modprobe v4l2loopback
> gphoto2 --stdout --capture-movie | gst-launch-1.0 fdsrc fd=0 ! decodebin name=dec ! queue ! videoconvert ! video/x-raw,format=YUY2 ! tee ! v4l2sink device=/dev/video1



Desired Functionality (**BOLD** required by Thursday, *Italics* desired by Thursday):

- [] Simulate camera settings
	- [x] **Brightness** 
	- [] *Contrast*
	- [] Zoom 
	- [x] Translation - asdf
	- [] Rotation
	- [] Keystone
	- [] Frame Rate
	- [] Time Delay
- [] Live editing camera settings
	- [] *Sliders below window for each setting*
- [] Overlay Effects
	- [x] **4 crosshairs on a circle (custom opencv fine)** - g
	- [] Center Dot (custom opencv fine)
	- [x] Arbitrary Initial Condition Images (overlaying PNG)
- [x] **Save images** - x
- [] Save Video


