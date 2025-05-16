import requests

# Simulação de um banco de dados de usuários
usuarios = {
    "1": {"email": "user1@email.com", "senha": "senha123"},
    "2": {"email": "user2@email.com", "senha": "senha456"},
    "3": {"email": "user3@email.com", "senha": "senha789"},
}

BASE_URL = "https://jsonplaceholder.typicode.com"

def autenticar_usuario():
    """Verifica se o usuário existe no banco de dados."""
    codigo = input("\nDigite seu código de usuário: ")
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")

    if codigo in usuarios and usuarios[codigo]["email"] == email and usuarios[codigo]["senha"] == senha:
        print("\nLogin bem-sucedido!")
        return codigo
    else:
        print("\nUsuário não encontrado ou credenciais incorretas.")
        return None

def obter_posts():
    """Busca todos os posts disponíveis."""
    resposta = requests.get(f"{BASE_URL}/posts")
    return resposta.json() if resposta.status_code == 200 else []

def obter_comentarios(post_id):
    """Busca os comentários de um post específico."""
    resposta = requests.get(f"{BASE_URL}/posts/{post_id}/comments")
    return resposta.json() if resposta.status_code == 200 else []

def obter_posts_usuario(user_id):
    """Filtra posts de um usuário específico."""
    resposta = requests.get(f"{BASE_URL}/posts", params={"userId": user_id})
    return resposta.json() if resposta.status_code == 200 else []

def criar_post(user_id):
    """Simula a criação de um novo post."""
    titulo = input("\nDigite o título do post: ")
    corpo = input("Digite o conteúdo do post: ")

    novo_post = {
        "userId": user_id,
        "title": titulo,
        "body": corpo
    }

    resposta = requests.post(f"{BASE_URL}/posts", json=novo_post)
    if resposta.status_code == 201:
        print("\nPost criado com sucesso!")
        return novo_post
    else:
        print("\nErro ao criar post.")
        return None

def menu_interativo(usuario_logado):
    """Menu para interação com posts e comentários."""
    interacoes = {"posts_vistos": 0, "comentarios_vistos": 0, "posts_criados": 0}

    while True:
        print("\n=== Menu Interativo ===")
        print("1. Ver todos os posts")
        print("2. Ver comentários de um post")
        print("3. Ver meus posts")
        print("4. Filtrar posts por outro usuário")
        print("5. Criar um novo post")
        print("6. Sair e ver resumo")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            posts = obter_posts()
            for post in posts[:5]:  # Mostrando apenas os primeiros 5 posts
                print(f"\nTítulo: {post['title']}\nConteúdo: {post['body']}")
                interacoes["posts_vistos"] += 1

        elif opcao == "2":
            post_id = input("Digite o ID do post para ver os comentários: ")
            comentarios = obter_comentarios(post_id)
            for comentario in comentarios:
                print(f"\nAutor: {comentario['name']}\nComentário: {comentario['body']}")
                interacoes["comentarios_vistos"] += 1

        elif opcao == "3":
            posts_usuario = obter_posts_usuario(usuario_logado)
            for post in posts_usuario:
                print(f"\nTítulo: {post['title']}\nConteúdo: {post['body']}")

        elif opcao == "4":
            user_id = input("Digite o ID do usuário para ver os posts dele: ")
            posts_usuario = obter_posts_usuario(user_id)
            for post in posts_usuario:
                print(f"\nTítulo: {post['title']}\nConteúdo: {post['body']}")

        elif opcao == "5":
            novo_post = criar_post(usuario_logado)
            if novo_post:
                interacoes["posts_criados"] += 1

        elif opcao == "6":
            print("\n=== Resumo das Interações ===")
            print(f"Posts visualizados: {interacoes['posts_vistos']}")
            print(f"Comentários visualizados: {interacoes['comentarios_vistos']}")
            print(f"Posts criados: {interacoes['posts_criados']}")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    print("\n=== Bem-vindo ao sistema de notícias ===")
    usuario_logado = autenticar_usuario()

    if usuario_logado:
        menu_interativo(usuario_logado)

if __name__ == "__main__":
    main()