from requests import Session

class InvalidGithubResourcesException(Exception): pass 

class Github:
    """Class for retrieving github resources as a stream.
   
    '_supported_resources' contain the github resources supported by this library.

    """

    _supported_resources = [ 'topics', 'vulnerability-alerts', 'topics', 'languages', 'teams', 'tags', 'pulls', 'issues', 'import', 'branches', 'interaction-limits', 'projects', 'contributors' ]

    def __init__(self, owner, repo, resources, user=None, token=None):
        """__init__ method

        :param owner: User/Organization of the github repositories
        :param repo: List of repositories to retrieve data from
        :param resources: List of resources associated with the repositories and owner to retrieve
        :param user: The user part of the user/token duo to execute authenticated requests to have a higher rate limit in API calls
        :param token: The token part of the user/token duo to execute authenticated requests to have a higher rate limit in API calls

        """

        self._resources_index = 0
        self._repo_index = 0
        self._owner = owner
        self._repo = list(set(repo))
        self._resources = list(set(resources))
        self._validate_resources()
        self._session = Session()

        if user and token:
            self._session.auth = (user, token)

        self._session_headers_map = {
                    'topics': 'application/vnd.github.mercy-preview+json',
                    'vulnerability-alerts': 'application/vnd.github.dorian-preview+json',
                    'issues': 'application/vnd.github.machine-man-preview',
                    'import': 'application/vnd.github.barred-rock-preview',
                    'projects': 'application/vnd.github.inertia-preview+json'
                }

    def __iter__(self):
        return iter(self)

    def __next__(self):
        """Retrieves the next data, iterating through each resource and repo

        :returns:
            {
                'resource': <Resource being retrieved>,
                'repo': <Repo where resource is being retrieved>,
                'data': <JSON response of github resource>
            }

        """

        if self._resources_index == len(self._resources):
            return None

        resource = self._resources[self._resources_index]
        repo = self._repo[self._repo_index]
        url = f'https://api.github.com/repos/{self._owner}/{repo}/{resource}'
        res = self._session.get(url, headers={
                'Accept': self._session_headers_map[resource] if resource in self._session_headers_map else 'application/vnd.github.v3+json'
            })

        ret = {
                'resource': resource,
                'repo': repo,
                'data': res.json()
                }

        self._repo_index += 1

        if self._repo_index == len(self._repo):
            self._repo_index = 0
            self._resources_index += 1

        return ret

    def read(self):
        """Method simulating the next function of the iterator"""
        return next(self)

    def _validate_resources(self):
        """Validates the resources list based on the supported resources

        :raises InvalidGithubResourcesException: Raises an exception when a non-supported resource is requested
        """
        invalid = set(self._resources).difference(self._supported_resources)
        if invalid:
            raise InvalidGithubResourcesException(invalid)

