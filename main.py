from flask import Flask, redirect, render_template, request, url_for
from pathlib import Path
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = Path("static/uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        img = request.files["image"]
        img_path = UPLOAD_FOLDER / img.filename
        img.save(img_path)
        uploaded_img = Image.open(img_path)

        try:
            img_rgb = uploaded_img.convert("RGB")

        except Exception:
            print(f"Error: {Exception}")

        else:
            colors = img_rgb.getcolors(uploaded_img.size[0] * uploaded_img.size[1])

            top_colors = sorted(colors, reverse=True)[:10]

            hex_top_colors = []

            for element in top_colors:
                rgb = element[1]
                hex_value = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
                hex_top_colors.append(hex_value)

            print(hex_top_colors)

        return render_template("index.html", filename=img.filename, hex_colors=hex_top_colors)
        
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

