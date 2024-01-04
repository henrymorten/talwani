import os

def remove_folder_contents(folder_path):
    # Iterate over all the files and subdirectories within the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        if os.path.isfile(item_path):
            # Remove file
            os.remove(item_path)
        elif os.path.isdir(item_path):
            # Remove subdirectory and its contents recursively
            remove_folder_contents(item_path)
            os.rmdir(item_path)