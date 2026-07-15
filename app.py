from flask import Flask

app = Flask(_name_)

@app.route("/")
def home():
    return """
    <h1>CI/CD Pipeline Demo</h1>
    <h2>Jenkins + Docker + Amazon ECR + Kubernetes</h2>
    <p>Deployment Successful!!!</p>
    """

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)
