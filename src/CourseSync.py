#!/usr/bin/python3
################################################################################
# Title     : CourseSync script for BITS-Pilani Hyderabad Campus               #
# Author    : Darshit Shah                                                     #
# Date      : October 2, 2013                                                  #
# License   : MIT                                                              #
################################################################################

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
    parser = argparse.ArgumentParser()
    configure_opt_parser (parser)
    args = parser.parse_args()
    #print (args)
    if args.view_logs is True:
        sys.exit (10)
    elif args.add_courses is True:
        action="add_courses"
    elif args.delete_courses is True:
        sys.exit (10)
    elif args.reset is True:
        sys.exit(10)
    else:
        action="sync"

    try:
        CourseSync(action=action)
    except exceptions.ConnectionError:
        print("Connection Error")

def configure_opt_parser (parser):
    outer_group = parser.add_mutually_exclusive_group()
    course_group = outer_group.add_mutually_exclusive_group()
    course_group.add_argument("-a", "--add-courses", action="store_true", help="Add courses to your Course List")
    course_group.add_argument("-d", "--delete-courses", action="store_true", help="Remove courses from your Course List")
    course_group.add_argument("-r", "--reset", action="store_true", help="Delete your Course List file and start a new one. Helpful when starting a new semester")
    outer_group.add_argument("-S", "--sync", action="store_true", help="Sync your machine with the CMS Servers")
    parser.add_argument("-v", "--verbosity", choices=["q", "v", "d"], default="q", help="Change verbosity of script output")
    outer_group.add_argument("-l", "--view-logs", action="store_true", help="View the contents of your Log File")


class CourseSync:
    def __init__(self, action="sync"):
        try:
            user_action = getattr(self, action)
        except Exception:
            print("===Error=== Method %s is not defined" %(action))
        else:
            user_action()

    def sync (self):
        self.cl_session = requests.Session()
        user_courses = self.get_course_list()
        cl_obj = self.guest_login()
        links = self.parseCourses(user_courses, cl_obj)
        self.download_files (links)

    def get_course_list(self):
        courses = list()
        if os.path.isfile(CONF_PATH):
            courses = self._read_conf_file(CONF_PATH)
        else:
            courses = self._create_conf_file(CONF_PATH)
        return courses

    def _read_conf_file(self, PATH):
        endl = os.linesep
        courses = open(PATH, 'r').read().splitlines()
        return courses

    def _create_conf_file(self, PATH):
        print ("Conf file does not exist")
        self.safe_chdir(DIR_PATH)
        self.add_courses()
        #TODO: Handle Course Input Here.
        sys.exit(1)

    def add_courses(self):
        conf_file = open(CONF_PATH, 'a+')
        print("Enter course codes, one per line, in this format: BITS C312\n")
        course_code = input ("Enter Course Code: ")
        while course_code != '':
            if (check_code(course_code)):
                conf_file.write(course_code + "\n")
                course_code = input ("Enter Course Code: ")
            else:
                print("Invalid Course Code")

    def guest_login(self):
        payload = {'username':'guest', 'password':'guest'}
        cl_obj = self.cl_session.post('http://%s/bits-cms/login/index.php' %(CMS_URL), data=payload)
        #print (cl_obj.status_code)
        #print (cl_obj.headers)
        #print (cl_obj.cookies)
        #print (cl_obj.url)
        #print (cl_obj.history)
        return cl_obj

    def parseCourses(self, course_list, cl_obj):
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

    def download_files (self, course_info):
        for c_code in course_info:
            c_name = course_info[c_code][0]
            c_link = course_info[c_code][1]
            print ("Course name: " + c_name)
            print ("Course Code: " + c_code)
            #print ("Course link: " + c_link)
            self._download_course (c_code, c_name, c_link)

    def _download_course (self, c_code, c_name, c_link):
        request = self.cl_session.get (c_link)
        #print (request)
        soup = BeautifulSoup(request.text)
        c_tag = None
        for tag in soup.find_all ('div'):
            if tag.has_attr('class'):
                if "course_category_tree" in tag['class']:
                    c_tag = tag
                    #print (c_tag)
        if c_tag is not None:
            for link in c_tag.find_all ('a'):
                if link.has_attr('class'):
                    c_dir = c_code + " - " + c_name
                    path = os.path.join (DIR_PATH, c_dir)
                    self.download_all_files(link.get('href'), path)

    def safe_mkdir (self, path):
        dirname = os.path.join (DIR_PATH, path)
        try:
            os.mkdir(dirname)
        except OSError:
            pass
        except Exception:
            print ("Something went wrong while creating directories")

    def safe_chdir (self, path):
        try:
            os.chdir (path)
        except OSError as ose:
            if ose.errno == ENOENT:
                self.safe_mkdir(path)
                self.safe_chdir(path)
            else:
                print ("Unknown I/O Exception: " + ose.errno)
        except Exception as e:
            print ("Something went wrong.")
            print (e)

    def download_all_files (self, class_link, location):
        self.safe_chdir (location)
        request = self.cl_session.get (class_link)
        soup = BeautifulSoup (request.text)
        #print (request.url)
        logfile = open(os.path.join(location,".log"),"a+")
        logfile.seek(0, os.SEEK_SET)
        existing_files = logfile.read().splitlines()
        #print(existing_files)
        tag = None
        for list_element in soup.find_all ('ul'):
            if list_element.has_attr ('class'):
                if 'topics' in list_element['class']:
                    tag = list_element
                    for file_link in tag.find_all ('a'):
                        #print (file_link)
                        file_href = file_link.get('href')
                        f_id = urlparse(file_href).query[3:]
                        if f_id not in existing_files:
                            file_request = self.cl_session.get (file_href)
                            content_disposition = file_request.headers['content-disposition'].split('=')[1].strip('"')
                            filename = os.path.join (os.getcwd(), content_disposition)
                            fd = open (filename, "wb")
                            for block in file_request.iter_content(1024):
                                if not block:
                                    break
                                fd.write(block)
                            fd.close()
                            print (content_disposition)
                            logfile.write(f_id + "\n")
        logfile.close()
        self.safe_chdir (DIR_PATH)

    def check_code(code):
        #course_tags='[BITS,AAOC,BIO,CS,CHEM,CDP,CE,CHE,DA,DE,ECE,ECON,EEE,FIN,HSS,IS,INSTR,MATH,ME,MEL,MF,PHA,PHY,POL,SOC,TA]'
        #pattern = '{} [F,G,C][0-9]'.format(course_tags)
        pattern = '^([A-Z]{2,5}) [(A-Z)*1]([0-9]{3}$)'
        if(re.search(pattern,code)):
            return True
        else:
            return False

if __name__ == '__main__':
    main()
# vim: set ts=4 sts=4 sw=4 tw=300 et :
