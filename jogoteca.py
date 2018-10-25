# Está utilizando somente a classe Flask da biblioteca flask
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'secreto'
app.config['MONGO_DBNAME'] = 'maitre_one'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/maitre_one'

class Jogo():
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario():
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('luan', 'luan', '1234')
usuario2 = Usuario('rafael', 'rafael', '4321')
usuario3 = Usuario('flavio', 'flavio', 'c++')
usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3} # DICIONARIO { CHAVE : VALOR}

jogo1 = Jogo("Zelda", "Ação", "N64")
jogo2 = Jogo("Mário Kart", "Corrida", "SNES")
jogo3 = Jogo("God of War", "Ação", "PS4")
lista = [jogo1,jogo2,jogo3]


# Cria uma nova rota
@app.route('/')
def index():
    return render_template("lista.html", titulo='Jogos Aqui!', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'), proxima=url_for('novo')) # novo é o cmainho a seguir depois que for feito o login. Próxima é o argumento
    return render_template('novo.html', titulo='Jogo Novo')

'''
    Atraves do formulário envia-se um request para CRIAR e o response era a página CRIAR, mas o certo é
    Redirecionar para a página NOVO para não haver duas rotas iguaaais
'''

# Para informar que essa rota irá receber um post passa o parâmetro methods, é uma rota que atualiza a rota novo
@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria,console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima_login = request.args.get('proxima') # proxima é o argumento passado da rota 'novo'
    return render_template('login.html', prox = proxima_login)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' Logado com sucesso!')
            proxima_pagina = request.form['PROXIMA']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route("/teste", methods=["POST"])
def teste():

    dados = request.get_json()
    nome = dados['nome']
    idade = dados['idade']
    telefone = dados['telefone']
    amigos = dados['amigos']

    return jsonify({"Sucess": "Flask-Mongodb", "nome": nome, "idade": idade, "telefone": telefone, "amigos": amigos[0]})


# Com debug=True não é necessário ficar fazendo reload
app.run(debug=True)

#url_for(nome da função de umas das rotas)