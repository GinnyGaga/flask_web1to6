import os
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
#redirect:重定向;reder_template:渲染模板;session:是用户会话，它是请求上下文中的变量，名为session，
#像标准的Python 字典一样操作程序,可以把数据存储在用户会话中，在请求之间“记住”数据。
#用户会话是一种私有存储，存在于每个连接到服务器的客户端中.默认情况下，用户会话保存在客户端cookie 中，使用设置的SECRET_KEY 进行加密签名。
#如果篡改了cookie 中的内容，签名就会失效，会话也会随之失效。
from flask_script import Manager,Shell
#Flask-Script支持命令行选项,是一个Flask 扩展，为Flask 程序添加了一个命令行解析器
from flask_bootstrap import Bootstrap
#使用Flask-Bootstrap集成Twitter Bootstrap,Bootstrap是Twitter 开发的一个开源框架，它提供的用户界面组件可用于创建整洁且具有吸引力的网页，
#而且这些网页还能兼容所有现代Web 浏览器。它引入了jquery.js。。
#Flask-Bootstrap 提供了一个非常高端的辅助函数，可以使用Bootstrap 中预先定义好的表单样式渲染整个Flask-WTF 表单，而这些操作只需一次调用即可完成
from flask_moment import Moment
#有一个使用JavaScript 开发的优秀客户端开源代码库，名为moment.js,它可以在浏览器中渲染日期和时间。
#Flask-Moment 是一个Flask 程序扩展，能把moment.js 集成到Jinja2 模板中；还依赖jquery.js
from flask_wtf import FlaskForm
#Flask-WTF扩展可以把处理Web表单的过程变成一种愉悦的体验。这个扩展对独立的WTForms包进行了包装，方便集成到Flask 程序中.
#默认情况下，Flask-WTF 能保护所有表单免受跨站请求伪造（Cross-Site Request Forgery，CSRF）的攻击。
#恶意网站把请求发送到被攻击者已登录的其他网站时就会引发CSRF 攻击。为了实现CSRF 保护，Flask-WTF 需要程序设置一个密钥。
#Flask-WTF 使用这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪.
from flask import Forms 
#使用Flask-WTF 时，每个Web 表单都由一个继承自Form 的类表示。这个类定义表单中的一组字段，每个字段都用对象表示。
#字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求。
from wtforms import StringField, SubmitField
from wtforms.validators import Required
#一个简单的Web 表单，包含一个文本字段和一个提交按钮
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)#程序实例
app.config['SECRET_KEY'] = 'hard to guess string'#设置密钥的方法;app.config字典可用来存储框架,扩展和程序本身的配置变量。
#使用标准的字典句法就能把配置值添加到app.config 对象中。这个对象还提供了一些方法，可以从文件或环境中导入配置值。
#SECRET_KEY 配置变量是通用密钥，可在Flask 和多个第三方扩展中使用。如其名所示，加密的强度取决于变量值的机密程度。
#不同的程序要使用不同的密钥，而且要保证其他人不知道你所用的字符串。为了增强安全性，密钥不应该直接写入代码，而要保存在环境变量中。
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#在Flask-SQLAlchemy 中，数据库使用URL指定.程序使用的数据库URL 必须保存到Flask 配置对象的SQLALCHEMY_DATABASE_URI 键中.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
#配置一个简单的SQLite 数据库;SQLALCHEMY_COMMIT_ON_TEARDOWN 键，将其设为True时，每次请求结束后都会自动提交数据库中的变动.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.qq.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USERNAME']=os.environ.get('2269937513@qq.com')
app.config['MAIL_PASSWORD']=os.environ.get('ayarohilcrmnebeg')

app.config['FLASKY_MAIL_SUBJECT_PREFIX']=['Flasky']#定义邮件主题的前缀
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <2269937513@qq.com>'#定义发件人的地址
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')

