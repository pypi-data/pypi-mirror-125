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


class GraphqlQuery(object):
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
        "query": "str",
        "variables": "AnyOfGraphqlQueryVariables",
        "operation_name": "str",
    }

    attribute_map = {
        "query": "query",
        "variables": "variables",
        "operation_name": "operationName",
    }

    def __init__(self, query=None, variables=None, operation_name=None):  # noqa: E501
        """GraphqlQuery - a model defined in Swagger"""  # noqa: E501
        self._query = None
        self._variables = None
        self._operation_name = None
        self.discriminator = None
        self.query = query
        self.variables = variables
        if operation_name is not None:
            self.operation_name = operation_name

    @property
    def query(self):
        """Gets the query of this GraphqlQuery.  # noqa: E501


        :return: The query of this GraphqlQuery.  # noqa: E501
        :rtype: str
        """
        return self._query

    @query.setter
    def query(self, query):
        """Sets the query of this GraphqlQuery.


        :param query: The query of this GraphqlQuery.  # noqa: E501
        :type: str
        """
        if query is None:
            raise ValueError(
                "Invalid value for `query`, must not be `None`"
            )  # noqa: E501

        self._query = query

    @property
    def variables(self):
        """Gets the variables of this GraphqlQuery.  # noqa: E501


        :return: The variables of this GraphqlQuery.  # noqa: E501
        :rtype: AnyOfGraphqlQueryVariables
        """
        return self._variables

    @variables.setter
    def variables(self, variables):
        """Sets the variables of this GraphqlQuery.


        :param variables: The variables of this GraphqlQuery.  # noqa: E501
        :type: AnyOfGraphqlQueryVariables
        """
        if variables is None:
            raise ValueError(
                "Invalid value for `variables`, must not be `None`"
            )  # noqa: E501

        self._variables = variables

    @property
    def operation_name(self):
        """Gets the operation_name of this GraphqlQuery.  # noqa: E501


        :return: The operation_name of this GraphqlQuery.  # noqa: E501
        :rtype: str
        """
        return self._operation_name

    @operation_name.setter
    def operation_name(self, operation_name):
        """Sets the operation_name of this GraphqlQuery.


        :param operation_name: The operation_name of this GraphqlQuery.  # noqa: E501
        :type: str
        """

        self._operation_name = operation_name

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
        if issubclass(GraphqlQuery, dict):
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
        if not isinstance(other, GraphqlQuery):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
