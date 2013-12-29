from distutils.core import setup

setup(
    name = 'pyCourseSync',
    py_modules = ['CourseSync.py'],
    version = '0.1',
    description = 'A Python script to synchronize all your courses from CMS',
    author = 'Darshit Shah',
    author_email = 'darnir@gmail.com',
    requires = ['beautifulsoup4', 'requests'],
    long_description = """ pyCourseSync is a Python 3 based script to
    synchronize your files from all your courses on CMS.

    This script requires atleast Python 3.2 and a couple of other libraries.
    Simply add your courses and leave pyCourseSync in your startup so that you
    always have all the files locally on your machine.
    """
)
