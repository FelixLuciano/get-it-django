from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=32)

    def __str__ (self):
        return self.title


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__ (self):
        return f"[{ self.tag }] {self.title}"
