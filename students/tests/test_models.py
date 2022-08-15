from django.test import TestCase

from ..models import Student


class StudentModelTests(TestCase):
    """Test student model"""

    def test_str(self):
        student = Student(first_name='Demo', last_name='Student')
        self.assertEqual(str(student), 'Demo Student')
