from textnode import TextNode
import os
# from os import path, listdir, mkdir
import shutil
from time import strftime

def main():
    
    move_dirs("static", "public", "logs")
    
    return

def move_dirs(src, dest, log):
    if src is None or dest is None or log is None:
        raise Exception("need all arguments")
    if not (os.path.exists(src)):
        raise Exception("source path does not exist")
    # if not (os.path.exists(dest)):
    #   raise Exception("destination path does not exist")
    if not (os.path.exists(log)):
        raise Exception("logs path does not exist")
    
    try:
        shutil.rmtree(dest)
    except FileNotFoundError:
        pass
    os.mkdir(dest)

    src_dir = os.listdir(src)
    
    for path in src_dir:
        parsed_path = os.path.join(src, path)
        new_path = os.path.join(dest, path)
        if os.path.isfile(parsed_path):
            shutil.copy(parsed_path, new_path)
            file_log(parsed_path, new_path, log)
        elif os.path.isdir(parsed_path):
            try:
                os.mkdir(new_path)
            except FileExistsError:
                pass
            move_dirs(parsed_path, new_path, log)

def file_log(src, dest, log):
    with open(os.path.join(log, "log.txt"), mode='a') as f:
        the_time = strftime("%H:%M:%S, %a %b %d")
        print(f"Copying {src} to {dest}. {the_time}", file=f)

main()