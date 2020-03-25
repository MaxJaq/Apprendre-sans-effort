from django.contrib import admin
from .models import (
	DynMCQInfo,
	DynMCQquestion,
	DynMCQanswer,
	Pass_DynMCQTest,
	Pass_DynMCQTest_Info,
	Dynquestion,
	Pass_DynquestionTest,
    )

# Register your models here.
admin.site.register(DynMCQInfo)
admin.site.register(DynMCQquestion)
admin.site.register(DynMCQanswer)
admin.site.register(Pass_DynMCQTest)
admin.site.register(Pass_DynMCQTest_Info)
admin.site.register(Dynquestion)
admin.site.register(Pass_DynquestionTest)

