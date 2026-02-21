CREATE DATABASE Ametista;
use Ametista;

create table Estacao (
	id_estacao int auto_increment primary key,
    nome varchar(100) not null,
    localizacao varchar(235),
    descricao text
);

create table Tipo_Metrica (
	id_metrica int auto_increment primary key,
    nome_metrica varchar(100) not null,
    descricao_metrica text,
    unidade_medida varchar(50) not null
);

create table Metrica (
    id_metrica int auto_increment primary key,
    tipo_metrica int not null,
    id_estacao int not null,
    data_hora datetime not null,
    valor decimal(10, 2) not null,
    foreign key (tipo_metrica) references Tipo_Metrica(id_metrica),
    foreign key (id_estacao) references Estacao(id_estacao)
);

SELECT * FROM Estacao;
SELECT * FROM tipo_metrica;
SELECT * FROM metrica;
SELECT COUNT(*) FROM metrica;
SELECT * FROM tipo_metrica WHERE nome_metrica = 'Temperatura do ar instantânea';

alter table Estacao
add latitude_graus int,
add latitude_minutos int,
add latitude_segundos int,
add sinal_latitude varchar(100),
add altitude decimal(6,2),
add albedo decimal(4,3),
add constante_nome decimal(18,15) default  0.000000004903;

