import os
import shutil
from flask import Flask, render_template, request

from HEE.image_processing import get_user_image_path, process_image
from HEE.model import Model, solve_equation

app = Flask(__name__)

print('Initializing model ....')
model = Model()
print('Model initialized!')

@app.route("/help")
def help_menu():
    return render_template("help.html")

@app.route('/', methods=['GET', 'POST'])
def start():
    # PATH -> user's image path.
    # IMG_PATH -> Path where image will be copied.

    PATH, IMG_PATH, equation, result = '', '', '', ''
    if request.method == 'POST':

        # Get path from user and copy image to 'static' path.
        PATH = get_user_image_path()
        if PATH != '':
            IMG_PATH = "static/" + os.path.basename(PATH)

            shutil.copy(PATH, IMG_PATH)

            # Convert image to list of 28*28*1 sized images of characters.
            image_list = process_image(IMG_PATH)

            # Predict equation and result from model.
            equation = model.predict_equation(image_list)
            result = str(solve_equation(equation))

    return render_template('app.html', image_path=IMG_PATH, equation=equation, result=result)


if __name__ == '__main__':
    app.run(debug=False)
