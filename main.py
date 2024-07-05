from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from qr_app import generate_qr
from io import BytesIO
import base64

app = FastAPI()


@app.get("/")
def get_index(response_class=HTMLResponse):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        div {
        display: flex;
        justify-content: center;
        align-items: center;
        }
        #qr-container {
            padding: 32px;
        }
        </style>
        <title>QR generator</title>
        <script src="https://unpkg.com/htmx.org@2.0.0"></script>
    </head>
    <body>
        <div id="content">
            <textarea hx-get="/get-qr" hx-target="#qr-container" hx-swap="innerHTML" hx-trigger="input changed delay:100ms" name="qr_data"></textarea>
        </div>
        <div id="qr-container"></div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/get-qr")
def get_qr(qr_data: str = Query("")):
    img = generate_qr(qr_data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    html_content = f'<img src="data:image/png;base64,{img_base64}" alt="QR Code" />'
    return HTMLResponse(content=html_content, status_code=200)
