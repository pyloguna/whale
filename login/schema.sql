CREATE TABLE usuario (
	id text PRIMARY KEY,
	nombre text NOT NULL,
	email text unique NOT NULL,
	foto_perfil text NOT NULL
);

create table credenciales(
	id text primary key,
	pass text not null,
	otpkey text not null
);

create table gcreds(
    openid text primary key,
    id text not null,
    CONSTRAINT FK_gcreds_id
        FOREIGN KEY (id)
        REFERENCES cliente(id)
);

