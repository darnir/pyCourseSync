.. _release:

Release Notes
=============

These are the release notes for version 0.1-alpha of pyCourseSync, the CMS
synchronization tool. This version was released on November 22, 2013 and is an
alpha release. At this stage, pyCourseSync works as expected and can be used
reliably in its task, but it lacks certain features that are expected out of an
application in its stable state. One of the most important of these is a
straight-forward installation process.

Installation
------------

Installation of pyCourseSync is pretty straightforward. You need Python 3.2 and above to run pyCourseSync.

Windows
+++++++

Setting up pyCourseSync on Windows is extremely easy. Simply download and run
the precompiled executable available `here
<https://github.com/darnir/pyCourseSync/releases/download/v0.1-alpha/pyCourseSync-0.1-alpha-Windows-precompiled.zip>`__

This file contains all the required external libraries and the corresponding
Python interpreter. Hence, it should simply work out of the box for everyone.

Those users who would like to check out the source of the script may access it
from the `GitHub repository <https://github.com/darnir/pyCourseSync>`_.

\*nix Systems
+++++++++++++

The process is a little more complicated for the users of Linux and/or MacOS
systems. We are trying to make this process much simpler by the v1.0 stable
release.

Currently, users on these systems must download the source tarball from `here
<https://github.com/darnir/pyCourseSync/archive/v0.1-alpha.tar.gz>`__. Once you
have the tarball, extract it using the following command::

    $ tar -xvzf pyCourseSync-0.1-alpha.tar.gz

Next, you must install the two external libraries that pyCourseSync depends on::

    $ sudo pip install requests
    $ sudo pip install beautifulsoup4

Dependencies
------------
pyCourseSync uses some of the best libraries available for Python 3 to
accomplish the task.

The libraries required for pyCourseSync to work are:

* **BeautifulSoup4**: This is an absolutely amazing library for parsing and
  navigating Web Pages.
* **Requests**: This stunningly simple library was chosen over the built-in
  urllib library after a lot of consideration. It provides the simplest and
  easiest HTTP Client API I have ever seen.

Usage
-----

pyCourseSync was created to be extremely user friendly and easy to use. It is
supposed to be a script that is configured only once each semester and then
forgotten about.

Check ``CourseSync.py --help`` for a list of functions available. The first time
you run CourseSync, you will be asked to input a list of all the courses you
want to synchronize locally. On all subsequent invokations of CourseSync.py, all
the files for those courses will be synchronized with the CMS.
At the end of the semester, you may run ``CourseSync --reset`` to delete the the
list of courses synchronized so that you may start with a new set of courses in
the next semester.

Your files will be downloaded in ``~/Academics/{Course Name}/``

Credits
-------

Code in this release of pyCourseSync was contributed by:

* Darshit Shah <darnir@gmail.com>

