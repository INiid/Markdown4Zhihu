

# Usage: This program aims to transfer your markdown file into a way zhihu.com can recognize correctly.
#        It will mainly deal with your local images and the formulas inside.

import os, re
import argparse
import codecs
import subprocess
import chardet

from PIL import Image
from pathlib2 import Path
from shutil import copyfile
###############################################################################################################
## Please change the GITHUB_REPO_PREFIX value according to your own GitHub user name and relative directory. ##
###############################################################################################################
# GITHUB_REPO_PREFIX = Path("https://raw.githubusercontent.com/`YourUserName`/`YourRepoName`/master/Data/")
GITHUB_REPO_PREFIX = "https://raw.githubusercontent.com/miracleyoo/Markdown4Zhihu/master/Data/"

def process_for_zhihu():
    if args.compress:
        reduce_image_size()
    with open(str(args.input), 'rb') as f:
        s = f.read()
        chatest = chardet.detect(s)
    print(chatest)
    with open(str(args.input),"r",encoding=chatest["encoding"]) as f:
        lines = f.read()
        lines = formula_ops(lines)
        lines = image_ops(lines)
        lines = table_ops(lines)
        with open(args.input.parent/(args.input.stem+"_for_zhihu.md"), "w+", encoding=chatest["encoding"]) as fw:
            fw.write(lines)
        git_ops()

def formula_ops(_lines):
    _lines = re.sub('((.*?)\$\$)(\s*)?([\s\S]*?)(\$\$)\n', '\n<img src="https://www.zhihu.com/equation?tex=\\4" alt="\\4" class="ee_img tr_noresize" eeimg="1">\n', _lines)
    _lines = re.sub('(\$)(?!\$)(.*?)(\$)', ' <img src="https://www.zhihu.com/equation?tex=\\2" alt="\\2" class="ee_img tr_noresize" eeimg="1"> ', _lines)
    return _lines

def image_ops(_lines):
    # if args.compress:
    #     _lines = re.sub(r"\!\[(.*?)\]\((.*?)\)","![\\1]("+GITHUB_REPO_PREFIX+"\\2"+")", _lines)
    #     _lines = re.sub(r'<img src="(.*?)"','<img src="'+GITHUB_REPO_PREFIX+'\\1'+'"', _lines)
    # else:
    _lines = re.sub(r"\!\[(.*?)\]\((.*?)\)",lambda m: "!["+m.group(1)+"]("+GITHUB_REPO_PREFIX+str(image_folder_path.name)+"/"+Path(m.group(2)).name+")", _lines)
    _lines = re.sub(r'<img src="(.*?)"',lambda m:'<img src="'+GITHUB_REPO_PREFIX+str(image_folder_path.name)+"/"+Path(m.group(1)).name+'"', _lines)
    return _lines

def table_ops(_lines):
    return re.sub("\|\n",r"|\n\n", _lines)

def reduce_image_size():
    global image_folder_path
    image_folder_new_path = args.input.parent/(args.input.stem+"_for_zhihu")
    if not os.path.exists(str(image_folder_new_path)): 
        os.mkdir(str(image_folder_new_path))
    print(list(image_folder_path.iterdir()))
    for image_path in [i for i in list(image_folder_path.iterdir()) if not i.name.startswith(".") and i.is_file()]:
        print(image_path)
        if os.path.getsize(image_path)>5e5:
            img = Image.open(str(image_path))
            img.save(str(image_folder_new_path/image_path.name), optimize=True,quality=85)
        else:
            copyfile(image_path, str(image_folder_new_path/image_path.name))
    image_folder_path = image_folder_new_path

def git_ops():
    subprocess.run(["git","add","-A"])
    subprocess.run(["git","commit","-m", "update file "+args.input.stem])
    subprocess.run(["git","push", "-u", "origin", "master"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Please input the file path you want to transfer using --input=""')

    # RGB arguments
    parser.add_argument(
        '--compress', action='store_true', help='Compress the image which is too large')

    parser.add_argument(
        '--input',
        type=str,
        help='Path to the file you want to transfer.')

    args = parser.parse_args()
    if args.input is None:
        raise FileNotFoundError("Please input the file's path to start!")
    else:
        args.input = Path(args.input)
        image_folder_path = args.input.parent/(args.input.stem)
        process_for_zhihu()