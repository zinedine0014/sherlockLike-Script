import requests
import os
import termcolor as tc
import sys
import json

def search_for_user(sites: dict[str, str], username: str):
    found = []
    for site_name, site_url in sites.items():
        url = site_url.format(username)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                found.append(f'[{username}]: {url}')
                tc.cprint(f'[+][{username}] ', 'green', end=' ')
                print(url)
        except requests.RequestException as error:
            tc.cprint(f"Error with {site_name}: {error}", 'red')
    return found

def save_data(data: list, username: str):
    directory = './saved'
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f'{username}.txt')
    with open(file_path, 'w') as save_file:
        save_file.write('\n'.join(data) + '\n')
    print(f'Saved results in {file_path}')

def load_sites(sites_json_file: str):
    try:
        with open(sites_json_file, 'r') as sites_file:
            return json.load(sites_file).get('sites', {})
    except (json.JSONDecodeError, KeyError) as error:
        tc.cprint(f"Error loading sites: {error}", 'red')
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 gather.py <target> <sitesfile.json>")
        sys.exit(1)

    username = sys.argv[1]
    sites_file = sys.argv[2]

    if not os.path.isfile(sites_file):
        tc.cprint(f"{sites_file} does not exist\nCreate one", 'red')
        sys.exit(1)

    print(f'Searching for {username}')
    sites = load_sites(sites_file)
    if not sites:
        tc.cprint(f"No valid sites found in {sites_file}", 'red')
        sys.exit(1)

    results = search_for_user(sites, username)
    if results:
        save_data(results, username)
    else:
        tc.cprint(f"No results found for {username}", 'yellow')
