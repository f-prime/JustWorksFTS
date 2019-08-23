from sanic import Sanic
from sanic.response import json
from engine import search, index
from concurrent.futures import ThreadPoolExecutor

app = Sanic()

tpe = ThreadPoolExecutor(max_workers=5)

def indexer(data):
    for item in data:
        index.index(item['text'], item['object']) 

@app.route("/search")
async def search_route(request):
    arguments = dict(request.query_args)
    query = arguments.get("q")
    if not query:
        return json([])
    return json(search.search(query))

@app.route("/index", methods=['POST'])
async def index_route(request):
    if not request.json:
        return json({"error":"No data to index"})
    index.index(request.json['text'], request.json['object'])
    return json({"message":"Indexed"})

@app.route("/bulk-index", methods=['POST'])
async def bulk_index(request):
    if not request.json:
        return json({"error":"No data to index"})
    if type(request.json) != list:
        return json({"error":"Data must be a list of strings"})
    tpe.submit(indexer, request.json)
    return json({"message":"Indexed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
