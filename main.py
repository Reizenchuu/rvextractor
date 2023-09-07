import os
import re
import map

#Directory creation
directory_path = './yaml/'
output_dir = './output/'
if not os.path.exists(output_dir):
        os.makedirs(output_dir)


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
        if filename.endswith(".yaml") and re.match(r'^Map00\d{1}\.yaml$', filename):
            # Get the complete file path
            file_path = os.path.join(directory_path, filename)
            # Send the file path to the sip() method
            textExtracts = map.extractTextFromMapYaml2(file_path, output_dir, textExtracts)
        


extractTextFromYAMLs()
with open("dictionary_output.txt", 'w', encoding='utf-8') as file:
    for key, value in textExtracts.items():
        file.write(f"{key}={value}\n")