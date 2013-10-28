#!/usr/bin/python3
################################################################################
# Title     : CourseSync script for BITS-Pilani Hyderabad Campus               #
# Author    : Darshit Shah                                                     #
# Date      : October 2, 2013                                                  #
# License   : MIT                                                              #
################################################################################

import requests
import os
import sys
import argparse
import exceptions
from bs4 import BeautifulSoup
from collections import defaultdict

CONF_FILE = "courses.lst"
CONF_DIR  = "Academics"
USER_DIR  = os.path.expanduser('~')
DIR_PATH  = os.path.join(USER_DIR, CONF_DIR)
CONF_PATH = os.path.join(DIR_PATH, CONF_FILE)

def main():
    parser = argparse.ArgumentParser()
    configure_opt_parser (parser)
    args = parser.parse_args()
    print (args)
    if args.view_logs is True:
        sys.exit (0)
    elif args.add_courses is True:
        CourseSync (action="add_courses")
    elif args.delete_courses is True:
        pass
    elif args.reset is True:
        pass
    try:
        CourseSync(action="sync")
    except exceptions.ConnectionError:
        print("Connection Error")

def configure_opt_parser (parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--add-courses", action="store_true", help="Add courses to your Course List")
    group.add_argument("-d", "--delete-courses", action="store_true", help="Remove courses from your Course List")
    group.add_argument("-r", "--reset", action="store_true", help="Delete your Course List file and start a new one. Helpful when starting a new semester")
    parser.add_argument("-S", "--sync", action="store_true", default=True, help="Sync your machine with the CMS Servers")
    parser.add_argument("-v", "--verbosity", choices=["q", "v", "d"], default="q", help="Change verbosity of script output")
    parser.add_argument("-l", "--view-logs", action="store_true", help="View the contents of your Log File")


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
        #TODO: Handle Course Input Here.
        sys.exit(1)

    def add_courses(self):
        conf_file = open(CONF_PATH, 'a+')
        print("Enter course codes, one per line, in this format: BITS C312\n")
        course_code = input ("Enter Course Code: ")
        while course_code != '':
            #TODO: Use Regular Expression checking for Course Code here.
            conf_file.write(course_code + "\n")
            course_code = input ("Enter Course Code: ")


    def guest_login(self):
        payload = {'username':'guest', 'password':'guest'}
        try:
            cl_obj = self.cl_session.post('http://172.16.100.125/bits-cms/login/index.php', data=payload)
        except requests.exceptions.ConnectionError:
            raise exceptions.ConnectionError
        print (cl_obj.status_code)
        print (cl_obj.headers)
        print (cl_obj.cookies)
        print (cl_obj.url)
        print (cl_obj.history)
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
        print (course_info)
        return course_info

    def download_files (self, course_info):
        for c_code in course_info:
            c_name = course_info[c_code][0]
            c_link = course_info[c_code][1]
            self._download_course (c_code, c_name, c_link)

    def _download_course (self, c_code, c_name, c_link):
        request = self.cl_session.get (c_link)
        soup = BeautifulSoup(request.text)
        c_tag = None
        for tag in soup.find_all ('div'):
            if tag.has_attr('class'):
                if "course_category_tree" in tag['class']:
                    c_tag = tag
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
        except FileNotFoundError:
            self.safe_mkdir (path)
            os.chdir (path)
        except Exception as e:
            print ("Something went wrong.")
            print (e)

    def download_all_files (self, class_link, location):
        self.safe_chdir (location)
        request = self.cl_session.get (class_link)
        soup = BeautifulSoup (request.text)
        print (request.url)
        tag = None
        for list_element in soup.find_all ('ul'):
            if list_element.has_attr ('class'):
                if 'topics' in list_element['class']:
                    tag = list_element
                    for file_link in tag.find_all ('a'):
                        file_request = self.cl_session.get (file_link.get('href'))
                        content_disposition = file_request.headers['content-disposition'].split('=')[1].strip('"')
                        filename = os.path.join (os.getcwd(), content_disposition)
                        if not os.path.isfile (filename):
                            fd = open (filename, "wb")
                            for block in file_request.iter_content(1024):
                                if not block:
                                    break
                                fd.write(block)
                            fd.close()
                            print (content_disposition)
        self.safe_chdir (DIR_PATH)

if __name__ == '__main__':
    main()
# vim: set ts=4 sts=4 sw=4 tw=300 et :
