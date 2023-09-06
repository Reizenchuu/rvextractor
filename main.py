import os

#Directory creation
output_dir = './output/'
if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def extractTextFromMapYaml(mapPath): 
    with open(mapPath, 'r', encoding='utf-8') as file:
        mapData = file.read()
    
    base_name = os.path.basename(mapPath)
    output_filename = os.path.join(output_dir, base_name)

    # Dump content into the new output YAML file
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(mapData)

extractTextFromMapYaml('./YAML/Map001.yaml')