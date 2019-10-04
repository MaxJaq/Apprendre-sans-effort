from django.test import TestCase
from .models import Pass_test_end_session

# Create your tests here.

class DumbModelTests(TestCase):

    def test_dumb_class(self):
        """
        test that id_student can not be 'admin'
        """
        Pass_test_id_student_admin = Pass_test_end_session(id_student='admin')
        self.assertIs(Pass_test_id_student_admin.test_dumb_id_student_not_admin(), False)
