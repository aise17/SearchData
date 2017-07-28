# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models






# Create your models here.

class Client(models.Model):
	name = models.CharField(max_length = 100, null= True)
	company = models.CharField(max_length = 100, null= True)
	passwoerd = models.CharField(max_length = 100, null= True)
	mail = models.EmailField()
	n_targeta = models.PositiveIntegerField()
	n_secret = models.PositiveSmallIntegerField()
	contact_number = models.PositiveIntegerField()


	def __unicode__(self):
		return self.name



class Engine (models.Model):
	name = models.CharField(max_length = 100, null= True)
	client = models.ForeignKey(Client, on_delete = models.CASCADE)
	start_date = models.DateField(auto_now = True, editable = False)

	def __unicode__(self):
		return self.name


class FileQuery(models.Model):
	name = models.CharField(max_length = 100)
	engine = models.ForeignKey(Engine, on_delete = models.CASCADE)
	file_style = models.CharField(max_length = 100)
	file = models.FileField(upload_to = 'Query_csv/' )



	def __unicode__(self):
		return self.name



class FileResults(models.Model):
	name = models.CharField(max_length = 100)
	engine = models.ForeignKey(Engine, on_delete = models.CASCADE)
	file_style = models.CharField(max_length = 100)
	file = models.FileField(upload_to= 'Results_csv/%Y/%m')

	def __unicode__(self):
		return self.name