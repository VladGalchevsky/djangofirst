from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from students.models import Group, Student


class TestStudentList(TestCase):

    def setUp(self):
        # create 2 groups
        group1, created = Group.objects.get_or_create(title="MtM-1")
        group2, created = Group.objects.get_or_create(title="MtM-2")

        # create 4 students: 1 for group1 and 3 for group2
        Student.objects.get_or_create(
            first_name="Vitaliy",
            last_name="Podoba",
            birthday=datetime.today(),
            ticket='12345',
            student_group=group1)
        Student.objects.get_or_create(
            first_name="Dmytro",
            last_name="Litvinov",
            birthday=datetime.today(),
            ticket='23456',
            student_group=group2)
        Student.objects.get_or_create(
            first_name="Sam",
            last_name="Stefenson",
            birthday=datetime.today(),
            ticket='34567',
            student_group=group2)
        Student.objects.get_or_create(
            first_name="Arnold",
            last_name="Kidney",
            birthday=datetime.today(),
            ticket='45678',
            student_group=group2)

        # remember url to our homepage
        self.url = reverse('home')

    def test_students_list(self):
        # make request to the server to get homepage page
        response = self.client.get(self.url)

        # have we received OK status from the server?
        self.assertEqual(response.status_code, 200)

        # do we have student name on a page?
        self.assertContains(response, 'Vitaliy')

        # do we have link to student edit form?
        student_id = Student.objects.first().id
        student_edit_link = reverse('students_edit', kwargs={'pk': student_id})
        self.assertContains(response, student_edit_link)

        # ensure we got 3 students, pagination limit is 3
        self.assertEqual(len(response.context['students']), 3)

    def test_current_group(self):
        # set group1 as currently selected group
        group = Group.objects.get(title="MtM-1")
        self.client.cookies['current_group'] = group.id

        # make request to the server to get homepage page
        response = self.client.get(self.url)

        # in group1 we have only 1 student
        self.assertEqual(len(response.context['students']), 1)

    def test_order_by(self):
        # set order by Last Name
        response = self.client.get(self.url, {'order_by': 'last_name'})

        # now check if we got proper order
        students = response.context['students']
        self.assertEqual(students[0].last_name, 'Kidney')
        self.assertEqual(students[1].last_name, 'Litvinov')
        self.assertEqual(students[2].last_name, 'Podoba')

    def test_reverse_order_by(self):
        # order students by ticket number in reverse order
        response = self.client.get(self.url, {'order_by': 'ticket',
                                              'reverse': '1'})

        # now check if we got proper order
        students = response.context['students']
        self.assertEqual(students[0].last_name, 'Kidney')
        self.assertEqual(students[1].last_name, 'Stefenson')
        self.assertEqual(students[2].last_name, 'Litvinov')

    def test_pagination(self):
        # navigate to second page with students
        response = self.client.get(self.url, {'page': '2'})

        self.assertEqual(response.context['is_paginated'], True)
        self.assertEqual(len(response.context['students']), 1)
        self.assertEqual(response.context['students'][0].last_name, 'Kidney')
