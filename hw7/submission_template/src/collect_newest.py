import json
import requests
import requests.auth

import os

import argparse

from dotenv import load_dotenv

load_dotenv()


def authenticate_user_pass(reddit_user, reddit_pass, reddit_client_id, reddit_client_secret, reddit_user_agent):
    """
    This function authenticates the user.
    """

    client_auth = requests.auth.HTTPBasicAuth(reddit_client_id, reddit_client_secret)
    post_data = {"grant_type": "password", "username": reddit_user, "password": reddit_pass}
    headers = {"User-Agent": reddit_user_agent}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    res_json = response.json()

    return res_json['access_token']

def get_posts(subreddit, limit, bearer_token, reddit_user_agent):
    """
    This function gets the posts from a subreddit.
    """
    posts_list = []
    limit_posts = 100
    url = f"https://oauth.reddit.com/r/{subreddit}/new.json?limit=100"
    print(url)
    print(bearer_token)

    

    try:

        headers = {"limit": str(limit_posts),  "Authorization": f"bearer {bearer_token}", "User-Agent": reddit_user_agent, "limit": str(limit_posts)}
        print(headers)
        r=requests.get(url, headers=headers)
        r.raise_for_status()
    except Exception as e:
        print("ERROR: ",e)
        return []

    res_json = r.json()
    print(res_json.keys())


    for post in res_json["data"]["children"]:
        posts_list.append(post["data"])

    # # get the rest of the posts
    # total = limit_posts
    # while total < limit:
    #     try:

    #         headers = {"limit": str(limit_posts), "count": str(total), "Authorization": f"bearer {bearer_token}", "User-Agent": reddit_user_agent}
    #         r=requests.get("http://www.reddit.com/r/{subreddit}/new.json", headers=headers)
    #         r.raise_for_status()
    #     except Exception as e:
    #         print(e)
    #         break


    #     res_json = r.json()
    #     for post in res_json["data"]["children"]:
    #         posts_list.append(post["data"])
    #     total += limit_posts
    
    return posts_list

def main():
    """
    This is the main function.
    """

    parser = argparse.ArgumentParser(description='Collects relationships from whodatedwho')
    parser.add_argument('-o', '--output', help='output file', default="output.json")
    parser.add_argument('-s', '--subreddit', help='subreddit', default="subreddit.json")

    args = parser.parse_args()


    reddit_user = os.environ['REDDIT_USER']
    reddit_pass = os.environ['REDDIT_PWD']
    reddit_client_id = os.environ['REDDIT_CLIENT_ID']
    reddit_client_secret = os.environ['REDDIT_CLIENT_SECRET']
    reddit_user_agent = os.environ['REDDIT_USER_AGENT']


    bearer_token = authenticate_user_pass(reddit_user, reddit_pass, reddit_client_id, reddit_client_secret, reddit_user_agent)
    # headers = {"Authorization": f"bearer {bearer_token}", "User-Agent": reddit_user_agent}

    # mcgill_file_path = "mcgill.json"
    # concordia_file_path = "concordia.json"
    output_file1 = open(args.output, "w", encoding="utf-8")
    # output_file2 = open(concordia_file_path, "w")

    # mcgill_subreddit = "mcgill"
    # concordia_subreddit = "concordia"

    posts = get_posts(args.subreddit, 100, bearer_token, reddit_user_agent)
    # Write the output to a file
    for post in posts:
        output_file1.write(json.dumps(post, ensure_ascii=False))
        output_file1.write('\n')


    output_file1.close()
    # output_file2.close()
    pass


if __name__ == '__main__':
    main()

