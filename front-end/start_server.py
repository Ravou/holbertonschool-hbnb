import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = "app"  # À adapter selon l’endroit où se trouve ton index.html

# Changer le dossier de travail pour servir depuis le bon répertoire
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("\033[92m[✔] Serveur lancé avec succès !\033[0m")
        print(f"🌐 Accédez au site ici : http://localhost:{PORT}/index.html\n")
        httpd.serve_forever()
except OSError as e:
    if e.errno == 98:
        print(f"\033[91m[✖] Le port {PORT} est déjà utilisé. Change de port ou libère-le.\033[0m")
    else:
        print(f"\033[91m[✖] Erreur inattendue : {e}\033[0m")
    sys.exit(1)
