from bs4 import BeautifulSoup
import pandas as pd


# Cargar archivo html
with open('./tiendaDeTenis/index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Analizar el contenido de HTML con Beaufitulsoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extraemos los datos de interes.
productos = []


for item in soup.select('.lista-productos .producto'):
    titulo = item.select_one('.título').get_text(strip=True)
    img = item.select_one('img')
    precio = item.select_one('.precio').get_text(strip=True)
    tallas = item.select_one('.tallas').get_text(strip=True)

    # Extraer el atributo src de la etiqueta img
    img_src = img['src'] if img else None

    productos.append({
        'Imagen': img,
        'Titulo': titulo,
        'Precio': precio,
        'Tallas':  tallas
    })
# Crear un DataFrame de pandas
df = pd.DataFrame(productos)

# Guardar el DataFrame en un archivo CSV
df.to_csv('productos.csv', index=False, encoding='utf-8')
print(productos)