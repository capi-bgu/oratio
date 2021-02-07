import requests
import typer

app = typer.Typer()


DLIB_FACE_MODEL_URL = "https://drive.google.com/uc?export=download&id=1AilalzxfrUbFYxK-CbN5AGzZntQ5y9mR"

@app.command()
def download_face_model(
    url: str = typer.Option(DLIB_FACE_MODEL_URL, "--url", "-u")):
    model_data = requests.get(url).content
    with open("src/resources/face_detection.dat", 'wb') as f:
        f.write(model_data)


if __name__ == "__main__":
    app()