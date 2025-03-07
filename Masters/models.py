from django.db import models
from django.db import models
from Account.models import *

class application_search(models.Model):
    id = models.AutoField(primary_key=True)
    name =models.TextField(null=True,blank=True)
    description =models.TextField(null=True,blank=True)
    href =models.TextField(null=True,blank=True)
    menu_id =models.TextField(null=True,blank=True)
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.TextField(null=True,blank=True)
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.TextField(null=True,blank=True)
    class Meta:
        db_table = 'application_search'
    def __str__(self):
        return self.name
         
class parameter_master(models.Model):
    parameter_id = models.AutoField(primary_key=True)
    parameter_name =models.TextField(null=True,blank=True)
    parameter_value =models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.TextField(null=True,blank=True)
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.TextField(null=True,blank=True)
    class Meta:
        db_table = 'parameter_master'
    def __str__(self):
        return self.parameter_name

class status_master(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.TextField(null=True, blank=True)
    status_type = models.TextField(null=True, blank=True)
    status_color = models.TextField(null=True, blank=True)
    is_active = models.IntegerField(default=1)  
    level = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'status_master'

class status_color(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'status_color'


class Log(models.Model):
    log_text = models.TextField(null=True,blank=True)
    class Meta:
        db_table = 'logs'
  

class classroom(models.Model):
    room_number = models.TextField(null=True,blank=True)
    name = models.TextField(null=True,blank=True)
    capacity = models.TextField(null=True,blank=True)
    face_recog_mid = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'classroom'
    
class timeslot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
    class Meta:
        db_table = 'timeslot'

class class_semester(models.Model):
    year  = models.TextField(null=True,blank=True)
    semester = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.year
    class Meta:
        db_table = 'class_semester'
    
class section(models.Model):
    name = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'section'
    
class faculty(models.Model):
    code = models.TextField(null=True,blank=True)
    name = models.TextField(null=True,blank=True)
    type = models.TextField(null=True,blank=True)
    email = models.TextField(null=True,blank=True)
    contact = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'faculty'
    
class course(models.Model):
    code = models.TextField(null=True,blank=True)
    title = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title 
    class Meta:
        db_table = 'course'
    
class course_faculty(models.Model):
    course_id = models.TextField(null=True,blank=True)
    ssemester_id = models.TextField(null=True,blank=True)
    faculty_id = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'course_faculty'

class course_section_faculty(models.Model):
    course_id = models.TextField(null=True,blank=True)
    section_id = models.TextField(null=True,blank=True)
    faculty_id = models.TextField(null=True,blank=True)
    course_coordinator = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'course_section_faculty'

class days(models.Model):
    name = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name 
    class Meta:
        db_table = 'days'
        
class schedule(models.Model):
    class_id = models.TextField(null=True,blank=True)
    course_id = models.TextField(null=True,blank=True)
    section_id = models.TextField(null=True,blank=True)
    faculty_id = models.TextField(null=True,blank=True)
    timeslot_id = models.TextField(null=True,blank=True)
    day_id = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'schedule'

class timetable(models.Model):
    classroom_id = models.TextField(null=True,blank=True)
    date = models.DateTimeField(null=True, blank=True, auto_now=True)
    schedule_id = models.TextField(null=True,blank=True)
    class_id = models.TextField(null=True,blank=True)
    course_id = models.TextField(null=True,blank=True)
    section_id = models.TextField(null=True,blank=True)
    faculty_id = models.TextField(null=True,blank=True)
    timeslot_id = models.TextField(null=True,blank=True)
    day_id = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'timetable'

class student(models.Model):
    student_id = models.TextField(null=True,blank=True)
    name = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'student'

class student_class_section(models.Model):
    student_id = models.TextField(null=True,blank=True)
    class_id = models.TextField(null=True,blank=True)
    section_id = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'student_class_section'

class student_course(models.Model):
    student_id = models.TextField(null=True,blank=True)
    course_id = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'student_course'

class student_face_recog(models.Model):
    student_id = models.TextField(null=True,blank=True)
    face_id = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'student_face_recog'

class student_attendance(models.Model):
    face_recog_mid = models.TextField(null=True,blank=True)
    face_id = models.TextField(null=True,blank=True)
    date = models.TextField(null=True,blank=True)
    time = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'student_attendance'