from textnode import TextNode
from processes import *
import os
# from os import path, listdir, mkdir
import shutil
from time import strftime

content = "content"
template_path = "src/template.html"
destination = "public"
logs = "logs"

def main():
    
    move_dirs("static", "public", "logs")
    # generate_page("content/index.md", "src/template.html", "public/index.html", "logs")
    generate_pages_recursive(content, template_path, destination, logs)

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

def template_log(src, template, dest, log):
    with open(os.path.join(log, "log.txt"), mode='a') as f:
        the_time = strftime("%H:%M:%S, %a %b %d")
        print(f"Generating page from {src}, storing in {dest}. Using {template} as template. {the_time}", file=f)

def generate_page(from_path, template_path, dest_path, log):
    template_log(from_path, template_path, dest_path, log)

    src_text = open(from_path, 'r').read()
    template_text= open(template_path, 'r').read()

    read_html = markdown_to_html_node(src_text).to_html()
    read_title = extract_title(src_text)

    template_title_target = "{{ Title }}"
    template_html_target = "{{ Content }}"

    generated_page = template_text.replace(template_title_target, read_title).replace(template_html_target, read_html)
    dest_file = open(dest_path, 'w')
    dest_file.write(generated_page)
    dest_file.close()

def generate_pages_recursive(dir_path_content, path_template, dir_path_dest, path_logs):
    if dir_path_content is None or path_template is None or dir_path_dest is None or logs is None:
        raise Exception("need all arguments")
    if not (os.path.exists(dir_path_content)):
        raise Exception("source path does not exist")
    if not (os.path.exists(path_template)):
        raise Exception("template path does not exist")
    

    src_dir = os.listdir(dir_path_content)
    print(src_dir)

    for path in src_dir:
        parsed_path = os.path.join(dir_path_content, path)
        print(parsed_path)
        new_path = os.path.join(dir_path_dest, path)
        if os.path.isfile(parsed_path):
            if parsed_path.endswith(".md"):
                new_path = new_path.removesuffix(".md") + ".html"
                generate_page(parsed_path, template_path, new_path, logs)
        elif os.path.isdir(parsed_path):
            try:
                os.mkdir(new_path)
            except FileExistsError:
                pass
            generate_pages_recursive(parsed_path, path_template, new_path, path_logs)
    


main()