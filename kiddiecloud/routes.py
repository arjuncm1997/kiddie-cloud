import os 
from flask import Flask, flash, session
from flask import render_template, flash, redirect, request, abort, url_for
from kiddiecloud import app,db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from kiddiecloud.models import User, Gallery,Feedback, AddChildRight, AddVaccination, AddHealthyDiet, AddSchool, AddBabyCare,  BookDoctor, AddTalent, BookAdmission, AddComplaints,AddQuestions, AddParenting
from kiddiecloud.forms import DoctorAccount, RegistrationForm, LoginForm, Resetrequest,Admingallery, Adminccount, UserAccount, Changepassword
from PIL import Image
from random import randint
from flask_mail import Message
import random
import string

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    image = Gallery.query.all()
    return render_template('gallery.html',image = image)


@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        feedback = Feedback(name = name,email = email,subject = subject,message = message,usertype='public')
        try:
            db.session.add(feedback)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template("contact.html")


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/register', methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = User(username= form.username.data,email=form.email.data, password=hashed_password, usertype= 'parent')
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('register.html',title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, usertype= 'parent' ).first()
        user1 = User.query.filter_by(email=form.email.data, usertype= 'doctor').first()
        user2 = User.query.filter_by(email=form.email.data, usertype= 'admin').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/user')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/doctor')
        if user2 and user2.password== form.password.data:
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')
        if user2 and bcrypt.check_password_hash(user2.password, form.password.data):
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route('/user')
@login_required
def user():
    return render_template('user.html')


