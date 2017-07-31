# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import render
from webInfo.models import Engine, Client, FileQuery, FileResults
from webInfo.forms import ClientForm, EngineForm, FileQueryForm, FileResultsForm
from django.http import HttpResponseRedirect


from django.shortcuts import redirect, get_object_or_404

# Create your views here.
'''TASK
-REGISTRO
-VISTA DETALLE USUARIO
-DESCARGA DE CSV 
-VISTA DETALLE
-VISTA EDITAR
'''

	

def engine_list(request):
	engines = Engine.objects.all()
	context = {'engines': engines}
	return render(request, 'engine_list.html', context)

def cliet_list(request):
	clients = Client.objects.all()
	context = {'clients': clients}
	return render(request, 'client_list.html', context)

def file_query_list(request):
	file_queries = FileQuery.objects.all()
	context = {'file_queries': file_queries}
	return render(request, 'file_query_list.html', context)
	print 'carga completa'

def file_results_list(request):
	file_results = FileResults.objects.all()
	context = {'file_results': file_results}
	return render(request, 'file_results_list.html', context)








def engine_detail(request, pk):
	engine_detail = Engine.objects.get(pk =pk)
	context = {'engine_detail': engine_detail}
	return render(request, 'engine_detail.html', context)

def client_detail(request, pk):
	client_detail = Client.objects.get(pk = pk)
	context = {'client_detail': client_detail}
	return render(request, 'client_detail.html', context)

def filequery_detail(request, pk):
	filequery_detail = FileQuery.objects.get(pk =pk)
	context = {'filequery_detail': filequery_detail}
	return render(request, 'filequery_detail.html',context)

def fileresult_detail(request, pk):
	fileresult_detail = FileResults.objects.get(pk = pk)
	context= {'fileresult_detail': fileresult_detail}
	return render(request, 'fileresult_detail.html', context)






def delete_client(request, pk):
	user = Client.objects.get(pk = pk)
	user.delete()
	return HttpResponseRedirect('/client')

def delete_engine(request, pk):
	engine = Engine.objects.get(pk = pk)
	engine.delete()
	return HttpResponseRedirect('/engine')
def delete_filequery(request, pk):
	file_query = FileQuery.objects.get(pk =pk)
	file_query.delete()

	return HttpResponseRedirect('/file_query')
def delete_fileresult(request, pk):
	file_results = FileResults.objects.get(pk = pk)
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

	return render(request, 'engine_form.html', {'form': form})

def get_engine(request):
	if request.method == "POST":
		form = EngineForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/engine')
			
	else:
		form = EngineForm()

	return render(request, 'engine_form.html', {'form': form})


def get_file_query(request):
	if request.method == 'POST':
		form = FileQueryForm(request.POST, request.FILES)
		if form.is_valid():

			instance = form.save(commit=False)
			instance.save()
			return HttpResponseRedirect('/file_query')
	else:
		form = FileQueryForm()


	return render(request, 'engine_form.html', {'form': form})

def get_file_result(request):
	if request.method == 'POST':
		form = FileResultsForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/file_results')
	else:
		form = FileResultsForm()

	return render(request, 'engine_form.html', {'form': form})











def edit_engine(request, pk):
	engine = get_object_or_404(Engine, pk=pk)
	if request.method == "POST":
		form = EngineForm(request.POST, instance=engine)
		if form.is_valid():
			engine = form.save(commit=False)
			engine.save()
			return redirect('engine_detail.html', pk=engine.pk)
	else:
		form = EngineForm(instance=engine)
	return render(request, 'engine_form.html', {'form': form})



def edit_client(request, pk):
	client = get_object_or_404(Client, pk=pk)
	if request.method == "POST":
		form = ClientForm(request.POST, instance=client)
		if form.is_valid():
			client = form.save(commit=False)
			client.save()
			return redirect('engine_detail.html', pk=client.pk)
	else:
		form = ClientForm(instance=client)
	return render(request, 'engine_form.html', {'form': form})



def edit_filequery(request, pk):
	file_query = get_object_or_404(FileQuery, pk=pk)
	if request.method == "POST":
		form = FileQueryForm(request.POST, instance=file_query)
		if form.is_valid():
			file_query = form.save(commit=False)
			file_query.save()
			return redirect('engine_detail.html', pk=file_query.pk)
	else:
		form = FileQueryForm(instance=file_query)
	return render(request, 'engine_form.html', {'form': form})

