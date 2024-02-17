import os


def clear(directories: tuple) -> None:
    """
    INPUT:
        directories: tuple - a list of directories to clean
    OUTPUT:
        Removes any file in the given directories
    """
    for l in directories:
        if(not(os.path.exists(l))):
            continue
        for f in os.listdir(l):
            os.remove(f"{l}{f}")


def find_filename(directory: str, extension: str) -> str:
    """
    INPUT:
        directory: str - directory in which you want to save the file to
        extension: str - exension of the file to be saved
    OUTPUT:
        str - filename in the form of directory/XXX.exension with XXX being numbers going from 1 to 999
    """
    if not os.path.exists(directory):
        directory_split = directory.split("/")
        for d in range(1, len(directory_split)+1):
            if(not(os.path.exists("/".join(directory_split[:d])))):
                os.mkdir("/".join(directory_split[:d]))

    output = f"{directory}/001.{extension}"
    i=0
    while os.path.exists(output):
        i+=1
        output = f"{directory}/{i:03d}.{extension}"
        if i > 999:
            raise NameError(f"Cannot find a filename, too many {extension} files in {directory}")
    return output