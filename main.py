import threading
import requests
from concurrent.futures import ThreadPoolExecutor

org_name = 'microsoft'
token = 'your_token'

headers = {'Authorization': f'token {token}',
           'Accept': 'application/vnd.github.v3+json'}

repos = requests.get(f'https://api.github.com/orgs/{org_name}/repos',
                     headers=headers).json()
committers = {}


def count_commits(repo):
    commits = requests.get(repo['commits_url'].replace('{/sha}', ''),
                           headers=headers).json()
    for commit in commits:
        dev = commit['commit']['author']['email']
        with lock:
            if dev not in committers:
                committers[dev] = 0
            committers[dev] += 1


lock = threading.Lock()
with ThreadPoolExecutor() as executor:
    executor.map(count_commits, repos)

for author, count in sorted(committers.items(), key=lambda item: item[1],
                            reverse=True)[:100]:
    print(f'{author}: {count} commits')
