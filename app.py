from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import os

app = Flask(__name__, static_folder="static", template_folder=".")

@app.route('/', methods=['GET', 'POST'])
def index():
    with open('upload.html', 'r') as f:
        template = f.read()

    if request.method == 'POST':
        number = request.form.get('number_input')
        
        # Handle number processing
        if not number:
            return 'No number provided', 400

        result = float(number) ** 2

        # Handle CSV processing
        uploaded_file = request.files.get('file')
        position = request.form.get('position', 'top')
        
        if uploaded_file and uploaded_file.filename != '':
            df = pd.read_csv(uploaded_file)
            
            # Depending on the position, get the top or bottom row
            if position == 'top':
                first_col_values = df.iloc[0, :].tolist()
            else:  # Bottom
                first_col_values = df.iloc[-1, :].tolist()
            
            return jsonify({'number_square': result, 'selected_row': first_col_values})

        return jsonify({'number_square': result})

    return render_template_string(template)
if __name__ == '__main__':
    app.run(debug=True)