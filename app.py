from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

from sqlalchemy.orm import query
from werkzeug.wrappers import response

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://pricing:pricing@10.100.113.25:5454/crud"

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    autor = db.Column(db.String(100))
    paginas = db.Column(db.String(50))
    preco = db.Column(db.String(50))
    anoLancamento = db.Column(db.String(50))

    def to_json(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "paginas": self.paginas,
            "preco": self.preco,
            "anoLancamento": self.anoLancamento
        }

@app.route('/livros', methods=['GET'])
def seleciona_livros():
    livros = Book.query.all()
    livros_json = [livro.to_json() for livro in livros]

    return gera_response(200, "livros", livros_json)

@app.route('/livro/<id>', methods=['GET'])
def seleciona_livro(id):
    livro = Book.query.filter_by(id=id).first()
    livro_json = livro.to_json()

    return gera_response(200, "livro", livro_json)

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body['mensagem'] = mensagem
    
    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()