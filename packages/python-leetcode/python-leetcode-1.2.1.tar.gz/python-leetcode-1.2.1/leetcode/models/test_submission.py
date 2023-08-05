# coding: utf-8

"""
    Leetcode API

    Leetcode API implementation.  # noqa: E501

    OpenAPI spec version: 1.0.1-1
    Contact: pv.safronov@gmail.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class TestSubmission(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "data_input": "str",
        "lang": "str",
        "question_id": "int",
        "test_mode": "bool",
        "typed_code": "str",
    }

    attribute_map = {
        "data_input": "data_input",
        "lang": "lang",
        "question_id": "question_id",
        "test_mode": "test_mode",
        "typed_code": "typed_code",
    }

    def __init__(
        self,
        data_input=None,
        lang=None,
        question_id=None,
        test_mode=None,
        typed_code=None,
    ):  # noqa: E501
        """TestSubmission - a model defined in Swagger"""  # noqa: E501
        self._data_input = None
        self._lang = None
        self._question_id = None
        self._test_mode = None
        self._typed_code = None
        self.discriminator = None
        self.data_input = data_input
        self.lang = lang
        self.question_id = question_id
        self.test_mode = test_mode
        self.typed_code = typed_code

    @property
    def data_input(self):
        """Gets the data_input of this TestSubmission.  # noqa: E501


        :return: The data_input of this TestSubmission.  # noqa: E501
        :rtype: str
        """
        return self._data_input

    @data_input.setter
    def data_input(self, data_input):
        """Sets the data_input of this TestSubmission.


        :param data_input: The data_input of this TestSubmission.  # noqa: E501
        :type: str
        """
        if data_input is None:
            raise ValueError(
                "Invalid value for `data_input`, must not be `None`"
            )  # noqa: E501

        self._data_input = data_input

    @property
    def lang(self):
        """Gets the lang of this TestSubmission.  # noqa: E501


        :return: The lang of this TestSubmission.  # noqa: E501
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Sets the lang of this TestSubmission.


        :param lang: The lang of this TestSubmission.  # noqa: E501
        :type: str
        """
        if lang is None:
            raise ValueError(
                "Invalid value for `lang`, must not be `None`"
            )  # noqa: E501

        self._lang = lang

    @property
    def question_id(self):
        """Gets the question_id of this TestSubmission.  # noqa: E501


        :return: The question_id of this TestSubmission.  # noqa: E501
        :rtype: int
        """
        return self._question_id

    @question_id.setter
    def question_id(self, question_id):
        """Sets the question_id of this TestSubmission.


        :param question_id: The question_id of this TestSubmission.  # noqa: E501
        :type: int
        """
        if question_id is None:
            raise ValueError(
                "Invalid value for `question_id`, must not be `None`"
            )  # noqa: E501

        self._question_id = question_id

    @property
    def test_mode(self):
        """Gets the test_mode of this TestSubmission.  # noqa: E501


        :return: The test_mode of this TestSubmission.  # noqa: E501
        :rtype: bool
        """
        return self._test_mode

    @test_mode.setter
    def test_mode(self, test_mode):
        """Sets the test_mode of this TestSubmission.


        :param test_mode: The test_mode of this TestSubmission.  # noqa: E501
        :type: bool
        """
        if test_mode is None:
            raise ValueError(
                "Invalid value for `test_mode`, must not be `None`"
            )  # noqa: E501

        self._test_mode = test_mode

    @property
    def typed_code(self):
        """Gets the typed_code of this TestSubmission.  # noqa: E501


        :return: The typed_code of this TestSubmission.  # noqa: E501
        :rtype: str
        """
        return self._typed_code

    @typed_code.setter
    def typed_code(self, typed_code):
        """Sets the typed_code of this TestSubmission.


        :param typed_code: The typed_code of this TestSubmission.  # noqa: E501
        :type: str
        """
        if typed_code is None:
            raise ValueError(
                "Invalid value for `typed_code`, must not be `None`"
            )  # noqa: E501

        self._typed_code = typed_code

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(TestSubmission, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TestSubmission):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
