import os
import re
import map
import util

#Directory creation
#path for yaml files to process
directory_path = './yaml/'
#path for translation folder to patch
translation_path = './translation/'

outputDir = './extractions/'
patchedYamlsPath = './patch/'

if not os.path.exists(outputDir):
        os.makedirs(outputDir)
if not os.path.exists(patchedYamlsPath):
        os.makedirs(patchedYamlsPath)


#dictionary: key->string (untranslated text) value->array (sources) 
textExtracts = {}

def extractTextFromYAMLs():
    global textExtracts
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' is missing!")
        print("Please add the yaml directory that contains the Data files")
        return

    # If directory exists, iterate over all files in the specified directory
    for filename in os.listdir(directory_path):
        # Check if the file is a .yaml file and its name matches the pattern 'MapXXX'
        print(f"Processing {filename}")
        if filename.endswith(".yaml") and re.match(r'^Map\d{3}\.yaml$', filename):
            # Get the complete file path
            file_path = os.path.join(directory_path, filename)
            # Send the file path to the sip() method
            textExtracts = map.extractTextFromMapYaml(file_path, textExtracts)
        

def fromDictionnaryToExtractedFiles():
    jsonDictionary = {}
    for jptxt in textExtracts.keys():
        jsonKey = textExtracts[jptxt][0][0]
        #defining the element that will be inserted into the json file
        jsonJptxtElement = {
             "JP": jptxt,
             "EN": "",
             "TYPE": textExtracts[jptxt][1]
        }
        if not jsonDictionary.get(jsonKey):
            jsonDictionary[jsonKey] = [jsonJptxtElement]
        else:
            jsonDictionary[jsonKey].append(jsonJptxtElement)
    #Writing json files
    util.fromJsonDicToFiles(jsonDictionary, outputDir)

def patchTranslationsIntoNewYamls():
    if not os.path.exists(translation_path):
        print(f"Error: Directory '{translation_path}' is missing!")
        print("Please add the yaml directory that contains the Data files")
        return
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' is missing!")
        print("Please add the yaml directory that contains the Data files")
        return
    translations = util.fromJsonFilesToOneDictionnary(translation_path)
    
    for filename in os.listdir(directory_path):
        # Check if the file is a .yaml file and its name matches the pattern 'MapXXX'
        print(f"Processing {filename}")
        if filename.endswith(".yaml") and re.match(r'^Map\d{3}\.yaml$', filename):
            # Get the complete file path
            yamlPath = os.path.join(directory_path, filename)
            # Send the file path to the sip() method
            if (map.patchTranslationsIntoMapYAML(yamlPath, patchedYamlsPath, translations) == -1):
                return



# Main: 
extractTextFromYAMLs()
fromDictionnaryToExtractedFiles()
patchTranslationsIntoNewYamls()
