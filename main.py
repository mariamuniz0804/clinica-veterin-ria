from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'chave'

tutores = []
pets = []
consultas = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar-alteracao-pet', methods=['POST'])
def salvar_alteracao_pet():
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

        maiuscula = False
        minuscula = False
        numero = False
        caracter = False

        for s in senha:
            if s.isupper():
                maiuscula = True
            if s.islower():
                minuscula = True
            if s.isdigit():
                numero = True
            if not s.isalnum():
                caracter = True

        if not (maiuscula and minuscula and numero and caracter):
            flash("A senha deve ter pelo menos um número, um caractere especial, uma letra maiúscula e uma minúscula!", 'danger')
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
            if email == tutor['email'] and senha == tutor['senha']:
                flash("Login realizado com sucesso!")
                return redirect(url_for('cadastrarpet'))

        flash('Tutor cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrarpet'))  # ✅ Redireciona diretamente para o cadastro do pet

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

        pet = {
            'codigo': codigo,
            'nome_pet': nome_pet,
            'raca_pet': raca_pet,
            'peso_pet': peso_pet,
            'genero': genero,
            'nome_tutor': nome_tutor,
            'telefone_tutor': telefone_tutor
        }
        pets.append(pet)



        flash('Pet cadastrado com sucesso!', 'success')
        return redirect(url_for('dadospets'))

    return render_template('cadastrarpet.html')


@app.route('/editar/<int:pet_id>', methods=['GET', 'POST'])
def editar(pet_id):
    if pet_id >= len(pets) or pet_id < 0:
        flash('Pet não encontrado!', 'danger')
        return redirect(url_for('cadastrarpet'))

    if request.method == 'POST':
        pets[pet_id]['nome_pet'] = request.form['nome']
        pets[pet_id]['raca_pet'] = request.form['raca']
        pets[pet_id]['peso_pet'] = request.form['peso']
        pets[pet_id]['genero'] = request.form.get('sexo', '')

        flash('Dados do pet atualizados com sucesso!', 'success')
        return redirect(url_for('dadospets'))

    return render_template('editar.html', pets=pets[pet_id], pet_id=pet_id)

@app.route('/excluir/<int:pet_id>')
def excluir(pet_id):
    if 0 <= pet_id < len(pets):
        pets.pop(pet_id)
        flash('Pet excluído com sucesso!', 'success')
    else:
        flash('Pet não encontrado!', 'danger')

    return redirect(url_for('dadospets'))

@app.route('/calcularsoro', methods=['GET', 'POST'])
def calcularsoro():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])
            quantidade = request.form['quantidade']

            resultado_soro = peso * 30 + altura * 10
            resultado = f"Quantidade de soro necessária: {resultado_soro:.2f}ml ({quantidade})"
        except ValueError:
            flash('Por favor, insira valores numéricos válidos!', 'danger')

    return render_template('calcularsoro.html', resultado=resultado)

@app.route('/calcularmedicamento', methods=['GET', 'POST'])
def calcularmedicamento():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])
            quantidade = request.form['quantidade']

            resultado_med = peso * 2 + altura * 0.5
            resultado = f"Dosagem recomendada: {resultado_med:.2f}mg ({quantidade})"
        except ValueError:
            flash('Por favor, insira valores numéricos válidos!', 'danger')

    return render_template('calcularmedicamento.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)