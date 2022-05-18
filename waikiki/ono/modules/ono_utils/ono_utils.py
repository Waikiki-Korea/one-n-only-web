import os

def removeFile(path, file):
    target_file = os.path.join(os.getcwd() + path, file)
    # print(os.getcwd())
    print("[ Remove ] ", target_file)
    if os.path.isfile(target_file):
        print("this is a file")
        os.remove(target_file)
    else:
        print("this is not a file")