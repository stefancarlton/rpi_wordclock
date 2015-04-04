.. _software_installation:

Software installation
=====================

Set locales
+++++++++++

Since the config-file contains layouts for multiple languages, assure to have a utf-8 compatible locale::

    echo $LANG

should return something, containing utf-8 at the end.
E.g.::

    en_US.UTF-8

If not, check this website, to adjust it: http://perlgeek.de/en/article/set-up-a-clean-utf8-environment


.. _3rd_party_deps_packages:

3rd party dependencies (packages)
+++++++++++++++++++++++++++++++++

To install 3rd party dependencies (packages) enter in a terminal/commandline::

    sudo apt-get install python-pip python-scipy scons git swig


.. _3rd_party_deps_python:

3rd party dependencies (python packages)
+++++++++++++++++++++++++++++++++++++++++

Required python dependencies:

  * astral (to get moon/sun information)
  * feedparser (to get access to latest feeds)
  * scipy
  * pil
  * svgwrite (to plot stancil/wiring layouts)

To install use::

    sudo pip install pytz astral feedparser pillow svgwrite


.. _3rd_party_deps_git:

3rd party dependencies (git repositories)
+++++++++++++++++++++++++++++++++++++++++

Install 3rd-party dependencies (compiled on your own).
.. todo:: Improve installation location.

Install rpi_ws281x to your home-directory (to access leds)::

    cd ~
    git clone git@github.com:richardghirst/rpi_ws281x.git
    cd rpi_ws281x
	python setup.py install
    sudo scons

.. note::
    There are two libraries available, jgarff/rpi_ws281x original and richardghirst/rpi_ws281x. RichardGHirtst version
	works with Raspberry Pi 2.
	
    Since this library is continiously updated: A version, which is tested to work with the wordclock is commit 6cffc95: 
    https://github.com/jgarff/rpi_ws281x/tree/6cffc954a3fc25f0d741d03b575ad9cdf3068103

Install fontdemo to your home-directory (to render strings)::

    cd ~
    git clone https://gist.github.com/5488053.git

This installs fontdemo.py to ~/5488053.

Install python-py for binding to the freetype library:

    cd ~
	git clone https://github.com/rougier/freetype-py.git
	cd python-py
	python setup.py build
	python setup.py install
	

Install pywapi as indicated on https://code.google.com/p/python-weather-api/#Weather.com


.. _wordclock_software:

The wordclock software
++++++++++++++++++++++


.. _download_software:

Download software
-----------------

Clone the wordclock software to the directory ~/rpi_wordclock (to run the actual wordclock)::

    cd ~
    git clone https://github.com/bk1285/rpi_wordclock.git

Link the previously installed file fontdemo.py to ~/rpi_wordclock using a softlink::

    ln -s ~/5488053/fontdemo.py ~/rpi_wordclock/fontdemo.py


.. _adopt_software:

Adopt software
--------------

To adjust the wordclock to your own settings, create and edit the file ~/rpi_wordclock/wordclock_config/wordclock_config.cfg

To start over, you might just copy the file ~/rpi_wordclock/wordclock_config/wordclock_config.example.cfg and adopt this file.

Note: Each plugin of the wordclock project has its own section in the config-file (create it, if needed, but not existant)

.. note:: If your wordclock has a stancil layout or display resolution, which is not supported yet, you might need to adopt the
  software by providing your own `wiring`-class (to the file wordclock_tools/wiring.py)


.. _run_software:

Run software
------------

To run the wordclock software (with adapted wiring and config-file) do::

    cd ~/rpi_wordclock
    sudo python wordclock.py

In case, the whole thing is not working as expected: Maybe the section :ref:`trouble-shooting` might help...


.. _run_software_on_startup:

Make software run on every startup
----------------------------------

Add the python-script to crontab by calling the command::

    sudo crontab -e

Add here::

    @reboot sudo python /home/pi/rpi_wordclock/wordclock.py

