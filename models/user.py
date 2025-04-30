from baseObject import baseObject
import pymysql
import hashlib

class user(baseObject):
    def __init__(self):
        self.setup()
        self.roles = [
            {'value': 'Faculty', 'text': 'Faculty'},
            {'value': 'Reviewer', 'text': 'Reviewer'},
            {'value': 'Dean', 'text': 'Dean'},
            {'value': 'Admin', 'text': 'Admin'}
        ]
        
    def hash_password(self, password):
        salt = 'xyz'
        return hashlib.md5((password + salt).encode('utf-8')).hexdigest()
    
    def get_valid_roles(self):
        return [role['value'] for role in self.roles]
    
    def is_valid_email(self, email):
        return '@' in email

    def email_exists(self, email):
        check_user = user()
        check_user.getByField('email', email)
        return len(check_user.data) > 0

    def verify_new(self, n=0):
        self.errors = []
        user_data = self.data[n]

        if not self.is_valid_email(user_data.get('email', '')):
            self.errors.append('Email must contain @')

        if user_data.get('role') not in self.get_valid_roles():
            self.errors.append(f"Role must be one of {self.get_valid_roles()}")

        if self.email_exists(user_data.get('email')):
            self.errors.append(f"Email address is already in use. ({user_data.get('email')})")

        if len(user_data.get('password', '')) < 3:
            self.errors.append('Password should be greater than 3 characters.')

        if user_data.get('password') != user_data.get('password2'):
            self.errors.append('Retyped password must match.')

        user_data['password_hash'] = self.hash_password(user_data['password'])
        del user_data['password']
        del user_data['password2']

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []
        user_data = self.data[n]

        if not self.is_valid_email(user_data.get('email', '')):
            self.errors.append('Email must contain @')

        if user_data.get('role') not in self.get_valid_roles():
            self.errors.append(f"Role must be one of {self.get_valid_roles()}")

        check_user = user()
        check_user.getByField('email', user_data.get('email'))
        if len(check_user.data) > 0 and check_user.data[0][check_user.pk] != user_data[self.pk]:
            self.errors.append(f"Email address is already in use. ({user_data.get('email')})")

        password = user_data.get('password', '')
        if password:
            if len(password) < 3:
                self.errors.append('Password should be greater than 3 characters.')
            else:
                user_data['password_hash'] = self.hash_password(password)
            del user_data['password']
        else:
            user_data.pop('password', None)

        return len(self.errors) == 0

    def try_login(self, email, password):
        hashed_pw = self.hash_password(password)
        sql = f'SELECT * FROM `{self.tn}` WHERE `email` = %s AND `password_hash` = %s AND is_verified = 1 AND status = "active";'
        tokens = [email, hashed_pw]
        self.cur.execute(sql, tokens)
        self.data = [row for row in self.cur]
        return len(self.data) == 1

    def update_last_login(self, user_id):
        sql = 'UPDATE users SET last_login = NOW() WHERE user_id = %s'
        self.cur.execute(sql, [user_id])

    def get_all_reviewers(self):
        self.cur.execute("SELECT user_id, name FROM users WHERE role IN ('Reviewer', 'Dean', 'Faculty')")
        return self.cur.fetchall()