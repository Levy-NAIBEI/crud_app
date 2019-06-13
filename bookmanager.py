from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookdatabase.db"

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(40), nullable =False)
    publisher = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return "<Title: {}, Author: {}, Published by: {}>".format(self.title, 
        	self.author, self.publisher)
    
    '''def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        '''
    
@app.route('/', methods = ['GET','POST'])
def create():
	books = None
	if request.form:
		try:
			book = Book(title=request.form.get("title"), 
			author=request.form.get("author"), 
			publisher=request.form.get("publisher"))
			db.session.add(book)
			db.session.commit()

		except Exception as e:
			print('Failed to add book')
			print(e)
	books = Book.query.all()
	return render_template('home.html', books = books)

'''@app.route('/get', method = ['GET'])
def read():
	books = Book.query.all()
	return render_template('home.html', books = books)'''

@app.route("/update", methods=["PUT"])
def update():
	try:
		newtitle = request.form.get("newtitle")
		oldtitle = request.form.get("oldtitle")
		new_author = request.form.get("new_author")
		old_author= request.form.get("old_author")
		new_publisher = request.form.get("new_publisher")
		old_publisher = request.form.get("old_publisher")
		
		book = Book.query.filter_by(title=oldtitle, 
	    	author=old_author, publisher=old_publisher).first()
		
		book.title = newtitle
		book.author = new_author
		book.publisher = new_publisher
		
		db.session.commit()

	except Exception as e:
		print('Failed to update')

	return redirect(url_for("/"))

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    author = request.form.get("author")
    publisher = request.form.get("publisher")
    book = Book.query.filter_by(title=title, 
    	author=author, publisher=publisher).first()
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for("/"))   


if __name__ =='__main__':
	app.run(debug = True)

