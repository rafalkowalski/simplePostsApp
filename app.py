import os
import os.path as op
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, url_for, redirect, render_template
from forms.post_form import PostForm
# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text, nullable=False)

    def __init(self, title=None, text=None):
        self.title = title
        self.text = text

    def __unicode__(self):
        return self.title


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('list.html',
                           posts=posts)


@app.route('/posts/new',  methods=('GET', 'POST'))
def new_post():
    form = PostForm(request.form)
    data = form.data
    if form.validate_on_submit():
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('create.html',
                           form=form)


@app.route('/posts/<post_id>/edit', methods=('GET', 'POST'))
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostForm(obj=post)
    data = form.data
    if form.validate_on_submit():
        db.session.query(Post)\
            .filter_by(id=post.id)\
            .update(dict(data))
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('create.html',
                           form=form)


@app.route('/posts/<post_id>/delete', methods=('GET', 'POST'))
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.index'))


def build_sample_db():
    """
    Populate a small db with some example entries.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
    return


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
