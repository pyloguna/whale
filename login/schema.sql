CREATE TABLE usuario (
	id text PRIMARY KEY,
	nombre text NOT NULL,
	email text unique NOT NULL,
	foto_perfil text NOT NULL
);

create table credenciales(
	id text primary key,
	pass text not null
);