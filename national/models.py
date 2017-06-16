# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.dispatch import dispatcher
from .decryption_tools import get_encrypted_votes, decrypt_vote

class Vote(models.Model):
    constituency = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    candidate_first_name = models.CharField(max_length=100)
    candidate_last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.constituency + ' - ' + self.party + ' - ' + self.candidate_last_name

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class PrivateKey(SingletonModel):
    key = models.TextField(blank=True, null=True)

class ConstituencyUrl(models.Model):
    url = models.URLField()



def decrypt_constituency_votes(sender, instance, created, *args, **kwargs):
    constit_url = instance.url
    private_key = PrivateKey.load().key
    if private_key != None:
        constit_response = get_encrypted_votes(constit_url)
        if constit_response['success']:
            encrypted_votes = constit_response['votes']
            for encrypted_vote in encrypted_votes:
                vote = decrypt_vote(encrypted_vote, private_key)

                constituency = vote['constituency']
                party = vote['party']
                candidate_first_name = vote['first_name']
                candidate_last_name = vote['last_name']

                if constituency and party and candidate_first_name and candidate_last_name:
                    vote_object = Vote(constituency=constituency,
                                       party=party,
                                       candidate_first_name=candidate_first_name,
                                       candidate_last_name=candidate_last_name)
                    vote_object.save()
                    print vote_object



models.signals.post_save.connect(decrypt_constituency_votes, sender=ConstituencyUrl)
