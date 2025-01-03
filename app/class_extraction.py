def get_class_savee(file_name):
    file_name = file_name.split("/")[2]

    if file_name[3] == "n":
        return "neutral"
    if file_name[3] == "a":
        return "angry"
    if file_name[3] == "d":
        return "disgusted"
    if file_name[3] == "f":
        return "fearful"
    if file_name[3] == "h":
        return "happy"
    if file_name[3:5] == "sa":
        return "sad"
    if file_name[3:5] == "su":
        return "surprised"
