import json
import re

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
        tags_title = data['tags']

        note = Note(title=title, content=content)

        note.save()

        for tag_title in tags_title:
            try:
                tag = Tag.objects.get(title=tag_title)

                note.tags.add(tag)
            except Tag.DoesNotExist:
                tag = Tag(title=tag_title)

                tag.save()
                note.tags.add(tag)

        response = serializers.serialize('json', [note], fields=('title', 'content', 'tags'))

        return HttpResponse(response, content_type='application/json')
    elif request.method == 'UPDATE':
        data = json.loads(request.body)
        _id = data['id']
        tags_title = data['tags']

        note = Note.objects.get(id=_id)

        note.tags.set([])

        for tag_title in tags_title:
            try:
                tag = Tag.objects.get(title=tag_title)

                note.tags.add(tag)
            except Tag.DoesNotExist:
                tag = Tag(title=tag_title)

                tag.save()
                note.tags.add(tag)

        note.title = data['title']
        note.content = data['content']

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
        notes = Note.objects.filter(tags__id=tag.id)
        old_title = tag.title
        tag.title = data['title']

        tag.save()

        for note in notes:
            regex = rf'(?<=#){old_title}(?=[#\s]|$)'

            note.title = re.sub(regex, tag.title, note.title)

            note.save()

        return HttpResponse('Success!')
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        _id = data['id']
        tag = Tag.objects.get(id=_id)
        notes = Note.objects.filter(tags__id=tag.id)

        for note in notes:
            regex = rf'#{tag.title}\s*(?=[#\s]|$)'

            note.title = re.sub(regex, '', note.title)

            note.save()

        tag.delete()

        return HttpResponse('Success!')
    else:
        tags = Tag.objects.all()

        for tag in tags:
            notes = Note.objects.filter(tags__id=tag.id)
            
            if len(notes) < 1:
                tag.delete()

        tags = Tag.objects.all()

        return render(request, 'notes/tags.html', {
            'tags': tags
        })


def tag_view(request, tag):
    notes = Note.objects.filter(tags__title=tag)

    return render(request, 'notes/tag.html', {
        'notes': notes,
        'tag': tag
    })


def handler404(request, exception):
    response = render(request, 'notes/errors/404.html', {})

    response.status_code = 404

    return response
