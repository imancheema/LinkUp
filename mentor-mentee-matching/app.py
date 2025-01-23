from flask import Flask, render_template, request, redirect
import os
import pandas as pd
from matching import matching_process

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'mentees' not in request.files or 'mentors' not in request.files:
        return redirect(request.url)

    mentees_file = request.files['mentees']
    mentors_file = request.files['mentors']

    if mentees_file and allowed_file(mentees_file.filename) and mentors_file and allowed_file(mentors_file.filename):
        mentees_filename = mentees_file.filename
        mentors_filename = mentors_file.filename

        # uploaded files are stored in this folder
        mentees_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mentees_filename))
        mentors_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mentors_filename))

        mentees_df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], mentees_filename))
        mentors_df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], mentors_filename))

        matched_pairs = matching_process(mentees_df, mentors_df)

        return render_template('results.html', pairs=matched_pairs)

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
