from io import TextIOWrapper
from dotenv import load_dotenv
from os import environ
from tqdm import tqdm
import mysql.connector

from data import EstacaoDados

def pode_adicionar(dado: EstacaoDados) -> bool:
    metricas = dado.métricas

    if (
        metricas["Temperatura do Ar Instantânea"] < 0
        or metricas["Temperatura do Ar Máxima 1h"] < 0
        or metricas["Temperatura do Ar Mínima 1h"] < 0
    ):
        return False
    return True

def ler_arquivo(file: TextIOWrapper):
    linhas = file.readlines()
    dados = []
    campos = linhas[0].strip().split(",")
    linhas = linhas[1:]
    dados_invalidos = 0

    for linha in linhas:
        try:
            dado = EstacaoDados.parse_csv(linha, campos)
            if pode_adicionar(dado):
                dados.append(dado)
            else:
                dados_invalidos += 1
        except Exception as e:
            print(f"Erro ao processar linha: {linha.strip()} | Motivo: {e}")
            dados_invalidos += 1

    return dados

def chunked(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i : i + n]

def conectar_banco():
    db = mysql.connector.connect(
        user=environ['DB_USER'],
        password=environ['DB_PASSWORD'],
        host=environ['DB_HOST'],
        database='Ametista'
    )
    return db

def inserir_estacoes(db, dados: list[EstacaoDados]):
    nomes_estacoes = set(map(lambda dado: dado.nome_estacao, dados))
    print(f"** Inserindo estações: {', '.join(nomes_estacoes)}")
    cursor = db.cursor(buffered=True)
    for estacao in nomes_estacoes:
        cursor.execute(
            "INSERT IGNORE INTO estacao (nome) VALUES (%s)", (estacao,)
        )
    db.commit()
    cursor.close()
    print("** OKAY.")

def pegar_id_estacao(db, nome_estacao: str) -> int:
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT id_estacao FROM estacao WHERE nome = %s", (nome_estacao,))
    resultado = cursor.fetchone()
  
    cursor.close()
  
    if not resultado:
        raise Exception(f"Estação {nome_estacao} não encontrada")
    return resultado[0]

def pegar_tipos_metricas(db) -> dict[str, int]:
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT id_metrica, nome_metrica FROM tipo_metrica")
    resultados = cursor.fetchall()
    cursor.close()
    return {nome: id for id, nome in resultados}

def inserir_metricas(db, dados: list[EstacaoDados]):
    # Normaliza os nomes das métricas do banco para letras minúsculas
    tipos_metricas_ids = {
        nome.strip().lower(): id_metrica
        for nome, id_metrica in pegar_tipos_metricas(db).items()
    }

    estacoes_ids = {
        estacao: pegar_id_estacao(db, estacao)
        for estacao in set(map(lambda dado: dado.nome_estacao, dados))
    }

    conjuntos = chunked(dados, len(dados) // 10 or 1)

    with tqdm(total=len(dados), smoothing=0) as barra:
        for dados_chunk in conjuntos:
            query = "INSERT INTO metrica (id_estacao, tipo_metrica, valor, data_hora) VALUES "
            valores = []

            for dado in dados_chunk:
                for nome_metrica, valor in dado.métricas.items():
                    if valor is None:
                        continue

                    chave_normalizada = nome_metrica.strip().lower()

                    if chave_normalizada not in tipos_metricas_ids:
                        print(f"Métrica ignorada: '{nome_metrica}' (não encontrada no banco)")
                        continue

                    id_metrica = tipos_metricas_ids[chave_normalizada]
                    id_estacao = estacoes_ids[dado.nome_estacao]
                    valores.append((id_estacao, id_metrica, valor, dado.data))

            if valores:
                query += ",".join(["(%s, %s, %s, %s)"] * len(valores))
                flat_values = [item for sublist in valores for item in sublist]

                cursor = db.cursor(buffered=True)
                cursor.execute(query, flat_values)
                db.commit()
                cursor.close()
            barra.update(len(dados_chunk))

def main(inputFilePath: str):
    load_dotenv()
    print(f"* Lendo arquivo {inputFilePath}")

    with open(inputFilePath, "r", encoding="utf-8") as file:
        dados = ler_arquivo(file)

    print(f"* {len(dados)} registros lidos")
    print("** Conectando ao banco de dados")
    db = conectar_banco()
    print("** Conexão estabelecida.")

    print("** Inserindo estações...")
    inserir_estacoes(db, dados)

    print("** Inserindo métricas...")
    inserir_metricas(db, dados)

    db.close()