#!/usr/bin/python3
###############################################################################
# Title     : CourseSync script for BITS-Pilani Hyderabad Campus              #
# Author    : Darshit Shah                                                    #
# Date      : October 2, 2013                                                 #
# License   : MIT                                                             #
###############################################################################

"""
pyCourseSync is a Python 3 based utility for downloading files from the
BITS-Pilani Hyderabad Campus CMS Server and keeping a synchronized local copy.
In order to use pyCourseSync effectively, one must keep it as an autostart
application. See README.md for more information.
"""

import os
import sys
import argparse
import exceptions
import re
from collections import defaultdict
from urllib.parse import urlparse
from errno import ENOENT


try:
    import requests
except ImportError:
    print("The Python Requests library for Python 3 is not installed.")
    print("Please install Requests and try again.")
    sys.exit(2)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("The BeautifulSoup4 library for Python 3 is not installed.")
    print("Please install BeautifulSoup4 and try again.")
    sys.exit(2)

CONF_FILE = "courses.lst"
CONF_DIR  = "Academics"
USER_DIR  = os.path.expanduser('~')
DIR_PATH  = os.path.join(USER_DIR, CONF_DIR)
CONF_PATH = os.path.join(DIR_PATH, CONF_FILE)
CMS_URL   = "111.93.5.216"


def main():
    """
    Init point of the code path. This function is executed only when the
    module is executed, but not when it is imported. Hence, making pyCourseSync
    safe to import in a separate module for extending its functionality.

    main() is supposed to simply handle the invokation parameters and call the
    respective functions.
    """
    parser = argparse.ArgumentParser()
    configure_opt_parser(parser)
    args = parser.parse_args()
    #print (args)
    if args.view_logs is True:
        sys.exit(10)
    elif args.add_courses is True:
        action = "add_courses"
    elif args.delete_courses is True:
        sys.exit(10)
    elif args.reset is True:
        sys.exit(10)
    else:
        action = "sync"

    try:
        CourseSync(action=action)
    except exceptions.ConnectionError:
        print("Connection Error")


def configure_opt_parser(parser):
    """
    This function is used to configure the argparse module for handling
    command line switches. This function is not marked as private since it may
    be called directly by other modules that attempt to extend pyCourseSync.
    """
    outer_group = parser.add_mutually_exclusive_group()
    course_group = outer_group.add_mutually_exclusive_group()
    course_group.add_argument(
        "-a", "--add-courses", action="store_true",
        help="Add courses to your Course List"
        )
    course_group.add_argument(
        "-d", "--delete-courses", action="store_true",
        help="Remove courses from your Course List"
        )
    course_group.add_argument(
        "-r", "--reset", action="store_true",
        help="Delete your Course List file and start a new one. \
            Helpful when starting a new semester"
        )
    outer_group.add_argument(
        "-S", "--sync", action="store_true",
        help="Sync your machine with the CMS Servers"
        )
    parser.add_argument(
        "-v", "--verbosity", choices=["q", "v", "d"],
        default="q", help="Change verbosity of script output"
        )
    outer_group.add_argument(
        "-l", "--view-logs", action="store_true",
        help="View the contents of your Log File"
        )


def safe_mkdir(path):
    """
    A `safe' function for os.mkdir. If the directory already exists, it
    silently continues. However in case of any other issue, it raises an
    exception and aborts.
    """
    dirname = os.path.join(DIR_PATH, path)
    try:
        os.mkdir(dirname)
    except OSError:
        pass
    except Exception:
        print("Something went wrong while creating directories")


def safe_chdir(path):
    """
    A `safe' function for os.chdir. If the directory does not exist, it
    attempts to create the directory first. In case of any other issues, it
    raises an exception and exits.
    """
    try:
        os.chdir(path)
    except OSError as ose:
        if ose.errno == ENOENT:
            safe_mkdir(path)
            safe_chdir(path)
        else:
            print("Unknown I/O Exception: " + ose.errno)
    except Exception as exception:
        print("Something went wrong.")
        print(exception)