manager = Manager(app)#Flask-Script 输出了一个名为Manager的类
bootstrap = Bootstrap(app)#Flask-Bootstrap 的初始化方法
moment = Moment(app)
db = SQLAlchemy(app)
#db 对象是SQLAlchemy 类的实例，表示程序使用的数据库，同时还获得了Flask-SQLAlchemy提供的所有功能。
migrate=Migrate(app,db)
#为了导出数据库迁移命令，Flask-Migrate 提供了一个MigrateCommand 类，可附加到Flask-Script 的manager 对象上。
#在这个例子中，MigrateCommand 类使用db 命令附加.
manager.add_command('db',MigrateCommand)
mail=Mail (app)#初始化Flask-Mail

class Role(db.Model):
	__tablename__ = 'roles'
#类变量__tablename__ 定义在数据库中使用的表名。如果没有定义__tablename__，Flask SQLAlchemy 会使用一个默认名字，
#但默认的表名没有遵守使用复数形式进行命名的约定，所以最好由我们自己来指定表名。其余的类变量都是该模型的属性，被定义为db.Column类的实例。
	id = db.Column(db.Integer, primary_key=True)
	#db.Column 类构造函数的第一个参数是数据库列和模型属性的类型。其余的参数指定属性的配置选项
	name = db.Column(db.String(64), unique=True)
	#primary_key 如果设为True，这列就是表的主键;unique 如果设为True，这列不允许出现重复的值.
	#Flask-SQLAlchemy 要求每个模型都要定义主键，这一列经常命名为id。
	users = db.relationship('User', backref='role', lazy='dynamic')
#db.relationship() 的第一个参数表明这个关系的另一端是哪个模型。
#如果模型类尚未定义，可使用字符串形式指定;db.relationship() 中的backref参数向User模型中添加一个role 属性，从而定义反向关系。
#这一属性可替代role_id 访问Role 模型，此时获取的是模型对象，而不是外键的值.

#lazy指定如何加载相关记录。可选值有select（首次访问时按需加载）、immediate（源对象加载后就加载）、
#joined（加载记录，但使用联结）、subquery（立即加载，但使用子查询），noload（永不加载）和dynamic（不加载记录，但提供加载记录的查询).

	def __repr__(self):
		return '<Role %r>' % self.name 
#虽然没有强制要求，但这两个模型都定义了__repr()__ 方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	#index 如果设为True，为这列创建索引，提升查询效率
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	#关系使用users 表中的外键连接了两行。添加到User 模型中的role_id 列被定义为外键，就是这个外键建立起了关系。
	#传给db.ForeignKey() 的参数'roles.id' 表明，这列的值是roles 表中行的id 值.

	def __repr__(self):
		return '<User %r>' % self.username
#Flask-SQLAlchemy 创建的数据库实例为模型提供了一个基类以及一系列辅助类和辅助函数，
#可用于定义模型的结构.以上roles 表和users 表可定义为模型Role 和User.
def send_async_email(app,msg):
	#异步发送电子邮件
    with app.app_context():
	#在不同线程中执行mail.send() 函数时，程序上下文要使用app.app_context() 人工创建。
	#在程序实例上调用app.app_context() 可获得一个程序上下文。
	        mail.send(msg)

def send_email(to,subject,template,**kwargs):
#send_email函数的参数分别为收件人地址、主题、渲染邮件正文的模板和关键字参数列表
#在程序中集成发送电子邮件功能
	msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+ ' ' +subject,
				sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
	msg.body=render_template(template+'.txt',**kwargs)
	msg.html=render_template(template+'.html',**kwargs)
#指定模板时不能包含扩展名，这样才能使用两个模板分别渲染纯文本正文和富文本正文.
#调用者将关键字参数传给render_template() 函数，以便在模板中使用，进而生成电子邮件正文。
#render_template 函数的第一个参数是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实值.
	thr = Thread(target=send_async_email,args=[app,msg])
	thr.start()
	return thr

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')
#一个简单的Web 表单，包含一个文本字段和一个提交按钮。

