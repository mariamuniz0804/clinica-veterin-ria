from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4

app = Flask(__name__)


pets = []


@app.route('/')
def index():
    return render_template('index.html', pets=pets)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        pet = {
            'id': str(uuid4()),
            'codigo': request.form['codigo'],
            'nome': request.form['nome'],
            'tutor': request.form['tutor'],
            'raca': request.form['raca'],
            'peso': float(request.form['peso']),
            'sexo': request.form['sexo'],
            'telefone': request.form['telefone']
        }
        pets.append(pet)
        return redirect(url_for('index'))

    return render_template('cadastrar.html')


@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar(id):
    pet = next((p for p in pets if p['id'] == id), None)

    if pet is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        pet.update({
            'codigo': request.form['codigo'],
            'nome': request.form['nome'],
            'tutor': request.form['tutor'],
            'raca': request.form['raca'],
            'peso': float(request.form['peso']),
            'sexo': request.form['sexo'],
            'telefone': request.form['telefone']
        })
        return redirect(url_for('index'))

    return render_template('editar.html', pet=pet)


@app.route('/excluir/<string:id>')
def excluir(id):
    global pets
    pets = [p for p in pets if p['id'] != id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)