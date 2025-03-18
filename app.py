from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model for login/signup
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    attendance_rate = db.Column(db.Float, nullable=False)
    study_hours = db.Column(db.Float, nullable=False)
    previous_grade = db.Column(db.Float, nullable=False)
    extracurricular_activities = db.Column(db.Integer, nullable=False)
    parental_support = db.Column(db.String(10), nullable=False)
    final_grade = db.Column(db.Float, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Services route
@app.route('/services')
def services():
    return render_template('dashboard.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/predictor')
def predictor():
    return render_template('predictor.html')

@app.route('/faculty_home')
def faculty_home():
    return render_template('faculty.html')

@app.route('/student_predictor')
def student_predictor():
    return render_template('spredictor.html')

@app.route('/student_result')
def student_result():
    return render_template('student_result.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data from the HTML and store in a dictionary
    input_data = {
        'sex': request.form.get('sex'),
        'age': float(request.form.get('age', 0)),  # Default to 0 if not found
        'address': request.form.get('address'),
        'famsize': request.form.get('famsize'),
        'pstatus': request.form.get('Pstatus'),
        'medu': int(request.form.get('Medu', 0)),  # Default to 0 if not found
        'fedu': int(request.form.get('Fedu', 0)),  # Default to 0 if not found
        'mjob': request.form.get('Mjob'),
        'fjob': request.form.get('Fjob'),
        'reason': request.form.get('reason'),
        'guardian': request.form.get('guardian'),
        'traveltime': int(request.form.get('traveltime', 0)),  # Default to 0 if not found
        'studytime': int(request.form.get('studytime', 0)),  # Default to 0 if not found
        'failures': int(request.form.get('failures', 0)),  # Default to 0 if not found
        'schoolsup': request.form.get('schoolsup'),
        'famsup': request.form.get('famsup'),
        'paid': request.form.get('paid'),
        'internet': request.form.get('internet'),
        'romantic': request.form.get('romantic'),
        'famrel': int(request.form.get('famrel', 0)),  # Default to 0 if not found
        'freetime': int(request.form.get('freetime', 0)),  # Default to 0 if not found
        'health': int(request.form.get('health', 0)),  # Default to 0 if not found
    }

    # Call the model prediction function
    prediction, important_factors, next_factors = model_predict(input_data)


    col_msg = {
        'sex': 'Gender of the student',
        'age': 'Age of the student',
        'address': 'Address type (urban/rural)',
        'famsize': 'Family size',
        'pstatus': 'Parent status (living together or apart)',
        'medu': 'Mother’s education level',
        'fedu': 'Father’s education level',
        'mjob': 'Mother’s job',
        'fjob': 'Father’s job',
        'reason': 'Reason for choosing the school',
        'guardian': 'Guardian of the student',
        'traveltime': 'Travel time to school',
        'studytime': 'Weekly study time',
        'failures': 'Number of past class failures',
        'schoolsup': 'Extra educational support',
        'famsup': 'Family educational support',
        'paid': 'Extra paid classes',
        'activities': 'Extra-curricular activities',
        'nursery': 'Attended nursery school',
        'higher': 'Wants to take higher education',
        'internet': 'Internet access at home',
        'romantic': 'With a romantic relationship',
        'famrel': 'Quality of family relationships',
        'freetime': 'Free time after school',
        'goout': 'Going out with friends',
        'dalc': 'Dalc (weekday alcohol consumption)',
        'walc': 'Walc (weekend alcohol consumption)',
        'health': 'Current health status',
        'absences': 'Number of school absences',
    }

    # Render the 'student_result.html' template with the prediction and other details
    return render_template('student_result.html',
                           prediction=prediction,
                           important_factors=important_factors,
                           next_factors=next_factors,
                           col_msg=col_msg)


def model_predict(data):
    # This function should contain the logic to integrate your trained model
    # For example, using sklearn, TensorFlow, etc.
    # Replace the following line with your model's prediction logic
    prediction = "Your prediction logic here"
    important_factors = "Factors that influenced the prediction"
    next_factors = "Next steps or factors to consider"
    
    return prediction, important_factors, next_factors


@app.route('/student_home')
def student_home():
    # Assuming the user is a student and has logged in
    return render_template('student.html')

# Dashboard route to view and add students
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        student_id = request.form.get('id')
        if student_id:  # Update operation
            student = Student.query.get(student_id)
            if student:
                student.name = request.form['name']
                student.gender = request.form['gender']
                student.attendance_rate = request.form['attendance_rate']
                student.study_hours = request.form['study_hours']
                student.previous_grade = request.form['previous_grade']
                student.extracurricular_activities = request.form['extracurricular_activities']
                student.parental_support = request.form['parental_support']
                student.final_grade = request.form['final_grade']
                db.session.commit()
                flash('Student updated successfully!', 'success')
        else:  # Create operation
            new_student = Student(
                name=request.form['name'],
                gender=request.form['gender'],
                attendance_rate=request.form['attendance_rate'],
                study_hours=request.form['study_hours'],
                previous_grade=request.form['previous_grade'],
                extracurricular_activities=request.form['extracurricular_activities'],
                parental_support=request.form['parental_support'],
                final_grade=request.form['final_grade']
            )
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))

    # Fetch all students from the database
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

# Edit student route
@app.route('/dashboard/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        # Update student details
        student.name = request.form['name']
        student.gender = request.form['gender']
        student.attendance_rate = request.form['attendance_rate']
        student.study_hours = request.form['study_hours']
        student.previous_grade = request.form['previous_grade']
        student.extracurricular_activities = request.form['extracurricular_activities']
        student.parental_support = request.form['parental_support']
        student.final_grade = request.form['final_grade']

        db.session.commit()  # Commit changes to the database
        flash('Student updated successfully!', 'info')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', student=student)

@app.route('/dashboard/add', methods=['POST'])
def add_student():
    # Get form data
    name = request.form.get('name')
    gender = request.form.get('gender')
    attendance_rate = request.form.get('attendance_rate')
    study_hours = request.form.get('study_hours')
    previous_grade = request.form.get('previous_grade')
    extracurricular_activities = request.form.get('extracurricular_activities')
    parental_support = request.form.get('parental_support')
    final_grade = request.form.get('final_grade')

    # Create a new student object
    new_student = Student(
        name=name,
        gender=gender,
        attendance_rate=attendance_rate,
        study_hours=study_hours,
        previous_grade=previous_grade,
        extracurricular_activities=extracurricular_activities,
        parental_support=parental_support,
        final_grade=final_grade
    )

    # Add student to the database
    db.session.add(new_student)
    db.session.commit()

    # Flash a success message
    flash('Student added successfully!', 'success')

    return redirect(url_for('dashboard'))

# Delete student route
@app.route('/dashboard/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']  # Get user type from the form
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['userEmail'] = email  # Store user type in session
            flash("Login successful!", "success")
            if user_type == 'student':
                return redirect(url_for('student_home'))  # Student dashboard
            elif user_type == 'faculty':
                return redirect(url_for('faculty_home'))  # Faculty dashboard
        else:
            flash("Invalid credentials. Please try again.", "error")
    return render_template('login.html')

# User signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "error")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

# User logout route
@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('userEmail', None)  # Remove user email from session
    session.pop('userPassword', None)  # Remove user password from session
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
