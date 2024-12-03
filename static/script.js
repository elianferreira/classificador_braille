let concatenatedText = ""; // String para armazenar o texto concatenado

// Adicionar evento de clique em cada imagem de Braille
document.querySelectorAll('.braille-key').forEach(image => {
    image.addEventListener('click', async (event) => {
        const imageName = event.target.dataset.image; // Nome da imagem clicada
        const resultDiv = document.getElementById('result');

        try {
            // Enviar requisição para a API
            const response = await fetch('http://127.0.0.1:5000/predict', { // URL completa do servidor
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageName }), // Envia o nome da imagem
            });

            const result = await response.json();

            if (response.ok) {
                // Concatenar a letra retornada ao texto
                concatenatedText += result.prediction;

                // Atualizar a exibição do texto concatenado
                resultDiv.textContent = concatenatedText;
            } else {
                resultDiv.textContent = `Erro: ${result.error}`;
            }
        } catch (error) {
            console.error('Erro ao conectar com o servidor:', error);
            resultDiv.textContent = "Erro ao conectar com o servidor.";
        }
    });
});

// Função para exibir a imagem selecionada do upload
const imageUploadInput = document.getElementById('image-upload');
const imagePreview = document.getElementById('image-preview');

imageUploadInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// Adicionar evento para enviar a imagem via upload
document.getElementById('image-upload').addEventListener('change', async (event) => {
    const resultDiv = document.getElementById('result');
    const formData = new FormData();
    formData.append('file', event.target.files[0]); // Adiciona o arquivo ao FormData

    try {
        // Enviar requisição para o endpoint de upload de imagem
        const response = await fetch('http://127.0.0.1:5000/predict_via_upload', { 
            method: 'POST',
            body: formData, // Envia o arquivo
        });

        const result = await response.json();

        if (response.ok) {
            // Concatenar a letra retornada ao texto
            concatenatedText += result.prediction;

            // Atualizar a exibição do texto concatenado
            resultDiv.textContent = concatenatedText;
        } else {
            resultDiv.textContent = `Erro: ${result.error}`;
        }
    } catch (error) {
        console.error('Erro ao conectar com o servidor:', error);
        resultDiv.textContent = "Erro ao conectar com o servidor.";
    }
});
