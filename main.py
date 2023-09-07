import os
import re

#Directory creation
output_dir = './output/'
if not os.path.exists(output_dir):
        os.makedirs(output_dir)

#dictionary: key->string (untranslated text) value->array (sources) 
textExtracts = {}

def extractTextFromMapYaml(mapPath): 
    with open(mapPath, 'r', encoding='utf-8') as file:
        mapData = file.read().splitlines()  

    base_name = os.path.basename(mapPath).replace(".yaml", "")
    output_filename = os.path.join(output_dir, base_name)

    # Dump content into the new output YAML file
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(mapData))

    
    for idx, line in enumerate(mapData):
        # Check for desired line and extract relevant data
        if "!ruby/object:RPG::EventCommand" in line and "401" in line:
            start_index = line.find("p: [") + 4
            end_index = line.find("]}")
            extracted_text = line[start_index:end_index]
            eventName = ""
            # Search for the "!ruby/object:RPG::Event$" in lines above the current line
            # Search for the "!ruby/object:RPG::Event$" in lines above the current line
            for reverse_index in range(idx, -1, -1):
                if re.match(r".*!ruby/object:RPG::Event$", mapData[reverse_index]):
                    # After finding the line, look for the line with "name:" after it
                    for forward_index in range(reverse_index + 1, len(mapData)):
                        if "name: " in mapData[forward_index]:
                            eventName = mapData[forward_index]
                            eventName = eventName.replace("name: ", "").strip()
                            break
                    break
            print(f"{base_name} || {eventName} || {extracted_text}")

            

    


extractTextFromMapYaml('./YAML/Map001.yaml')