create schema if not exists raw;

create table if not exists raw.secop_contratos (
    id_contrato                    text primary key,
    proceso_de_compra              text,
    nombre_entidad                 text,
    nit_entidad                    text,
    codigo_entidad                 text,
    departamento                   text,
    ciudad                         text,
    orden                          text,
    sector                         text,
    rama                           text,
    estado_contrato                text,
    codigo_de_categoria_principal  text,
    objeto_del_contrato            text,
    descripcion_del_proceso        text,
    tipo_de_contrato               text,
    modalidad_de_contratacion      text,
    fecha_de_firma                 text,
    fecha_de_inicio_del_contrato   text,
    fecha_de_fin_del_contrato      text,
    proveedor_adjudicado           text,
    documento_proveedor            text,
    valor_del_contrato             text,
    url_proceso                    text,
    cargado_en                     timestamptz not null default now()
);

create table if not exists raw.tvec_ordenes (
    identificador_de_la_orden  text primary key,
    a_o                        text,
    fecha                      text,
    entidad                    text,
    nit_entidad                text,
    id_entidad                 text,
    rama_de_la_entidad         text,
    orden_de_la_entidad        text,
    sector_de_la_entidad       text,
    ciudad                     text,
    proveedor                  text,
    nit_proveedor              text,
    estado                     text,
    solicitud                  text,
    agregacion                 text,
    items                      text,
    total                      text,
    cargado_en                 timestamptz not null default now()
);

create table if not exists raw.cargas (
    id            bigint generated always as identity primary key,
    fuente        text not null,
    iniciada_en   timestamptz not null default now(),
    terminada_en  timestamptz,
    filas         integer,
    estado        text not null default 'en_curso',
    detalle       text
);