from django.test import TestCase, override_settings
from django.urls import reverse

from students.models import Group, Student


@override_settings(LANGUAGE_CODE='en')
class TestStudentUpdateForm(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember url to edit form
        self.url = reverse('students_edit', kwargs={'pk': 1})

    def test_form(self):
        # login as admin to access student edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)

        # check response status
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertContains(response, 'Edit Student')
        self.assertContains(response, 'Ticket')
        self.assertContains(response, 'Last Name')
        self.assertContains(response, 'name="add_button"')
        self.assertContains(response, 'name="cancel_button"')
        self.assertContains(response, 'action="%s"' % self.url)
        self.assertContains(response, 'podoba.jpg')

    def test_success(self):
        # login as admin to access student edit form
        self.client.login(username='admin', password='admin')

        # post form with valid data
        group = Group.objects.get(title='Group2')
        post_data = {
            'first_name': 'Updated Name',
            'last_name': 'Updated Last Name',
            'ticket': '567',
            'student_group': group.id,
            'birthday': '1990-11-11'
        }
        response = self.client.post(self.url, post_data, follow=True)

        # check response status
        self.assertEqual(response.status_code, 200)

        # test updated student details
        student = Student.objects.get(pk=1)
        self.assertEqual(student.first_name, 'Updated Name')
        self.assertEqual(student.last_name, 'Updated Last Name')
        self.assertEqual(student.ticket, '567')
        self.assertEqual(student.student_group, group)

        # check proper redirect after form post
        self.assertContains(response, 'Student updated successfully')
        self.assertEqual(response.redirect_chain[0][0],
                         '/?status_message=Student%20updated%20successfully!')

    def test_access(self):
        # try to access form as anonymous user
        response = self.client.get(self.url, follow=True)

        # we have to get 200 code and login form
        self.assertEqual(response.status_code, 200)

        # check that we're on login form
        self.assertContains(response, 'Login Form')

        # check redirect url
        self.assertEqual(response.redirect_chain[0],
                         ('/accounts/login/?next=/students/1/edit/', 302))
