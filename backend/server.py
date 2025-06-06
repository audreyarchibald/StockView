import json
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from backtest import backtest
from scanner import scan


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    if path == '/backtest':
        size = int(environ.get('CONTENT_LENGTH', 0) or 0)
        body = environ['wsgi.input'].read(size)
        params = json.loads(body.decode() or '{}')
        data = params.get('data', 'data/sample_stock.csv')
        short = int(params.get('short', 5))
        long = int(params.get('long', 20))
        result = backtest(data, short, long)
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json.dumps(result).encode()]
    elif path == '/scan':
        query = parse_qs(environ.get('QUERY_STRING', ''))
        data = query.get('data', ['data/sample_stock.csv'])[0]
        short = int(query.get('short', ['5'])[0])
        long = int(query.get('long', ['20'])[0])
        result = scan(data, short, long)
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json.dumps(result).encode()]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']


def serve(host='0.0.0.0', port=8000):
    print(f"Serving on {host}:{port} ...")
    with make_server(host, port, application) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    serve()
