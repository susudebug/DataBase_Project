from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from login import *
from admin import *
from updateFines import *
from print_fines import *
from borrowbook import *
from reader_query import *
from book_search import *
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

update_fines()

app = Flask(__name__)
app.secret_key = 'password'  # 设置一个密钥，用于加密会话数据


@app.route('/')
def home():
    return redirect(url_for('Login'))


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        # 假设 login 函数实现了登录逻辑
        login_status = login(account, password)
        if login_status['success']:
            user_data = login_status['data']
            session['account'] = account
            print(user_data)
            session['role'] = user_data['role']
            if int(session['role']) == 1:
                return redirect(url_for('Admin_menu'))
            else:
                session['name'] = user_data['name']
                return redirect(url_for('User_home'))
        else:
            flash(login_status["message"])
            return redirect(url_for('Login'))
    return render_template('login.html')


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        password = request.form['password']
        password2 = request.form['password2']
        name = request.form['name']
        contact = request.form['contact']
        gender = request.form['gender']
        department = request.form['department']
        title = request.form['title']

        if password != password2:
            print("两次密码不一致")
            flash("两次密码不一致")
            return render_template('register.html')

        register_status = register(name=name, password=password, title=title, phone_number=contact,
                                   department=department, gender=gender)
        if register_status['success']:
            out_string = "注册成功，你的账号为：" + str(register_status['data']) + " 请及时保存这个账号"
            print(out_string)
            flash(out_string)
            return redirect(url_for('Login'))
        else:
            print(register_status['message'])
            flash(register_status['message'])
            return render_template('register.html')
    return render_template('register.html')


# 登出页面
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Login'))


# 管理员页面
@app.route('/admin/index', methods=['GET', 'POST'])
def Admin_menu():
    return render_template('adminIndex.html')


# 添加图书
@app.route('/admin/Add_book', methods=['GET', 'POST'])
def Admin_add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        book_title = request.form['book_title']

        publisher = request.form['publisher'] if request.form['publisher'] != '' else None
        author = request.form['author'] if request.form['author'] != '' else None
        total_quantity = int(request.form['total_quantity']) if request.form.get('total_quantity') else 10
        available_quantity = int(request.form['available_quantity']) if request.form.get('available_quantity') else 10

        is_borrowable = request.form['is_borrowable']

        status = add_book(isbn=isbn, book_title=book_title, publisher=publisher, author=author,
                          total_quantity=total_quantity, available_quantity=available_quantity,
                          is_borrowable=is_borrowable)
        print(status)
        # if status['success']==True:
        #     print(status)
    return render_template('addbook.html')


# 到期未还图书
@app.route('/admin/Overdue_book', methods=['GET', 'POST'])
def Admin_overdue_book():
    data = get_overdue_books()
    books = data['data']['overdue_books']
    return render_template('overduebook.html', books=books)


# 添加读者信息
@app.route('/admin/Add_reader', methods=['GET', 'POST'])
def Admin_add_reader():
    if request.method == 'POST':
        # 从表单获取数据
        library_card_number = request.form['library_card_number']
        name = request.form['name'] if request.form['name'] != '' else None
        gender = request.form['gender'] if request.form['gender'] != '' else None
        title = request.form['title'] if request.form['title'] != '' else None
        available_quantity = int(request.form['available_quantity']) if request.form.get('available_quantity') else 10
        borrowed_quantity = int(request.form['borrowed_quantity']) if request.form.get('borrowed_quantity') else 0
        department = request.form['department'] if request.form['department'] != '' else None
        contact_number = request.form['contact_number'] if request.form['contact_number'] != '' else None

        # 调用添加读者的函数
        status = add_reader(library_card_number=library_card_number, name=name, gender=gender,
                            title=title, available_quantity=available_quantity, borrowed_quantity=borrowed_quantity,
                            department=department, contact_number=contact_number)
        print(status)

    # 渲染添加读者信息页面
    return render_template('addreader.html')


# 更新读者信息
@app.route('/admin/Update_reader', methods=['GET', 'POST'])
def Admin_update_reader():
    if request.method == 'POST':
        # 从表单获取数据
        library_card_number = request.form['library_card_number']
        name = request.form['name'] if request.form['name'] != '' else None
        gender = request.form['gender'] if request.form['gender'] != '' else None
        title = request.form['title'] if request.form['title'] != '' else None
        available_quantity = int(request.form['available_quantity']) if request.form.get('available_quantity') else 10
        borrowed_quantity = int(request.form['borrowed_quantity']) if request.form.get('borrowed_quantity') else 0
        department = request.form['department'] if request.form['department'] != '' else None
        contact_number = request.form['contact_number'] if request.form['contact_number'] != '' else None

        # 调用添加读者的函数
        status = update_reader(library_card_number=library_card_number, name=name, gender=gender,
                               title=title, available_quantity=available_quantity, borrowed_quantity=borrowed_quantity,
                               department=department, contact_number=contact_number)
        print(status)
    return render_template('updatereader.html')


@app.route('/admin/Delete_reader', methods=['GET', 'POST'])
def Admin_delete_reader():
    data = print_all_reader_info()
    readers = data['data']['readers']
    return render_template('deletereader.html', data=readers)


@app.route('/get_data', methods=['GET'])
def get_data():
    data = print_all_reader_info()
    readers = data['data']['readers']
    return jsonify(readers)


@app.route('/delete_row', methods=['POST'])
def delete_row():
    code = request.form.get('library_card_number')
    status = delete_reader(code)
    if status['success']:
        return jsonify({'success': True, 'message': 'Deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Deletion failed'})


