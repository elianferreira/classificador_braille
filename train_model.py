import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from pathlib import Path
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from tqdm import tqdm

# Configurações
class_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
dataset_dir = Path('./data')  # Atualize com o caminho para seu dataset

# Função para carregar e pré-processar imagens
def load_images_and_labels(dataset_dir, class_names):
    train_images = []
    labels = []

    for file_path in tqdm(dataset_dir.glob('*.jpg')):
        # Carregar e redimensionar a imagem
        image = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (32, 32)) / 255.0

        # Adicionar imagem e label
        train_images.append(image)
        label = class_names.index(file_path.name[0].lower())
        labels.append(label)

        # Data augmentation (corte central)
        augmented_image = tf.image.central_crop(image, central_fraction=0.8).numpy()
        augmented_image = cv2.resize(augmented_image, (32, 32))
        train_images.append(augmented_image)
        labels.append(label)

    # Converter para arrays numpy
    train_images = np.expand_dims(np.array(train_images), axis=-1)
    labels = np.array(labels)

    return train_images, labels

# Carregar dados
print("Carregando imagens...")
train_images, labels = load_images_and_labels(dataset_dir, class_names)

# Dividir em treino e teste
train_images, test_images, train_labels, test_labels = train_test_split(
    train_images, labels, test_size=0.2, stratify=labels, random_state=42
)

# Construir o modelo
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.3),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Treinar modelo
print("Treinando modelo...")
history = model.fit(train_images, train_labels, epochs=50,
                    validation_data=(test_images, test_labels))

# Salvar o modelo
model.save('./models/modelo_letras.h5')

# Avaliação com matriz de confusão
predictions = model.predict(test_images)
predicted_labels = np.argmax(predictions, axis=1)
cm = confusion_matrix(test_labels, predicted_labels)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap='viridis')
plt.show()
