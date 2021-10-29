import sys
import json

from datetime import datetime


if len(sys.argv) >= 3:
    if sys.argv[1] == '-i':
        input_file = sys.argv[2]
else:
    input_file = 'data/example.json'


if len(sys.argv) >= 5:
    if sys.argv[3] == '-o':
        output_file = sys.argv[4]
else:
    output_file = input_file + '.clean'

json.dump({}, open(output_file, 'w'))

with open(input_file) as file:
    i = 0
    for line in file:
        # print(line.rstrip())

        new_json_data = {}

        try:
            json_data = json.loads(line.rstrip())
        except Exception as e:
            print('Error:', e)
            print(line.rstrip())
            continue

        if not ('author' in json_data):
            continue

        if json_data['author'] == None or json_data['author'] == 'na' or json_data['author'] == 'NA' or json_data['author'] == 'N/A' or json_data['author'] == 'n/a':
            continue
        else:
            new_json_data['author'] = json_data['author']

        if 'createdAt' in json_data:
            try:
                datetime.strptime(json_data['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
                new_json_data['createdAt'] = json_data['createdAt']
            except Exception as e:
                continue
            # try:
            #     new_json_data['createdAt'] = datetime.fromisoformat(json_data['createdAt'])
                # new_json_data['createdAt'] = json_data['createdAt']
            # except Exception as e:
            #     continue
        else:
            continue

        if 'total_count' in json_data:
            if type(json_data['total_count']) == int:
                new_json_data['total_count'] = json_data['total_count']
            elif type(json_data['total_count']) == str:
                try:
                    new_json_data['total_count'] = int(json_data['total_count'])
                except Exception as e:
                    continue
            elif type(json_data['total_count']) == float:
                try:
                    new_json_data['total_count'] = round(json_data['total_count'])
                except Exception as e:
                    continue
            else:
                continue
        else:
            continue


        if 'title' in json_data:
            new_json_data['title'] = json_data['title']
        elif 'title_text' in json_data:
            new_json_data['title'] = json_data['title_text']
        else:
            continue

        
        if 'tags' in json_data:
            new_tags = []

            for tag in json_data['tags']:
                splitted_tag = tag.split()
                if len(splitted_tag) == 1:
                    new_tags.append(tag)
                else:
                    for word in splitted_tag:
                        if word != "" and word != " ":
                            new_tags.append(word)
            new_json_data['tags'] = new_tags

                
        json.dump(new_json_data, open(output_file, 'a'))

        # print(i, json_data)

        # i += 1
