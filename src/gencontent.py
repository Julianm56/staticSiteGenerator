import os
from block_type import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # List all entries in the content directory
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        # Create full paths
        entry_path = os.path.join(dir_path_content, entry)
        
        # If the entry is a file and ends with .md
        if os.path.isfile(entry_path) and entry.endswith(".md"):
            # Create the corresponding destination path
            # We need to replace content directory with public directory
            # and change .md extension to .html
            rel_path = os.path.relpath(entry_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, rel_path.replace(".md", ".html"))
            
            # Generate the page
            generate_page(entry_path, template_path, dest_path)
        
        # If it's a directory, recursively process it
        elif os.path.isdir(entry_path):
            # Create corresponding directory in destination
            new_dest_dir = os.path.join(dest_dir_path, entry)
            # Recursively process the subdirectory
            generate_pages_recursive(entry_path, template_path, new_dest_dir)
