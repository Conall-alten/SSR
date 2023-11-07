# -*- coding: utf-8 -*-
"""
Created on Wed May 10 01:58:09 2023

@author: DECLINE
"""

import sys
import argparse


def generate_at(in_path, out_path):
    with open(in_path, "r+") as file:
        data = file.read()
        data = data.replace(",","")
    
    with open(out_path, "w") as file:
        file.write(str(data))

    pass


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("intput_file", help = 'The file containing the values.')
    parser.add_argument("output_file", help = 'The path to the at file.')
    args = parser.parse_args(sys.argv[1:])

    generate_at(args.intput_file, args.output_file)
