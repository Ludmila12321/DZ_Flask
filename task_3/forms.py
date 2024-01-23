from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class RegistrationForm(FlaskForm):
    name = StringField('Имя')
    surname = StringField('Фамилия')
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль',
                            validators=[DataRequired(), Length(min=8),
                                        Regexp('(?=.*[a-z])(?=.*[0-9])',
                                                message="Ошибка! Нужны цифры и буквы!")])
    confirm_password = PasswordField('Повторите пароль',
                                    validators=[DataRequired(),
                                                EqualTo('password')])
    terms = BooleanField("Я согласен с правилами, условиями и политикой конфиденциальности",
                        validators=[DataRequired()])