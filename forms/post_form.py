from flask_wtf import Form
from wtforms import StringField
class PostForm(Form):
    title = StringField('title')
    text = StringField('text')