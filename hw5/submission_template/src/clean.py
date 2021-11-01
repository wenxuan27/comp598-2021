import sys
import json
import datetime





def validate_author_exists(json_data):
    return 'author' in json_data

def validate_author_not_null_or_na(json_data):
    return not (json_data['author'] == None or json_data['author'] == 'na' or json_data['author'] == 'NA' or json_data['author'] == 'N/A' or json_data['author'] == 'n/a')

def validate_datetime_exists(json_data):
    return 'createdAt' in json_data

def validate_title_or_title_text_exists(json_data):
    return 'title' in json_data or 'title_text' in json_data

def validate_total_count_exists(json_data):
    return 'total_count' in json_data


def load_json(input_str):
    try:
        json_data = json.loads(input_str)
    except Exception as e:
        return None
    
    return json_data


def validate_and_transform(json_data):

    if json_data == None:
        return None

    new_json_data = {}
    if (validate_author_exists(json_data)):
        if validate_author_not_null_or_na(json_data):
            new_json_data['author'] = json_data['author']
        else:
            return None


    if validate_datetime_exists(json_data):
        timeiscorrect = True
        try:
            t = datetime.datetime.strptime(json_data['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
            utc_tz = datetime.timezone(datetime.timedelta(seconds=0))
            new_json_data['createdAt'] = (t.astimezone(utc_tz)).isoformat()
        except Exception as e:
            timeiscorrect = False

        if timeiscorrect == False:
            try:
                t = datetime.datetime.fromisoformat(json_data['createdAt'])
                utc_tz = datetime.timezone(datetime.timedelta(seconds=0))
                new_json_data['createdAt'] = (t.astimezone(utc_tz)).isoformat()

            except Exception as e:
                return None


    if validate_total_count_exists(json_data):
        if type(json_data['total_count']) == int:
            new_json_data['total_count'] = json_data['total_count']
        elif type(json_data['total_count']) == str:
            try:
                new_json_data['total_count'] = int(json_data['total_count'])
            except Exception as e:
                return None
        elif type(json_data['total_count']) == float:
            try:
                new_json_data['total_count'] = round(json_data['total_count'])
            except Exception as e:
                return None
        else:
            return None



    if 'title' in json_data:
        new_json_data['title'] = json_data['title']
    elif 'title_text' in json_data:
        new_json_data['title'] = json_data['title_text']
    else:
        return None

    
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


    if 'text' in json_data:
        new_json_data['text'] = json_data['text']
    
    return new_json_data
    

def main():

    if len(sys.argv) >= 3:
        if sys.argv[1] == '-i':
            input_file = sys.argv[2]
    else:
        input_file = 'data/example.json'
        # input_file = 'test/fixtures/test_6.json'


    if len(sys.argv) >= 5:
        if sys.argv[3] == '-o':
            output_file = sys.argv[4]
    else:
        output_file = input_file + '.clean'


    with open(output_file, 'w') as the_file:
        the_file.write('')


    with open(input_file) as file:
        for line in file:
            json_data = load_json(line.rstrip())
 
            if(json_data == None):
                continue

            new_json_data = validate_and_transform(json_data)

            if new_json_data == {}:
                continue
            elif new_json_data == None:
                continue
                    
            with open(output_file, 'a') as the_file:
                the_file.write(json.dumps(new_json_data)+'\n')
        

if __name__ == '__main__':
    main()