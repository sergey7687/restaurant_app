from wtforms import Form, StringField, TextAreaField, PasswordField, validators



class Employee(Form):
    emp_f_name = StringField('Имя', [validators.Length(min=1, max=50)])
    emp_l_name = StringField('Фамилия', [validators.Length(min=1, max=50)])
    emp_phone = StringField('Номер телефона', [validators.Length(min=1, max=50)])
    position = StringField('Должность', [validators.Length(min=1, max=50)])
    department = StringField('Подразделение', [validators.Length(min=1, max=50)])


class Guests(Form):
    guest_f_name = StringField('Имя', [validators.Length(min=1, max=50, message='Имя должно быть от 2 до 50 символов')])
    guest_l_name = StringField('Фамилия', [validators.Length(min=1, max=50, message='Фамилия должна быть от 2 до 50 символов')])
    guest_phone = StringField('Номер телефона', [validators.Length(min=1, max=50, message='Телефон должен быть от 6 до 50 символов')])
    guest_email = StringField('Электронная почта', [validators.Length(min=1, max=50, message='Почта должна быть от 6 до 50 символов')])
    guest_address = StringField('Адрес', [validators.Length(min=1, max=50)])
    guest_note = TextAreaField('ЗАМЕТКА О ГОСТЕ', [validators.Length(min=10)])


class Register(Form):
    user_f_name = StringField('Имя', [validators.Length(min=2, max=50, message='Имя должно быть от 2 до 50 символов')])
    user_l_name = StringField('Фамилия', [validators.Length(min=2, max=50, message='Фамилия должна быть от 2 до 50 символов')])
    username = StringField('Логин', [validators.Length(min=6, max=50, message='Логин должен быть от 6 до 50 символов')])
    user_phone = StringField('Телефон', [validators.Length(min=6, max=50, message='Телефон должен быть от 6 до 50 символов')])
    user_email = StringField('Электронная почта', [validators.Length(min=6, max=50, message='Почта должна быть от 6 до 50 символов')])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='пароль не соответствует')])
    confirm = PasswordField('Подтвердить пароль')


class Orders(Form):
    order_name = StringField('Имя', [validators.Length(min=2, max=100, message='Имя должно быть от 1 до 50 символов')])
    order_phone = StringField('Номер телефона', [validators.Length(min=6, max=100, message='Телефон должен быть от 1 до 50 символов')])
    order_address = StringField('Адрес', [validators.Length(min=6, max=100, message='Адрес должен быть не менее 1 символа')])
