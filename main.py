from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:3343@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(5,000))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Blog post " + str(self.id) + ": '" + self.title + "'>"


@app.route("/blog", methods=['POST', 'GET'])
def index():
    return render_template("blog.html")
    
    

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

        post = Post(title)
        db.session.add(post)
        db.commit()

        post = Post.query.filter_by(max(id)).all()
        return redirect("/blog?=" + str(post.id))
    else:
        return render_template('newpost.html')


if __name__ == "__main__":
    app.run()

    





    