#这个表单中的字段都定义为类变量，类变量的值是相应字段类型的对象。
#在这个示例中，NameForm 表单中有一个名为name 的文本字段和一个名为submit 的提交按钮。
#StringField类表示属性为type="text" 的<input> 元素。SubmitField 类表示属性为type="submit" 的<input> 元素。
#字段构造函数的第一个参数是把表单渲染成HTML 时使用的标号。
#StringField 构造函数中的可选参数validators 指定一个由验证函数组成的列表，在接受用户提交的数据之前验证数据。
#验证函数Required() 确保提交的字段不为空;Form 基类由Flask-WTF 扩展定义，所以从flask.ext.wtf 中导入。
#字段和验证函数却可以直接从WTForms 包中导入.

def make_shell_context():
#让Flask-Script 的shell 命令自动导入特定的对象。若想把对象添加到导入列表中，我们要为shell 命令注册一个make_context回调函数。
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
#make_shell_context() 函数注册了程序、数据库实例以及模型，因此这些对象能直接导入shell.

@app.errorhandler(404)
#客户端请求未知页面或路由时显示400
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
#有未处理的异常时显示500
def internal_server_error(e):
	return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
#路由;app.route 修饰器中添加的methods 参数告诉Flask在URL映射中把这个视图函数注册为GET 和POST 请求的处理程序。
#如果没指定methods 参数，就只把视图函数注册为GET 请求的处理程序。
def index():#视图函数
	form = NameForm()
	#局部变量name 用来存放表单中输入的有效名字,在视图函数中创建一个NameForm 类实例用于表示表单
	if form.validate_on_submit():
	#提交表单后，如果数据能被所有验证函数接受，那么validate_on_submit() 方法的返回值为True，
	#否则返回False。这个函数的返回值决定是重新渲染表单还是处理表单提交的数据。
		user = User.query.filter_by(username=form.name.data).first()
#用户提交表单后，服务器收到一个包含数据的POST 请求。validate_on_submit() 会调用name 字段上附属的Required() 验证函数。
#如果名字不为空，就能通过验证，validate_on_submit() 返回True。现在，用户输入的名字可通过字段的data 属性获取.

#使用过滤器filter_by(把等值过滤器添加到原查询上，返回一个新查询)可以配置query 对象进行更精确的数据库查询,
#User.query.filter_by(username=form.name.data)查找角色为User的用户,即为用户输入的名字。

#first() 返回查询的第一个结果，如果没有结果，则返回None.
#在这个修改后的版本中，提交表单后，程序会使用filter_by() 查询过滤器在数据库中查找提交的名字.
		if user is None:
			user=User(username=form.name.data)
			db.session.add(user)
			session['known']=False
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'],'New User',
							'mail/new_user',user=user)
#电子邮件的收件人保存在环境变量FLASKY_ADMIN 中，在程序启动过程中，它会加载到一个同名配置变量中。
#我们要创建两个模板文件，分别用于渲染纯文本和HTML 版本的邮件正文。
#这两个模板文件都保存在templates 文件夹下的mail 子文件夹中，以便和普通模板区分开来。
#电子邮件的模板中要有一个模板参数是用户，因此调用send_mail() 函数时要以关键字参数的形式传入用户。

		else:
			session['known']=True
#变量known 被写入用户会话中，因此重定向之后，可以把数据传给模板，用来显示自定义的欢迎消息.
		session['name']=form.name.data
		return redirect(url_for('index'))
	#由于使用频繁，Flask 提供了redirect() 辅助函数，用于生成这种重定向响应:这种响应没有页面文档，只告诉浏览器一个新地址用以加载新页面。
	#重定向经常在Web表单中使用.推荐使用url_for() 生成URL，因为这个函数使用URL 映射生成URL，从而保证URL 和定义的路由兼容，而且修改路由名字后依然可用.
	#url_for() 函数的第一个且唯一必须指定的参数是端点名，即路由的内部名字。默认情况下，路由的端点是相应视图函数的名字。
	return render_template('index.html',
		form=form,name=session.get('name'),
		#使用session.get('name') 直接从会话中读取name 参数的值。和普通的字典一样，
		#这里使用get() 获取字典中键对应的值以避免未找到键的异常情况，因为对于不存在的键，get() 会返回默认值None。
		known=session.get('known',False))


if __name__ == '__main__': #启动服务器
	manager.run()#服务器由manager.run()启动,启动后就能解析命令行了。
