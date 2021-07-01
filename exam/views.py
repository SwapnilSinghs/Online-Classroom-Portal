from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from ocp_app.models import Student, Department, Teacher, Courses, Announcement, Forum
from exam.models import Exam, Assignment, AssignmentAnswer, ExamAnswer
from django.http import HttpResponse, JsonResponse
from . import facesTrain
import numpy as np
from django.conf import settings
from django.core.mail import send_mail
import cv2
import pickle
# Create your views here.


def fun(request):
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        student = Student.objects.filter(username=id)
        img = student[0].img

    else:
        teacher = Teacher.objects.filter(username=id)
        img = teacher[0].img
    return img, id


def faceTest(request):
    face_cascade = cv2.CascadeClassifier(
        'exam/haarcascade_frontalface_alt2.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("exam/trainner.yml")

    labels = {"person_name": 1}
    with open("exam/labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    # intiating webcam
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # converting image into gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # getting faces
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 10)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            # pridicting faces
            id_, conf = recognizer.predict(roi_gray)
            # confi sbesically accuracy of the pridiction
            # if conf>=70 and conf <= 80:
            #     font = cv2.FONT_HERSHEY_SIMPLEX
            print(labels[id_], conf)
            return labels[id_]


def examlogin(request):
    return render(request, 'examlogin.html')


def examloginhandle(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        ans = faceTest(request)
        l = list(map(str, ans.split('.')))
        if l[0].lower() == username.lower():
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('../examDashboard/')
        else:
            # context = "Please enter valid username and password."
            return render(request, 'examlogin.html/')
    else:
        return render(request, 'examlogin.html/')


def examDashboard(request):
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        student = Student.objects.filter(username=id)
        img = student[0].img
        params = {'img': img, 'user': id}
        return render(request, 'examDashboard.html', params)
    else:
        return HttpResponse("<script>setTimeout(function(){window.location.href='/signIn/'},0000);</script>")

def vannouncements(request):
    img, id = fun(request)
    vannounce=Announcement.objects.all()
    params = {'img': img, 'user': id,'vannounce':vannounce}
    return render(request,'vannouncements.html',params)

def addAssignment(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        return render(request, 'examDashboard.html')
    else:
        teacher = Teacher.objects.filter(username=id)
        uploadedBy = teacher[0].firstname + ' ' + teacher[0].lastname
        courses = Courses.objects.all()
        departments = Department.objects.all()
    params = {'uploadedBy': uploadedBy,
              'courses': courses, 'departments': departments, 'img': img}
    if request.method == "POST" and request.FILES['assign_file']:
        assignfile = request.FILES['assign_file']
        fileurl = assignfile
        assign_name = request.POST.get('assign_name', '')
        doa = request.POST.get('doa', '')
        ast = request.POST.get('ast', '')
        aet = request.POST.get('aet', '')
        cname = request.POST.get('course', '')
        course = Courses.objects.get(course_name=cname)
        dept = request.POST.get('dept', '')
        uploadedBy = request.POST.get('uploadedBy', '')
        upby = Teacher.objects.get(username=id)
        detail = request.POST.get('detail', '')
        amarks_outof = request.POST.get('amarks_outof')
        if g_id == 1:
            return render(request, 'examDashboard.html')
        else:
            assignment = Assignment(assignment_fileUpload=fileurl, assignment_name=assign_name, assignment_date=doa, assignment_start_time=ast,
                                    assignment_end_time=aet, assignment_detail=detail, dept=dept, uploaded_by=upby, course=course, assignment_marksOutOf=amarks_outof)
            assignment.save()
            return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/addAssignment/'},0000);</script>")
    return render(request, 'addAssignment.html', params)


def viewAssignment(request, assignid):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    assign = Assignment.objects.filter(assignment_id=assignid)
    name = assign[0].assignment_name
    date = assign[0].assignment_date
    st = assign[0].assignment_start_time
    et = assign[0].assignment_end_time
    detail = assign[0].assignment_detail
    fileUpload = assign[0].assignment_fileUpload
    dept = assign[0].dept
    uploadedBy = assign[0].uploaded_by_id
    cid = assign[0].course_id
    moutof = assign[0].assignment_marksOutOf
    if g_id == 1:
        template_values = 'examDashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'name': name, 'date': date, 'st': st, 'et': et, 'detail': detail,
              'fileUpload': fileUpload, 'dept': dept, 'uploadedBy': uploadedBy, 'cid': cid, 'template': template_values, 'img': img}
    if request.method == "POST" and request.FILES['fileassign']:
        if g_id == 1:
            solutionfile = request.FILES['fileassign']
            fileurl = solutionfile
            solution = AssignmentAnswer(
                assign_id=assignid, stud_id=id, submittedfile=fileurl, course_id=cid, amarksOutOf=moutof)
            solution.save()
            return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/viewAllAssignment/'},0000);</script>")
    return render(request, 'viewAssignment.html', params)


def deleteAssignment(request, assignid):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        return render(request, 'examDashboard.html')
    else:
        dc = Assignment.objects.get(assignment_id=assignid)
        dc.delete()
        return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/viewAllAssignment/'},0000);</script>")
    return render(request, 'viewAllAssignment.html')


def viewAllAssignment(request):
    assignments = Assignment.objects.all()
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        deleteVisible = False
        template_values = 'examDashboard.html'
    else:
        deleteVisible = True
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'assignments': assignments,
              'deleteVisible': deleteVisible, 'template': template_values, 'img': img}
    return render(request, 'viewAllAssignment.html', params)


def viewSubmitAssignTeach(request, assignid):
    answers = AssignmentAnswer.objects.filter(assign_id=assignid)
    assign_id = answers[0].assign_id
    course_id = answers[0].course_id
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id != 1:
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'assignmentAnswer': answers, 'template': template_values,
              'assign_id': assign_id, 'course_id': course_id, 'img': img}
    return render(request, 'viewSubmitAssignTeach.html', params)


