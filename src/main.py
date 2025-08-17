import os, sys

from fileio import copy_static_dir_to_public, generate_pages_recursive

def main():
    if sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_static_dir_to_public()

    src = os.path.abspath("content/")
    tmp = os.path.abspath("template.html")
    dst = os.path.abspath("docs/")
    generate_pages_recursive(src, tmp, dst, basepath)

if __name__ == "__main__":
    main()