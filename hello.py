from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Hello World</h1>'

@app.route('/user/<name>')
def my_name(name):
	return 'hello,<i>%s</i>' % name

if __name__=='__main__':
	app.run(debug=True)

