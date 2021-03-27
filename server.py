# Questo modulo utilizza Flask per realizzare un web server. L'applicazione può essere eseguita in vari modi
# FLASK_APP=server.py FLASK_ENV=development flask run
# python server.py se aggiungiamo a questo file app.run()

from flask import Flask, request, jsonify
import user
import message

# viene creata l'applicazione con il nome del modulo corrente.
app = Flask(__name__)

# getErrorCode è una funzione di utilità che mappa i valori ritornati dal modulo user con quelli del
# protocollo HTTP in caso di errore. 
# 404 - Not Found: una risorsa non è stata trovata sul server;
# 403 - Forbidden: accesso negato;
# 409 - Conflict: è violato un vincolo di unicità. Ad esempio, esiste già un utente con la stessa mail registrata;
# Come ultima spiaggia è buona norma ritornare "500 - Internal Server Error" per indicare che qualcosa è andato storto
def getErrorCode(result: user.Result)->int:
    
    if result is user.Result.NOT_FOUND:
        code = 404
    elif result is user.Result.NOT_AUTHORIZED:
        code = 403
    elif result is user.Result.DUPLICATED:
        code = 409
    else:
        code = 500

    return code

@app.route('/user', methods=['POST'])
def createUser():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    email = data['email']
    password = data['password']
    
    result, u = user.SaveUser(name, surname, email, password)

    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return u, 201

@app.route('/login', methods=['POST'])
def logUser():
    data = request.get_json()
    email = data['email']
    password = data['password']

    result, u = user.Login(email, password)
    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '',code
    else:
        return u,201


@app.route('/inbox', methods=['POST'])
def SendMessage():
    data = request.get_json()
    email_sender = data ['email_sender']
    email_receiver = data ['email_receiver']
    body = data ['body']
    user_sender = user.findUserByEmail(email_sender)
    user_receiver = user.findUserByEmail(email_receiver)

    if user_sender != None and user_receiver != None :

        result,m = message.SaveMessage(user_sender['id'],user_receiver['id'],body)
        return m, 200
    else:
        return 'email non trovata' ,404

@app.route('/inbox', methods=['GET'])
def receiveMessage():
    data = request.get_json()
    idd = data['id']
    received_message = message.GetMessagebyIdm(idd)
    return jsonify(received_message), 200

@app.route('/user/<id_utente>', methods=['DELETE'])
def delete(id_utente):
    email = request.authorization.username
    password = request.authorization.password
    result = user.autenticazione(email, password, id_utente)
    if result is not user.Result.OK:
        code = getErrorCode(result)
        return '',code
    else:
        return '',200
            
            

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
