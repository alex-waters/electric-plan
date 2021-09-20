import os
from flask import Flask, render_template, send_from_directory, request


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
