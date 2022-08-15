from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class CountStudentsTest(TestCase):
    """Test countstudents command"""

    fixtures = ['students_test_data.json']

    def test_command_output(self):
        # prepare output file for command
        out = StringIO()

        # call our command
        call_command('countstudents', 'student', 'group', 'user', stdout=out)

        # get command output
        result = out.getvalue()

        # check if we get proper number of objects in database
        self.assertIn('students in database: 4', result)
        self.assertIn('groups in database: 2', result)
        self.assertIn('users in database: 1', result)
