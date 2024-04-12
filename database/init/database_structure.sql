--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Ubuntu 13.10-1.pgdg20.04+1)
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: btree_gin; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gin WITH SCHEMA public;


--
-- Name: EXTENSION btree_gin; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION btree_gin IS 'support for indexing common datatypes in GIN';


--
-- Name: btree_gist; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gist WITH SCHEMA public;


--
-- Name: EXTENSION btree_gist; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION btree_gist IS 'support for indexing common datatypes in GiST';


--
-- Name: citext; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


--
-- Name: cube; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS cube WITH SCHEMA public;


--
-- Name: EXTENSION cube; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION cube IS 'data type for multidimensional cubes';


--
-- Name: dblink; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public;


--
-- Name: EXTENSION dblink; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION dblink IS 'connect to other PostgreSQL databases from within a database';


--
-- Name: dict_int; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dict_int WITH SCHEMA public;


--
-- Name: EXTENSION dict_int; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION dict_int IS 'text search dictionary template for integers';


--
-- Name: dict_xsyn; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dict_xsyn WITH SCHEMA public;


--
-- Name: EXTENSION dict_xsyn; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION dict_xsyn IS 'text search dictionary template for extended synonym processing';


--
-- Name: earthdistance; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS earthdistance WITH SCHEMA public;


--
-- Name: EXTENSION earthdistance; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION earthdistance IS 'calculate great-circle distances on the surface of the Earth';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: hstore; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public;


--
-- Name: EXTENSION hstore; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION hstore IS 'data type for storing sets of (key, value) pairs';


--
-- Name: intarray; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS intarray WITH SCHEMA public;


--
-- Name: EXTENSION intarray; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION intarray IS 'functions, operators, and index support for 1-D arrays of integers';


--
-- Name: ltree; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS ltree WITH SCHEMA public;


--
-- Name: EXTENSION ltree; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION ltree IS 'data type for hierarchical tree-like structures';


--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: pgrowlocks; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgrowlocks WITH SCHEMA public;


--
-- Name: EXTENSION pgrowlocks; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgrowlocks IS 'show row-level locking information';


--
-- Name: pgstattuple; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgstattuple WITH SCHEMA public;


--
-- Name: EXTENSION pgstattuple; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgstattuple IS 'show tuple-level statistics';


--
-- Name: tablefunc; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA public;


--
-- Name: EXTENSION tablefunc; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION tablefunc IS 'functions that manipulate whole tables, including crosstab';


--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: EXTENSION unaccent; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: xml2; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS xml2 WITH SCHEMA public;


--
-- Name: EXTENSION xml2; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION xml2 IS 'XPath querying and XSLT';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agencia; Type: TABLE; Schema: public; Owner: zvkmnkpx
--

CREATE TABLE public.agencia (
    id_agencia character varying(6) NOT NULL,
    nome character varying(255) NOT NULL,
    rua character varying(255) NOT NULL,
    cidade character varying(100) NOT NULL,
    estado character(2) NOT NULL
);


ALTER TABLE public.agencia OWNER TO zvkmnkpx;

--
-- Name: cartoes_cliente; Type: TABLE; Schema: public; Owner: zvkmnkpx
--

CREATE TABLE public.cartoes_cliente (
    id_cartao character varying(11) NOT NULL,
    conta_id character varying(11) NOT NULL,
    data_validade date NOT NULL,
    cript_cod_seguranca bytea NOT NULL,
    status character varying(20) NOT NULL,
    tipo character varying(20) NOT NULL,
    data_emissao date NOT NULL,
    cript_pin bytea NOT NULL,
    data_desativacao date,
    cript_num_cartao bytea NOT NULL,
    hash_num_cartao character varying(64) NOT NULL
);


ALTER TABLE public.cartoes_cliente OWNER TO zvkmnkpx;

--
-- Name: cliente; Type: TABLE; Schema: public; Owner: zvkmnkpx
--

CREATE TABLE public.cliente (
    id_cliente integer NOT NULL,
    nome character varying(255) NOT NULL,
    data_nascimento date NOT NULL,
    cpf character(11) NOT NULL,
    rg character varying(15) NOT NULL,
    telefone character(11) NOT NULL,
    email character varying(255)
);


ALTER TABLE public.cliente OWNER TO zvkmnkpx;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE; Schema: public; Owner: zvkmnkpx
--

CREATE SEQUENCE public.cliente_id_cliente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cliente_id_cliente_seq OWNER TO zvkmnkpx;

--
-- Name: cliente_id_cliente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zvkmnkpx
--

