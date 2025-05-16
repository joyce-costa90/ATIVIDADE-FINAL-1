import requests
import os

api_key = "08611eb9326947c8b93855d73e7d83a8"

if not api_key:
    raise ValueError("API Key não encontrada nas variáveis de ambiente.")

url = "https://newsapi.org/v2/everything"

historico_buscas = {}

def buscar_noticias(tema, quantidade):
   
    params = {
        "q": tema,
        "apiKey": api_key,
        "language": "pt",
        "pageSize": quantidade,
        "sortBy": "publishedAt"
    }

    resposta = requests.get(url, params=params)
    if resposta.status_code == 200:
        return resposta.json().get("articles", [])
    else:
        print("\nErro ao buscar notícias.")
        return []

def exibir_historico():

    if historico_buscas:
        print("\n=== Histórico de buscas ===")
        total_noticias = sum(historico_buscas.values())
        for tema, qtd in historico_buscas.items():
            print(f" Tema: {tema} | Notícias buscadas: {qtd}")
        print(f"\nTotal de notícias buscadas: {total_noticias}")
    else:
        print("\nNenhuma busca foi registrada ainda.")

def menu():
 
    while True:
        print("\n=== Menu de Notícias ===")
        print("1. Buscar notícias")
        print("2. Ver histórico de buscas")
        print("3. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            tema = input("\nDigite um tema para buscar notícias: ")
            quantidade = int(input("Quantas notícias deseja buscar? (Máximo 10): "))
            quantidade = min(quantidade, 10)  

            noticias = buscar_noticias(tema, quantidade)

            if noticias:
                print("\n=== Notícias encontradas ===")
                for idx, noticia in enumerate(noticias, 1):
                    titulo = noticia["title"]
                    fonte = noticia["source"]["name"]
                    autor = noticia.get("author", "Desconhecido")
                    print(f"\n{idx}. {titulo}\n   Fonte: {fonte}\n   Autor: {autor}")

           
                historico_buscas[tema] = historico_buscas.get(tema, 0) + quantidade
            else:
                print("\nNenhuma notícia encontrada sobre esse tema.")

        elif opcao == "2":
            exibir_historico()

        elif opcao == "3":
            print("\nSaindo do programa. Até mais!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()