import os
import time
import re
import shutil
import requests

starttime = time.time()
dir_path = os.path.dirname(os.path.realpath(__file__))

source = "/home/gway/ddos-detect/"
destination = "/home/gway/temp/"

def search_file(folder_path, partial_name):
    pattern = re.compile(fr".*{partial_name}.*", re.IGNORECASE)
    matching_files = []

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if pattern.match(file_name):
                file_path = os.path.join(root, file_name)
                creation_time = os.path.getctime(file_path)
                current_time = time.time()
                time_diff = current_time - creation_time
                if time_diff > 60:  # More than 1 hour 1 minute ago (3660 seconds)
                    matching_files.append((file_path, creation_time))
    
    if len(matching_files)>1:
        matching_files.sort(key=lambda x: x[1])
        first_file_path, _ = matching_files[0]
        file_name = os.path.basename(first_file_path)
        file_path = os.path.dirname(first_file_path)
        file_name_without_ext, file_ext = os.path.splitext(file_name)
        return file_path, file_name, file_name_without_ext, file_ext
    else:
        return None

while True:
    print("tick - waiting")
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

    partial_name = 'ddos_attack_log'
    result = search_file(source, partial_name)

    if result:
        file_path, file_name, _, _ = result
        src_path = os.path.join(file_path, file_name)
        dst_path = os.path.join(destination, file_name)

        if os.path.isfile(src_path):
            with open(src_path, 'rb') as open_file:
                files = {'file': (file_name, open_file)}
                reply = requests.post('http://172.20.10.4:5000/upload', files=files)
                print(reply.text)
                print("File has been successfully sent to the server")

            try:
                shutil.move(src_path, dst_path)
                print(f"File '{file_name}' moved from '{src_path}' to '{dst_path}'")
            except Exception as e:
                print(f"Error moving file: {str(e)}")
        else:
            print(f"File '{file_name}' does not exist in '{src_path}'")
    else:
        print(f"No file with partial name '{partial_name}' found in '{source}'")
