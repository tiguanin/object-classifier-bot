import configparser
import os

cwd = os.getcwd()
files = os.listdir(cwd)
props = configparser.ConfigParser()
props.read('properties.ini')
