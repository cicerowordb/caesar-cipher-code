"""
A simple web application that demonstrates a Caesar Cipher encryption technique.

This module provides a Flask application that allows users to encrypt text using
the Caesar Cipher method through a web interface. It supports handling GET and
POST requests to render forms and process encryption based
on user input.
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

def caesar_cipher(text, shift):
    """
    Encrypts text using the Caesar Cipher technique.
    Args:
        text (str): The text to be encrypted.
        shift (int): The number of positions each character in the text should be shifted.
    Returns:
        str: The encrypted text.
    """
    encrypted = ''
    for char in text:
        code = ord(char) + shift
        while code > 255:
            code -= 255
        while code < 0:
            code += 255
        encrypted += chr(code)
    return encrypted

def render_form(encrypted_text=None, error=None):
    """
    Renders an HTML form for text encryption.
    Optionally includes a result of encryption or an error message within the form.
    Args:
        encrypted_text (str, optional): The result of an encryption to be displayed. 
                        Defaults to None.
        error (str, optional): An error message to be displayed if there was an issue
                        with encryption. Defaults to None.
    Returns:
        str: An HTML string of the form for user interaction.
    """
    form_html = '''
        <h1>Caesar Cipher</h1>
        <form method="post">
            Text: <input type="text" name="text"><br>
            Shift: <input type="number" name="shift"><br>
            <input type="submit" value="Encrypt">
        </form>
    '''
    if encrypted_text:
        form_html += f'<p>Encrypted Text: {encrypted_text}</p>'
    if error:
        form_html += f'<p style="color:red;">{error}</p>'
    return render_template_string(form_html)

def process_caesar_cipher():
    """
    Processes the encryption request from form data.
    Retrieves data from the form, attempts to encrypt the provided text, and renders the form with the result or error message.
    Returns:
        str: The rendered HTML form including any results or error messages.
    """
    text = request.form.get('text')
    shift_str = request.form.get('shift')
    if text is None or shift_str is None:
        return render_form(error="ERROR: Please fill out all fields.")
    try:
        shift = int(shift_str)
    except ValueError:
        return render_form(error="ERROR: Shift must be an integer.")

    encrypted_text = caesar_cipher(text, shift)
    return render_form(encrypted_text)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Root endpoint handler for GET and POST requests.
    Renders the form on GET requests and processes the form on POST requests.
    Returns:
        str: The rendered HTML form or the form with results/error message.
    """
    if request.method == 'POST':
        return process_caesar_cipher()
    else:
        return render_form()

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=False)
