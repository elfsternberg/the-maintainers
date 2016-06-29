from django.db import models
from django.db.models import Count, Sum
from autoslug.fields import AutoSlugField


class Owner(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            verbose_name="Owner's name")
    slug = AutoSlugField(populate_from='name', max_length=32, unique=True)
    image_url = models.URLField(unique=False, max_length=255, blank=True)

    def __str__(self):
        return '%s' % (self.name)


class Property(models.Model):
    owner = models.ForeignKey(Owner, related_name="properties",
                              verbose_name="Property")
    name = models.CharField(max_length=250, blank=False)
    slug = AutoSlugField(populate_from='name', max_length=32, unique=True)
    image_url = models.URLField(unique=False, max_length=255, blank=True)

    class Meta:
        unique_together = ("name", "owner")

    def __str__(self):
        return '%s' % (self.name)


class Fixer(models.Model):
    name = models.CharField(
        max_length=250, blank=False,
        verbose_name="Fixer's name")
    slug = AutoSlugField(populate_from='name', max_length=32, unique=True)
    image_url = models.URLField(unique=False, max_length=255, blank=True)
    rating = models.DecimalField(
        default=0,
        max_digits=3,
        decimal_places=2,
        verbose_name="Fixer's initial rating")

    def __str__(self):
        return '%s' % (self.name)


class FixerRank(models.Model):
    fixer = models.OneToOneField(Fixer, related_name="score")
    rank = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        score = self.fixer.jobs.aggregate(Sum('rating'))
        jobs = self.fixer.jobs.count()
        self.rank = float(self.fixer.rating) + (score['rating__sum'] / 10.0)
        if jobs >= 10:
            rank = score['rating__sum'] / jobs
        return super(FixerRank, self).save(*args, **kwargs)


class Job(models.Model):
    fixer = models.ForeignKey(Fixer, related_name="jobs")
    properties = models.ManyToManyField(Property, related_name="jobs")
    comment = models.TextField(default="")
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=True)
    rating = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '%s sat %s for %s' % (self.fixer.name, self.propertylist,
                                     self.properties.all()[0].owner.name)

    @property
    def propertylist(self):
        return ', '.join([a.name for a in self.properties.all()])

    def save(self, *args, **kwargs):
        job = super(Job, self).save(*args, **kwargs)
        score, c = FixerRank.objects.get_or_create(fixer=self.fixer)
        score.save()
        return job

    def delete(self, *args, **kwargs):
        job = super(Job, self).delete(*args, **kwargs)
        score = job.fixer.score
        score.save()
        return job
