from django.forms import ModelForm
from webInfo.models import Engine, Client, FileResults, FileQuery
from django.contrib.auth.models import User



class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        

class EngineForm(ModelForm):
    class Meta:
        model = Engine
        fields = '__all__'
        

class FileQueryForm(ModelForm):
    class Meta:
        model = FileQuery
        fields = '__all__'
        

class FileResultsForm(ModelForm):
    class Meta:
        model = FileResults
        fields = '__all__'
        

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields= 'username', 'password'

