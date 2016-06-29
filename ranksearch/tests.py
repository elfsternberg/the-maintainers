from django.test import TestCase
from .models import Owner, Fixer, Property, Job
from random import randint


class CanSeeAll(TestCase):

    def setUp(self):
        owner, c = Owner.objects.get_or_create(name="Alice")
        owner.image_url = "http://localhost/"
        owner.save()

        property, c = Property.objects.get_or_create(
            name="Apartment #1", owner=owner)
        property.save()

        fixer, c = Fixer.objects.get_or_create(name="Carol")
        fixer.image_url = "http://localhost"
        fixer.rating = 3

        job = Job(
            fixer=fixer,
            start_date="2016-04-23",
            end_date="2016-04-26",
            comment="Lorem ipsum goes here",
            rating=4)
        job.save()

        job.properties.add(property)
        job.save()

    # A quick set of tests, just a walk through the database.
    # Asserts, at least, that given one owner, fixer, and property, we can
    # see every object in the system.

    def test_01_get_index(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_02_get_fixer(self):
        response = self.client.get('/search/')
        fixer = response.context['fixers'][0]
        response = self.client.get('/search/fixer/' + fixer.slug + '/')
        self.assertEqual(response.status_code, 200)

    def test_03_get_property(self):
        response = self.client.get('/search/')
        fixer = response.context['fixers'][0]
        response = self.client.get('/search/fixer/' + fixer.slug + '/')
        jobs = response.context['fixer'].jobs
        job = jobs.all()[0]
        property = job.properties.all()[0]
        response = self.client.get('/search/property/' + property.slug + '/')
        self.assertEqual(response.status_code, 200)

    def test_03_get_owner(self):
        response = self.client.get('/search/')
        fixer = response.context['fixers'][0]
        response = self.client.get('/search/fixer/' + fixer.slug + '/')
        jobs = response.context['fixer'].jobs
        job = jobs.all()[0]
        property = job.properties.all()[0]
        response = self.client.get('/search/property/' + property.slug + '/')
        owner = response.context['owner']
        response = self.client.get('/search/owner/' + owner.slug + '/')
        self.assertEqual(response.status_code, 200)
