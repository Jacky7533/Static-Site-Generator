import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()  # Split the markdown content into individual lines
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace
        if line.startswith("# "):  # Check if the line starts with '# '
            return line[2:].strip()  # Remove the '# ' and return the remaining text
    # If no h1 header is found, raise an exception
    raise ValueError("No h1 header found in the markdown content.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown content
    with open(from_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    
    # Read the template content
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML to the destination path
    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)

def generate_pages_recursive(from_path, template_path, dest_path):
    print(f"Generating page recursively from {from_path} to {dest_path} to {template_path}")

    for root, dirs, files in os.walk(from_path):
        for file_name in files:
            if file_name.endswith('.md'):
                 # Construct the full path for the markdown file
                md_file_path = os.path.join(root, file_name)
                
                # Calculate the relative path from the content directory
                rel_path = os.path.relpath(root, from_path)
                
                # Determine the destination directory based on the relative path
                dest_dir = os.path.join(dest_path, rel_path)
                
                # Ensure the destination directory exists
                os.makedirs(dest_dir, exist_ok=True)
                
                # Construct the destination HTML file path
                dest_file_path = os.path.join(dest_dir, file_name.replace('.md', '.html'))
                
                # Generate the HTML file
                generate_page(md_file_path, template_path, dest_file_path)               