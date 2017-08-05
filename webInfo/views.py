# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate
from django.shortcuts import render
from webInfo.models import Engine, Client, FileQuery, FileResults
from webInfo.forms import ClientForm, EngineForm, FileQueryForm, FileResultsForm, LoginForm
from django.http import HttpResponseRedirect, HttpResponse


from django.shortcuts import redirect, get_object_or_404
from django.contrib import auth


from django.contrib.auth.decorators import login_required

from django.db.models import Count
import random 
import json
# Create your views here.
'''TASK

'''





@login_required(login_url='/')
def engine_list(request):
	engines = Engine.objects.all()
	context = {'engines': engines}
	return render(request, 'engine_list.html', context)

@login_required(login_url='/')
def cliet_list(request):
	clients = Client.objects.all()
	context = {'clients': clients}
	return render(request, 'client_list.html', context)

@login_required(login_url='/')
def file_query_list(request):
	file_queries = FileQuery.objects.all()
	context = {'file_queries': file_queries}
	return render(request, 'file_query_list.html', context)
	print 'carga completa'

@login_required(login_url='/')
def file_results_list(request):
	file_results = FileResults.objects.all()
	context = {'file_results': file_results}
	return render(request, 'file_results_list.html', context)







def engine_detail(request, pk):
	engine_detail = Engine.objects.get(pk=pk)
	context = {'engine_detail': engine_detail}
	return render(request, 'engine_detail.html', context)


def client_detail(request, pk):
	client_detail = Client.objects.get(pk=pk)
	context = {'client_detail': client_detail}
	return render(request, 'client_detail.html', context)


def filequery_detail(request, pk):
	filequery_detail = FileQuery.objects.get(pk=pk)
	context = {'filequery_detail': filequery_detail}
	return render(request, 'filequery_detail.html', context)


def fileresult_detail(request, pk):
	fileresult_detail = FileResults.objects.get(pk=pk)
	context = {'fileresult_detail': fileresult_detail}
	return render(request, 'fileresult_detail.html', context)


def delete_client(request, pk):
	user = Client.objects.get(pk=pk)
	user.delete()
	return HttpResponseRedirect('/client')


def delete_engine(request, pk):
	engine = Engine.objects.get(pk=pk)
	engine.delete()
	return HttpResponseRedirect('/engine')


def delete_filequery(request, pk):
	file_query = FileQuery.objects.get(pk=pk)
	file_query.delete()

	return HttpResponseRedirect('/file_query')


def delete_fileresult(request, pk):
	file_results = FileResults.objects.get(pk=pk)
	file_results.delete()
	return HttpResponseRedirect('/file_result')


def get_client(request):
	if request.method == "POST":
		form = ClientForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/client')

	else:
		form = ClientForm()

	return render(request, 'login.html', {'form': form})


def superuser(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/client')

	else:
		form = LoginForm()

	return render(request, 'login.html', {'form': form})


def get_engine(request):
	if request.method == "POST":
		form = EngineForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/engine')

	else:
		form = EngineForm()

	return render(request, 'login.html', {'form': form})


def get_file_query(request):
	if request.method == 'POST':
		form = FileQueryForm(request.POST, request.FILES)
		if form.is_valid():

			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/file_query')
	else:
		form = FileQueryForm()

	return render(request, 'login.html', {'form': form})


def get_file_result(request):
	if request.method == 'POST':
		form = FileResultsForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/file_results')
	else:
		form = FileResultsForm()

	return render(request, 'login.html', {'form': form})









def edit_engine(request, pk):
	engine = get_object_or_404(Engine, pk=pk)
	if request.method == "POST":
		form = EngineForm(request.POST, instance=engine)
		if form.is_valid():
			engine = form.save(commit=False)
			engine.save()
			return redirect('/engine')
	else:
		form = EngineForm(instance=engine)
	return render(request, 'login.html', {'form': form})


def edit_client(request, pk):
	client = get_object_or_404(Client, pk=pk)
	if request.method == "POST":
		form = ClientForm(request.POST, instance=client)
		if form.is_valid():
			client = form.save(commit=False)
			client.save()
			return redirect('/client')
	else:
		form = ClientForm(instance=client)
	return render(request, 'login.html', {'form': form})


def edit_filequery(request, pk):
	file_query = get_object_or_404(FileQuery, pk=pk)
	if request.method == "POST":
		form = FileQueryForm(request.POST, instance=file_query)
		if form.is_valid():
			file_query = form.save(commit=False)
			file_query.save()
			return redirect('/file_query')
	else:
		form = FileQueryForm(instance=file_query)
	return render(request, 'login.html', {'form': form})



def login(request):
	menssage = None
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			name, password= Client.objects.all()
			name = request.POST['name']
			password = request.POST['password']
			user =authenticate(username=name, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					menssage = 'Identificaciòn correcta'
					return redirect('/engine')
				else:
					menssage = 'Tu usuario esta inactivo'
					return redirect('/client')
			else:
				menssage = 'nombre y/o password incorrectos'
				return redirect('/file_query')
	else:
		form = LoginForm()
	return render(request, 'login.html', {'menssage': menssage, 'form': form})




def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")









def grph_client(request, pk):
	user = Client.objects.get(pk = pk)
	data = []
	name = user.name
	r = lambda: random.randint(0,255)

	engine_list = user.engine_set.all()
	num_engine = 0
	for engine in engine_list:
		num_engine += 1


		file_query_list = engine.filequery_set.all()
		num_file_query = 0
		for filequery in file_query_list:
			num_file_query += 1

		file_results_list = engine.fileresults_set.all()
		num_file_results = 0
		for fileresults in file_results_list:
			num_file_results += 1

		data.append({'name': name, 'n_engine': num_engine,'n_filequery': num_file_query ,'n_fileresults': num_file_results ,'color': '#%02X%02X%02X' % (r(),r(),r())})			

	return HttpResponse(json.dumps(data), content_type='application/json; utf-8')