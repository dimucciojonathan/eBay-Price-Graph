from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import DashboardFunctions

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def link_form():
    if "boxplot" in request.form:
        item_search = request.form['boxplot']
        session['url'] = item_search
        return redirect(url_for('box_plot'))
    elif "statistics" in request.form:
        item_search = request.form['statistics']
        session['url'] = item_search
        return redirect(url_for('statistics'))
    else:
        return render_template('link-form.html')


@app.route('/dashboard', methods=['GET'])
def box_plot():
    new_var = session.get('url')
    df = DashboardFunctions.get_sold_info_dataframe(new_var, 25)
    graph = DashboardFunctions.box_to_bytes(df)

    return send_file(graph,
                     attachment_filename='plot.png',
                     mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)