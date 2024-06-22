from flask import Flask, request,render_template,send_file
from login import *
from admin import *
app = Flask(__name__)

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        account=request.form['account']
        password = request.form['password']
        login_status=login(account,password)
        if login_status['success']==True:
            print(login_status['data'])
    return render_template('login.html')
# 管理员页面
@app.route('/index', methods=['GET', 'POST'])
def Admin_menu():

    return render_template('base.html')


# 添加图书
@app.route('/Add_book', methods=['GET','POST'])
def Add_book():
    if request.method == 'POST':
        isbn=request.form['isbn']
        book_title = request.form['book_title']

        publisher = request.form['publisher'] if request.form['publisher'] != '' else None
        author = request.form['author'] if request.form['author'] != '' else None
        total_quantity = int(request.form['total_quantity']) if request.form.get('total_quantity') else 10
        available_quantity = int(request.form['available_quantity']) if request.form.get('available_quantity') else 10

        is_borrowable = request.form['is_borrowable']
        print(isbn,is_borrowable)
        status=add_book(isbn=isbn, book_title=book_title, publisher=publisher, author=author, total_quantity=total_quantity, available_quantity=available_quantity, is_borrowable=is_borrowable)
        print(status)
        # if status['success']==True:
        #     print(status)
    return render_template('addbook.html')

# 到期未还图书
@app.route('/Overdue_book', methods=['GET', 'POST'])
def Overdue_book():
    return render_template('overduebook.html')

if __name__ == '__main__':
    app.run()