@app.route('/bookdoctor',methods=['GET','POST'])
@login_required
def bookdoctor():
    doctor = User.query.filter_by(usertype='doctor').all()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        reason = request.form['reason']
        doctorname = request.form['doctorname']
        booking = BookDoctor(user = current_user.username,name=name,age=age,reason=reason,doctorname=doctorname,status='not confirmed')
        print(booking)
        try:
            db.session.add(booking)
            db.session.commit()
            return redirect('/bookdoctorview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('bookdoctor.html',doctor = doctor)

@app.route('/bookdoctorview')
@login_required
def bookdoctorview():
    tasks = BookDoctor.query.all()
    return render_template('bookdoctorview.html',tasks=tasks)

@app.route('/bookdoctordelete/<int:id>')
@login_required
def bookdoctordelete(id):
    task_to_delete = BookDoctor.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/bookdoctorview')
    except:
        return 'There was a problem deleting that task'

@app.route('/bookdoctorupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def bookdoctorupdate(id):
    task = BookDoctor.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.age = request.form['age']
        task.reason = request.form['reason']
        task.doctorname = request.form['doctorname']

        try:
            db.session.commit()
            return redirect('/bookdoctorview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('bookdoctorupdate.html', task=task)

 

@app.route('/addtalent', methods=['POST','GET'])
@login_required
def addtalent():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        talent = request.form['talent']
        kidtalent = AddTalent(user = current_user.username,name=name,age=age,talent=talent)

        try:
            db.session.add(kidtalent)
            db.session.commit()
            return redirect('/addtalentview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('addtalent.html')

@app.route('/addtalentview')
@login_required
def addtalentview():
    tasks=AddTalent.query.all()
    return render_template('addtalentview.html',tasks=tasks)

@app.route('/addtalentdelete/<int:id>')
@login_required
def addtalentdelete(id):
    task_to_delete = AddTalent.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/addtalentview')
    except:
        return 'There was a problem deleting that task'

@app.route('/addtalentupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def addtalentupdate(id):
    task = AddTalent.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.age = request.form['age']
        task.talent = request.form['talent']

        try:
            db.session.commit()
            return redirect('/addtalentview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('addtalentupdate.html', task=task)






@app.route('/bookadmission',methods=['GET','POST'])
@login_required
def bookadmission():
    school = AddSchool.query.all()
    if request.method == 'POST':
        school = request.form['school']
        name = request.form['name']
        dob = request.form['dob']
        std = request.form['std']
        admission = BookAdmission(user = current_user.username,school=school,name=name,dob=dob,std=std, status='not confirmed')

        try:
            db.session.add(admission)
            db.session.commit()
            return redirect('/bookadmissionview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('bookadmission.html',school = school)

@app.route('/bookadmissionview')
@login_required
def bookadmissonview():
    tasks = BookAdmission.query.all()
    return render_template('bookadmissionview.html',tasks=tasks)

@app.route('/bookadmissiondelete/<int:id>')
@login_required
def bookadmissiondelete(id):
    task_to_delete = BookAdmission.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/bookadmissionview')
    except:
        return 'There was a problem deleting that task'


@app.route('/bookadmissionupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def bookadmissionupdate(id):
    school = AddSchool.query.all()
    task = BookAdmission.query.get_or_404(id)

    if request.method == 'POST':
        task.school = request.form['school']
        task.name = request.form['name']
        task.dob = request.form['dob']
        task.std = request.form['std']

        try:
            db.session.commit()
            return redirect('/bookadmissionview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('bookadmissionupdate.html', task=task,school= school)






@app.route('/addcomplaint',methods=['GET','POST'])
@login_required
def addcomplaint():
    if request.method == 'POST':
        complaint = request.form['complaint']
        complaints = AddComplaints(user = current_user.username,complaint=complaint)

        try:
            db.session.add(complaints)
            db.session.commit()
            return redirect('/addcomplaintview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('addcomplaint.html')

@app.route('/addcomplaintview')
@login_required
def addcomplaintview():
    tasks=AddComplaints.query.all()
    return render_template('addcomplaintview.html',tasks=tasks)

@app.route('/addcomplaintdelete/<int:id>')
@login_required
def addcomplaintdelete(id):
    task_to_delete = AddComplaints.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/addcomplaintview')
    except:
        return 'There was a problem deleting that task'






        

@app.route('/addqueries',methods=['GET','POST'])
@login_required
def addqueries():
    doctor = User.query.filter_by(usertype='doctor').all()
    if request.method == 'POST':
        question = request.form['question']
        doctorname = request.form['doctorname']
        queries = AddQuestions(user = current_user.username,question=question,doctor=doctorname,status='no replay')

        try:
            db.session.add(queries)
            db.session.commit()
            return redirect('/addqueriesview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('addqueries.html',doctor = doctor)

@app.route('/addqueriesview')
@login_required
def addqueriesview():
    tasks=AddQuestions.query.all()
    return render_template('addqueriesview.html',tasks=tasks)

@app.route('/addqueriesdelete/<int:id>')
@login_required
def addqueriesdelete(id):
    task_to_delete = AddQuestions.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/addqueriesview')
    except:
        return 'There was a problem deleting that task'

               



@app.route('/doctor')
@login_required
def doctor():
    return render_template('doctor.html')



@app.route('/parenting', methods=['GET','POST'])
@login_required
def parenting():
    if request.method == 'POST':
        parentingtips = request.form['parentingtips']
        tips = AddParenting(user = current_user.username,parentingtips=parentingtips)

        try:
            db.session.add(tips)
            db.session.commit()
            return redirect('/parentingview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('parenting.html')

@app.route('/parentingview')
@login_required
def parentingview():
    tasks = AddParenting.query.all()
    return render_template('parentingview.html',tasks=tasks)

@app.route('/parentingdelete/<int:id>')
@login_required
def parentingdelete(id):
    task_to_delete = AddParenting.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/parentingview')
    except:
        return 'There was a problem deleting that task'

@app.route('/parentingupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def parentingupdate(id):
    task = AddParenting.query.get_or_404(id)

    if request.method == 'POST':
        task.parentingtips = request.form['parentingtips']

        try:
            db.session.commit()
            return redirect('/parentingview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('parentingupdate.html', task=task)


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')





@app.route('/childright', methods = ['POST', 'GET'])
@login_required
def childright():
    if request.method == 'POST':
        crime_section = request.form['crimesection']
        child_right = request.form['childright']
        right = AddChildRight(user = current_user.username,crimesection=crime_section,childright=child_right)

        try:
            db.session.add(right)
            db.session.commit()
            return redirect('/childrightview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template("childright.html")

@app.route('/childrightview')
@login_required
def childrightview():
    tasks = AddChildRight.query.all()
    return render_template('childrightview.html',tasks=tasks)

@app.route('/childrightdelete/<int:id>')
@login_required
def childrightdelete(id):
    task_to_delete = AddChildRight.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/childrightview')
    except:
        return 'There was a problem deleting that task'

@app.route('/childrightupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def childrightupdate(id):
    task = AddChildRight.query.get_or_404(id)

    if request.method == 'POST':
        task.crimesection = request.form['crimesection']
        task.childright = request.form['childright']

        try:
            db.session.commit()
            return redirect('/childrightview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('childrightupdate.html', task=task)



@app.route('/vaccination', methods = ['POST','GET'])
@login_required
def vaccination():
    if request.method == 'POST':
        age = request.form['age']
        vaccination = request.form['vaccination']
        vaccine = AddVaccination(user = current_user.username,age=age,vaccination=vaccination)

        try:
            db.session.add(vaccine)
            db.session.commit()
            return redirect('/vaccinationview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('vaccination.html')

@app.route('/vaccinationview')
@login_required
def vaccinationview():
    tasks = AddVaccination.query.all()
    return render_template('vaccinationview.html',tasks=tasks)

@app.route('/vaccinationdelete/<int:id>')
@login_required
def vaccinationdelete(id):
    task_to_delete = AddVaccination.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/vaccinationview')
    except:
        return 'There was a problem deleting that task'

@app.route('/vaccinationupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def vaccinationupdate(id):
    task = AddVaccination.query.get_or_404(id)

    if request.method == 'POST':
        task.age = request.form['age']
        task.vaccination = request.form['vaccination']

        try:
            db.session.commit()
            return redirect('/vaccinationview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('vaccinationupdate.html', task=task)



@app.route('/healthydiet', methods=['GET','POST'])
@login_required
def healthydiet():
    if request.method == 'POST':
        age = request.form['age']
        food = request.form['food']
        diet = AddHealthyDiet(user = current_user.username,age=age,food=food)

        try:
            db.session.add(diet)
            db.session.commit()
            return redirect('/healthydietview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('healthydiet.html')

@app.route('/healthydietview')
@login_required
def healthydietview():
    tasks = AddHealthyDiet.query.all()
    return render_template('healthydietview.html',tasks=tasks)

@app.route('/healthydietdelete/<int:id>')
@login_required
def healthdietdelete(id):
    task_to_delete = AddHealthyDiet.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/healthydietview')
    except:
        return 'There was a problem deleting that task'

@app.route('/healthydietupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def healthydietupdate(id):
    task = AddHealthyDiet.query.get_or_404(id)

    if request.method == 'POST':
        task.age = request.form['age']
        task.food = request.form['food']

        try:
            db.session.commit()
            return redirect('/healthydietview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('healthydietupdate.html', task=task)




@app.route('/school' , methods=['GET','POST'])
@login_required
def school():
    if request.method == 'POST':
        school = request.form['school']
        location = request.form['location']
        schools = AddSchool(user = current_user.username,school=school,location=location)

        try:
            db.session.add(schools)
            db.session.commit()
            return redirect('/schoolview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('school.html')

@app.route('/schoolview')
@login_required
def schoolview():
    tasks = AddSchool.query.all()
    return render_template('schoolview.html',tasks=tasks)

@app.route('/schooldelete/<int:id>')
@login_required
def schooldelete(id):
    task_to_delete = AddSchool.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/schoolview')
    except:
        return 'There was a problem deleting that task'

@app.route('/schoolupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def schoolupdate(id):
    task = AddSchool.query.get_or_404(id)

    if request.method == 'POST':
        task.school = request.form['school']
        task.location = request.form['location']

        try:
            db.session.commit()
            return redirect('/schoolview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('schoolupdate.html', task=task)




@app.route('/babycare', methods=['GET','POST'])
@login_required
def babycare():
    image = ""
    if request.method == 'POST':
        product = request.form['product']
        usage = request.form['usage']
        location = request.form['location']
        baby = AddBabyCare(user = current_user.username,product=product,usage=usage,location=location)


        try:
            db.session.add(baby)
            db.session.commit()
            return redirect('/babycareview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('babycare.html')

@app.route('/babycareview')
@login_required
def babycareview():
    tasks = AddBabyCare.query.all()
    return render_template('babycareview.html',tasks=tasks)

@app.route('/babycaredelete/<int:id>')
@login_required
def babycaredelete(id):
    task_to_delete = AddBabyCare.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/babycareview')
    except:
        return 'There was a problem deleting that task'


@app.route('/babycareupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def babycareupdate(id):
    task = AddBabyCare.query.get_or_404(id)

    if request.method == 'POST':
        task.product = request.form['product']  
        task.usage = request.form['usage']
        task.location = request.form['location']

        try:
            db.session.commit()
            return redirect('/babycareview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('babycareupdate.html', task=task)
        
    


@app.route('/adddoctor',methods=['GET','POST'])
@login_required
def adddoctor():
    if request.method == 'POST':
        doctor = request.form['doctor']
        email = request.form['email']
        address = request.form['address']
        contactno = request.form['contactno']
        def randomString(stringLength=10):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        password =randomString()
        sendemail(email,password)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        doctors = User(username=doctor,address=address,phone=contactno,email=email,password = hashed_password, usertype = 'doctor')

        try:
            db.session.add(doctors)
            db.session.commit()
            return redirect('/adddoctorview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('adddoctor.html')


def sendemail(email,password):
    msg = Message(' Password',
                  recipients=[email])
    msg.body = f'''  Your Password is, {password}  '''
    mail.send(msg)

@app.route('/adddoctorview')
@login_required
def adddoctorview():
    tasks = User.query.filter_by(usertype='doctor').all()
    return render_template('adddoctorview.html',tasks=tasks)

@app.route('/adddoctordelete/<int:id>')
@login_required
def adddoctordelete(id):
    task_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/adddoctorview')
    except:
        return 'There was a problem deleting that task'

@app.route('/adddoctorupdate/<int:id>', methods=['GET', 'POST'])
@login_required
def adddoctorupdate(id):
    task = User.query.get_or_404(id)

    if request.method == 'POST':
        task.username = request.form['doctor']  
        task.address = request.form['address']
        task.email = request.form['email']
        task.phone = request.form['contactno']

        try:
            db.session.commit()
            return redirect('/adddoctorview')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('adddoctorupdate.html', task=task)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (5000, 5000)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/dbookingrequest')
@login_required
def dbookingrequest():
    tasks = BookDoctor.query.filter_by(doctorname = current_user.username,status='not confirmed').all()
    return render_template("dbookingrequest.html",tasks = tasks)

@app.route('/dbookingconfirm/<int:id>', methods=['GET', 'POST'])
@login_required
def dbookingconfirm(id):
    task = BookDoctor.query.get_or_404(id)
    task.status = 'confirmed'  
    db.session.commit()
    return redirect('/doctor')

@app.route('/dbookingapprove')
@login_required
def dbookingapprove():
    tasks = BookDoctor.query.filter_by(doctorname = current_user.username,status='confirmed').all()
    return render_template("dbookingapprove.html",tasks = tasks)

@app.route('/atalentview')
@login_required
def atalentview():
    tasks = AddTalent.query.all()
    return render_template("atalentview.html",tasks = tasks)

@app.route('/ausercomplaint')
@login_required
def ausercomplaint():
    tasks = AddComplaints.query.all()
    return render_template("ausercomplaint.html",tasks = tasks)

@app.route('/aschooladmission')
@login_required
def aschooladmission():
    tasks = BookAdmission.query.filter_by(status='not confirmed').all()
    return render_template("aschooladmission.html",tasks=tasks)

@app.route('/aschoolconfirm/<int:id>', methods=['GET', 'POST'])
@login_required
def aschoolconfirm(id):
    task = BookAdmission.query.get_or_404(id)
    task.status='confirmed'
    db.session.commit()
    return redirect('/aschooladmission')

@app.route('/aadmissionconfirm')
@login_required
def aadmissionconfirm():
    tasks = BookAdmission.query.filter_by(status='confirmed').all()
    return render_template("aadmissionconfirm.html",tasks =tasks)
    
@app.route('/dnewqueries')
@login_required
def dnewqueries():
    tasks = AddQuestions.query.filter_by(doctor=current_user.username,status='no replay').all()
    return render_template("dnewqueries.html",tasks =tasks)


@app.route('/dqueryreplay/<int:id>',methods=['GET','POST'])
@login_required
def dqueryreplay(id):
    question = AddQuestions.query.get_or_404(id)
    if request.method == 'POST':
        question.replay = request.form['answer']
        question.status = 'replay'
        try:
            db.session.commit()
            return redirect('/doctor')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('dqueryreplay.html',question = question)

@app.route('/doldqueries')
@login_required
def doldqueries():
    tasks = AddQuestions.query.filter_by(doctor=current_user.username,status='replay').all()
    return render_template("doldqueries.html",tasks = tasks)

@app.route('/uhealthview')
@login_required
def uhealthview():
    tasks = AddHealthyDiet.query.all()
    return render_template("uhealthview.html",tasks = tasks)

@app.route('/uchildrightview')
@login_required
def uchildrightview():
    tasks = AddChildRight.query.all()
    return render_template("uchildrightview.html",tasks = tasks)

@app.route('/uvaccinationview')
@login_required
def uvaccinationview():
    tasks = AddVaccination.query.all()
    return render_template("uvaccinationview.html",tasks = tasks)

@app.route('/uparentingview')
@login_required
def uparentingview():
    tasks = AddParenting.query.all()
    return render_template("uparentingview.html",tasks =tasks)

@app.route('/aimageadd',methods=['GET','POST'])
@login_required
def aimageadd():
    form = Admingallery()
    if form.validate_on_submit():
        if form.image.data:
            pic = save_picture(form.image.data)
            view = pic
        new = Gallery(name= form.name.data,desc=form.desc.data, image = view)
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/aimageview')
    return render_template("aimageadd.html",form = form)

@app.route('/aimageview')
def aimageview():
    tasks = Gallery.query.all()
    return render_template("aimageview.html",tasks=tasks)



@app.route('/aimageupdate/<int:id>', methods=['GET', 'POST'])
def aimageupdate(id):
    gallery = Gallery.query.get_or_404(id)
    form = Admingallery()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            gallery.image = picture_file
        gallery.name = form.name.data
        gallery.desc = form.desc.data
        db.session.commit()
        flash('Your gallery has been updated!', 'success')
        return redirect('/aimageview')
    elif request.method == 'GET':
        form.name.data = gallery.name
        form.desc.data = gallery.desc
        form.image.data = gallery.image
    return render_template('aimageupdate.html',form=form,gallery =gallery)

@app.route('/aimagedelete/<int:id>')
def aimagedelete(id):
    delete = Gallery.query.get_or_404(id)

    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/aimageview')
    except:
        return 'There was a problem deleting that Image'

@app.route('/dcontact',methods=['GET','POST'])
def dcontact():
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        new = Feedback(name=current_user.username,email=current_user.email,subject= subject,message=message,usertype='doctor')

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/doctor')
        except:
            return 'Issueee'
    else:
        return render_template("dcontact.html")

@app.route('/apublicfeedback')
def apublicfeedback():
    tasks = Feedback.query.filter_by(usertype='public').all()
    return render_template("apublicfeedback.html",tasks=tasks)

@app.route('/adoctorfeedback')
def adoctorfeedback():
    tasks = Feedback.query.filter_by(usertype='doctor').all()
    return render_template("adoctorfeedback.html",tasks=tasks)

@app.route('/adminprofile/<int:id>',methods=['GET','POST'])
@login_required
def adminprofile(id):
    form = Adminccount()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            current_user.image = picture_file
        current_user.username = form.name.data
        current_user.email = form.email.data
        db.session.commit() 
    elif request.method == 'GET':
        form.name.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pics/' + current_user.image)
    return render_template("adminprofile.html",form= form)

@app.route('/userprofile/<int:id>',methods=['GET','POST'])
@login_required
def userprofile(id):
    form = UserAccount()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            current_user.image = picture_file
        current_user.username = form.name.data
        current_user.email = form.email.data
        db.session.commit() 
    elif request.method == 'GET':
        form.name.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pics/' + current_user.image)
    return render_template("userprofile.html",form= form)

@app.route('/doctorprofile/<int:id>',methods=['GET','POST'])
@login_required
def doctorprofile(id):
    form = DoctorAccount()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            current_user.image = picture_file
        current_user.username = form.name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.phone = form.phone.data
        db.session.commit() 
    elif request.method == 'GET':
        form.name.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
    image_file = url_for('static', filename='pics/' + current_user.image)
    return render_template("doctorprofile.html",form= form)


@app.route('/dchangepassword/<int:id>',methods=['GET','POST'])
@login_required
def dchangepassword(id):
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Password changed please login again')
        return redirect('/logout')
    return render_template("dchangepassword.html",form= form)

@app.route('/uchangepassword/<int:id>',methods=['GET','POST'])
@login_required
def uchangepassword(id):
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Password changed please login again')
        return redirect('/logout')
    return render_template("uchangepassword.html",form= form)




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)




@app.route("/resetrequest", methods=['GET', 'POST'])
def resetrequest():
    form = Resetrequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/resetrequest')
    return render_template('resetrequest.html', title='Reset Password', form=form)




@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('resetpassword.html', title='Reset Password', form=form)

