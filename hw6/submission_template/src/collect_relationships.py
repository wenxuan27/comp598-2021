import argparse
import hashlib
import os

import requests
import json

from bs4 import BeautifulSoup



def download_and_store_html(url, file_name):
    """
    Downloads the html from the given url and stores it in the given file_name.
    """


    print(f"Downloading {url}")
    html_file = requests.get(url)
    html = html_file.text
    with open(file_name, "w+") as f:
        f.write(html)


def main():
    """
    This is the main function.
    """ 

    parser = argparse.ArgumentParser(description='Collects relationships from whodatedwho')
    parser.add_argument('-c', '--config', help='config file', default="config.json")
    parser.add_argument('-o', '--output', help='output file', default="output.json")

    args = parser.parse_args()
    print(args.output)
    print(args.config)

    config_json = json.load(open(args.config))
    cache_dir = config_json["cache_dir"]


    output_dict = {}

    for person in config_json["target_people"]:
        url = f'https://www.whosdatedwho.com/dating/{person}'
        name_hash = hashlib.sha1(url.encode("UTF-8")).hexdigest()
        file_name = os.path.join(cache_dir, name_hash + ".html")

        if(not os.path.isdir(cache_dir)) :
            os.mkdir(cache_dir)

        if not os.path.exists(file_name):
            download_and_store_html(url, file_name)
        
        print(f"Processing {person}")

        with open(file_name, "r") as f:
            html = f.read()
            soup = BeautifulSoup(html, 'html.parser')

            div_tag = soup.find("div", {"class": "ff-panel clearfix"})

            # print(div_tag)

            relationships = []


            #find current relationship
            current_relationship = div_tag.find_all("div", recursive=False)[3].find_all("a", recursive=False)
            # print(current_relationship)

            if (len(current_relationship) > 0):
                other = current_relationship[0]['href'].split("/")[-1]
                other2 = current_relationship[1]['href'].split("/")[-1]
                if(other == person):
                    relationships.append(other2)
                else:
                    relationships.append(other)
                
                


            p_list = div_tag.find_all("p")

            # print(p_list)

            

            # # get main relationships
            # main_p = p_list[0]
            
            # for a_tag in main_p.find_all("a"):
            #     relationships.append(a_tag.text)

            # # get encounters
            # encounters_p = p_list[1]

            # for a_tag in encounters_p.find_all("a"):
            #     relationships.append(a_tag.text)


            # # get hookups
            # hookups_p = p_list[2]
            
            # for a_tag in hookups_p.find_all("a"):             
            #     relationships.append(a_tag.text)

            counter = 0
            for p in p_list:
                for a_tag in p.find_all("a", recursive=False):
                    if 'href' in a_tag.attrs:
                        print(a_tag.class_)
                        splitted = a_tag['href'].split('/')
                        if(splitted[1] == "dating"):
                            counter += 1
                            # print(counter, a_tag['href'])
                            relationships.append(a_tag.text)
            
            print(counter)

            # print(relationships)
            output_dict[person] = relationships

            print(f"{person} has {len(relationships)} relationships")

    
    with open(args.output, "w+") as f:
        json.dump(output_dict, f)

            

if __name__ == "__main__":
    main()