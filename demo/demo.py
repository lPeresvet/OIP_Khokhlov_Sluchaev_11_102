import os.path

from flask import Flask, request, render_template, send_from_directory

from hw_4.tf_idf_calculation import PROJECT_ROOT
from hw_5.searcher import VectorSearch

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = []

    if query:
        searcher = VectorSearch()
        results = searcher.search(query)

    return render_template('search.html', results=results, query=query)

@app.route('/pages/<page>', methods=['GET'])
def show_page(page):
    return send_from_directory(os.path.join(PROJECT_ROOT, "out"), page)

if __name__ == '__main__':
    app.run(debug=False)
