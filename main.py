from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:3343@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'Yt82slo29mw'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(5000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def __repr__(self):
        return "<Blog post " + str(self.id) + ": '" + self.title + "'>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Post', backref='author')

    def __init__(self, username, password):
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

        author = User.query.filter_by(username=session['user']).first()
        post = Post(title, content, author)
        db.session.add(post)
        db.session.commit()

        return redirect("/blog?id=" + str(post.id))
    else:
        return render_template('newpost.html')


#@app.route('/signup', methods = ['POST'])
#def signup():



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('That user does not exist!', 'error')
            return render_template('login.html')

        if password != user.password:
            flash('Incorrect password!', 'error')
            return render_template('login.html', username=username)

        else:
            session['user'] = username
            flash("Login Success!", 'success')            
            return redirect('/newpost')
    else:
        return render_template('login.html')
            
    


#@app.route('/index')
#def index():


@app.route('/logout', methods=['POST'])
def logout():
    if session['user']:
        del session['user']
    return redirect()





if __name__ == "__main__":
    app.run()

    





    
