import os
from flask import Flask, render_template, send_from_directory, request


app = Flask(__name__)

# del the old carbon plot explicitly
os.remove('templates/carbon_plot.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.route('/', methods=['GET', 'POST'])
def asset_refine():

    page = render_template('carbon_plot.html')
    return page


if __name__ == '__main__':
    port = app.config.get("PORT", 5000)
    app.run(port=port)
