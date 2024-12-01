let concatenatedText = ""; // String para armazenar o texto concatenado

// Adicionar evento de clique em cada imagem
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

