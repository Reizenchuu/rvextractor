
import json
import os 
from ruamel.yaml import YAML

#Inserts text into global dictionnary
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
        if src not in dictionnary[text][1]:
            dictionnary[text][1].append(src)
    return dictionnary


#Takes a json dictionnary and creates json files out of it
def fromJsonDicToFiles(jsonDic, outputDir):
    for jsonName in jsonDic.keys():
        path = os.path.join(outputDir, f"{jsonName}.json")
        with open(path, "w", encoding='utf-8') as outfile:
            json.dump(jsonDic[jsonName], outfile, ensure_ascii=False)


#Takes list of translated json files and turns them into one big dictionnary
def fromJsonFilesToOneDictionnary(yamlDir):
    JPENDictionnary = {}
    for jsonFile in os.listdir(yamlDir):
        jsonFilePath = os.path.join(yamlDir, jsonFile)
        with open(jsonFilePath, "r", encoding='utf-8') as jsonContent:
            data = json.load(jsonContent)
            for node in data:
                JPENDictionnary[node["JP"]] = node["EN"]
    return JPENDictionnary
            

        

