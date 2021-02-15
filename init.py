import typer
import requests

app = typer.Typer()


DLIB_FACE_MODEL_URL = "https://drive.google.com/uc?export=download&id=1AilalzxfrUbFYxK-CbN5AGzZntQ5y9mR"
TASK_KEYWORDS_URL = "https://drive.google.com/uc?id=1gEXK7X-QyW56MUZ8LUAZ9wf6jPBGVuaH&export=download"

@app.command()
def download_face_model(
    url: str = typer.Option(DLIB_FACE_MODEL_URL, "--url", "-u")):
    model_data = requests.get(url).content
    with open("oratio/resources/face_detection.dat", 'wb') as f:
        f.write(model_data)

@app.command()
def download_task_keywords(
    url: str = typer.Option(TASK_KEYWORDS_URL, "--url", "-u")):
    model_data = requests.get(url).content
    with open("oratio/resources/task_keywords.json", 'wb') as f:
        f.write(model_data)


if __name__ == "__main__":
    app()
