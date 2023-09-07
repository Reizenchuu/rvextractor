import os
import re
from util import insertText


def extractTextFromMapYaml(mapPath, output_dir, textExtracts): 
    with open(mapPath, 'r', encoding='utf-8') as file:
        mapData = file.read().splitlines()  

    fileName = os.path.basename(mapPath).replace(".yaml", "")

    
    for idx, line in enumerate(mapData):
        # Check for desired line and extract relevant data
        if "!ruby/object:RPG::EventCommand" in line and "401" in line:
            start_index = line.find("p: [") + 4
            end_index = line.find("]}")
            japaneseText = line[start_index:end_index]
            eventName = ""
            eventId = ""
            pageCount = 0
            # Search for the "!ruby/object:RPG::Event$" in lines above the current line
            # Search for the "!ruby/object:RPG::Event$" in lines above the current line
            for reverse_index in range(idx, -1, -1):
                if re.match(r".*!ruby/object:RPG::Event$", mapData[reverse_index]):
                    # After finding the line, look for the line with "name:" after it
                    nameFound = False
                    eventIdFound = False
                    for forward_index in range(reverse_index + 1, len(mapData)):
                        if "name: " in mapData[forward_index]:
                            eventName = mapData[forward_index]
                            eventName = eventName.replace("name: ", "").strip()
                            nameFound = True
                        if "id: " in mapData[forward_index]:
                            eventId = mapData[forward_index]
                            eventId = eventId.replace("id: ", "").strip()
                            eventIdFound = True
                        if eventIdFound and nameFound:
                            break
                    #Getting page number
                    for forward_index in range(reverse_index+1, idx):
                        if re.match(r".*!ruby/object:RPG::Event::Page$", mapData[forward_index]):
                            pageCount += 1
                    break
            eventSrc = f"{fileName}/{eventName}(id:{eventId})/p{pageCount}"
            textExtracts = insertText(textExtracts, japaneseText, eventSrc, fileName)
    return textExtracts

