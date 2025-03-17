import json
import pydoc
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout,get_user_model
from Account.forms import RegistrationForm
from Account.models import *
from Masters.models import *
import Db 
import bcrypt
from django.contrib.auth.decorators import login_required
from IBS.encryption import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from Account.utils import decrypt_email, encrypt_email
import requests
import traceback
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
import openpyxl
from openpyxl.styles import Font, Border, Side
import calendar
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
from Account.models import *
from Masters.models import *
from Db import callproc
from django.views.decorators.csrf import csrf_exempt
import os
from django.urls import reverse
from IBS.settings import *
import logging
from django.http import FileResponse, Http404
import mimetypes
logger = logging.getLogger(__name__)
from collections import defaultdict
import xlsxwriter
from io import BytesIO

@login_required
def masters(request):
    pre_url = request.META.get('HTTP_REFERER')
    header, data = [], []
    entity, type, name, class1 = '', '', '', ''
    global user
    user  = request.session.get('user_id', '')
    try:
         
        if request.method=="GET":
            
            entity = request.GET.get('entity', '')
            type = request.GET.get('type', '')
            datalist1= callproc("stp_get_masters",[entity,type,'name',user])
            name = datalist1[0][0]
            header = callproc("stp_get_masters", [entity, type, 'header',user])
            rows = callproc("stp_get_masters",[entity,type,'data',user])
            data = []
            if (entity == 'tt'): 
                for row in rows:
                    encrypted_id = enc(str(row[0]))
                    data.append((encrypted_id,) + row[1:])
                class1 = callproc("stp_get_dropdown_values",['class'])
            else:data = rows

        if request.method=="POST":
            entity = request.POST.get('entity', '')
            type = request.POST.get('type', '')
            if entity=='tt':
                class1 = request.POST.get('class1', '')
                date = request.POST.get('date', '')
                r = callproc("stp_post_timetable",[class1,date,user])
                response_data = r[0][0]
                messages.success(request, 'Data Generated successfully !')
                          
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        if request.method=="GET":
            return render(request,'Master/index.html', {'entity':entity,'type':type,'name':name,'header':header,'data':data,'class1':class1})
        elif request.method=="POST":  
            new_url = f'/masters?entity={entity}&type={type}'
            return redirect(new_url) 



@login_required
def time_table(request):
    pre_url = request.META.get('HTTP_REFERER')
    id,id1,rows = '','',''
    global user
    user  = request.session.get('user_id', '')
    timetable = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    td = callproc("stp_get_dropdown_values",['timeslot'])
    sd = callproc("stp_get_dropdown_values",['section'])
    cd = callproc("stp_get_dropdown_values",['course'])
    fd = callproc("stp_get_dropdown_values",['faculty'])
    crd = callproc("stp_get_dropdown_values",['classroom'])
    
    try:
        if request.method=="GET":
            id1 = request.GET.get('id', '')
            if id1:
                id = dec(id1)
                id = id.split('_')
                rows = callproc("stp_get_etimetable",[id[0],id[1],user])
                for row in rows:
                    class_name, day, timeslot = row[0], row[1], row[2]
                    section, course, faculty_name, classroom, ttid = row[3], row[4], row[5], row[6], row[7] 
                    timetable[class_name][day][timeslot].append({
                        'section': section,
                        'course': course,
                        'faculty_name': faculty_name,
                        'classroom': classroom,
                        'ttid': enc(str(ttid))
                    })

            timetable = convert_defaultdict_to_dict(timetable)
            
        if request.method=="POST":
            id1 = request.POST.get('id1', '')
            if id1:
                id = dec(id1)
                id = id.split('_')
                for key, value in request.POST.items():
                    if key.startswith("section_"):
                        parts = key.split("_")
                        day_index = parts[1]
                        slot_index = parts[2]
                        row_index = parts[3]

                        timeslot = request.POST.get(f"timeslot_{day_index}_{slot_index}")
                        section = request.POST.get(f"section_{day_index}_{slot_index}_{row_index}")
                        course = request.POST.get(f"course_{day_index}_{slot_index}_{row_index}")
                        faculty_name = request.POST.get(f"faculty_name_{day_index}_{slot_index}_{row_index}")
                        classroom = request.POST.get(f"classroom_{day_index}_{slot_index}_{row_index}")
                        ttid = request.POST.get(f"ttid_{day_index}_{slot_index}_{row_index}")

                        if timeslot and section and course and faculty_name and classroom:
                            callproc("stp_update_etimetable", [dec(ttid),id[0],id[1],timeslot, section, course, faculty_name, classroom, user])

            messages.success(request, 'Data updated successfully !')
                          
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        if request.method=="GET":
            return render(request,'Master/timetable.html', {'id1':id1,'timetable': timetable,'td':td,'sd': sd,'cd':cd,'fd': fd,'crd':crd})
        elif request.method=="POST":  
            new_url = f'/masters?entity=tt&type=i'
            return redirect(new_url) 


