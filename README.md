# Github Ingester
A module that uses the github API to retrieve github data as a stream.

## Getting Started
Install dependencies found in [requirements.txt](https://github.com/daryllft19/github-ingester/blob/master/etc/requirements.txt)

## Usage
```
from github import Github

# Github(<owner>, [ <list of repos> ], [ <list of resources> ], <user | optional>, <token | optional>)
gi = Github('moby', [ 'moby' ], [ 'topics' ])

gi.read()
# {'resource': 'topics', 'repo': 'moby', 'data': {'names': ['docker', 'containers', 'go']}}
```

## Tests
```
python -m unittest discover tests/
```
