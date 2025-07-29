import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

print("\033[92m[✔] Serveur lancé avec succès !\033[0m")
print(f"🌐 Accédez au site ici : http://localhost:{PORT}/templates/index.html\n")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()