def submitAssignScore(request, assignid, studid):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if request.method == "POST":
        if g_id != 1:
            mgot = request.POST.get('mgot', '')
            AssignmentAnswer.objects.filter(
                assign_id=assignid, stud=studid).update(amarksObtained=mgot)
    return HttpResponse("<script>setTimeout(function(){window.history.back();},0000);</script>")


def resultAssignment(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    st = Student.objects.filter(username=id)
    st1 = st[0].firstname + " " + st[0].lastname
    stud = AssignmentAnswer.objects.filter(stud_id=id)
    if g_id == 1:
        template_values = 'examDashboard.html'
    params = {'template': template_values,
              'img': img, 'stud': stud, 'name': st1}
    return render(request, 'resultAssignment.html', params)


def addExam(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        return render(request, 'examDashboard.html')
    else:
        teacher = Teacher.objects.filter(username=id)
        uploadedBy = teacher[0].firstname + ' ' + teacher[0].lastname
        courses = Courses.objects.all()
        departments = Department.objects.all()
    params = {'uploadedBy': uploadedBy,
              'courses': courses, 'departments': departments, 'img': img}
    if request.method == "POST" and request.FILES['exam_file']:
        qpaperfile = request.FILES['exam_file']
        fileurl = qpaperfile
        examName = request.POST.get('examName', '')
        doe = request.POST.get('doe', '')
        est = request.POST.get('est', '')
        eet = request.POST.get('eet', '')
        examtype = request.POST.get('examType', '')
        cname = request.POST.get('course', '')
        course = Courses.objects.get(course_name=cname)
        dept = request.POST.get('dept', '')
        uploadedBy = request.POST.get('uploadedBy', '')
        upby = Teacher.objects.get(username=id)
        detail = request.POST.get('detail', '')
        emarks_outof = request.POST.get('emarks_outof')
        if g_id == 1:
            return render(request, 'examDashboard.html')
        else:
            exam = Exam(exam_fileUpload=fileurl, exam_name=examName, exam_type=examtype, exam_date=doe,
                        exam_start_time=est, exam_end_time=eet, exam_detail=detail, course=course, dept=dept, uploaded_by=upby, exam_marksOutOf=emarks_outof)
            exam.save()
            return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/addExam/'},0000);</script>")
    return render(request, 'addExam.html', params)


def viewExam(request, examid):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    exam = Exam.objects.filter(exam_id=examid)
    name = exam[0].exam_name
    etype = exam[0].exam_type
    date = exam[0].exam_date
    st = exam[0].exam_start_time
    et = exam[0].exam_end_time
    detail = exam[0].exam_detail
    fileUpload = exam[0].exam_fileUpload
    dept = exam[0].dept
    uploadedBy = exam[0].uploaded_by_id
    cid = exam[0].course_id
    moutof = exam[0].exam_marksOutOf
    if g_id == 1:
        template_values = 'examDashboard.html'
    else:
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'name': name, 'etype': etype, 'date': date, 'st': st, 'et': et, 'detail': detail,
              'fileUpload': fileUpload, 'dept': dept, 'uploadedBy': uploadedBy, 'cid': cid, 'template': template_values, 'img': img}
    if request.method == "POST" and request.FILES['exam_file']:
        if g_id == 1:
            solutionfile = request.FILES['exam_file']
            fileurl = solutionfile
            solution = ExamAnswer(exam_id=examid, stud_id=id,
                                  submittedfile=fileurl, course_id=cid, emarksOutOf=moutof)
            solution.save()
            return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/viewAllExam/'},0000);</script>")
    return render(request, 'viewExam.html', params)


def viewAllExam(request):
    exams = Exam.objects.all()
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        deleteVisible = False
        template_values = 'examDashboard.html'
    else:
        deleteVisible = True
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'exams': exams, 'deleteVisible': deleteVisible,
              'template': template_values, 'img': img}
    return render(request, 'viewAllExam.html', params)


