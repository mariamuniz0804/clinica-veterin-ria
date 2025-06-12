from flask import Flask, render_template, request, flash

app = Flask(__name__)

conultas = []
@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')


@app.route('/cadastrar_agenda', methods=['POST'])
def cadastrar_agenda():
    if request.method == 'POST':
        codigo = str(len(conultas) + 1)
        nometutor = request.form['nometutor']
        celular = request.form['celular']
        email = request.form['email']
        especie = request.form['especie']
        nomepet = request.form['nomepet']
        data_consulta = request.form['data_consulta']

        consulta = {
            "codigo": codigo,
            "nometutor": nometutor,
            "celular": celular,
            "email": email,
            "especie": especie,
            "nomepet": nomepet,
            "data_consulta": data_consulta
        }
        consulta.append(consulta)
        flash("Agenda realizada com sucesso!")
        return render_template('index.html')
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
