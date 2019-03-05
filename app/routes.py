from app import app, db
import os
from flask import render_template, flash, redirect, url_for, send_from_directory
from flask_login import current_user, login_user
from app.models import User, Document, Template, Status, Template_field, Document_field, Docs
from flask_login import logout_user, login_required
from app.forms import LoginForm, RegistrationForm, EditProfileForm, Template_view, Field_template, DocumentsForm, DocumentForm
from flask import request
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
from docxtpl import DocxTemplate

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

#Проверка корректности имени файла
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

#Главная страница
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = DocumentsForm()
    if request.method == 'POST':
        template_id = form.templates.data
        fields = Template_field.query.filter_by(template=template_id)
        document = Document()
        db.session.add(document)
        db.session.commit()
        for field in fields:
            document_field = Document_field(document=document.id, name = field.name, index=field.index, alias=field.alias, template_field=field.id)
            db.session.add(document_field)
            db.session.commit()
        doc_fields = Document_field.query.filter_by(document=document.id)
        return redirect(url_for('document', document_id=document.id))
    else:
        form = DocumentsForm()
        form.templates.choices = [(s.id, s.name) for s in Template.query.filter_by(status=1)]
        result = Document.query.all()
        documents = [document for document in result]
    return render_template('index.html', title='Home', documents=documents, form=form)

#Форма входа в аккаунт
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

#Форма выхода из аккаунта
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Форма регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, performer=form.performer.data, appraiser=form.appraiser.data, signer=form.signer.data, controler=form.controler.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем с регистрацией!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#Профиль
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

#Форма редактирования профиля
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.patronymic = form.patronymic.data
        current_user.performer = form.performer.data
        current_user.appraiser = form.appraiser.data
        current_user.signer = form.signer.data
        current_user.controler = form.controler.data
        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.patronymic.data = current_user.patronymic 
        form.last_name.data = current_user.last_name
        form.performer.data = current_user.performer
        form.appraiser.data = current_user.appraiser
        form.signer.data = current_user.signer
        form.controler.data = current_user.controler
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

#Отображение документа
@app.route('/document/<document_id>', methods=['GET', 'POST'])
@login_required
def document(document_id):
    if request.method == 'POST':
        document_form = DocumentForm()
        document = Document.query.filter_by(id=document_id).first()
        document.number = document_form.number.data
        document.customer = document_form.customer.data
        db.session.commit()
        fields = Document_field.query.filter_by(document=document.id)
        for field in fields:
            field.value = request.form.get(field.alias)
        db.session.commit()
        flash('Документ сохранен!')
        return render_template('document.html', document=document, fields=fields, document_form=document_form)
    else:
        document = Document.query.filter_by(id=document_id).first_or_404()
        document_form = DocumentForm(obj=document)
        fields = Document_field.query.filter_by(document=document.id)
        return render_template('document.html', document=document, fields=fields, document_form=document_form)

#Отображение шаблонов
@app.route('/templates')
@login_required
def templates():
    result = Template.query.all()
    templates = [template for template in result]
    result2 = Status.query.order_by('name')
    statuses = [status for status in result2]
    return render_template('templates.html', title='Шаблоны', templates=templates, statuses=statuses)

#Отображение шаблона
@app.route('/template/<template_id>', methods=['GET', 'POST'])
@login_required
def template(template_id):
    if request.method == 'POST':
        form = Template_view()
        template = Template.query.filter_by(id=template_id).first()
        filename = template.file_name
        file_path = template.file_path
        try:
            file = request.files['template_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], app.config['TEMPLATES_FOLDER'], filename))
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['TEMPLATES_FOLDER'], filename)
        except:
            pass        
        template.name = form.name.data
        template.status = form.status.data
        template.file_name = filename
        template.file_path = file_path
        db.session.commit()
        return redirect(url_for('templates'))
    elif request.method == 'GET':
        template = Template.query.filter_by(id=template_id).first()
        form = Template_view(obj=template)
        form.status.choices = [(s.id, s.name) for s in Status.query.order_by('name')]
        #Так и не пдгружается в форму в поле файла файл, поставил костыль, если в шаблоне указано имя файла, поле для подгрузки файла не вывожу, а вывожу кнопки
        # для открытия и удаления файла. При обработке получения данных формы, через try отсекаю случаи, когда в форму не подгружен файл. 
        result = Template_field.query.filter_by(template = template_id)
        fields = [field for field in result]   
    return render_template('template.html',title='Шаблон', template = template, form = form, fields = fields) 

