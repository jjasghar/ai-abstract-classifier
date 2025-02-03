import json
import glob
import os

json_files = glob.glob("chat_primes/jsons/*.json")

for json_name in json_files:
    file_name = json_name.split('/')
    base_file_name = file_name[2]
    name = base_file_name.split('.')
    markdown_name = name[0]

    with open(json_name, 'r') as f:
        data = json.load(f)

    markdown_out = f'''# {data['title']}

## Abstract
{data['abstract']}
    '''

    with open(f"chat_primes/{markdown_name}.md","w") as w:
        w.write(markdown_out)
