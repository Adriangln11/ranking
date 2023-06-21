import http.server
import socketserver
import json


PORT = 8000

def load_data():
    try:
        with open('movies.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []

def save_data(data):
    with open('movies.json', 'w') as file:
        json.dump(data, file)

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            data = load_data()
            content = ""
            for movie in data:
                content += f'<li class="list-group-item">{movie["title"]}: {movie["rating"]}</li>'
            
            response = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="https://bootswatch.com/5/darkly/bootstrap.min.css">
                <title>Miniproyectos | Ranking de Peliculas</title>
            </head>
            <body>
                <main class="container d-flex flex-column align-items-center text-center">
                    <h1 class="m-5">Ranking</h1>
                    <form class="d-flex flex-column" method="POST" action="/add_movie">
                        <label>Título de la película:</label>
                        <input type="text" name="title" required><br>
                        <label>Calificación de la película (0-5):</label>
                        <input type="number" name="rating" min="0" max="5" step="0.1" required><br>
                        <input type="submit" value="Agregar película">
                    </form>
                    <ul class="list-group list-group-flush m-5">{content}</ul>
                </main>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/add_movie':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            title = post_data.split('&')[0].split('=')[1]
            rating = float(post_data.split('&')[1].split('=')[1])

            movie = {
                'title': title,
                'rating': rating
            }

            data = load_data()
            data.append(movie)
            save_data(data)

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            super().do_POST()

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print("Server listening on port: ", PORT)
    httpd.serve_forever()
