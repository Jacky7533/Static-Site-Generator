from textnode import TextNode
import os
import shutil

def clear_directory(directory_path):
    """Remove all files and subdirectories in the given directory."""
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    print(f"Cleared contents of directory: {directory_path}")

def copy_directory(src, dst):
    """Recursively copy all contents from src directory to dst directory."""
    if not os.path.exists(dst):
        os.makedirs(dst)  # Create destination directory if it doesn't exist
    
    # Clear the destination directory to ensure it's clean
    clear_directory(dst)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isdir(src_path):
            # Recursively copy subdirectories
            shutil.copytree(src_path, dst_path)
            print(f"Copied directory: {src_path} to {dst_path}")
        else:
            # Copy files
            shutil.copy2(src_path, dst_path)
            print(f"Copied file: {src_path} to {dst_path}")



def main():
    # Example usage:
    source_directory = '/home/jacky/workspace/github.com/Jacky7533/Static-Site-Generator/static'
    destination_directory = '/home/jacky/workspace/github.com/Jacky7533/Static-Site-Generator/public'
    
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    copy_directory(source_directory, destination_directory)
    print(node)


main()
