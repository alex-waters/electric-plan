import os
import time
import live_data_collect
from flask import Flask, render_template, send_from_directory, request, Response

# instantiate app with static path to help PA distributed filesystem
app = Flask(
    __name__,
    static_url_path='/home/anw/mysite/electric-plan/static/'
)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.route('/', methods=['GET', 'POST'])
def region_choice():

    if request.method == 'GET':

        page = render_template('layout.html')
        print('just get')
    elif request.method == 'POST':
        chosen_region = int(request.form.getlist("menu")[0])
        print(chosen_region)
        if chosen_region == 5:
            page = render_template('carbon_plot_5.html')
        elif chosen_region in (*range(1, 3), *range(4, 15)):
            render_template('wait.html')
            live_data_collect.NewPlot(chosen_region).gen_plot()
            time.sleep(7)
            page = render_template(
                'carbon_plot_{}.html'.format(chosen_region))

    return page


@app.route('/ips', methods=['GET', 'POST'])
def serve_file():
    with open('/home/anw/mysite/electric-plan/static/ips.txt', 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/plain')


@app.route('/steps', methods=['GET'])
def watch_vis():

    page = render_template('layout_watch.html')

    return page


if __name__ == '__main__':
    port = app.config.get("PORT", 5000)
    app.run(port=port)
