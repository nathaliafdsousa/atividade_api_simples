from flask import Flask, jsonify, request
from flasgger import Swagger 

app = Flask(__name__)
swagger = Swagger(app)


usuarios = []
contador_id = 1

@app.route("/users", methods=["GET"])
def listar_usuarios():
    """Listar todos os usuários
    
    ---
    tags:
        - Usuarios
    responses:
        200:
            description: lista de usuários
            schema:
                type:object
                properties:
                    mensagem:
                        type: string
                        example: Lista de usuários
                    usuarios:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                    example: 1
                                nome:
                                    type: string
                                    example: Rebeca
                                email:
                                    type: string
                                    example: rebeca@email.com
    
    
    """
    
    if not usuarios:
        return jsonify({"mensagem": "Nenhum usuário cadastrado ainda", "usuarios": []}), 200
    return jsonify({"mensagem": "Lista de usuários", "usuarios": usuarios}), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def buscar_usuario(user_id):
    """Buscar usuários
      ---
    tags:
        - Usuarios
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
              description: ID do usuário a ser buscado
            responses:
                200:
                    description: Usuário encontrado
                    scheme:
                        type: object
                        properties:
                            mensagem:
                                type: string
                                example: Usuário encontrado
                            usuario:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        example: 1
                                    nome:
                                        type: string
                                        example: Rebeca
                                    email:
                                        type: string
                                        example: rebeca@email.com
                404:
                    description: Usuário não encontrado
                    schema:
                        type: object
                        properties:
                            erro:
                                type: string
                                example: Usuário não encontrado
    
    
    """
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return jsonify({"mensagem": "Usuário encontrado", "usuario": usuario}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404


@app.route("/users", methods=["POST"])
def criar_usuario():
    """Criar novos usuários
        ---
        tags:
            - Usuários:
            consumes:
                - application/json
                parameters:
                    - int: body
                        name: user
                        required: true
                        schema:
                            type: object
                            required: 
                                - nome
                                - email
                            properties:
                                nome:
                                    type: string
                                    example: Rebeca
                                email:
                                    type: string
                                    example:rebeca@email.com
            responses:
                201:
                    description:Usuário criado com sucesso
                    schema:
                        type: object
                        properties:
                            mensagem:
                                type: string
                                example: Usuário criado com sucesso
                            usuario:
                                type: object
                                properties:
                                    id:
                                        type: integer
                                        example: 1
                                    nome:
                                        type: string
                                        example: Rebeca
                                    email:
                                        type: string
                                        example: rebeca@email.com
                400:
                    description: Requisição inválida


    
    
    
    """
    
    
    global proximo_id
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Requisição inválida, envie JSON"}), 400

    nome = dados.get("nome")
    email = dados.get("email")

    if not nome or not email:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

    novo = {"id": proximo_id, "nome": nome, "email": email}
    usuarios.append(novo)
    proximo_id += 1
    return jsonify({"mensagem": "Usuário criado com sucesso", "usuario": novo}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def atualizar_usuario(user_id):
    """Atualizar usuários
    ---
    tags:
        - Usuarios
        consumes:
            - application/json
            parameters:
                - name: user_id
                  in: path
                  type: integer
                  required: true
                  description: ID do usuário a ser atualizado
                - in: body
                  name: user
                  required: true
                  schema:
                    type: object
                    properties:
                        nome:
                            type: string
                            example: Rebeca
                        email:
                            type: string
                            example:rebeca@email.com
        responses:
            200:
            description: Usuário atualizado com sucesso
            400:
                description: Requisição inválida
            404:
                description: Usuário não encontrado


    """
    
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Requisição inválida, envie JSON"}), 400

    for usuario in usuarios:
        if usuario["id"] == user_id:
            usuario["nome"] = dados.get("nome", usuario["nome"])
            usuario["email"] = dados.get("email", usuario["email"])
            return jsonify({"mensagem": "Usuário atualizado com sucesso", "usuario": usuario}), 200

    return jsonify({"erro": "Usuário não encontrado"}), 404


@app.route("/users/<int:user_id>", methods=["DELETE"])
def deletar_usuario(user_id):
    """Deletar usuários
    ---
    tags:
        - Usuarios
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
              description: ID do usuário a ser deletado
            responses:
                200:
                    description: Usuário deletado com sucesso
                    schema:
                        type: object
                        properties:
                            mensagem:
                                type: string
                                example: Usuário deletado com sucesso
                404:
                    description: Usuário não encontrado
                    schema:
                        type: object
                        properties:
                            erro:
                                type: string
                                example: Usuário não encontrado
    
    
    """
    
    
    
    
    
    for i, usuario in enumerate(usuarios):
        if usuario["id"] == user_id:
            usuarios.pop(i)
            return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)



