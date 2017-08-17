from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Hello World</h1>'

@app.route('/user/<name>')
def my_name(name):
	return 'hello,<i>%s</i>' % name

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return 'my post <strong>%d</strong>' % post_id

if __name__=='__main__':
	app.run(debug=True)

