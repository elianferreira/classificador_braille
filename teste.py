import requests

url = "http://127.0.0.1:5000/predict"
file_path = "./DataSet/DataSet/c1.JPG1rot.jpg"

# Enviar arquivo
with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

# Exibir a resposta
print(response.json())
