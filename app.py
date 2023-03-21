import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

## function to get a post
def get_post(post_id):
    #get a database connection
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    
    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #get a database connection
    conn = get_db_connection()

    #execute an sql query to select all entries from the posts table
    #use fetchall() to get all of the rows of the query result
    posts = conn.execute('SELECT * FROM posts').fetchall()

    #close the connection  
    conn.close()
    
    return render_template('index.html', posts=posts)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        #get title and content
        title = request.form['title']
        content = request.form['content']

        #display error if title of content not submitted
        #otherwise make database connection and insert the content
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

#route to edit post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        #get title and content
        title = request.form['title']
        content = request.form['content']

        #display error if title of content not submitted
        #otherwise make database connection and insert the content
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))


    return render_template('edit.html', post=post)

# route to delete a post
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    #get post
    post = get_post(id)

    #connect to database
    conn = get_db_connection()

    #run the delete query
    conn.execute('DELETE FROM POSTS WHERE id = ?', (id,))

    #commit the changes and close the connection
    conn.commit()
    conn.close()

    #show deletes successful message
    flash('"{}" was successfully deleted!'.format(post['title']))
    
    #go to index page after delete
    return redirect(url_for('index'))


app.run(host="0.0.0.0")