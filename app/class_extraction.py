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


def get_class_tess(file_name):
    file_name = file_name.split("/")[-1]

    if file_name == "O":
        sex = "man"
    elif file_name == "Y":
        sex = "woman"
    
    if file_name[-11] == "n":
        emotion = "neutral"
    elif file_name[-9] == "a":
        emotion = "angry"
    elif file_name[-11] == "d":
        emotion = "disgusted"
    elif file_name[-8] == "f":
        emotion = "fearful"
    elif file_name[-9] == "h":
        emotion = "happy"
    elif file_name[-7] == "s":
        emotion = "sad"
    elif file_name[-6] == "p":
        emotion = "surprised"

    return sex + "_" + emotion