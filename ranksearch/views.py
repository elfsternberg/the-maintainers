from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from .models import Fixer, Owner, Property


def index(request):
    fixers = Fixer.objects.all().order_by('score__rank')
    context = {'fixers': fixers}
    return render(request, 'ranksearch/index.html', context)


def fixer(request, slug):
    object = get_object_or_404(Fixer, slug=slug)
    return render(request, 'ranksearch/fixer.html',
                  {'fixer': object,
                   'jobs': object.jobs.order_by('start_date')})


def owner(request, slug):
    object = get_object_or_404(Owner, slug=slug)
    return render(request, 'ranksearch/owner.html',
                  {'owner': object,
                   'properties': object.properties.all()})


def property(request, slug):
    object = get_object_or_404(Property, slug=slug)
    return render(request, 'ranksearch/property.html',
                  {'property': object,
                   'properties': object.owner.properties.all().exclude(pk=object.pk),
                   'owner': object.owner})
