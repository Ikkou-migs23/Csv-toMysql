from app import main
from sys import argv

if __name__ == "__main__":
    if len(argv) < 2:
        print("Uso: python __main__.py <caminho_para_arquivo_csv>")
        exit(1)

    caminho_csv = argv[1]
    main(caminho_csv)