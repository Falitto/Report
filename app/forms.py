from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    performer = BooleanField('Исполнитель отчетов об оценке')
    appraiser = BooleanField('Оценщик')
    signer = BooleanField('Подписант')
    controler = BooleanField('Контролер качества')

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    performer = BooleanField('Исполнитель отчетов об оценке')
    appraiser = BooleanField('Оценщик')
    signer = BooleanField('Подписант')
    controler = BooleanField('Контролер качества')
    submit = SubmitField('Submit')
    cancel = SubmitField('Назад')

class Template_view(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    status = SelectField('Статус', choices=[])
    template_file = FileField('Файл шаблона')
    submit = SubmitField('Сохранить')
    
class Field_template(FlaskForm):
    name = StringField('Имя поля')
    alias = StringField('Алиас в документе')
    group_id = SelectField('Раздел', choices=[])
    value = TextAreaField('Значение по умолчанию')
    index = IntegerField('Номер в группе')
    comment = TextAreaField('Комментарий(будет выводится вместе с полем)')
    submit = SubmitField('Сохранить')

class DocumentsForm(FlaskForm):
    templates = SelectField('Шаблон для документа', choices=[])
    submit = SubmitField('Создать документ')

class DocumentForm(FlaskForm):
    number = StringField('Номер документа')
    customer = StringField('Заказчик')
    submit = SubmitField('Сохранить документ')
    
class GroupForm(FlaskForm):
    name = StringField('Название раздела')
    comment = TextAreaField('Комментарий(будет выводится вместе с разделом)')
    index = IntegerField('Номер раздела в шаблоне(порядковый номер)')
    submit = SubmitField('Сохранить раздел')

class PerformersForm(FlaskForm):
    performers = SelectField('Исполнители', choices=[])
    submit = SubmitField('Добавить исполнителя')

class OrganizationForm(FlaskForm):
    name = StringField('Организация')
    inn = StringField('ИНН')
    ogrn = StringField('ОГРН')
    kpp = StringField('КПП')
    submit = SubmitField('Сохранить')