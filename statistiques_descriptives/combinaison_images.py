from PIL import Image
import os
import matplotlib.pyplot as plt

def combiner_images(filepath):
    """
    Combine 4 images d'un dossier en une grille 2x2
    """
    #Récupérer toutes les images du dossier
    fichiers = [f for f in os.listdir(filepath) if f.endswith(('.png', '.jpg', '.jpeg'))]
    fichiers = sorted(fichiers)[:4]  #Prendre les 4 premières
    
    if len(fichiers) < 4:
        raise ValueError(f"Le dossier doit contenir au moins 4 images (trouvé: {len(fichiers)})")
    
    #Charger les 4 images
    images = [Image.open(os.path.join(filepath, f)) for f in fichiers]
    
    #Récupérer la taille d'une image
    largeur, hauteur = images[0].size
    
    #Créer une nouvelle image 2x2
    nouvelle_image = Image.new('RGB', (largeur * 2, hauteur * 2), 'white')
    
    # Coller les 4 images
    nouvelle_image.paste(images[0], (0, 0))                    # Haut gauche
    nouvelle_image.paste(images[1], (largeur, 0))              # Haut droite
    nouvelle_image.paste(images[2], (0, hauteur))              # Bas gauche
    nouvelle_image.paste(images[3], (largeur, hauteur))        # Bas droite
    
    plt.figure()
    plt.imshow(nouvelle_image)
    plt.axis('off')
    plt.tight_layout()
    plt.show()