ALTER SEQUENCE public.cliente_id_cliente_seq OWNED BY public.cliente.id_cliente;


--
-- Name: conta_bancaria; Type: TABLE; Schema: public; Owner: zvkmnkpx
--

CREATE TABLE public.conta_bancaria (
    id_conta character varying(11) NOT NULL,
    agencia_id character varying(6) NOT NULL,
    cliente_id integer NOT NULL,
    saldo_atual numeric(15,2) NOT NULL,
    saldo_disponivel numeric(15,2) NOT NULL,
    tipo_conta character varying(20) NOT NULL,
    status_conta character varying(20) NOT NULL,
    data_criacao date NOT NULL,
    data_fechamento date,
    senha_hash character varying(100) NOT NULL
);


ALTER TABLE public.conta_bancaria OWNER TO zvkmnkpx;

--
-- Name: conta_bancaria_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: zvkmnkpx
--

CREATE SEQUENCE public.conta_bancaria_cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.conta_bancaria_cliente_id_seq OWNER TO zvkmnkpx;

--
-- Name: conta_bancaria_cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zvkmnkpx
--

ALTER SEQUENCE public.conta_bancaria_cliente_id_seq OWNED BY public.conta_bancaria.cliente_id;


--
-- Name: transacao; Type: TABLE; Schema: public; Owner: zvkmnkpx
--

CREATE TABLE public.transacao (
    id_transacao integer NOT NULL,
    conta_id character varying(11) NOT NULL,
    tipo character varying(25) NOT NULL,
    data_transacao date NOT NULL,
    valor numeric(15,2) NOT NULL,
    saldo_final numeric(15,2) NOT NULL,
    saldo_inicial numeric(15,2) NOT NULL
);


ALTER TABLE public.transacao OWNER TO zvkmnkpx;

--
-- Name: transacao_id_transacao_seq; Type: SEQUENCE; Schema: public; Owner: zvkmnkpx
--

CREATE SEQUENCE public.transacao_id_transacao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transacao_id_transacao_seq OWNER TO zvkmnkpx;

--
-- Name: transacao_id_transacao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zvkmnkpx
--

ALTER SEQUENCE public.transacao_id_transacao_seq OWNED BY public.transacao.id_transacao;


--
-- Name: cliente id_cliente; Type: DEFAULT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id_cliente SET DEFAULT nextval('public.cliente_id_cliente_seq'::regclass);


--
-- Name: conta_bancaria cliente_id; Type: DEFAULT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.conta_bancaria ALTER COLUMN cliente_id SET DEFAULT nextval('public.conta_bancaria_cliente_id_seq'::regclass);


--
-- Name: transacao id_transacao; Type: DEFAULT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.transacao ALTER COLUMN id_transacao SET DEFAULT nextval('public.transacao_id_transacao_seq'::regclass);


--
-- Name: agencia agencia_pkey; Type: CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.agencia
    ADD CONSTRAINT agencia_pkey PRIMARY KEY (id_agencia);


--
-- Name: cartoes_cliente cartoes_cliente_cript_num_cartao_key; Type: CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.cartoes_cliente
    ADD CONSTRAINT cartoes_cliente_cript_num_cartao_key UNIQUE (cript_num_cartao);


--
-- Name: cartoes_cliente cartoes_cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.cartoes_cliente
    ADD CONSTRAINT cartoes_cliente_pkey PRIMARY KEY (id_cartao);


--
-- Name: cliente cliente_email_key; Type: CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_email_key UNIQUE (email);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id_cliente);


--
-- Name: conta_bancaria conta_bancaria_pkey; Type: CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.conta_bancaria
    ADD CONSTRAINT conta_bancaria_pkey PRIMARY KEY (id_conta);


--
-- Name: transacao transacao_pkey; Type: CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.transacao
    ADD CONSTRAINT transacao_pkey PRIMARY KEY (id_transacao);


--
-- Name: conta_bancaria conta_bancaria_agencia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.conta_bancaria
    ADD CONSTRAINT conta_bancaria_agencia_id_fkey FOREIGN KEY (agencia_id) REFERENCES public.agencia(id_agencia);


--
-- Name: conta_bancaria conta_bancaria_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.conta_bancaria
    ADD CONSTRAINT conta_bancaria_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id_cliente);


--
-- Name: transacao transacao_conta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zvkmnkpx
--

ALTER TABLE ONLY public.transacao
    ADD CONSTRAINT transacao_conta_id_fkey FOREIGN KEY (conta_id) REFERENCES public.conta_bancaria(id_conta);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

