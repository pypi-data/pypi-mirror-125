"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import unittest

import lakefs_client
from lakefs_client.api.refs_api import RefsApi  # noqa: E501


class TestRefsApi(unittest.TestCase):
    """RefsApi unit test stubs"""

    def setUp(self):
        self.api = RefsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_diff_refs(self):
        """Test case for diff_refs

        diff references  # noqa: E501
        """
        pass

    def test_dump_refs(self):
        """Test case for dump_refs

        Dump repository refs (tags, commits, branches) to object store  # noqa: E501
        """
        pass

    def test_log_commits(self):
        """Test case for log_commits

        get commit log from ref  # noqa: E501
        """
        pass

    def test_merge_into_branch(self):
        """Test case for merge_into_branch

        merge references  # noqa: E501
        """
        pass

    def test_restore_refs(self):
        """Test case for restore_refs

        Restore repository refs (tags, commits, branches) from object store  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
