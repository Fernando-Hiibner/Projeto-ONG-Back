USE PROJETO_ONG;



CREATE TABLE IF NOT EXISTS CONTA (
    EMAIL VARCHAR(200) PRIMARY KEY,
    SENHA VARCHAR(200) NOT NULL,
    TIPO_CONTA VARCHAR(20) NOT NULL,
    DATA_CRIACAO DATETIME NOT NULL,
    DATA_ATUALIZACAO DATETIME NOT NULL,
    HASH VARCHAR(64) NOT NULL,
    VERIFICADA INT NOT NULL DEFAULT '0'
);

CREATE TABLE IF NOT EXISTS VOLUNTARIOS (
    EMAIL VARCHAR(200) NOT NULL,
    NOME VARCHAR(35) NOT NULL,
    SOBRENOME VARCHAR(200) NOT NULL,
    IDADE INT NOT NULL,
    GENERO VARCHAR(100) NOT NULL,
    DESCRICAO VARCHAR(2000),
    RANKING DECIMAL(3,2),

    FOREIGN KEY(EMAIL) REFERENCES CONTA(EMAIL) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ONGS (
    EMAIL VARCHAR(200) NOT NULL,
    NOME VARCHAR(200) NOT NULL,
    DESCRICAO VARCHAR(2000),
    DESCRICAO_DOACAO VARCHAR(500),

    FOREIGN KEY(EMAIL) REFERENCES CONTA(EMAIL) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS INTERESSES (
    EMAIL VARCHAR(200) NOT NULL,
    INTERESSE VARCHAR(200) NOT NULL,

    FOREIGN KEY(EMAIL) REFERENCES CONTA(EMAIL) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PALAVRAS_CHAVE (
    EMAIL VARCHAR(200) NOT NULL,
    PALAVRA_CHAVE VARCHAR(200) NOT NULL,

    FOREIGN KEY(EMAIL) REFERENCES CONTA(EMAIL) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS FEEDBACKS (
    EMAIL VARCHAR(200) NOT NULL,
    NOTA INT,
    FEEDBACK VARCHAR(500),

    FOREIGN KEY(EMAIL) REFERENCES CONTA(EMAIL) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CHAT (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    EMAIL_VOL VARCHAR(200) NOT NULL,
    EMAIL_ONG VARCHAR(200) NOT NULL,

    FOREIGN KEY(EMAIL_VOL) REFERENCES CONTA(EMAIL) ON DELETE CASCADE,
    FOREIGN KEY(EMAIL_ONG) REFERENCES CONTA(EMAIL) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MENSAGEM (
    CHAT_ID INT NOT NULL,
    EMAIL VARCHAR(200) NOT NULL,
    DATA_ENVIO DATETIME NOT NULL,
    TIPO VARCHAR(10) NOT NULL,
    MENSAGEM VARCHAR(10000) NOT NULL,

    FOREIGN KEY(EMAIL) REFERENCES CONTA(EMAIL) ON DELETE CASCADE
);