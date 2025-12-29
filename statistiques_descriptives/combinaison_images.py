from PIL import Image
import os
import matplotlib.pyplot as plt

def combiner_images(filepath):
    """
    Combine 4 images d'un dossier en une grille 2x2

    Prend en argument le lien vers le dossier
    """
    #On récupère les images du sossier images
    fichiers = [f for f in os.listdir(filepath) if f.endswith(('.png', '.jpg', '.jpeg'))]
    fichiers = sorted(fichiers)[:4]  #On prend les 4 premières
    
    if len(fichiers) < 4:
        raise ValueError(f"Il manque des images")
    
    #On charge les images et on créé un panneau blanc 2*2
    images = [Image.open(os.path.join(filepath, f)) for f in fichiers]
    largeur, hauteur = images[0].size
    nouvelle_image = Image.new('RGB', (largeur * 2, hauteur * 2), 'white')
    
    #On colle les images
    nouvelle_image.paste(images[0], (0, 0))                  
    nouvelle_image.paste(images[1], (largeur, 0))             
    nouvelle_image.paste(images[2], (0, hauteur))              
    nouvelle_image.paste(images[3], (largeur, hauteur))        
    
    plt.figure()
    plt.imshow(nouvelle_image)
    plt.axis('off')
    plt.tight_layout()
    plt.show()