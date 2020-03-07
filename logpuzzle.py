#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""
__author__ = "luisfff29"

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    with open('animal_code.google.com') as f:
        urls = f.read()
    matches = re.findall(r'\S*puzzle\S*', urls)
    alpha_sort = sorted(set(matches))
    return ["http://code.google.com" + x for x in alpha_sort]


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    try:
        os.mkdir(dest_dir)
    except OSError:
        print("Directory '{}' already exists".format(dest_dir))
    html_img = ''
    for i, link in enumerate(img_urls):
        image_name = 'img' + str(i)
        urllib.urlretrieve(link, image_name)
        src_path = os.path.join(os.getcwd(), image_name)
        dst_path = os.path.join(os.path.abspath(dest_dir), image_name)
        os.rename(src_path, dst_path)
        html_img += '<img src="./{}">'.format(image_name)
    print(html_img)
        


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
