
import os


def dir_to_file(dir, file="dir.txt"):
    """ Find the files and directories in 'dir', remove hidden files,
        also get the files at the next level, and put everything
        into 'file' with this format:
            Contents of dir
            f1
            f2
            D: d1
              f1
              f2
            D: d2
              f1
    """
    # Check input
    if not isinstance(dir, str):
        raise TypeError("dir is not a string")
    if not isinstance(file, str):
        raise TypeError("file_name is not a string")

    if not os.path.isdir(dir):
        raise TypeError("dir is not a directory")

    try:
       sub = os.listdir(path=dir)
    except FileNotFoundError:
        return -1

    dir_list = []
    file_list = []
    # Get level 1 files and directories and drop hidden files
    for file_name in sub:
        if file_name[0:1] == '.':
            try:
                os.remove(os.path.join(dir, file_name))
            except FileExistsError:
                return -2

        elif os.path.isdir(os.path.join(dir, file_name)):
            dir_list.append(file_name)

        else:
            file_list.append(file_name)

    # Initialize output text
    try:
         with open(file, "r") as my_file:
             text = my_file.read()
             if text is None:
                 print("no content exists")
             else:  # overload file
                 my_file.truncate()

    except PermissionError:
        print("Permission error")

    except FileNotFoundError:
        print("File Not Found")

    except UnicodeDecodeError:
        print("Unicode Error")

    # Helper to put filenames into a str, optionally indenting
    # Input is a list of file names, their path, and an indent switch

    # Add level 1 files to output text

    # Get directories at level 1
    # Add directory and files for each level 1 directory
    level2_file = [os.listdir(path=dir+dir_name) for dir_name in dir_list]

    # Write to file

    try:
        with open(file, "w") as my_file:
            for file_name in file_list:
                my_file.write("\n".join(file_name))
            for i, dir_name in enumerate(dir_list):
                my_file.write("\n".join(dir_name))
                for sub_file_name in level2_file[i]:
                    my_file.write("\n".join("    ").join(sub_file_name))

    except PermissionError:
        print("Permission error")

    except FileNotFoundError:
        print("File Not Found")

    except IOError:
        print("Unicode Error")

    return None


if __name__ == "__main__":
    dir_to_file("")
