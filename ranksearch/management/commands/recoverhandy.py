from django.core.management.base import BaseCommand, CommandError
from ranksearch.models import Owner, Property, Fixer, Job
import re
import csv


def artifice(name):
    ret = {i: 1 for i in list(set(re.sub('[^a-z]', '', name.lower())))}
    return 5 * len(ret.keys()) / 26


class Command(BaseCommand):

    def handle(self, *args, **options):
        count = 0
        jobs = csv.reader(open('./initial_data/newreviews.csv', 'rt'))
        for job in jobs:
            count = count + 1
            if (count % 10 == 0):
                print("Done %s jobs" % count)
            (rating, fixer_image, end_date, text, owner_image,
            properties, fixer, owner, start_date) = job

            # Skip opening line, if present.
            if rating == 'rating':
                continue

            properties = properties.split('|')
            newowner, isnew = Owner.objects.get_or_create(name=owner)
            newowner.image_url = owner_image
            newowner.save()

            newjobproperties = []
            for propertyname in properties:
                newproperty, isnew = Property.objects.get_or_create(
                    owner=newowner, name=propertyname)
                newproperty.save()
                newjobproperties.append(newproperty)

            newfixer, isnew = Fixer.objects.get_or_create(name=fixer)
            newfixer.image_url = fixer_image
            newfixer.rating = artifice(fixer)
            newfixer.save()

            newjob = Job(
                fixer=newfixer,
                start_date=start_date,
                end_date=end_date,
                comment=text,
                rating=int(rating))
            newjob.save()

            for property in newjobproperties:
                newjob.properties.add(property)
                newjob.save()
