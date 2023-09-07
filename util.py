
#text: extracted japanese text
#src: source of extracted japanese text (event, page, file)
#filename: file name from which japanese text was extracted

def insertText(dictionnary, text, src, fileName):
    # Check if the text is already present in the dictionary
    if text not in dictionnary:
        # If not found, create a new entry with the given text, filename, and src
        dictionnary[text] = [[fileName], [src]]
    else:
        # If found, append the fileName and src to their respective lists
        #make sure file name doesn't already exist
        if fileName not in dictionnary[text][0]:
            dictionnary[text][0].append(fileName)
        dictionnary[text][1].append(src)
    return dictionnary

