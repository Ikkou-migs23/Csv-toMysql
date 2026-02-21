-- Script para inserir métricas na tabela Tipo_Metrica

-- Inserção dos atributos como registros na tabela Tipo_Metrica
INSERT INTO Tipo_Metrica (nome_metrica, descricao_metrica, unidade_medida) VALUES
('Tensão da Bateria', 'Nível de tensão da bateria da estação meteorológica', 'V'),
('Temperatura Interna da Caixa', 'Temperatura dentro da caixa da PCD', 'C'),
('Temperatura do Ar Instantânea', 'Temperatura do ar registrada instantaneamente', 'C'),
('Temperatura do Ar Máxima 1h', 'Maior temperatura do ar registrada em 1 hora', 'C'),
('Temperatura do Ar Mínima 1h', 'Menor temperatura do ar registrada em 1 hora', 'C'),
('Umidade Relativa Instantânea', 'Umidade relativa do ar registrada instantaneamente', '%'),
('Umidade Relativa Máxima 1h', 'Maior umidade relativa do ar registrada em 1 hora', '%'),
('Umidade Relativa Mínima 1h', 'Menor umidade relativa do ar registrada em 1 hora', '%'),
('Ponto de Orvalho Instantâneo', 'Ponto de orvalho registrado instantaneamente', 'C'),
('Ponto de Orvalho Máximo 1h', 'Maior ponto de orvalho registrado em 1 hora', 'C'),
('Ponto de Orvalho Mínimo 1h', 'Menor ponto de orvalho registrado em 1 hora', 'C'),
('Pressão Atmosférica Instantânea', 'Pressão atmosférica registrada instantaneamente', 'hPa'),
('Pressão Atmosférica Máxima 1h', 'Maior pressão atmosférica registrada em 1 hora', 'hPa'),
('Pressão Atmosférica Mínima 1h', 'Menor pressão atmosférica registrada em 1 hora', 'hPa'),
('Direção do Vento Média 10min', 'Direção média do vento calculada em 10 minutos', 'graus'),
('Velocidade do Vento Média 10min', 'Velocidade média do vento calculada em 10 minutos', 'm/s'),
('Velocidade do Vento Máxima 1h', 'Maior velocidade do vento registrada em 1 hora', 'm/s'),
('Somatório da Radiação Solar 1h', 'Somatório da radiação solar registrada em 1 hora', 'KJ/m2'),
('Somatório da Precipitação 1h', 'Somatório da precipitação acumulada em 1 hora', 'mm')
ON CONFLICT DO NOTHING;
