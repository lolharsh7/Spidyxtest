
from flask import Flask, render_template, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["GET"])
def download():
    m3u8_url = request.args.get("url")
    if not m3u8_url:
        return "Missing 'url' parameter", 400

    filename = f"/tmp/{uuid.uuid4()}.mp4"

    try:
        # Run ffmpeg to download and convert m3u8 to mp4
        cmd = [
            "ffmpeg", "-i", m3u8_url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-y", filename
        ]
        subprocess.run(cmd, check=True)

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error during download: {e}", 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
