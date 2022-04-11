import json

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.middleware import csrf
from .models import Tag, Note


def index_view(request):
    notes = Note.objects.all()

    csrf.get_token(request)

    return render(request, 'notes/index.html', {
        'notes': notes
    })


def notes_view(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        response = serializers.serialize('json', notes, fields=('title', 'content', 'tag'))

        return HttpResponse(response, content_type='application/json')
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        content = data['content']
        tag_title = data['tag']

        tag = None
        try:
            tag = Tag.objects.get(title=tag_title)
        except Tag.DoesNotExist:
            tag = Tag(title=tag_title)

            tag.save()

        note = Note(title=title, content=content, tag=tag)

        note.save()

        response = serializers.serialize('json', [note], fields=('title', 'content', 'tag'))

        return HttpResponse(response, content_type='application/json')
    elif request.method == 'UPDATE':
        data = json.loads(request.body)
        _id = data['id']
        tag_title = data['tag']

        note = Note.objects.get(id=_id)

        tag = None
        try:
            tag = Tag.objects.get(title=tag_title)
        except Tag.DoesNotExist:
            tag = Tag(title=tag_title)

            tag.save()

        note.title = data['title']
        note.content = data['content']
        note.tag = tag

        note.save()

        return HttpResponse('Success!')
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        _id = data['id']

        try:
            note = Note.objects.get(id=_id)

            note.delete()

            return HttpResponse('Success!')
        except Note.DoesNotExist:
            return HttpResponse('Note doesn\'t exist!', status='404')
    else:
        return HttpResponse(status='400')


def tags_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']

        tag = Tag(title=title)

        tag.save()

        response = serializers.serialize('json', [tag], fields=('title', 'content', 'tag'))

        return HttpResponse(response, content_type='application/json')
    elif request.method == 'UPDATE':
        data = json.loads(request.body)
        _id = data['id']

        tag = Tag.objects.get(id=_id)

        tag.title = data['title']

        tag.save()

        notes = Note.objects.all()

        for note in notes:
            if note.tag == tag:
                title = note.title[note.title.index(' '):]

                note.title = f'#{tag.title}{title}'

                note.save()

        return HttpResponse('Success!')
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        _id = data['id']

        try:
            tag = Tag.objects.get(id=_id)

            tag.delete()

            return HttpResponse('Success!')
        except Tag.DoesNotExist:
            return HttpResponse('Note doesn\'t exist!', status='404')
    else:
        tags = Tag.objects.all()
        notes = Note.objects.all()

        for tag in tags:
            if all([note.tag != tag for note in notes]):
                tag.delete()

        tags = Tag.objects.all()

        return render(request, 'notes/tags.html', {
            'tags': tags
        })


def tag_view(request, tag):
    notes = Note.objects.filter(tag__title=tag)

    return render(request, 'notes/tag.html', {
        'notes': notes,
        'tag': tag
    })
