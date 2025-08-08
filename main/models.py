from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Nominee(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='nominee-images/')
    description = models.TextField(blank=True, null=True)
    telegram = models.CharField(max_length=25)

    class Meta:
        db_table = 'nominee'
        verbose_name_plural = 'Nominees'

    def __str__(self):
        return self.name

class Award(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=50)
    icon = models.ImageField(upload_to='award-icons/')
    slug = models.SlugField(unique=True)
    awardImage = models.ImageField(upload_to='award-images/', blank=True, null=True)
    nominees = models.ManyToManyField(Nominee, related_name='awards')
    is_major = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'award'
        verbose_name_plural = 'Awards'

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nominee = models.ForeignKey(Nominee, on_delete=models.CASCADE, related_name='votes')
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'award'),)
        db_table = 'vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        return f'{self.user} voted for {self.nominee} in {self.award}'

class Winner(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='winners')
    nominee = models.CharField(max_length=30)
    image = models.ImageField(upload_to='winners-images/')


    class Meta:
        db_table = 'winner'
        verbose_name_plural = 'Winners'

    def __str__(self):
        return f'{self.nominee} winner in {self.award.name}'