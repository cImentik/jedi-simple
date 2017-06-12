from django.contrib import admin

from .models import Planet
from .models import Jedi, Candidate

from .models import Question, OrderCode, Exam


admin.site.register(Planet)


@admin.register(Jedi)
class JediAdmin(admin.ModelAdmin):
    pass


class Questions(admin.StackedInline):
    model = Question
    max_num = 3


@admin.register(OrderCode)
class OrderCodeAdmin(admin.ModelAdmin):
    inlines = [Questions]
    readonly_fields = ('code',)


class Exams(admin.StackedInline):
    model = Exam
    extra = 0


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    inlines = [Exams]