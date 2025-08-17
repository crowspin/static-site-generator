import os
from re import sub
from shutil import rmtree, copy

from blocks import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r') as f:
            markdown = f.read()
    except FileNotFoundError:
        print(f"File at '{from_path}' not found")
    except PermissionError:
        print(f"File at '{from_path}' could not be opened")
    except Exception:
        print(f"An unexplained error occurred while opening '{from_path}'")

    try:
        with open(template_path, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"File at '{template_path}' not found")
    except PermissionError:
        print(f"File at '{template_path}' could not be opened")
    except Exception:
        print(f"An unexplained error occurred while opening '{template_path}'")
    
    html_nodes = markdown_to_html_node(markdown)
    html_string = html_nodes.to_html()
    page_title = extract_title(markdown)

    output_string = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)
    output_string = sub(r"href=\"/", f"href=\"{basepath}", output_string)
    output_string = sub(r"src=\"/", f"src=\"{basepath}", output_string)

    try:
        os.makedirs(os.path.dirname(dest_path), 666, True)
        with open(dest_path, 'w') as f:
            f.write(output_string)
    except Exception:
        print(f"An exception occurred while writing to {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_contents = os.listdir(dir_path_content)
    for obj in dir_contents:
        obj_abs_path = os.path.join(dir_path_content, obj)
        dst_abs_path = os.path.join(dest_dir_path, obj)
        if os.path.isfile(obj_abs_path):
            if obj[-3:] == ".md":
                generate_page(obj_abs_path, template_path, (dst_abs_path[:-3] + ".html"), basepath)
        else:
            os.mkdir(dst_abs_path, 0o755)
            generate_pages_recursive(obj_abs_path, template_path, dst_abs_path, basepath)

def copy_static_dir_to_public(subdir = ""):
    stat_abs = os.path.join(os.path.abspath("static"), subdir)
    pub_abs = os.path.join(os.path.abspath("docs"), subdir)

    if not subdir:
        if os.path.exists(pub_abs):
            print("Deleting public folder and all contents...")
            rmtree(pub_abs)
        print("Making public folder...")
        os.mkdir(pub_abs, 0o755)

    print("In " + stat_abs)
    dir_contents = os.listdir(stat_abs)
    for obj in dir_contents:
        obj_abs_path = os.path.join(stat_abs, obj)
        dst_abs_path = os.path.join(pub_abs, obj)
        if os.path.isfile(obj_abs_path):
            copy(obj_abs_path, dst_abs_path)
            print(f"Copied '{obj_abs_path}' to '{dst_abs_path}'")
        else:
            os.mkdir(dst_abs_path, 0o755)
            if subdir:
                copy_static_dir_to_public(f"{subdir}/{obj}")
            else:
                copy_static_dir_to_public(obj)
