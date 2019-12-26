import unittest
from github import Github, InvalidGithubResourcesException

class TestGithubModule(unittest.TestCase):
    def setUp(self):
        # self.github_iter = Github('moby', [ 'moby', ], [ 'topics' ])
        self.github_iter = Github('moby', [ 'moby' ], [ 'topics' ], 'daryllft19', 'a361bf08ddcee4cecd4571490b82563d2dc0fde1')

    def test_invalid_github_resource(self):
        """Tests if module throws an exception after incorrect resource"""
        with self.assertRaises(InvalidGithubResourcesException):
            Github('any', [ 'any' ], [ 'unsupported' ])
            self.fail('InvalidGithubResourcesException not raised when an unsupported resource is added')

    def test_required_functions(self):
        """Tests for expected functions that is being used in the class"""

        _expected_functions = [
                    '__init__',
                    '__next__',
                    '__iter__',
                    'read',
                    '_validate_resources',
                ]

        for fn in _expected_functions:
            self.assertTrue(hasattr(self.github_iter, fn), f'Github is missing expected function {fn}')

    def test_read(self):
        """Tests for the read function that retrieves the data. Probably better to separate http client to mock requests. Prone to errors for now due to API rate limit"""

        data = self.github_iter.read()

        self.assertDictEqual(data, {'resource': 'topics', 'repo': 'moby', 'data': {'names': ['docker', 'containers', 'go']}})


if __name__ == '__main__':
    unittest.main(warnings='ignore')