#Отображение поля шаблона
@app.route('/template/<template_id>/<field_id>', methods=['GET', 'POST'])
@login_required
def field(template_id, field_id):
    if request.method == 'POST':
        form = Field_template()
        field = Template_field.query.filter_by(id=field_id).first()
        field.name = form.name.data
        field.alias = form.alias.data
        db.session.commit()
        return redirect(url_for('template', template_id = template_id))
    elif request.method == 'GET':
        field = Template_field.query.filter_by(id=field_id).first()
        form = Field_template(obj=field)   
    return render_template('field.html',title='Поле', field = field, form = form, template_id = template_id) 

#Создание нового поля шаблона
@app.route('/template/<template_id>/new_field', methods=['GET', 'POST'])
@login_required
def new_field(template_id):
    if request.method == 'POST':
        form = Field_template()
        field = Template_field(name = form.name.data, alias = form.alias.data, template = template_id)
        db.session.add(field)
        db.session.commit()
        return redirect(url_for('template', template_id = template_id))
    elif request.method == 'GET':
        form = Field_template()   
    return render_template('field.html',title='Поле', form = form, template_id = template_id) 

#Удаление поля шаблона
@app.route('/template/<template_id>/delete_field/<field_id>', methods=['GET'])
@login_required
def delete_field(template_id, field_id):
    field = Template_field.query.filter_by(id=field_id).first()
    db.session.delete(field)
    db.session.commit()   
    return redirect(url_for('template', template_id = template_id))

#Скачивание файла
@app.route('/download/<filename>')
@login_required
def download_template(filename):
    return send_from_directory(os.path.join('uploads/', app.config['TEMPLATES_FOLDER']), filename, as_attachment=True)

#Удаление данных о файле из записи шаблона в БД
@app.route('/delete_template_file/<template_id>/<filename>')
@login_required
def delete_template_file(template_id, filename):
    template = Template.query.filter_by(id=template_id).first()
    template.file_name = ''
    template.file_path = ''
    db.session.commit() 
    return redirect(url_for('template', template_id = template.id))

@app.route('/templates/new_template', methods=['GET', 'POST'])
@login_required
def new_template():
    if request.method == 'POST':
        form = Template_view()
        filename = ''
        file_path = ''
        try:
            file = request.files['template_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], app.config['TEMPLATES_FOLDER'], filename))
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['TEMPLATES_FOLDER'], filename)
        except:
            pass    
        template = Template(name = form.name.data, status = form.status.data, file_name = filename, file_path = file_path)    
        db.session.add(template)
        db.session.commit()
        return redirect(url_for('templates'))
    elif request.method == 'GET':
        form = Template_view()
        form.status.choices = [(s.id, s.name) for s in Status.query.order_by('name')]  
    return render_template('new_template.html',title='Создание нового шаблона', form = form)

@app.route('/generate_doc/<document_id>')
@login_required
def generate_doc(document_id):
    #Генерирую файл по шаблону
    document = Document.query.filter_by(id=document_id).first()
    template = Template.query.filter_by(id = document.template_id).first()
    fields = Document_field.query.filter_by(document=document_id)
    doc = DocxTemplate(template.file_path)
    context=[]
    for field in fields:
        context[field.alias] = field.value
    try:
        doc.render(context)
        #flash(context)
            
        #flash('accepted!!!')
    except:
        flash('Ошибка при формировании файла')
    #Записываю файл в папку docs
    try:
        doc.save(os.path.join(app.config['UPLOAD_FOLDER'], app.config['DOCS_FOLDER'], str(document.id)+ str(document.number)+ str(template.file_name)))  
        record=Docs(document_id=document_id, user=current_user.id, create_date=datetime.utcnow(), result=True, path=os.path.join(app.config['UPLOAD_FOLDER'], app.config['DOCS_FOLDER']), filename=str(document.id) + str(document.number) + str(template.file_name))
        db.session.add(record)
        db.session.commit()
    #flash(record.path + record.filename)
        return send_from_directory('uploads/docs/', record.filename, as_attachment=True)
    except:
        flash('Ошибка')
        return redirect(url_for('document', document_id=document_id))    
    #Делаю запись в базу данных о создании файла и отправляю файл на клиент
    