from django.db import models


class Question(models.Model):
    NEW = 'New'
    ACTIVE = 'Active'
    ENDED = 'Ended'
    STATE = (
        (NEW, 'Новый'),
        (ACTIVE, 'Активный'),
        (ENDED, 'Конечный'),
    )
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    state = models.CharField(max_length=6, choices=STATE, default=NEW)
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text



STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)

class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):              # __unicode__ on Python 2
        return self.title