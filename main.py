from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Привіт! 👋</h1>
    <p>Я навчаюсь створювати сайти на Python.</p>
    <p>Це моя перша сторінка!</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
  
