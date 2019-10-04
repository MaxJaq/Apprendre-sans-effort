from django.contrib import admin
from .models import (
    Test_end_session,
    Pass_test_end_session,
    Test_mcq_end_session,
    Pass_test_mcq_end_session,
    Test,
    Question,
    Choice,
    )

# Register your models here.
admin.site.register(Test_end_session)
admin.site.register(Pass_test_end_session)
admin.site.register(Test_mcq_end_session)
admin.site.register(Pass_test_mcq_end_session)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)

