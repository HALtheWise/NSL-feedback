# NSL-feedback
Project 2 for Nonlinear Systems Lab

To run: 

> pipenv shell 
> python display.py

Potential working DSLR to Python:

> sudo modprobe v4l2loopback
> gphoto2 --stdout --capture-movie | gst-launch-1.0 fdsrc fd=0 ! decodebin name=dec ! queue ! videoconvert ! video/x-raw,format=YUY2 ! tee ! v4l2sink device=/dev/video1

Current Camera Settings that working

- Auto-lighting off
- Canon EOS 60-D
- IT's Optima HD65 (Q89F943AAAAACO937)
- Projector Sharpness at highest settings
- Auto-focus off
- Camera standing directly behind projector

Other setting adjustment here: https://www.ortery.com/ortery-software-camera-settings-page/canon-dslr-camera-settings/


Desired Functionality (**BOLD** required by Thursday, *Italics* desired by Thursday):

- [] Simulate camera settings
	- [x] **Brightness**  - b+, v-, c(compensation)
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
	- [x] Arbitrary Initial Condition Images (overlaying PNG) - o
- [x] **Save images** - x
- [] Save Video

Steps before Presentation:

- [] Charlie fixes settings so we don't have stupid lighting stuff
- [] Image Demonstrations of:
  - [] Recursion
	- [] "Chaos"
	- [] Growth
- [] Within Chaos, at least one video each of:
	- [] Low frequency SC
	- [] Medium Frequency SC
	- [] High Frequency SC
- [] MATLAB Code Modification
	- [] Video Input
		- [] Output a vector of max frequency content at each frame
		- [] Output a vector of angle intensity calculation
			- [] Do not include 90-180-270-360 as max
	- [] Graph frequency vs time for various starting conditions
	- [] Graph angle intensity vs time for various starting conditions
