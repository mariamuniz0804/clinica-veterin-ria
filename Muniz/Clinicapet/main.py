from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = ('chave secreta para os nao uçar')

tutores = []
pets = []
consultas = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastrartutor', methods=['GET', 'POST'])
def cadastrartutor():
    if request.method == 'POST':
        nome = request.form['nomeTutor']
        telefone = request.form['telefoneTutor']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmaSenha']

        if confirmar_senha != senha:
            flash("As senhas não coincidem!", 'danger')
            return redirect(url_for('cadastrartutor'))

        maiuscula = any(c.isupper() for c in senha)
        minuscula = any(c.islower() for c in senha)
        numero = any(c.isdigit() for c in senha)
        especial = any(not c.isalnum() for c in senha)

        if not (maiuscula and minuscula and numero and especial):
            flash("A senha deve ter pelo menos uma letra maiúscula, minúscula, número e caractere especial.", 'danger')
            return redirect(url_for('cadastrartutor'))

        tutores.append({
            'nome': nome,
            'telefone': telefone,
            'email': email,
            'senha': senha
        })

        flash('Tutor cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastrartutor.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        for tutor in tutores:
            if tutor['email'] == email and tutor['senha'] == senha:
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('cadastrarpet'))

        flash('Email ou senha incorretos!', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/cadastrarpet', methods=['GET', 'POST'])
def cadastrarpet():
    if request.method == 'POST':
        codigo = len(pets)
        nome_pet = request.form['nome_pet']
        raca_pet = request.form['raca_pet']
        peso_pet = request.form['peso_pet']
        genero = request.form.get('genero', '')
        nome_tutor = request.form['nome_tutor']
        telefone_tutor = request.form['telefone_tutor']

        pets.append({
            'codigo': codigo,
            'nome_pet': nome_pet,
            'raca_pet': raca_pet,
            'peso_pet': peso_pet,
            'genero': genero,
            'nome_tutor': nome_tutor,
            'telefone_tutor': telefone_tutor
        })

        flash('Pet cadastrado com sucesso!', 'success')
        return redirect(url_for('dadospets'))

    return render_template('cadastrarpet.html')


@app.route('/dadospets')
def dadospets():
    return render_template('dadospets.html', pets=pets)


@app.route('/editar/<int:pet_id>', methods=['GET', 'POST'])
def editar(pet_id):
    if 0 <= pet_id < len(pets):
        if request.method == 'POST':
            pets[pet_id]['nome_pet'] = request.form['nome']
            pets[pet_id]['raca_pet'] = request.form['raca']
            pets[pet_id]['peso_pet'] = request.form['peso']
            pets[pet_id]['genero'] = request.form.get('sexo', '')
            flash('Dados do pet atualizados com sucesso!', 'success')
            return redirect(url_for('dadospets'))

        return render_template('editar.html', pets=pets[pet_id], pet_id=pet_id)

    flash('Pet não encontrado!', 'danger')
    return redirect(url_for('dadospets'))


@app.route('/excluir/<int:pet_id>')
def excluir(pet_id):
    if 0 <= pet_id < len(pets):
        pets.pop(pet_id)
        flash('Pet excluído com sucesso!', 'success')
    else:
        flash('Pet não encontrado!', 'danger')
    return redirect(url_for('dadospets'))


@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        nome = request.form['nome']
        celular = request.form['celular']
        email = request.form['email']
        especie = request.form['especie']
        data_hora = request.form['data_hora']
        nome_pet = request.form['nome_pet']

        consultas.append({
            'nome': nome,
            'celular': celular,
            'email': email,
            'especie': especie,
            'data_hora': data_hora,
            'nome_pet': nome_pet
        })

        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('dados_consultas'))

    return render_template('agendamento.html')


@app.route('/dadosconsultas')
def dados_consultas():
    return render_template('dadosconsultas.html', consultas=consultas)


@app.route('/calcularsoro', methods=['GET', 'POST'])
def calcularsoro():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            quantidade = request.form['quantidade']
            total = peso * quantidade
            resultado = f"Quantidade de soro necessária: {total:.2f}ml ({quantidade})"
        except ValueError:
            flash('Insira apenas números válidos.', 'danger')

    return render_template('calcularsoro.html', resultado=resultado)


@app.route('/calcularmedicamento', methods=['GET', 'POST'])
def calcularmedicamento():
    resultado = None
    if request.method == 'POST':
            peso = float(request.form['peso'])
            quantidades = float(request.form['quantidades'])
            total = peso * quantidades
            print(peso)
            print(quantidades)
            flash(f"Dosagem recomendada: {total:.2f}mg ")

    return render_template('calcularmedicamento.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)
