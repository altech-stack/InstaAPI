from wtforms import Form, StringField, SubmitField,TextField,validators


class ContactForm(Form):
    name = TextField("Name",[validators.Required("Please enter your name.")])
    submit = SubmitField("Send")