def convert_defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        return {k: convert_defaultdict_to_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_defaultdict_to_dict(i) if isinstance(i, defaultdict) else i for i in d]
    return d

def timetable_xlsx(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    bold_format = workbook.add_format({'bold': True, 'align': 'center','bg_color': '#AAD08B', 'valign': 'vcenter', 'border': 1, 'font_size': 12})
    cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#AAD08B', 'align': 'center', 'border': 1, 'font_size': 14})
    timeslot_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#AAD08B', 'border': 1,'font_size': 14})
    timetable = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    user = request.session.get('user_id', '')
    
    try:
        if request.method == "GET":
            id1 = request.GET.get('id', '')
            if id1:
                id = dec(id1).split('_')
                rows = callproc("stp_get_timetable_xlsx", [id[0], id[1], user])
                for row1 in rows:
                    class_name, day, timeslot = row1[0], row1[1], row1[2]
                    section, course_code, course_title, faculty_name, classroom = row1[3:]
                    timetable[class_name][day][timeslot].append({
                        'section': section,
                        'course_code': course_code,
                        'course_title': course_title,
                        'faculty_name': faculty_name,
                        'classroom': classroom,
                    })

            timetable = convert_defaultdict_to_dict(timetable)

            for class_name, days in timetable.items():
                worksheet = workbook.add_worksheet(class_name[:31])
                row = 0

                worksheet.merge_range(row, 0, row + 1, 14, f"{class_name}", header_format)
                row += 3

                for day, timeslots in days.items():
                    worksheet.merge_range(row, 0, row, 14, day, header_format)
                    row += 1

                    timeslot_columns = list(timeslots.keys())
                    timeslot_count = len(timeslot_columns)
                    total_columns = timeslot_count * 5  # 5 columns per timeslot

                    for i, timeslot in enumerate(timeslot_columns):
                        start_col = i * 5  # Each timeslot takes exactly 5 columns
                        end_col = start_col + 4  # Merge 5 columns
                        worksheet.merge_range(row, start_col, row, end_col, timeslot, timeslot_format)
                    row += 2

                    headers = ["Section", "Course", "Course Title", "Faculty Name", "Classroom"]
                    for i, timeslot in enumerate(timeslot_columns):
                        start_col = i * 5
                        for j, header in enumerate(headers):
                            worksheet.write(row, start_col + j, header, bold_format)
                    row += 1

                    max_rows = max(len(details) for details in timeslots.values())

                    col_widths = [len(h) for h in headers] * timeslot_count  # Initialize with header lengths
                    
                    for r in range(max_rows):
                        for i, timeslot in enumerate(timeslot_columns):
                            details = timeslots[timeslot]
                            start_col = i * 5
                            if r < len(details):
                                item = details[r]
                                values = [item['section'], item['course_code'], item['course_title'], item['faculty_name'], item['classroom']]
                                for j, value in enumerate(values):
                                    worksheet.write(row, start_col + j, value, cell_format)
                                    col_widths[start_col + j] = max(col_widths[start_col + j], len(str(value)))
                        row += 1
                    row += 1
                
                # Auto-adjust column widths based on data length
                for col_num, width in enumerate(col_widths):
                    worksheet.set_column(col_num, col_num, width + 2)  # Adjust width with padding
                
        workbook.close()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="TimeTable.xlsx"'
        output.seek(0)
        response.write(output.read())
        return response
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])  
        messages.error(request, 'Oops...! Something went wrong!')
