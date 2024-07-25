import os
import sys

current_file_path = __file__
absolute_path = os.path.abspath(current_file_path)
file_directory = os.path.dirname(absolute_path)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))