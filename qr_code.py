from flask import Flask, render_template_string, request, send_file
import qrcode
import io
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QR Code Generator</title>
    <style>
        body{font-family: Arial; background:#0f172a; color:white; display:flex; align-items:center; justify-content:center; height:100vh}
        .card{background:#111827; padding:30px; border-radius:16px; box-shadow:0 10px 30px rgba(0,0,0,.5); width:350px; text-align:center}
        input,button{width:100%; padding:12px; margin:10px 0; border-radius:8px; border:none}
        input{background:#1f2937; color:white}
        button{background:#22c55e; color:black; font-weight:bold; cursor:pointer}
        img{margin-top:15px; width:200px}
    </style>
</head>
<body>
    <div class="card">
        <h2>QR Code Generator</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Image name" required>
            <input type="text" name="url" placeholder="Enter URL or text" required>
            <button type="submit">Generate QR</button>
        </form>
        {% if qr_img %}
            <img src="{{ qr_img }}" alt="QR Code">
            <a href="{{ qr_img }}" download="qr.png"><button>Download</button></a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    qr_img = None
    if request.method == 'POST':
        data = request.form['url']
        img = qrcode.make(data)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        qr_img = 'data:image/png;base64,' + __import__('base64').b64encode(buf.getvalue()).decode()
    return render_template_string(HTML, qr_img=qr_img)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)   