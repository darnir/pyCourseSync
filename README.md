pyCourseSync
============

A clone of the original CourseSync client written in Python 3.

*DEPRECATED* This Module has now been deprecated. The CMS changed since Semester
2, AY 2013-14 and the original author is no longer on campus. Since no one is
interested in maintaining this module, I am closing it down. However, in the
future if anyone wishes to fix it and extend it, please fork it and maintain
your own copy. I will be accepting no more pull requests.

Dependencies
============

pyCourseSync uses some of the best libraries available for Python 3 to
 accomplish the task.

The libraries required for pyCourseSync to work are:
   * BeautifulSoup4: This is an absolutely amazing library for parsing and
     navigating Web Pages.
   * Requests: This stunningly simple library was chosen over the built-in
     urllib library after a lot of consideration. It provides the simplest and
     easiest HTTP Client API I have ever seen.

Usage
=====

```
usage: CourseSync.py [-h] [-a | -d | -r] [-S] [-v {q,v,d}] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -a, --add-courses     Add courses to your Course List
  -d, --delete-courses  Remove courses from your Course List
  -r, --reset           Delete your Course List file and start a new one.
                        Helpful when starting a new semester
  -S, --sync            Sync your machine with the CMS Servers
  -v {q,v,d}, --verbosity {q,v,d}
                        Change verbosity of script output
  -l, --view-logs       View the contents of your Log File
```

Using pyCourseSync is very easy. Use the --add-courses or --delete-courses to
change what data is synced from the CMS.

Then leave this script in your startup applications so that it syncs with the
CMS on every system startup. In case you leave your system ON for multiple days,
set up a scheduled task to execute pyCourseSync.

The verbosity and logging options are currently not implemented and will
hopefully be implemented soon, by V1.0

Credits
=======

The original CourseSync client was written by Vishwajit Kolathur and Aravind
Pedapudi in Perl and can be found at: https://github.com/ajit-kolathur/CMS
This was the inspiration based on which pyCourseSync is written.

Authors
=======

   * Darshit Shah  <darnir@gmail.com>


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/darnir/pycoursesync/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

