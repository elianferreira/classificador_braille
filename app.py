import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Importar CORS
import tensorflow as tf
import numpy as np
from PIL import Image

# Detectar se estamos rodando em modo congelado (PyInstaller)
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS  # Diretório temporário criado pelo PyInstaller
else:
    base_dir = os.path.abspath(os.path.dirname(__file__))

# Inicializar Flask com caminhos corrigidos para PyInstaller
app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static")
)

# Habilitar CORS
CORS(app)  # Permitir CORS para todas as rotas

# Carregar o modelo treinado
model_path = os.path.join(base_dir, 'models', 'modelo_letras.h5')
model = tf.keras.models.load_model(model_path)
class_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Função para pré-processar a imagem
def process_image(image_path):
    """
    Pré-processa a imagem a partir de um caminho:
    - Redimensiona para 32x32
    - Converte para escala de cinza
    - Normaliza os valores (0 a 1)
    """
    image = Image.open(image_path).resize((32, 32)).convert('L')
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=(0, -1))
    return image

# Página inicial para exibir as imagens
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint para predição
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para fazer predições com base na imagem referenciada.
    """
    try:
        data = request.json  # Recebe o nome da imagem
        if not data or 'image' not in data:
            return jsonify({'error': 'Nenhuma imagem foi especificada.'}), 400

        image_name = data['image']
        image_path = os.path.join(base_dir, "static", "braille", image_name)  # Caminho corrigido
        processed_image = process_image(image_path)

        # Faz a predição
        predictions = model.predict(processed_image)
        predicted_class = class_names[np.argmax(predictions)]

        return jsonify({'prediction': predicted_class})
    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro ao processar a imagem: {str(e)}'}), 500

# Executar a API
if __name__ == '__main__':
    app.run(debug=True)

