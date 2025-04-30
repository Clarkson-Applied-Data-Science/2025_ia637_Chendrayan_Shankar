from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
import time
import datetime
from models.user import user
from models.dossier import dossier
from models.evaluation import evaluation
from models.evaluation_stage import evaluation_stage
from models.evaluation_comments import evaluation_comments
import os
from werkzeug.utils import secure_filename

app = Flask(__name__,static_url_path='')

app.config['SECRET_KEY'] = '5sdghsgRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

@app.route('/')
def home():
    return redirect('/login')

@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    if value is None:
        return ''
    try:
        return value.strftime(format)
    except AttributeError:
        return 'NA'

app.jinja_env.filters['format_datetime'] = format_datetime

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.form.get('email') is not None and request.form.get('password') is not None:
        u = user()
        if u.try_login(request.form.get('email'),request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:   
        if 'msg' not in session.keys() or session['msg'] is None:
            m = ''
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)    
    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return redirect('/login')
    #return render_template('login.html', title='Login', msg='You have logged out.')
@app.route('/main')
def main():
    if checkSession() == False: 
        return redirect('/login')
    
    if session['user']['role'] == 'Admin':
        return render_template('admin/admin.html', title='Main menu') 
    else:
        return render_template('index.html', title='Homepage') 

@app.route('/admin/users/manage',methods=['GET','POST'])
def manage_user():
    if checkSession() == False: #or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.", redirect_url="/admin/users/manage")
    if action is not None and action == 'insert':
        d = {}
        d['name'] = request.form.get('name')
        d['email'] = request.form.get('email')
        d['role'] = request.form.get('role')
        d['password'] = 'password'
        d['password2'] = 'password'
        d['is_verified'] = 1
        d['status'] = 'active'
        o.set(d)
        if o.verify_new():
            #print(o.data)
            o.insert()
            return render_template('ok_dialog.html',msg= "User added.", redirect_url="/admin/users/manage")
        else:
            return render_template('admin/users/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        if request.form and any(request.form.values()):
            o.data[0]['name'] = request.form.get('name')
            o.data[0]['email'] = request.form.get('email')
            o.data[0]['role'] = request.form.get('role')
            o.data[0]['password'] = request.form.get('password_hash')
            o.data[0]['password2'] = request.form.get('password2')
            if o.verify_update():
                o.update()
                return render_template('ok_dialog.html',msg= "User updated.", redirect_url="/admin/users/manage")
        else:
            return render_template('admin/users/manage.html',obj = o)
    if pkval is None:
        o.getAll()
        return render_template('admin/users/list.html',obj = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('admin/users/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('admin/users/manage.html',obj = o)

# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#standalone function to be called when we need to check if a user is logged in.
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        #print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False   

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = user()
        u.data = [{
            'email': request.form.get('email', '').strip(),
            'name': request.form.get('name', '').strip(),
            'role': 'Faculty',  # Hardcoded here for security,
            'status': 'active',
            'is_verified': 1,
            'password': request.form.get('password', ''),
            'password2': request.form.get('password2', '')
        }]
        
        if u.verify_new():
            u.insert()
            session['user'] = u.data[0]
            return redirect('main')  # redirect to dashboard or login
        else:
            return render_template('register.html', title='Register', errors=u.errors, form=request.form)

    return render_template('register.html', title='Register', form={})

@app.route('/admin/users/delete/<int:id>')
def delete_user(id):
    u = user()
    u.deleteById(id)
    return render_template('ok_dialog.html',msg= "Deleted.", redirect_url="/admin/users/manage")

@app.route('/admin/evaluations/create', methods=['GET', 'POST'])
def create_evaluation():
    from models.dossier import dossier
    from models.evaluation import evaluation
    from models.evaluation_stage import evaluation_stage
    from models.user import user
    from models.stage_reviewers import stage_reviewers

    # Get all dossiers
    d = dossier()
    d.cur.execute("""
        SELECT d.dossier_id, d.title, u.name
        FROM dossiers d JOIN users u ON d.user_id = u.user_id
        WHERE d.status = 'Submitted'
    """)
    dossiers = d.cur.fetchall()

    # Get all reviewers using model method
    u = user()
    reviewers = u.get_all_reviewers()

    if request.method == 'POST':
        dossier_id = request.form.get('dossier_id')
        total_stages = int(request.form.get('total_stages', 0))

        # Create evaluation
        e = evaluation()
        e.data.append({'dossier_id': dossier_id})
        e.insert()
        evaluation_id = e.data[0]['evaluation_id']

        # Loop through all stages
        for i in range(1, total_stages + 1):
            stage_name = request.form.get(f'stage_name_{i}')
            stage_order = request.form.get(f'stage_order_{i}')
            reviewer_ids = request.form.getlist(f'reviewers_{i}[]')

            if stage_name and reviewer_ids:
                # Create stage
                s = evaluation_stage()
                s.data.append({
                    'evaluation_id': evaluation_id,
                    'stage_name': stage_name,
                    'stage_order': stage_order,
                    'status': 'Pending'
                })
                s.insert()
                stage_id = s.data[0]['stage_id']

                # Assign reviewers using model
                for reviewer_id in reviewer_ids:
                    sr = stage_reviewers()
                    sr.data.append({
                        'stage_id': stage_id,
                        'reviewer_id': reviewer_id,
                        'status': 'Pending'
                    })
                    sr.insert()

        return render_template("ok_dialog.html", msg="Evaluation created successfully.", redirect_url="/admin/evaluations")

    return render_template("admin/evaluations/create.html", dossiers=dossiers, reviewers=reviewers)

@app.route('/dossiers/<int:dossier_id>/status')
def dossier_status(dossier_id):
    from models.evaluation import evaluation
    from models.evaluation_stage import evaluation_stage

    # Step 1: Get the evaluation associated with the dossier
    e = evaluation()
    e.get_by_dossier(dossier_id)
    if not e.data:
        return render_template("ok_dialog.html", msg="No evaluation found for this dossier.")

    evaluation_id = e.data[0]['evaluation_id']

    # Step 2: Get the current active stage (the first 'Pending' stage)
    stage = evaluation_stage()
    stage.get_current_stage(evaluation_id)

    if not stage.data:
        return render_template("ok_dialog.html", msg="All stages are complete.")

    # Step 3: Display the current stage and reviewer
    return render_template(
        "ok_dialog.html",
        msg=f"Current stage: {stage.data[0]['stage_name']} — Reviewer ID: {stage.data[0]['reviewer_id']}"
    )

@app.route('/dossiers/mine')
def my_dossiers():
    from models.dossier import dossier

    d = dossier()
    d.cur.execute("SELECT * FROM dossiers WHERE user_id = %s ORDER BY created_at DESC", (session['user']['user_id'],))
    dossiers = d.cur.fetchall()

    return render_template("dossiers_mine.html", dossiers=dossiers)

@app.route('/dossiers/new', methods=['GET', 'POST'])
def create_dossier():
    from models.dossier import dossier

    if request.method == 'POST':
        d = dossier()
        d.data.append({
            'user_id': session['user']['user_id'],
            'title': request.form.get('title'),
            'status': 'Submitted'
        })
        d.insert()
        return render_template("ok_dialog.html", msg="Dossier submitted successfully.", redirect_url="/dossiers/mine")

    return render_template("dossiers_submit.html")

@app.route('/dossiers/<int:dossier_id>/progress')
def dossier_progress(dossier_id):
    from models.evaluation import evaluation
    from models.evaluation_stage import evaluation_stage

    # Get the evaluation for the dossier
    e = evaluation()
    e.get_by_dossier(dossier_id)
    if not e.data:
        return render_template("ok_dialog.html", msg="No evaluation found for this dossier.", redirect_url="/dossiers/mine")
    
    evaluation_id = e.data[0]['evaluation_id']

    # Get all stages ordered by stage_order
    s = evaluation_stage()
    s.get_by_evaluation(evaluation_id)

    return render_template("dossiers_progress.html", stages=s.data)

@app.route('/reviews/edit/<int:assignment_id>', methods=['GET', 'POST'])
def edit_review(assignment_id):
    from models.stage_reviewers import stage_reviewers
    from models.evaluation_stage import evaluation_stage
    from models.evaluation_comments import evaluation_comments
    from models.documents import documents
    from models.user import user
    import os
    from werkzeug.utils import secure_filename
    import datetime

    # Step 1: Get the reviewer assignment
    sr = stage_reviewers()
    sr.getById(assignment_id)

    if not sr.data or sr.data[0]['reviewer_id'] != session['user']['user_id']:
        return render_template("ok_dialog.html", msg="Unauthorized or invalid review assignment.", redirect_url="/reviews/assigned")

    stage_id = sr.data[0]['stage_id']

    # Step 2: Load stage info
    s = evaluation_stage()
    s.getById(stage_id)
    if not s.data:
        return render_template("ok_dialog.html", msg="Stage not found.", redirect_url="/reviews/assigned")
    stage_data = s.data[0]
    evaluation_id = stage_data['evaluation_id']

    # Step 3: Handle POST (submit review)
    if request.method == 'POST':
        sr.data[0]['status'] = 'Completed'
        sr.update()

        # Save comment
        c = evaluation_comments()
        c.data.append({
            'stage_id': stage_id,
            'commenter_id': session['user']['user_id'],
            'comment': request.form.get('comment'),
            'created_at': datetime.datetime.now()
        })
        c.insert()

        # Save uploaded file
        file = request.files.get('review_file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_dir = os.path.join("static", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            d = documents()
            d.data.append({
                'stage_id': stage_id,
                'reviewer_id': session['user']['user_id'],
                'title': filename,
                'file_path': file_path
            })
            d.insert()

        return render_template("ok_dialog.html", msg="Review and document submitted successfully.", redirect_url="/reviews/assigned")

    # Step 4: Fetch reviewer names
    u = user()
    u.cur.execute("SELECT user_id, name FROM users")
    user_map = {row["user_id"]: row["name"] for row in u.cur.fetchall()}

    # Step 5: Load all comments and tag with reviewer name
    c = evaluation_comments()
    c.get_by_evaluation(evaluation_id)
    for comment in c.data:
        comment["reviewer_name"] = user_map.get(comment["commenter_id"], f"Reviewer {comment['commenter_id']}")

    # Step 6: Load all documents and tag with reviewer name
    d = documents()
    d.get_by_evaluation(evaluation_id)
    for doc in d.data:
        doc["reviewer_name"] = user_map.get(doc["reviewer_id"], f"Reviewer {doc['reviewer_id']}")

    return render_template("reviews_edit.html", stage=stage_data, comments=c.data, documents=d.data)


@app.route('/reviews/view/<int:evaluation_id>')
def view_evaluation(evaluation_id):
    from models.stage_reviewers import stage_reviewers
    from models.evaluation_stage import evaluation_stage
    from models.evaluation_comments import evaluation_comments
    from models.documents import documents
    from models.user import user

    user_id = session['user']['user_id']

    # Step 1: Get all stage IDs for this evaluation
    es = evaluation_stage()
    es.get_by_evaluation(evaluation_id)
    stage_ids = [row['stage_id'] for row in es.data]

    if not stage_ids:
        return render_template("ok_dialog.html", msg="No stages found for this evaluation.", redirect_url="/reviews/assigned")

    # Step 2: Check if this user is assigned to any of those stages
    sr = stage_reviewers()
    sr.cur.execute("""
        SELECT * FROM stage_reviewers
        WHERE reviewer_id = %s AND stage_id IN %s
    """, (user_id, tuple(stage_ids)))

    if not sr.cur.rowcount:
        return render_template("ok_dialog.html", msg="You are not authorized to view this evaluation.", redirect_url="/reviews/assigned")

    # Step 3: Load comments and documents (with reviewer names)
    u = user()
    u.cur.execute("SELECT user_id, name FROM users")
    user_map = {u["user_id"]: u["name"] for u in u.cur.fetchall()}

    c = evaluation_comments()
    c.get_by_evaluation(evaluation_id)
    for comment in c.data:
        comment["reviewer_name"] = user_map.get(comment["commenter_id"])

    d = documents()
    d.get_by_evaluation(evaluation_id)
    for doc in d.data:
        doc["reviewer_name"] = user_map.get(doc["reviewer_id"])

    return render_template("reviews_view.html", comments=c.data, documents=d.data, evaluation_id=evaluation_id)

@app.route('/reviews/assigned')
def assigned_reviews():
    from models.stage_reviewers import stage_reviewers
    from models.evaluation_stage import evaluation_stage

    # Step 1: Get all assignments from stage_reviewers for current user
    sr = stage_reviewers()
    sr.cur.execute("""
        SELECT sr.stage_id, sr.status, sr.id AS assignment_id,
               es.stage_name, es.evaluation_id
        FROM stage_reviewers sr
        JOIN evaluation_stages es ON sr.stage_id = es.stage_id
        WHERE sr.reviewer_id = %s
        ORDER BY es.stage_order
    """, (session['user']['user_id'],))
    assignments = sr.cur.fetchall()

    return render_template("reviews_assigned.html", reviews=assignments)

@app.route('/admin/evaluations')
def admin_evaluations():
    from models.evaluation import evaluation
    from models.evaluation_stage import evaluation_stage

    # Step 1: Get all evaluations
    e = evaluation()
    e.cur.execute("""
        SELECT e.evaluation_id, d.title AS dossier_title, u.name AS faculty_name, e.dossier_id
        FROM evaluations e
        JOIN dossiers d ON e.dossier_id = d.dossier_id
        JOIN users u ON d.user_id = u.user_id
        ORDER BY e.evaluation_id DESC
    """)
    evaluations = e.cur.fetchall()

    # Step 2: Fetch current stage for each evaluation
    for ev in evaluations:
        s = evaluation_stage()
        s.get_current_stage(ev['evaluation_id'])
        ev['current_stage'] = s.data[0] if s.data else None

    return render_template("admin/evaluations/list.html", evaluations=evaluations)

if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   