import os


def find_filename(directory, extension):
    if not os.path.exists(directory):
        os.mkdir(directory)

    output = f"{directory}/001.{extension}"
    i=0
    while os.path.exists(output):
        i+=1
        output = f"{directory}/{i:03d}.{extension}"
    return output