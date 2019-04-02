from compressor import compress
from wiki_converter import wiki_knml_converter
import os

file_name = input("Enter path of XML file:")
wiki_knml_converter(file_name)
file_name = file_name[:-4] + '.knml'
compress(file_name)
os.remove(file_name)