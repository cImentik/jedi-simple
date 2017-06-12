from django.db import models
from django.core.mail import send_mail
from django.conf import settings

import hashlib


class Planet(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='name')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Planet'
        verbose_name_plural = 'Planets'


class Jedi(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    training_planet = models.ForeignKey(Planet, verbose_name='planet')

    def add_padawan(self, candidate):
        if self.candidate_set.count() < 3:
            candidate.is_padawan = True
            self.candidate_set.add(candidate)
            candidate.save()
            send_mail(
                    'Candidates notice', 'You are Padawan now.',
                    settings.FROM_EMAIL, [candidate.email]
            )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Jedi'
        verbose_name_plural = 'Jedies'


class Candidate(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    life_planet = models.ForeignKey(Planet, verbose_name='planet')
    age = models.PositiveIntegerField(verbose_name='age')
    email = models.EmailField(unique=True, verbose_name='e-mail')
    is_padawan = models.BooleanField(default=False, editable=False)
    padawans_room = models.ForeignKey(
        Jedi, blank=True, null=True, verbose_name='jedi')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'


class OrderCode(models.Model):
    code = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='order`s code'
    )

    def save(self, *args, **kwargs):
        if not self.code and not self.pk:
            super(OrderCode, self).save(*args, **kwargs)
            self.code = hashlib.sha256(str(self.pk).encode('utf-8')).hexdigest()
        super(OrderCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Question(models.Model):
    code = models.ForeignKey(OrderCode)
    content = models.CharField(max_length=255, verbose_name='content')

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('content',)
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Exam(models.Model):
    candidate = models.ForeignKey(Candidate, verbose_name='candidate')
    question = models.ForeignKey(Question, verbose_name='question')
    answer = models.NullBooleanField(verbose_name='question')

    def __str__(self):
        return self.question.content + ' ' + str(self.answer)

    class Meta:
        ordering = ('candidate',)
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
