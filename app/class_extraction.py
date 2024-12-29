def get_class_savee(file_name):
    file_name = file_name.split("/")[2]

    if file_name[3] == "n":
        return "neutral"
    if file_name[3] == "a":
        return "anger"
    if file_name[3] == "d":
        return "disgust"
    if file_name[3] == "f":
        return "fear"
    if file_name[3] == "h":
        return "happiness"
    if file_name[3:5] == "sa":
        return "sadness"
    if file_name[3:5] == "su":
        return "surprise"
