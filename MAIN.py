import os
import socket
import glob
import qrcode
import webbrowser
from jinja2 import Template


# Obtenir le nom de l'hôte local
hostname = socket.gethostname()
# Obtenir l'adresse IP locale
ip_address = socket.gethostbyname(hostname)
print(f"Le nom de l'hôte local est : {hostname}")
print(f"L'adresse IP de l'hôte local est : {ip_address}")

# Chemin relatif du répertoire racine à partir duquel on veut chercher les fichiers index.html
root_dir = './'

# Chercher tous les fichiers index.html dans le répertoire racine et ses sous-répertoires
html_files = glob.glob(os.path.join(root_dir, '**/index.html'), recursive=True)

# créer le répertoire "images" s'il n'existe pas déjà
os.makedirs('images', exist_ok=True)

# Liste des QR codes et des chemins d'images correspondants
qr_codes = []

# Obtenir l'adresse IP de la carte réseau wifi
# INUTILISÉ POUR L'INSTANT ==> eth_ip = socket.gethostbyname(socket.gethostname() + ".local")
wifi_ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

# Parcourir toutes les combinaisons d'adresses IP et fichiers HTML
for i, html_file in enumerate(html_files):
    # Construire le chemin absolu du fichier HTML
    html_file_path = os.path.abspath(html_file)

    # Utiliser l'adresse IP de la carte réseau wifi ou ethernet
    # INUTILISÉ POUR L'INSTANT ==> for ip_address in [wifi_ip, eth_ip]:
        
    # Construire le contenu du QR code
    qr_content = f"http://{ip_address}/{os.path.relpath(html_file_path, root_dir)}"
    qr_content = qr_content.replace("\\","/")

    # Générer le QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Exporter le QR code dans le répertoire "images"
    image_filename = f"qr_code_{i}.png"
    image_path = os.path.join('images', image_filename)
    qr_img.save(image_path)
    print(f"Le QR code pour {qr_content} a été enregistré dans {image_path}")

    # Ajouter le chemin d'image et le contenu du QR code à la liste
    qr_codes.append((image_filename, qr_content))

# Générer le code HTML pour afficher tous les QR codes
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>BZHCOMPAGNY</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }

        #header {
            background-color: #333;
            color: #fff;
            padding: 10px;
            text-align: center;
        }

        #container {
            margin: 20px auto;
            max-width: 600px;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }

        h1 {
            font-size: 24px;
            margin-bottom: 10px;
        }

        h2 {
            font-size: 18px;
            margin-bottom: 10px;
        }

        img.qrcode {
            display: block;
            margin: 10px auto;
            max-width: 100%;
            height: auto;
        }

        a {
            color: #333;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .qrcode-item {
            margin-bottom: 20px;
        }

        .qrcode-item:last-child {
            margin-bottom: 0;
        }

        .qrcode-content {
            font-size: 14px;
            word-break: break-all;
            overflow-wrap: break-word;
        }
    </style>
</head>
<body>
    <div id="header">
      <img src="images/hermine_bretonne.png" alt="Image de gauche" >
      <h1>BZHCOMPAGNY</h1>
    </div>
    <div id="container">
"""

for image_filename, qr_content in qr_codes:
    html += f"""
        <div class="qrcode-item">
            <h2>QRCODE :</h2>
            <img class="qrcode" src="images/{image_filename}">
            <p class="qrcode-content"><a href="{qr_content}">{qr_content}</a></p>
        </div>
    """

html += """
    </div>
</body>
</html>
"""

# Enregistrer la page HTML dans le fichier data.html
with open('data.html', 'w') as f:
    f.write(html)

# Ouvrir la page HTML dans un navigateur web
webbrowser.open_new_tab('data.html')

# Afficher l'emplacement du fichier data.html
print(f"La page HTML est enregistrée dans {os.path.abspath('data.html')}")
