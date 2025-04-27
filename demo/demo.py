from flask import Flask, request, render_template

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


if __name__ == '__main__':
    app.run(debug=True)
