from django.core.paginator import Paginator
from django.template import Template, Context
from django.test import TestCase


class TemplateTagTests(TestCase):

    def test_pagenav_tag(self):
        """Pagenav tag returns page navigation widget"""
        # prepare paginator
        paginator = Paginator([1, 2, 3, 4], 1)
        my_list = paginator.page('1')

        # render template with pagenav tag
        out = Template(
            "{% load pagenav %}"
            "{% pagenav object_list is_paginated paginator %}"
        ).render(Context({'object_list': my_list, 'is_paginated': True,
                          'paginator': paginator}))

        # paginator should create 4 pages
        self.assertIn('<nav aria-label="Page navigation">', out)
        self.assertIn('<a class="page-link" href="?page=1">1</a>', out)
        self.assertIn('<a class="page-link" href="?page=2">2</a>', out)
        self.assertIn('<a class="page-link" href="?page=3">3</a>', out)
        self.assertIn('<a class="page-link" href="?page=4">4</a>', out)

    def test_str2int(self):
        """Test str2int template filter"""
        out = Template(
            "{% load str2int %}"
            "{% if 36 == '36'|str2int %}"
            "it works"
            "{% endif  %}"
        ).render(Context({}))

        # check for our addition operation result
        self.assertIn("it works", out)
