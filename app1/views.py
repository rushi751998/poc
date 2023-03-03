from django.shortcuts import render, HttpResponse, redirect
from .forms import Video_form
from .models import Video
import datetime
import pandas as pd
import json
import time

# def index(request):
#     all_video=Video.objects.all()
#     if request.method == "POST":
#         form=Video_form(data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return render(request,'index.html')
#     else:
#         form=Video_form()
#         return render(request,'index.html',{"form":form})



def index(request):
    return render(request, 'index.html')


def videos(request):
    # time.sleep(2) 
    
    all_video = Video.objects.all()
    if request.method == "POST":
        dates = ['2023-02-01','2023-02-02','2023-02-03','2023-02-04',]
        global date
        date = request.POST.get('date')
        print((date))
        if date in dates:
            return render(request, 'videos1.html', {"all": all_video, "date": date})
    return render(request,'index.html')
    # return render(request, 'videos1.html', {"all": all_video})
    


def videos2(request):
    # time.sleep(10)
    
    all_video = Video.objects.all()

    return render(request, 'videos2.html', {"all": all_video, "date": date})



    
data = pd.read_csv('processed.csv')
data.columns = data.columns.str.replace(" ","_")
data['Suspecious'].replace(0,"Non_Suspecious")
data['Suspecious'].replace(1,"Suspecious")
# print(data['Suspecious'])




    
    
emotions_lables = data['Emotion'].unique()
emotions_values = data.groupby('Emotion').count()['Age'].values

gender = data['Gender'].unique()
gender_values = data.groupby('Gender').count()['Age'].values

activity = data['Suspecious'].unique()
activity_values = data.groupby('Suspecious').count()['Emotion'].values
    


# it will geive data frame to html
json_records = data.reset_index().to_json(orient='records')
data_html = json.loads(json_records)
col_name = data.columns


# param = {'all':range(4),"chart_fields":df}
param = {'col_name': col_name,
            "data_html": data_html,
            'all': range(4),
            "emotions_lables": emotions_lables, 'emotions_values': emotions_values,
            'gender': gender, 'gender_values': gender_values,
            'activity': activity, 'activity_values': activity_values,       
            }


def dashboard(request):
    # time.sleep(3) 
    
    return render(request, 'dashboard_filter.html', param)


def graph(request):
    # time.sleep(3) 
    if request.method =="POST":
        temp = request.POST.getlist('form_inputs')  
        dict_ = {
            "1":'Suspecious',
            "0":'Suspecious',
            "Man":'Gender',
            "Women":'Gender',
            "neutral":'Emotion',
            "fear":'Emotion',
        }
    
        df_col=data[[dict_[i] for i in temp]]
        print(temp)
        
        print(df_col) 

    return render(request, 'charts.html', param )



def kpi_dashboard(request):

    # time.sleep(3)
    return render(request, 'kpi_dashboard/kpi_dashboard.html')

def operation(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        
        parms = { 'time':time}
        return render(request, 'kpi_dashboard/operation.html',parms)
    return render(request, 'kpi_dashboard/error.html')
    
    

def customer_service(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        
        parms = { 'time':time}
        return render(request, 'kpi_dashboard/customer_service.html',parms)
    return render(request, 'kpi_dashboard/error.html')

    

def primer_customer(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        
        parms = { 'time':time}
        return render(request, 'kpi_dashboard/primer_customer.html',parms)
    return render(request, 'kpi_dashboard/error.html')
    

    

def security(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        
        parms = { 'time':time}
        return render(request, 'kpi_dashboard/security.html',parms)
    return render(request, 'kpi_dashboard/error.html')

    