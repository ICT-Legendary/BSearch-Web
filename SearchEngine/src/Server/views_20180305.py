# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser
from django.contrib import auth

from models import DirectoryInfo, FileInfo
from forms import addDirectoryForm
import plugins
from plugins import getFileFromDirectory, getDirectoryStatusList, importFileInfoToDatabase, importDirInfoToDatabase, makeAlgorithmConfigFiles, runIndexCreateProgram, runIndexSearchProgram, formatIndexSearchResult
# Create your views here.
import subprocess
import json
import time
import os

ISOTIMEFORMAT = '%Y-%m-%d %X'

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
# print sys.getdefaultencoding()

def index(request):
    #directory_list = makeAlgorithmConfigFiles()
    #directory_list = runIndexCreateProgram()
    #message = request.GET.get("message", "")
    error_message = request.session.get("error_message", "")
    return render_to_response('index.html', {"error_message":error_message})
    #result = runIndexCreateProgram()
    #return HttpResponse(result)

@csrf_exempt
def login(request):
    errors = []
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/dashboard/')
    else:
        return render_to_response('login.html', {"errors":errors})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def register(request):
    if request.method=="POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        errors = []

        tag = len(AuthUser.objects.filter(username=username))
        if tag>0:
            errors.append(u"Username Already exist!")
            return render_to_response("register.html", {"errors":errors})
        else:
            u = AuthUser.objects.create_user(username=username, password=password, email=email)
            u.is_staff = True
            u.save()
            return HttpResponseRedirect('/login/')
    return render_to_response("register.html", {})

@login_required(login_url='/login/')
def dashboard(request, status="creating"):
    directory_list = getDirectoryStatusList()
    return render_to_response("{}.html".format(status), {"dir_list":directory_list})

@csrf_exempt
def directoryAddition(request):
    directory_string = request.POST.get('directory', '')
    result = plugins.directoryValidAndImport(directory_string)
    if result["code"]==0:
        result = plugins.directoryAnalysisProgram(directory_string)
        if result["code"]==0:
            result = plugins.makeAlgorithmConfigFiles()
            if result["code"]==0:
                result = plugins.runIndexCreateProgram()
                if result["code"]==0:
                    return HttpResponseRedirect('/dashboard/')
                    #return HttpResponse(json.dumps(result), content_type="application/json")
                else:
                    #return HttpResponse(json.dumps(result), content_type="application/json")
                    return HttpResponseRedirect('/dashboard/')
            else:
                #return HttpResponse(json.dumps(result), content_type="application/json")
                return HttpResponseRedirect('/dashboard/')
        else:
            #return HttpResponse(json.dumps(result), content_type="application/json")
            return HttpResponseRedirect('/dashboard/')
    else:
        #return HttpResponse(json.dumps(result), content_type="application/json")
        return HttpResponseRedirect('/dashboard/')


def history(request):
    plugins.runHistorySearchStatisticUpdateProgram()
    search_string = request.GET.get("searchString", "")
    if search_string:
        return render_to_response("historyDetail.html", {"request": request, "search_string": search_string})
    else:
        history_list = plugins.getHistorySearchList()
        return render_to_response("history.html", {"history_list":history_list})

@csrf_exempt
def getHistoryDetail(request):
    search_string = request.POST.get("searchString", "")
    if search_string:
        result = plugins.getHistorySearchDetail(search_string)
        return HttpResponse(json.dumps(result))
    else:
        HttpResponseRedirect('/history/')

@csrf_exempt
def addHDFSDirectoryToDB(request):
    pass

@csrf_exempt
def addDirectorytoDatabase(request):
    dirs_string = request.POST['directories']
    dir_list = dirs_string.split(';')
    dir_list = [d for d in dir_list if os.path.exists(d.strip())]
    importDirInfoToDatabase(dir_list)
    file_list = []
    for dir in dir_list:
        tmp = dir.strip()
        file_list += getFileFromDirectory(tmp)
    importFileInfoToDatabase(file_list)
    config_file_list = makeAlgorithmConfigFiles()
    runIndexCreateProgram()
    return HttpResponseRedirect('/dashboard/')
    #return HttpResponse(file_list)
    #return render_to_response('dashboard.html',{})
    '''
    if request.method == "POST":
        form = addDirectoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            dirs_string = data['directories']
            dir_list = dirs_string.split(';')
            #importDirInfoToDatabase(dir_list)
            file_list = []
            for dir in dir_list:
                tmp = dir.strip()
                file_list += getFileFromDirectory(tmp)
            #importFileInfoToDatabase(file_list)
            return HttpResponse(file_list)
            #return HttpResponseRedirect('/dashboard')
    else:
        form = addDirectoryForm()
    return render_to_response('dashboard.html',{'form':form})
    '''
    
def search(request):
    result = []
    search_string = request.GET.get("searchString","")
    result = plugins.searchStringValid(search_string)
    if result["code"] == 0:
        #return HttpResponse(json.dumps(result), content_type="application/json")
        request.session["error_message"] = ""
        return render_to_response('searchResult.html',{"searchString":search_string})
    else:
        #return HttpResponse(json.dumps(result), content_type="application/json")
        request.session["error_message"] = result["message"]
        #return HttpResponseRedirect('/?message=inputError')
        return HttpResponseRedirect('/')
    # if len(search_string)>14:
    #     '''
    #     #search_string = "1010101010101010101011111"
    #     time_start = time.time()
    #     result_list = runIndexSearchProgram(search_string)
    #     time_end = time.time()
    #     format_result = formatIndexSearchResult(result_list)
    #     format_result["summary"]["time_cost"] = "{:.4}".format(time_end-time_start)
    #     #return HttpResponse(json.dumps(format_result))
    #     return render_to_response('searchResult.html',{"format_result":format_result, "searchString":search_string})
    #     '''
    #     return render_to_response('searchResult.html',{"searchString":search_string})
    # else:
    #     #return render_to_response('index.html',{"errors":errors})
    #     return HttpResponseRedirect('/?message=inputError')

def test(request):
    # search_string = request.GET.get("searchString","")
    # return render_to_response('bsearch.html',{"searchString":search_string})
    #result = plugins.runHistorySearchStatisticUpdateProgram()
    
    # result = plugins.getDetailMatchInfo()
    # result = unicode(result, errors="replace")
    # print result
    #return HttpResponse(result)
    
    return render_to_response("test.html", {})
    

@csrf_exempt
def getDetailMatchInfo(request):

    file_name = request.POST.get("name", "")
    matches = json.loads(request.POST.get("matches", ""))
    pageNum = int(request.POST.get("pageNum", ""))

    match_list = matches[(pageNum-1)*5:pageNum*5]
    for i in match_list:
        i["length_bit"] = i["length"]

    result = plugins.getDetailMatchInfo(file_name, match_list)
    #result = unicode(result, errors="ignore")
    #print result
    #return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(result)

@csrf_exempt
def getDirectoryBrowserInfo(request):
    base_dir = request.POST.get("currentPath", "")
    result = plugins.getBrowserInfo(base_dir) if base_dir else plugins.getBrowserInfo()
    return HttpResponse(result)

@csrf_exempt
def getHDFSDirectoryBrowserInfo(request):
    base_dir = request.POST.get("currentPath", "")
    result = plugins.getHDFSBrowserInfo(base_dir) if base_dir else plugins.getHDFSBrowserInfo()
    return HttpResponse(result)