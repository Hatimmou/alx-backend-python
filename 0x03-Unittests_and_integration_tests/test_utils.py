#!/usr/bin/env python3
"""
This module contains a class used to perform unit testing for the utils class
"""
import json
from unittest.mock import patch
from unittest import TestCase
from parameterized import parameterized
from typing import Mapping
from typing import Sequence
from typing import Union
from utils import access_nested_map
from utils import get_json
from utils import memoize


class TestAccessNestedMap(TestCase):
    """
    unittest class to test the access_nested_map method
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nest: Mapping, path: Sequence,
                               expected: Union[dict, int]) -> None:
        """
        Test the access_nested_map method
        """
        self.assertEqual(access_nested_map(nest, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nest: Mapping,
                                         path: Sequence) -> None:
        """
        Test that the method raises the right exception
        """
        self.assertRaises(KeyError, access_nested_map, nest, path)


class TestGetJson(TestCase):
    """
    Test class for get_json function
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(self, url, payload, mock_requests_get) -> None:
        """
        Test the get_json method
        """
        mock_requests_get.return_value.json.return_value = payload
        self.assertEqual(get_json(url), payload)
        mock_requests_get.assert_called_once_with(url)


class TestMemoize(TestCase):
    """
    Test the memoization decorator, memoize
    """

    def test_memoize(self):
        """
        Test that utils.memoize decorator works as intended
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(TestClass, 'a_method') as mock_object:
            test = TestClass()
            test.a_property()
            test.a_property()
            mock_object.assert_called_once()