# 打印所有读者信息
@app.route('/admin/Admin_all_reader_info', methods=['GET', 'POST'])
def Admin_all_reader_info():
    data = print_all_reader_info()
    readers = data['data']['readers']
    return render_template('allReaderInfo.html', readers=readers)


@app.route('/admin/Get_reader_info', methods=['GET', 'POST'])
def Admin_get_reader_info():
    if request.method == 'POST' and request.form.get('library_card_number'):
        library_card_number = request.form.get('library_card_number')
        data = get_reader_info(library_card_number)
        reader = data['data']
        return render_template('getReaderInfo.html', reader=reader)
    else:
        data = print_all_reader_info()
        reader = data['data']
        return render_template('getReaderInfo.html', reader=reader)


@app.route('/admin/Get_reader_fines', methods=['GET', 'POST'])
def Admin_get_reader_fines():
    data = get_reader_fines()
    print(data)
    fines = data['data']['readers_fines']
    print(fines)
    return render_template('getReaderfines.html', fines=fines)


@app.route('/reader_detail_fines')
def reader_detail_fines():
    library_card_number = int(request.args.get('library_card_number'))
    try:
        data = print_fines_record(library_card_number)
        data = data['data']['fines_info']
        return render_template('reader_detail_fines.html', fines=data)

    except pyodbc.DatabaseError as e:
        return f"查询失败：{str(e)}"


@app.route('/user/index')
def User_home():
    """
    TODO:用户的主界面
    """
    return render_template('userindex.html')


@app.route('/user/select', methods=['GET', 'POST'])
def User_select_book():
    """
    查询和借书功能
    """
    books = []
    if request.method == 'POST':
        if 'search' in request.form:
            search_term = request.form['search_term']
            search_result = search_books(search_term)
            if search_result['success']:
                books = search_result['data']
            else:
                flash("查询失败: " + search_result["message"])
        elif 'isbn' in request.form:
            isbn = request.form['isbn']
            borrow_status = borrow_book(library_card_number=int(session['account']), isbn=isbn)
            if borrow_status['success']:
                flash("借书成功")
            else:
                flash("借书失败: " + borrow_status["message"])

    return render_template("user_select_book.html", books=books)


# 表单类
# 表单类
class UserForm(FlaskForm):
    library_card_number = StringField('Library Card Number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    available_quantity = StringField('Available Quantity', validators=[DataRequired()])
    borrowed_quantity = StringField('Borrowed Quantity', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    submit = SubmitField('Update Info')

@app.route('/user/info', methods=['GET', 'POST'])
def User_reader_info():
    form = UserForm()
    reader_data = {}
    borrowed_books_data = []

    if request.method == 'GET':
        user_data = get_reader_info(session['account'])

        if user_data['success']:
            reader_data = user_data['data']['reader_info']
            borrowed_books_data = user_data['data']['borrowed_books']
            form.library_card_number.data = reader_data['library_card_number']
            form.name.data = reader_data['name']
            form.gender.data = reader_data['gender']
            form.title.data = reader_data['title']
            form.available_quantity.data = reader_data['available_quantity']
            form.borrowed_quantity.data = reader_data['borrowed_quantity']
            form.department.data = reader_data['department']
            form.contact_number.data = reader_data['contact_number']
        else:
            flash(user_data['message'])
            return redirect(url_for('Login'))

    return render_template('user_reader_info.html', form=form, reader_data=reader_data, borrowed_books_data=borrowed_books_data)

@app.route('/user/borrow', methods=['GET', 'POST'])
def User_borrow():
    """
    TODO:当前借书信息
    """
    if request.method == 'POST':
        isbn = request.form['isbn']
        return_status = return_book(int(session['account']), isbn)
        if return_status['success']:
            flash("还书成功")
            session['return_data'] = return_status['data'][0]
            return redirect(url_for("after_return"))
        else:
            flash("还书失败 " + return_status['message'])
            return render_template('user_borrow.html')

    return render_template('user_borrow.html')


@app.route('/user/books_overdue')
def User_books_overdue():
    """
    用户逾期未归还的书籍
    """
    overdue_books = get_overdue_books()

    if overdue_books['success']:
        overdue_books_data = overdue_books['data']
    else:
        flash(overdue_books['message'])
        overdue_books_data = []

    return render_template('useroverdue.html', overdue_books_data=overdue_books_data)



@app.route('/user/test', methods=['GET', 'POST'])
def User_test():
    if request.method == 'POST':
        isbn = request.form['isbn']
        isread = request.form['isread']
        if isread == "借":
            borrow_status = borrow_book(library_card_number=int(session['account']), isbn=isbn)
            if borrow_status['success']:
                flash("借书成功")
                return render_template("test_borrow.html")
            else:
                flash("借书失败" + borrow_status["message"])
                return render_template("test_borrow.html")
        else:
            return_status = return_book(int(session['account']), isbn)
            if return_status['success']:
                flash("还书成功")
                print(return_status['data'])
                session['return_data'] = json.dumps(return_status['data'], default=str)
                return redirect(url_for("after_return"))
            else:
                flash("还书失败 " + return_status['message'])
                return render_template("test_borrow.html")
    return render_template("test_borrow.html")


@app.route('/user/notreturn')
def after_return():
    data = session.pop('return_data', None)  # 读取并移除 session 中的数据
    return render_template('after_return.html', book=data)


if __name__ == '__main__':
    app.run()
