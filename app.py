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
def process_image(image):
    """
    Pré-processa a imagem:
    - Redimensiona para 32x32
    - Converte para escala de cinza
    - Normaliza os valores (0 a 1)
    """
    image = image.resize((32, 32)).convert('L')
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=(0, -1))
    return image

# Endpoint para predição com nome da imagem
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Recebe o nome da imagem
        if not data or 'image' not in data:
            return jsonify({'error': 'Nenhuma imagem foi especificada.'}), 400

        image_name = data['image']
        image_path = os.path.join(base_dir, "static", "braille", image_name)  # Caminho corrigido
        image = Image.open(image_path)
        processed_image = process_image(image)

        # Faz a predição
        predictions = model.predict(processed_image)
        predicted_class = class_names[np.argmax(predictions)]

        return jsonify({'prediction': predicted_class})
    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro ao processar a imagem: {str(e)}'}), 500


# Novo endpoint para predição com upload de imagem
@app.route('/predict_via_upload', methods=['POST'])
def predict_via_upload():
    try:
        # Verifique se um arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado.'}), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400
        
        # Abrir a imagem
        image = Image.open(file)
        processed_image = process_image(image)

        # Faz a predição
        predictions = model.predict(processed_image)
        predicted_class = class_names[np.argmax(predictions)]

        return jsonify({'prediction': predicted_class})
    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro ao processar a imagem: {str(e)}'}), 500

# Executar a API
if __name__ == '__main__':
    app.run(debug=False)