def resultExam(request):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    st = Student.objects.filter(username=id)
    st1 = st[0].firstname + " " + st[0].lastname
    stud = ExamAnswer.objects.filter(stud_id=id)
    if g_id == 1:
        template_values = 'examDashboard.html'
    params = {'template': template_values, 'img': img, 'stud': stud, 'name': st1, 'st1': "Sessional Test - 1",
              'st2': "Sessional Test - 2", 'put': "Pre-University Test", 'ut': "University Test"}
    return render(request, 'resultExam.html', params)


def viewSubmitExamTeach(request, examid):
    answers = ExamAnswer.objects.filter(exam_id=examid)
    exam_id = answers[0].exam_id
    course_id = answers[0].course_id
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id != 1:
        template_values = 'ocp_app/dashboardTeach.html'
    params = {'examAnswer': answers, 'template': template_values, 'exam_id': exam_id,
              'course_id': course_id, 'img': img}
    return render(request, 'viewSubmitExamTeach.html', params)


def deleteExam(request, examid):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if g_id == 1:
        return render(request, 'examDashboard.html')
    else:
        dc = Exam.objects.get(exam_id=examid)
        dc.delete()
        return HttpResponse("<script>setTimeout(function(){window.location.href='/exam/viewAllExam/'},0000);</script>")
    return render(request, 'viewAllExam.html')


def submitExamScore(request, examid, studid):
    img, id = fun(request)
    g = request.user.groups.all()
    g_id = Group.objects.get(name=g[0]).id
    id = request.user.username
    if request.method == "POST":
        if g_id != 1:
            mgot = request.POST.get('mgot', '')
            ExamAnswer.objects.filter(
                exam_id=examid, stud=studid).update(emarksObtained=mgot)
    return HttpResponse("<script>setTimeout(function(){window.history.back();},0000);</script>")


def test_proc(request):
    face_cascade = cv2.CascadeClassifier(
        'exam/haarcascade_frontalface_alt2.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("exam/trainner.yml")

    labels = {"person_name": 1}
    with open("exam/labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    firstname=request.user.first_name
    lastname=request.user.last_name
    email = request.user.email
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, 'admin123@admin.com']
    n1='\n'

    
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)
    user = request.user.username
    result = cv2.VideoWriter('exam/recordings/'+str(user)+'.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             10, size)
    count = 0

    x = 0

    while(True):
        ret, frame = cap.read()
        print(x)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        result.write(frame)
        if x > 1000:
            print(x)
            count = 2
            subject = 'Candidature Cancellation'
            message = f'Dear {firstname} {lastname}, {n1}{n1}Welcome to the Online Classroom Portal.{n1}{n1}You ave been indulge in suspicious activity. No Faces  have been Detected. Your Candidature is Cancelled.{n1}{n1} Wish You all the very Best. {n1} Thankyou!!.'
            send_mail(subject, message, email_from, recipient_list)
            return JsonResponse({'status': 0, 'count': count})
            return JsonResponse({'status': 0, 'count': count})

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 10)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            # pridicting faces
            id_, conf = recognizer.predict(roi_gray)
            if (x < 0):
                x = 100

            x = x-50
            if conf >= 40:
                if labels[id_] == request.user.username:
                    print(labels[id_])
                    result.write(frame)
                    continue
                else:
                    count = 1
                    subject = 'Candidature Cancellation'
                    message = f'Dear {firstname} {lastname}, {n1}{n1}Welcome to the Online Classroom Portal.{n1}{n1}You ave been indulge in suspicious activity. Unknown Faces have been Detected. Your Candidature is Cancelled.{n1}{n1} Wish You all the very Best. {n1} Thankyou!!.'
                    send_mail(subject, message, email_from, recipient_list)
                    print(count)
                    return JsonResponse({'status': 1, 'count': count})
            else:
                count = 2
                subject = 'Candidature Cancellation'
                message = f'Dear {firstname} {lastname}, {n1}{n1}Welcome to the Online Classroom Portal.{n1}{n1}You ave been indulge in suspicious activity. Unknown Faces have been Detected. Your Candidature is Cancelled.{n}{n} Wish You all the very Best. {n} Thankyou!!.'
                send_mail(subject, message, email_from, recipient_list)
                return JsonResponse({'status': 0, 'count': count})
        x = x+25
