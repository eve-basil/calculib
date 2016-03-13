from __future__ import absolute_import
from hamcrest.library import *
from hamcrest.core import *
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher as wrap_shortcut
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription


def with_return(func, match):
    class FunctionWithValue(BaseMatcher):
        def __init__(self, func, value_matcher):
            self.func = func
            self.value_matcher = value_matcher

        def _matches(self, item):
            value = func()
            return self.value_matcher.matches(value)

        def describe_to(self, description):
            description.append_text("an object with a property '")\
                .append_text(self.property_name) \
                .append_text("' matching ") \
                .append_description_of(self.value_matcher)

    return FunctionWithValue(func, wrap_shortcut(match))


def nearly(obj):
    class Nearly(BaseMatcher):
        def __init__(self, nearly):
            self.nearly = nearly
            self._other = None

        def _matches(self, item):
            self._other = item
            return item - self.nearly < 0.00000000000001

        def describe_to(self, description):
            nested_matcher = isinstance(self.nearly, Matcher)
            if nested_matcher:
                description.append_text('<')
            description.append_description_of(self.nearly)
            description.append_text(' delta= ')
            description.append_description_of(abs(self._other - self.nearly))
            if nested_matcher:
                description.append_text('>')

    return Nearly(obj)


def has_method(name, match=None):
    class IsObjectWithMethod(BaseMatcher):

        def __init__(self, method_name, value_matcher):
            self.method_name = method_name
            self.value_matcher = value_matcher

        def _matches(self, o):
            if o is None:
                return False

            if not hasattr(o, self.method_name):
                return False

            method = getattr(o, self.method_name)
            value = method()
            return self.value_matcher.matches(value)

        def describe_to(self, description):
            description.append_text("an object with a method '") \
                                            .append_text(self.method_name) \
                                            .append_text("' matching ") \
                                            .append_description_of(self.value_matcher)

        def describe_mismatch(self, item, mismatch_description):
            if item is None:
                mismatch_description.append_text('was None')
                return

            if not hasattr(item, self.method_name):
                mismatch_description.append_value(item) \
                                                        .append_text(' did not have the ') \
                                                        .append_value(self.method_name) \
                                                        .append_text(' method')
                return

            mismatch_description.append_text('method ').append_value(self.method_name).append_text(' ')
            method = getattr(item, self.method_name)
            value = method()
            self.value_matcher.describe_mismatch(value(), mismatch_description)

        def __str__(self):
            d = StringDescription()
            self.describe_to(d)
            return str(d)

    if match is None:
        match = anything()

    return IsObjectWithMethod(name, wrap_shortcut(match))
