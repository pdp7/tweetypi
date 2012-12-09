tweetypi
========

Repository for Python scripts to display tweets on a character LCD connected to a Raspberry Pi.

Written by Drew Fustini.  Released as public domain.

Blog post: http://www.element14.com/community/groups/raspberry-pi/blog/2012/11/26/display-tweets-on-a-character-lcd

display-hashtag.py 
------------------
Displays tweets that contain a specified hashtag

Instructions:
<pre>
sudo pip install twitter
mkdir ~/python
cd ~/python
git clone https://github.com/pdp7/Adafruit-Raspberry-Pi-Python-Code.git
git clone https://github.com/pdp7/tweetypi.git
cd tweetypi
</pre>

The only required argument for display-hashtag is the hashtag.  The '#' prefix should be omitted as it is added by the code.  The defaults assume 16x2 char LCD.

<pre>
sudo ./display-hashtag bears
</pre>

Here would be the arguments for 20x4 LCD:

<pre>
sudo ./display-hashtag --verbose --cols 20 --rows 4 --delay 3 bears
</pre>

