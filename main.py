from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '4zd3gpc$1d!9d1z'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    day = db.Column(db.String(10))
    date = db.Column(db.String(10))

    def __init__(self, title, body, day, date):
        self.title = title
        self.body = body
        self.day = day
        self.date = date   

def empty_field(entry):
    if entry:
        return True
    else: 
        return False

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        blog_day = request.form.get('day')
        blog_date = request.form['date']

        #validation of an entry for blog_title and blog_body#
        if not empty_field(blog_title) and not empty_field(blog_body):
            flash ('Error: Title and blog entry required.')
            return redirect('/newpost')
        elif not empty_field(blog_title):  
            flash('Error: Title for blog required.')
            return redirect('/newpost')
        elif not empty_field(blog_body):
            flash('Error: Blog entry required.')
            return redirect('/newpost')



        newblog = Blog(blog_title, blog_body, blog_day, blog_date)

        db.session.add(newblog)
        db.session.commit()

        return render_template('newpost.html', title='Blog', newblog=newblog)  #needs to show the post      

    else: #if user doesn't enter anything take them back to blog entry page
        return render_template('blog.html')


@app.route('/blog', methods=['POST','GET'])
def blog():
    blog_id = request.args.get('id') #gets id from db

    if (blog_id):
        newblog = Blog.query.get(blog_id)
        return render_template('newpost.html', title='Blog', newblog=newblog)
    else:
        allblogs = Blog.query.all()
        
    return render_template('blogall.html', title='blog', allblogs=allblogs)

if __name__ == '__main__':
    app.run()