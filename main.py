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

def logged_in():
    if 'user' in session:
        return User.query.filter_by(username=session['user']).first()
    else:
        return False

@app.route("/blog", methods=['POST', 'GET'])
def blog():
    current_user = None
    if logged_in():
        current_user = logged_in()   

    post_id = request.args.get("id")
    single_post = False

    if post_id:
        posts = [Post.query.filter_by(id=int(post_id)).first()]
        single_post = True
        return render_template("blog.html", posts=posts, single_post=single_post, current_user=current_user)
    
    user_id = request.args.get("user")

    if user_id:
        user_posts = Post.query.filter_by(author_id=user_id).all()
        user = User.query.filter_by(id=user_id).first()
        return render_template("singleuser.html", user_posts=user_posts, user=user, current_user=current_user)

    posts = Post.query.all()
    return render_template("blog.html", posts=posts, single_post=single_post, current_user=current_user)    
    

@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    current_user = None
    if logged_in():
        current_user = logged_in()


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
                title_error=title_error, content_error=content_error, current_user=current_user)

        author = User.query.filter_by(username=session['user']).first()
        post = Post(title, content, author)
        db.session.add(post)
        db.session.commit()

        return redirect("/blog?id=" + str(post.id))
    else:
        return render_template('newpost.html', current_user=current_user)


@app.route('/signup', methods = ['GET', 'POST'])

def signup():
    current_user = None
    if logged_in():
        current_user = logged_in()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if not username or not 3 < len(username) < 20:
            flash("You must enter a name between 3 and 20 characters.", "error")
            return render_template('signup.html', current_user=current_user)

        if User.query.filter_by(username=username).first():
            flash("That username is already taken.", "error")
            return render_template('signup.html', current_user=current_user)
        
        if not password or not 3 < len(password) < 20: 
            flash("You must enter a password between 3 and 20 characters.", "error")
            return render_template('signup.html', username=username, current_user=current_user)

        if password != verify:
            flash("Those passwords do not match.", "error")
            return render_template('signup.html', username=username, current_user=current_user)

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()        
        session['user'] = username
        flash("Signup Success! Welcome!", "success")
        return redirect('/newpost')
    else:
        return render_template('signup.html', current_user=current_user)
        
        
@app.route("/login", methods=['GET', 'POST'])
def login():
    current_user = None
    if logged_in():
        current_user = logged_in()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('That user does not exist!', 'error')
            return render_template('login.html', current_user=current_user)

        if password != user.password:
            flash('Incorrect password!', 'error')
            return render_template('login.html', username=username, current_user=current_user)

        else:
            session['user'] = username
            flash("Login Success!", 'success')            
            return redirect('/newpost')
    else:
        return render_template('login.html', current_user=current_user)
            
    


@app.route('/')
def index():
    current_user = None
    if logged_in():
        current_user = logged_in()

    users = User.query.all()

    #user_names = []

    #for user in users:
        #user_names.append(user.username)
    
    return render_template('index.html', users=users, current_user=current_user)


@app.route('/logout')
def logout():
    if session['user']:
        del session['user']
    flash("Logged Out", 'success')
    return redirect("/blog")


@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']

    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


if __name__ == "__main__":
    app.run()

    





    
