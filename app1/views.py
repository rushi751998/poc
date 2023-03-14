from django.shortcuts import render, HttpResponse, redirect
from .forms import Video_form
from .models import Video2
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
    if request.method == "POST":
        dates = Video2.objects.values_list('caption',flat=True)
        global date
        date = request.POST.get('date')
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        
        if date_time_obj.date() in dates:
            global filterd_videos
            filterd_videos = Video2.objects.filter(caption=date)
            return render(request, 'videos1.html', {"all": filterd_videos, "date": date})
        
    return render(request,'index.html')
    # return render(request, 'videos1.html', {"all": all_video})
    


def videos2(request):
    # time.sleep(10)
    return render(request, 'videos2.html', {"all": filterd_videos, "date": date})


def get_param(data):
    data.columns = data.columns.str.replace(" ","_")
    gender = data['Gender'].unique()
    gender_values = data.groupby('Gender').count()['Age'].values

    activity = data.groupby('Suspecious').sum()['Customer_ID']
    age=data.groupby('Age').count()['Customer_ID']
    race  = data.groupby('Race').sum()['Customer_ID']
    emotion = data.groupby('Emotion').count()['Customer_ID']


    # it will geive data frame to html
    json_records = data.reset_index().to_json(orient='records')
    data_html = json.loads(json_records)
    col_name = data.columns


    param = {'col_name': col_name,
    "data_html": data_html,
    "emotions_lables": list(emotion.index), 'emotions_values': list(emotion.values),
    'gender': gender, 'gender_values': gender_values,
    'activity_lable': list(activity.index), 'activity_values': list(activity.values), 
    'age_id_index' : list(age.index),'age_id_values' : list(age.values),
    'race_id_index' :list(race.index),  'race_id_values':list(race.values)}
    
    return param

def dashboard(request):
    data = None
    if date == "2023-03-01":
        data = pd.read_csv('data/processed1.csv')
    
    elif date == "2023-03-02":
        data = pd.read_csv('data/processed3.csv')
        
    elif date == "2023-03-03":
        data = pd.read_csv('data/processed4.csv')
    
    elif date == "2023-03-04":
        data = pd.read_csv('data/processed5.csv')
        
    else:
        pass
        
        
    return render(request, 'dashboard_filter.html', get_param(data))



def get_data_kpi():
    data = pd.read_csv('data/kpi_datas.csv')
    data.columns = data.columns.str.replace(" ","_")
    return data

def kpi_dashboard(request):

    # time.sleep(3)
    return render(request, 'kpi_dashboard/kpi_dashboard.html')

def operation(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        footfall = get_data_kpi()['Total_footfall'].values
        date = get_data_kpi()['date'].values
        transactions=get_data_kpi()['transactions'].values
    
        parms = {'kpi':'Operational', "foot_fall":footfall,'date':date,'n_transactions':transactions}
        return render(request, 'kpi_dashboard/operation.html',parms)
    return render(request, 'kpi_dashboard/error.html')
    
    

def customer_service(request):
    if request.method == "POST":
        global time
        time = request.POST.get('time')
        
        parms = {'kpi':'customer service', 'time':time}
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

    