class CourseSync(object):
    """
    This class keeps all the functions that directly relate to the actual
    working of pyCourseSync together. Any method that works on interacting with
    the server should be a part of this class.
    """
    def __init__(self, action="sync"):
        try:
            user_action = getattr(self, action)
        except AttributeError:
            print("===Error=== Method %s is not defined" % (action))
        else:
            user_action()

    def sync(self):
        """
        This method handles the default function of the script. Syncing with
        the CMS server.
        There are 3 responsibilities of this method:
        * Get a list of all the courses the user is registered in
        * Log into the CMS system
        * Download all the files related to the courses
        All of these responsibilites are delegated to different methods.
        """
        self.cl_session = requests.Session()
        user_courses = self.get_course_list()
        cl_obj = self.guest_login()
        links = self.parse_courses(user_courses, cl_obj)
        self.download_files(links)

    def get_course_list(self):
        """
        This method is concerned simply with reading the configuration file and
        returning a list of all the courses the user is watching.
        """
        courses = list()
        if os.path.isfile(CONF_PATH):
            courses = self._read_conf_file(CONF_PATH)
        else:
            courses = self._create_conf_file()
        return courses

    def _read_conf_file(self, path):
        """
        *INTERNAL FUNCTION*
        This method may change without any notice.
        Currently, it reads the configuration file and returns a list of all
        the courses listed in the file.
        """
        courses = open(path, 'r').read().splitlines()
        return courses

    def _create_conf_file(self):
        """
        *INTERNAL FUNCTION*
        This method may change without any notice.
        This method simply changes the active directory and calls the
        add_courses() method since it was written such that is handles a non
        existing configuration file.

        FIXME: Do not call a public method from a private method.
        """
        print("Conf file does not exist")
        safe_chdir(DIR_PATH)
        self.add_courses()
        sys.exit(1)

    def add_courses(self):
        """
        This method takes input from the user through stdin, the list of
        courses that they want to sync. This course codes entered are checked
        against a simple regex of: "\w \c[0-9][0-9][0-9]"

        *IMPORTANT: Since this function is called from an internal function, it
        stands at a high risk of being edited in a backward-incompatible
        manner.

        FIXME: Do not call a public method from a private method.
        """
        conf_file = open(CONF_PATH, 'a+')
        print("Enter course codes, one per line, in this format: BITS C312\n")
        course_code = input("Enter Course Code: ")
        while course_code != '':
            if (self.check_code(course_code)):
                conf_file.write(course_code + "\n")
                course_code = input("Enter Course Code: ")
            else:
                print("Invalid Course Code")

    def guest_login(self):
        """
        Simple method whose sole responsibility is to login to the CMS as a
        guest user.
        """
        payload = {'username': 'guest', 'password': 'guest'}
        cl_obj = self.cl_session.post(
            'http://%s/bits-cms/login/index.php' % (CMS_URL), data=payload)
        #print (cl_obj.status_code)
        #print (cl_obj.headers)
        #print (cl_obj.cookies)
        #print (cl_obj.url)
        #print (cl_obj.history)
        return cl_obj

    def parse_courses(self, course_list, cl_obj):
        """
        This method is primarily responsible for reading the CMS page and
        creating a dictionary of the various URLs of the pages for each course
        in the course list. It returns a Python defaultdict(list) of the
        courses and the URLs of their respective pages.
        """
        page = cl_obj.text
        soup_obj = BeautifulSoup(page)
        div_tag = None
        course_info = defaultdict(list)
        for tag in soup_obj.find_all('div'):
            if tag.has_attr('class'):
                if "subcategories" in tag['class']:
                    div_tag = tag
        for link in div_tag.find_all('a'):
            c_details = link.text.split('-')
            c_code = c_details[0][:-1]
            c_name = c_details[1][1:]
            if c_code in course_list:
                course_info[c_code] = [c_name, link.get('href')]
        #print (course_info)
        return course_info

    def download_files(self, course_info):
        """
        This function simply iterates over all the courses to be sync'ed and
        calls a function for downloading each course in its respective
        location.
        """
        for c_code in course_info:
            c_name = course_info[c_code][0]
            c_link = course_info[c_code][1]
            print("Course name: " + c_name)
            print("Course Code: " + c_code)
            #print ("Course link: " + c_link)
            self._download_course(c_code, c_name, c_link)

    def _download_course(self, c_code, c_name, c_link):
        """
        *INTERNAL FUNCTION*
        For each section in the course, this method will navigate to the
        respective page and download all files.

        The input parameters to this function may change without notice and
        hence is an internal function. Do not call this function for other
        modules.
        """
        request = self.cl_session.get(c_link)
        #print (request)
        soup = BeautifulSoup(request.text)
        c_tag = None
        for tag in soup.find_all('div'):
            if tag.has_attr('class'):
                if "course_category_tree" in tag['class']:
                    c_tag = tag
                    #print (c_tag)
        if c_tag is not None:
            for link in c_tag.find_all('a'):
                if link.has_attr('class'):
                    c_dir = c_code + " - " + c_name
                    path = os.path.join(DIR_PATH, c_dir)
                    self.download_all_files(link.get('href'), path)

    def download_all_files(self, class_link, location):
        """
        For a given URL and location, download all files from that page to the
        given location on disk.

        TODO: Refactor for better readability.
        """
        safe_chdir(location)
        request = self.cl_session.get(class_link)
        soup = BeautifulSoup(request.text)
        #print (request.url)
        logfile = open(os.path.join(location, ".log"), "a+")
        logfile.seek(0, os.SEEK_SET)
        existing_files = logfile.read().splitlines()
        #print(existing_files)
        tag = None
        for list_element in soup.find_all('ul'):
            if list_element.has_attr('class'):
                if 'topics' in list_element['class']:
                    tag = list_element
                    for file_link in tag.find_all('a'):
                        #print (file_link)
                        file_href = file_link.get('href')
                        f_id = urlparse(file_href).query[3:]
                        if f_id not in existing_files:
                            file_request = self.cl_session.get(file_href)
                            cd = file_request.headers['content-disposition']
                            content_disposition = cd.split('=')[1].strip('"')
                            filename = os.path.join(
                                os.getcwd(), content_disposition)
                            fd = open(filename, "wb")
                            for block in file_request.iter_content(1024):
                                if not block:
                                    break
                                fd.write(block)
                            fd.close()
                            print(content_disposition)
                            logfile.write(f_id + "\n")
        logfile.close()
        safe_chdir(DIR_PATH)

    def check_code(self, code):
        """
        Check if the course code given matches a given regex.
        """
        #course_tags='[BITS,AAOC,BIO,CS,CHEM,CDP,CE,CHE,DA,DE,ECE,ECON,EEE, \
        #        FIN,HSS,IS,INSTR,MATH,ME,MEL,MF,PHA,PHY,POL,SOC,TA]'
        #pattern = '{} [F,G,C][0-9]'.format(course_tags)

        pattern = '^([A-Z]{2,5}) [(A-Z)*1]([0-9]{3}$)'
        if(re.search(pattern, code)):
            return True
        else:
            return False

if __name__ == '__main__':
    main()
# vim: set ts=4 sts=4 sw=4 tw=300 et :
