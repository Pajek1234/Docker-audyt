from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecret123')

DB_HOST = os.environ.get('DB_HOST', 'mysql')
DB_USER = os.environ.get('DB_USER', 'root')
# BŁĄD VULN-03: Hasło w zmiennej środowiskowej Dockerfile
DB_PASS = os.environ.get('DB_PASSWORD', 'Admin123!')
DB_NAME = os.environ.get('DB_NAME', 'gastroshop')


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/')
def index():
    user = session.get('user')
    cart = session.get('cart', [])
    return render_template('index.html', user=user, cart=cart, cart_count=len(cart))


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if not email or not password:
        return render_template('index.html', user=None, cart=[], cart_count=0,
                               login_error='Wypełnij oba pola.', active_tab='login')
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # BŁĄD VULN-01: SQL Injection — brak parametryzacji zapytania
        query = "SELECT * FROM users WHERE email='%s' AND password='%s'" % (email, password)
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = {'id': user['id'], 'name': user['name'],
                               'email': user['email'], 'role': user['role']}
            return redirect(url_for('index'))
        else:
            return render_template('index.html', user=None, cart=[], cart_count=0,
                                   login_error='Nieprawidłowy e-mail lub hasło.', active_tab='login')
    except Exception as e:
        return render_template('index.html', user=None, cart=[], cart_count=0,
                               login_error='Błąd SQL: ' + str(e), active_tab='login')


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '').strip()
    email = request.form.get('reg_email', '').strip()
    password = request.form.get('reg_pass', '')

    if not name or not email or not password:
        return render_template('index.html', user=None, cart=[], cart_count=0,
                               reg_error='Wypełnij wszystkie pola.', active_tab='register')
    if len(password) < 6:
        return render_template('index.html', user=None, cart=[], cart_count=0,
                               reg_error='Hasło musi mieć min. 6 znaków.', active_tab='register')
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # BŁĄD VULN-02: Hasło zapisane jako plaintext — brak bcrypt/argon2
        # BŁĄD VULN-01: SQL Injection w rejestracji — brak parametryzacji
        query = "INSERT INTO users(name, email, password, role) VALUES('%s','%s','%s','klient')" % (name, email, password)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return render_template('index.html', user=None, cart=[], cart_count=0,
                               reg_success='Konto utworzone! Możesz się teraz zalogować.', active_tab='register')
    except Exception as e:
        conn.close()
        if 'Duplicate entry' in str(e):
            msg = 'Ten e-mail już istnieje w bazie.'
        else:
            msg = 'Błąd: ' + str(e)
        return render_template('index.html', user=None, cart=[], cart_count=0,
                               reg_error=msg, active_tab='register')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/cart/add', methods=['POST'])
def cart_add():
    product = request.form.get('product')
    price = request.form.get('price')
    if product:
        cart = session.get('cart', [])
        cart.append({'name': product, 'price': price})
        session['cart'] = cart
    return redirect(url_for('index') + '#produkty')


@app.route('/cart/clear')
def cart_clear():
    session['cart'] = []
    return redirect(url_for('index') + '#produkty')


@app.route('/users')
def users():
    """Endpoint tylko dla admina — lista użytkowników z bazy (do panelu audytu)"""
    if not session.get('user') or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Brak dostępu'}), 403
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, password, role FROM users ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
