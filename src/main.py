import os
import shutil
from pathlib import Path
from textnode import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No H1 header found in the markdown file.")


def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory(s, d)
        else:
            shutil.copy2(s, d)
            print(f"Copied {s} to {d}")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown = file.read()

    with open(template_path, 'r') as file:
        template = file.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)
    print(f"Title: {title}")

    new_html = template.replace(
        "{{ Title }}", title).replace("{{ Content }}", html)
    # print(f"New HTML: {new_html}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(new_html)
    print(f"Written to {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(source_path) and source_path.endswith('.md'):
            dest_path = os.path.join(
                dest_dir_path, Path(source_path).stem + '.html')
            generate_page(source_path, template_path, dest_path)
        elif os.path.isdir(source_path):
            new_dest_dir_path = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest_dir_path, exist_ok=True)
            generate_pages_recursive(
                source_path, template_path, new_dest_dir_path)


def main():
    copy_directory("static", "public")
    generate_pages_recursive("content", "templates/base.html", "public")


if __name__ == "__main__":
    main()
