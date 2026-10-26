from flask import Flask, request, make_response, redirect, url_for, send_from_directory, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


posts_db = []

LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head><title>MiniInsta - Login</title></head>
<body style="font-family: Arial, sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
    <div style="width: 320px; background: white; padding: 30px; border: 1px solid #dbdbdb; border-radius: 4px; text-align: center;">
        <h2 style="font-family: cursive; margin-bottom: 25px; color: #262626;">MiniInsta</h2>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username" style="width: 100%; padding: 9px; margin-bottom: 8px; border: 1px solid #dbdbdb; background: #fafafa; border-radius: 3px; box-sizing: border-box;"><br>
            <input type="password" name="password" placeholder="Password" style="width: 100%; padding: 9px; margin-bottom: 15px; border: 1px solid #dbdbdb; background: #fafafa; border-radius: 3px; box-sizing: border-box;"><br>
            <button type="submit" style="width: 100%; background: #0095f6; color: white; border: none; padding: 9px; border-radius: 4px; font-weight: bold; cursor: pointer;">Log In</button>
        </form>
    </div>
</body>
</html>
'''

FEED_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>MiniInsta - Feed</title></head>
<body style="font-family: Arial, sans-serif; background: #fafafa; margin: 0; padding: 20px;">
    <div style="max-width: 470px; margin: auto;">
        <h2 style="font-family: cursive; text-align: center; color: #262626;">MiniInsta Feed</h2>
        
        <!-- Upload Post Box -->
        <div style="background: white; border: 1px solid #dbdbdb; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
            <h4>Create New Post</h4>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="file" name="photo" accept="image/*" required style="margin-bottom: 10px;"><br>
                <input type="text" name="caption" placeholder="Write a caption..." style="width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #dbdbdb; border-radius: 4px; box-sizing: border-box;"><br>
                <button type="submit" style="background: #0095f6; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer;">Share Post</button>
            </form>
        </div>

        <!-- Dynamic Post Feed Loop -->
        {% for post in posts %}
        <div style="background: white; border: 1px solid #dbdbdb; border-radius: 8px; margin-bottom: 20px;">
            <div style="padding: 12px; font-weight: bold; border-bottom: 1px solid #efefef;">@{{ post.username }}</div>
            {% if post.filename %}
                <img src="/uploads/{{ post.filename }}" style="width: 100%; max-height: 400px; object-fit: cover;">
            {% else %}
                <div style="height: 200px; background: #efefef; display: flex; align-items: center; justify-content: center; color: #8e8e8e;">[No Image Attached]</div>
            {% endif %}
            <div style="padding: 12px;"><b>{{ post.username }}</b> {{ post.caption }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return LOGIN_PAGE

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == "relan" and password == "relan28":
        resp = make_response(redirect(url_for('feed')))
        resp.set_cookie('session_id', 'user_authenticated_123')
        return resp
    return "Invalid credentials!", 401

@app.route('/feed')
def feed():
    session_cookie = request.cookies.get('session_id')
    if session_cookie == 'user_authenticated_123':
        return render_template_string(FEED_TEMPLATE, posts=posts_db)
    return "Access Denied: Please log in first.", 403

@app.route('/upload', methods=['POST'])
def upload_file():
    session_cookie = request.cookies.get('session_id')
    if session_cookie != 'user_authenticated_123':
        return "Unauthorized", 403

    caption = request.form.get('caption', '')
    file = request.files.get('photo')
    
    filename = None
    if file and file.filename != '':
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    posts_db.insert(0, {"username": "relan", "caption": caption, "filename": filename})
    return redirect(url_for('feed'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)