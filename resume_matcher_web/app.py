from flask import Flask, render_template, request, jsonify
import os
import tempfile
from matcher_logic import clean_text, extract_text_from_pdf, calculate_match

app = Flask(__name__)

# Basic settings
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload size
UPLOAD_FOLDER = tempfile.gettempdir()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/match', methods=['POST'])
def match():
    resume_text = ""
    job_text = request.form.get('job_description', '')
    
    # Check if user provided resume as text
    resume_text_input = request.form.get('resume_text', '')
    
    if resume_text_input:
        resume_text = resume_text_input
    
    # Check if user uploaded a file
    elif 'resume_file' in request.files:
        file = request.files['resume_file']
        if file.filename != '':
            if file.filename.endswith('.pdf'):
                # Save temporarily to parse
                temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(temp_path)
                resume_text = extract_text_from_pdf(temp_path)
                try:
                    os.remove(temp_path)
                except:
                    pass
            elif file.filename.endswith('.txt'):
                resume_text = file.read().decode('utf-8')
            else:
                return jsonify({'error': 'Unsupported file format. Please upload PDF or TXT.'}), 400

    if not resume_text or not job_text:
        return jsonify({'error': 'Please provide both a resume and a job description.'}), 400

    result = calculate_match(resume_text, job_text)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
