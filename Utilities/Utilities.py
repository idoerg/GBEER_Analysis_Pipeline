import os

def return_recursive_files(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in flist:
            fname = os.path.join(path, f)
            if not os.path.isdir(fname):
                result.append(fname)
    return result

def return_recursive_dir_files(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in dir_name:
            fname = os.path.join(path, f)
            if os.path.isdir(fname):
                result.append(fname)
    return result