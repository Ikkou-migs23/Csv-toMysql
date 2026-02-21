from dataclasses import dataclass
from datetime import datetime
from typing import Literal


TiposEstação = Literal[
    "Nome da Estação",
    "Data",
    "Hora",
    "Tensão da Bateria",
    "Temperatura Interna da Caixa",
    "Temperatura do Ar Instantânea",
    "Temperatura do Ar Máxima 1h",
    "Temperatura do Ar Mínima 1h",
    "Umidade Relativa Instantânea",
    "Umidade Relativa Máxima 1h",
    "Umidade Relativa Mínima 1h",
    "Ponto de Orvalho Instantâneo",
    "Ponto de Orvalho Máximo 1h",
    "Ponto de Orvalho Mínimo 1h",
    "Pressão Atmosférica Instantânea",
    "Pressão Atmosférica Máxima 1h",
    "Pressão Atmosférica Mínima 1h",
    "Direção do Vento Média 10min",
    "Velocidade do Vento Média 10min",
    "Velocidade do Vento Máxima 1h",
    "Somatório da Radiação Solar 1h",
    "Somatório da Precipitação 1h",
]


@dataclass
class EstacaoDados:
    nome_estacao: str
    data: datetime
    métricas: dict[TiposEstação, float | None]

    @staticmethod
    def parse_csv(linha: str, campos: list[str]) -> "EstacaoDados":
        """
        Converte uma linha de dados delimitada por vírgulas em um dicionário com nomes reais dos campos e valores opcionais.
        """
        # Divide a linha em valores usando split
        valores = linha.split(",")
        campos = map(str.strip, campos)  # Remove espaços extras dos nomes dos campos

        dados = {}
        for campo, valor in zip(campos, valores):
            valor = valor.strip()  # Remove espaços extras
            if valor == "/":
                dados[campo] = None  # Valores opcionais tratados como None
            elif campo == "Data":
                dados[campo] = valor  # Temporariamente mantém a data como string
            elif campo == "Hora":
                if "Data" in dados and dados["Data"] is not None:
                    # Junta Data e Hora em um objeto datetime
                    dados["Data"] = datetime.strptime(
                        f"{dados['Data']} {valor}:00", "%Y-%m-%d %H:%M"
                    )
                else:
                    dados["Data"] = None  # Caso "Data" não exista, trata como None
            elif "/" in valor:
                continue  # Ignora valores com "/" (indicam dados faltantes)
            elif "(" in valor:
                campo_limpo = campo.split("(")[0].strip()  # Remove unidades

                dados[campo_limpo] = float(
                    valor
                )  # Converte valores numéricos com unidades para float
            else:
                campo_limpo = campo.split("(")[0].strip()  # Remove unidades

                try:
                    dados[campo_limpo] = float(valor)
                except ValueError:
                    # Outros campos permanecem como string
                    dados[campo_limpo] = valor

        nome = dados.pop("Nome da Estação")  # Remove o nome da estação dos dados
        data = dados.pop("Data")  # Remove a data dos dados
        return EstacaoDados(nome_estacao=nome, métricas=dados, data=data)
