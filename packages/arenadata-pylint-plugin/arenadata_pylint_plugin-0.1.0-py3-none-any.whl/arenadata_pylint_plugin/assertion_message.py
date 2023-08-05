# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Assertion message checker implementation"""

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class AssertMessageChecker(BaseChecker):
    """Checker to ensure assertion message is provided"""

    __implements__ = IAstroidChecker

    NO_MESSAGE = "missing-assertion-message"

    name = "assertion-message"
    priority = -1
    msgs = {
        "W7701": (
            "Assertion message is empty or not provided",
            NO_MESSAGE,
            "Each assert should have readable assertion message",
        ),
    }

    def visit_assert(self, node: nodes.Assert):
        """Check if assert message is provided and not an empty string"""
        if node.fail and (not isinstance(node.fail, nodes.Const) or node.fail.value):
            return

        self.add_message(self.NO_MESSAGE, node=node)


def register(linter):
    """Register plugin to linter"""
    linter.register_checker(AssertMessageChecker(linter))
