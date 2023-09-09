import os
import re
from util import insertText


def extractTextFromMapYaml(mapPath, textExtracts): 
    # Pattern to extract Japanese text
    pattern = re.compile(r".*!ruby/object:RPG::EventCommand.*c: 401.*p.*")

    # Other pattern initializations
    event_pattern = re.compile(r".*!ruby/object:RPG::Event$")
    name_pattern = re.compile(r".*name: .*")
    id_pattern = re.compile(r".*id: .*")
    page_pattern = re.compile(r".*!ruby/object:RPG::Event::Page$")

    fileName = os.path.basename(mapPath).replace(".yaml", "")
    
    with open(mapPath, "r", encoding='utf-8') as file:
        line = file.readline()
        while line:
            #emptying list of lines to decrease loop computing
            eventName = ""
            eventId = ""
            pageCount = 0
            # Try to match the pattern
            if pattern.match(line):
                eventName = ""
                eventId = -1
                pageCount = 0
                start_index = line.find("p: [") + 4
                end_index = line.find("]}")
                japaneseText = line[start_index:end_index]

                # # Find the associated event name and id + page
                # for prev_line in listOfLines:
                #     if event_pattern.match(prev_line):
                #         break
                #     if name_pattern.match(prev_line):
                #         eventName = prev_line.replace("name: ", "").strip()
                #     elif id_pattern.match(prev_line):
                #         eventId = prev_line.replace("id: ", "").strip()
                #     elif page_pattern.match(prev_line):
                #         pageCount += 1

                # eventSrc = f"{fileName}/{eventName}(id:{eventId})/p{pageCount}"
                textExtracts = insertText(textExtracts, japaneseText, "Dialogue", fileName)
        
            line = file.readline()
    return textExtracts

def patchTranslationsIntoMapYAML(mapPath, outputPath, translationsDic):
    fileName = os.path.basename(mapPath).replace(".yaml", "")
    # Pattern to extract Japanese text
    pattern = re.compile(r".*!ruby/object:RPG::EventCommand.*c: 401.*p.*")
    with open(mapPath, "r", encoding='utf-8') as file:
        fileContent = file.readlines()
    translatedFileLines = []
    for line in fileContent:
        japaneseText = ""
        if pattern.match(line):
            start_index = line.find("p: [") + 4
            end_index = line.find("]}")
            japaneseText = line[start_index:end_index]
            # Raising exception if japanese text is not found in translation dictionnary
            if japaneseText not in translationsDic:
                print(f"Translation files corrupted! couldn't find the following japanese text: {japaneseText}")
                return -1
            #If no translation, skip text
            if translationsDic[japaneseText].strip() == "":
                translatedFileLines.append(line)
                continue
            #replacing the japanese text with its translation
            line = line.replace(japaneseText, translationsDic[japaneseText])
            translatedFileLines.append(line)
        else: 
            translatedFileLines.append(line)
    #writing new translated yaml file
    translatedYaml = os.path.join(outputPath, f"{fileName}.yaml")
    with open(translatedYaml, "w", encoding='utf-8') as file:
        file.writelines(translatedFileLines)