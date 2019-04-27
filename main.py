from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:3343@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(5000))
    author_id = db.Column(db.Integer, db.ForeignKey['User.id'])

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def __repr__(self):
        return "<Blog post " + str(self.id) + ": '" + self.title + "'>"

class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Post', backref="author")

    def __init__(self, username, password)
        self.username = username
        self.password = password


@app.route("/blog", methods=['POST', 'GET'])
def index():
    post_id = request.args.get("id")
    single_post = False

    if post_id:
        posts = [Post.query.filter_by(id=int(post_id)).first()]
        single_post = True
        return render_template("blog.html", posts=posts, single_post=single_post)

    posts = Post.query.all()
    return render_template("blog.html", posts=posts, single_post=single_post)    
    

@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    if request.method == "POST":

        title = request.form['title']
        content = request.form['content']

        title_error = ""
        content_error = ""
        error = False

        if not title:
            title_error = "You must enter a title for your post."
            error = True 

        if not content:
            content_error = "You must enter content here."
            error = True

        if error:
            return render_template("newpost.html", title=title, content=content, 
                title_error=title_error, content_error=content_error)

        post = Post(title, content)
        db.session.add(post)
        db.session.commit()

        return redirect("/blog?id=" + str(post.id))
    else:
        return render_template('newpost.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Login Success!")
            print(session)
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist!', 'error')
    return render_template('login.html')



if __name__ == "__main__":
    app.run()

    





    
