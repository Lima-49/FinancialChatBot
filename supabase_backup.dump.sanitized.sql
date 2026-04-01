--
-- PostgreSQL database dump
--

\restrict wGcIDNs9ExccIsuYFkUPseLmhkEp5VcxwOTcLpqtGkD42hVyHXpGzqeMFGiASGe

-- Dumped from database version 17.6
-- Dumped by pg_dump version 18.3

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--



--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bancos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bancos (
    id_banco integer NOT NULL,
    nome_banco character varying(255) NOT NULL,
    valor_em_conta numeric(15,2) DEFAULT 0,
    valor_investido numeric(15,2) DEFAULT 0
);


--
-- Name: bancos_id_banco_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bancos_id_banco_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bancos_id_banco_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bancos_id_banco_seq OWNED BY public.bancos.id_banco;


--
-- Name: cartoes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cartoes (
    id_cartao integer NOT NULL,
    id_banco integer,
    nome_cartao character varying(255) NOT NULL,
    tipo_cartao integer,
    dia_vencimento integer
);


--
-- Name: cartoes_de_credito_id_cartao_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cartoes_de_credito_id_cartao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cartoes_de_credito_id_cartao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cartoes_de_credito_id_cartao_seq OWNED BY public.cartoes.id_cartao;


--
-- Name: categorias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categorias (
    id_categoria integer NOT NULL,
    nome_categoria character varying(255) NOT NULL,
    tipo character varying,
    CONSTRAINT chk_tipo_categoria CHECK (((tipo)::text = ANY ((ARRAY['ENTRADA'::character varying, 'SAIDA'::character varying])::text[])))
);


--
-- Name: categorias_de_compras_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categorias_de_compras_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categorias_de_compras_id_categoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categorias_de_compras_id_categoria_seq OWNED BY public.categorias.id_categoria;


--
-- Name: compras_cartao; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compras_cartao (
    id_compra_cartao integer NOT NULL,
    id_cartao integer,
    data_compra date,
    estabelecimento character varying(255),
    id_categoria integer,
    valor_compra numeric(15,2),
    observacoes text,
    numero_parcelas integer DEFAULT 1,
    parcela_atual integer DEFAULT 1,
    created_at timestamp without time zone DEFAULT now()
);


--
-- Name: compras_cartoes_de_credito_id_compra_cartao_credito_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.compras_cartoes_de_credito_id_compra_cartao_credito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: compras_cartoes_de_credito_id_compra_cartao_credito_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.compras_cartoes_de_credito_id_compra_cartao_credito_seq OWNED BY public.compras_cartao.id_compra_cartao;


--
-- Name: entradas_config; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.entradas_config (
    id_entrada integer NOT NULL,
    id_banco integer,
    nome_entrada character varying(255) NOT NULL,
    valor_entrada numeric(15,2),
    dia_entrada integer,
    id_categoria integer
);


--
-- Name: entradas_id_entrada_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.entradas_id_entrada_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: entradas_id_entrada_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.entradas_id_entrada_seq OWNED BY public.entradas_config.id_entrada;


--
-- Name: entradas_realizadas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.entradas_realizadas (
    id_entrada integer NOT NULL,
    id_banco integer,
    id_categoria integer,
    data_entrada date NOT NULL,
    valor numeric NOT NULL,
    descricao text,
    created_at timestamp without time zone DEFAULT now()
);


--
-- Name: entradas_realizadas_id_entrada_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.entradas_realizadas_id_entrada_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: entradas_realizadas_id_entrada_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.entradas_realizadas_id_entrada_seq OWNED BY public.entradas_realizadas.id_entrada;


--
-- Name: faturas_cartoes_de_credito; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.faturas_cartoes_de_credito (
    id_fatura_cartao_credito integer NOT NULL,
    id_cartao integer,
    valor_fatura numeric(15,2),
    paga boolean DEFAULT false,
    data_fatura date,
    data_vencimento date
);


--
-- Name: faturas_cartoes_de_credito_id_fatura_cartao_credito_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.faturas_cartoes_de_credito_id_fatura_cartao_credito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: faturas_cartoes_de_credito_id_fatura_cartao_credito_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.faturas_cartoes_de_credito_id_fatura_cartao_credito_seq OWNED BY public.faturas_cartoes_de_credito.id_fatura_cartao_credito;


--
-- Name: historico_de_mensagens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.historico_de_mensagens (
    mensagem_id integer NOT NULL,
    numero_telefone text NOT NULL,
    tipo_mensageiro text NOT NULL,
    conteudo_mensagem text NOT NULL,
    data_criacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT historico_de_mensagens_tipo_mensageiro_check CHECK ((tipo_mensageiro = ANY (ARRAY[('user'::character varying)::text, ('assistant'::character varying)::text])))
);


--
-- Name: TABLE historico_de_mensagens; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.historico_de_mensagens IS 'Histórico de conversas do WhatsApp com conteúdo criptografado';


--
-- Name: COLUMN historico_de_mensagens.numero_telefone; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.historico_de_mensagens.numero_telefone IS 'Número de telefone do usuário (formato internacional do Twilio)';


--
-- Name: COLUMN historico_de_mensagens.tipo_mensageiro; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.historico_de_mensagens.tipo_mensageiro IS 'Papel da mensagem: user ou assistant';


--
-- Name: COLUMN historico_de_mensagens.conteudo_mensagem; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.historico_de_mensagens.conteudo_mensagem IS 'Conteúdo da mensagem (CRIPTOGRAFADO)';


--
-- Name: COLUMN historico_de_mensagens.data_criacao; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.historico_de_mensagens.data_criacao IS 'Data e hora da mensagem';


--
-- Name: historico_de_mensagens_mensagem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.historico_de_mensagens_mensagem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: historico_de_mensagens_mensagem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.historico_de_mensagens_mensagem_id_seq OWNED BY public.historico_de_mensagens.mensagem_id;


--
-- Name: limites_compras; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.limites_compras (
    id_limite_compra integer NOT NULL,
    id_categoria integer,
    limite_categoria numeric(15,2)
);


--
-- Name: limites_compras_id_limite_compra_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.limites_compras_id_limite_compra_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: limites_compras_id_limite_compra_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.limites_compras_id_limite_compra_seq OWNED BY public.limites_compras.id_limite_compra;


--
-- Name: logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.logs (
    id integer NOT NULL,
    nivel character varying(20) NOT NULL,
    mensagem text NOT NULL,
    modulo character varying(255),
    funcao character varying(255),
    linha integer,
    traceback text,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT logs_nivel_check CHECK (((nivel)::text = ANY ((ARRAY['ERROR'::character varying, 'INFO'::character varying, 'WARNING'::character varying, 'DEBUG'::character varying, 'CRITICAL'::character varying])::text[])))
);


--
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;


--
-- Name: saidas_frequentes_config; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.saidas_frequentes_config (
    id_saida_frequente integer NOT NULL,
    nome_saida character varying(255) NOT NULL,
    valor_saida numeric(15,2),
    dia_saida integer,
    id_categoria integer
);


--
-- Name: saidas_frequentes_id_saida_frequente_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.saidas_frequentes_id_saida_frequente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saidas_frequentes_id_saida_frequente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.saidas_frequentes_id_saida_frequente_seq OWNED BY public.saidas_frequentes_config.id_saida_frequente;


--
-- Name: saidas_realizadas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.saidas_realizadas (
    id_saida integer NOT NULL,
    id_categoria integer,
    id_banco integer,
    data_saida date NOT NULL,
    valor numeric NOT NULL,
    descricao text,
    created_at timestamp without time zone DEFAULT now()
);


--
-- Name: saidas_realizadas_id_saida_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.saidas_realizadas_id_saida_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saidas_realizadas_id_saida_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.saidas_realizadas_id_saida_seq OWNED BY public.saidas_realizadas.id_saida;


--
-- Name: bancos id_banco; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bancos ALTER COLUMN id_banco SET DEFAULT nextval('public.bancos_id_banco_seq'::regclass);


--
-- Name: cartoes id_cartao; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cartoes ALTER COLUMN id_cartao SET DEFAULT nextval('public.cartoes_de_credito_id_cartao_seq'::regclass);


--
-- Name: categorias id_categoria; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categorias ALTER COLUMN id_categoria SET DEFAULT nextval('public.categorias_de_compras_id_categoria_seq'::regclass);


--
-- Name: compras_cartao id_compra_cartao; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compras_cartao ALTER COLUMN id_compra_cartao SET DEFAULT nextval('public.compras_cartoes_de_credito_id_compra_cartao_credito_seq'::regclass);


--
-- Name: entradas_config id_entrada; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entradas_config ALTER COLUMN id_entrada SET DEFAULT nextval('public.entradas_id_entrada_seq'::regclass);


--
-- Name: entradas_realizadas id_entrada; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entradas_realizadas ALTER COLUMN id_entrada SET DEFAULT nextval('public.entradas_realizadas_id_entrada_seq'::regclass);


--
-- Name: faturas_cartoes_de_credito id_fatura_cartao_credito; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.faturas_cartoes_de_credito ALTER COLUMN id_fatura_cartao_credito SET DEFAULT nextval('public.faturas_cartoes_de_credito_id_fatura_cartao_credito_seq'::regclass);


--
-- Name: historico_de_mensagens mensagem_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_de_mensagens ALTER COLUMN mensagem_id SET DEFAULT nextval('public.historico_de_mensagens_mensagem_id_seq'::regclass);


--
-- Name: limites_compras id_limite_compra; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.limites_compras ALTER COLUMN id_limite_compra SET DEFAULT nextval('public.limites_compras_id_limite_compra_seq'::regclass);


--
-- Name: logs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);


--
-- Name: saidas_frequentes_config id_saida_frequente; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saidas_frequentes_config ALTER COLUMN id_saida_frequente SET DEFAULT nextval('public.saidas_frequentes_id_saida_frequente_seq'::regclass);


--
-- Name: saidas_realizadas id_saida; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saidas_realizadas ALTER COLUMN id_saida SET DEFAULT nextval('public.saidas_realizadas_id_saida_seq'::regclass);


--
-- Data for Name: bancos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.bancos (id_banco, nome_banco, valor_em_conta, valor_investido) FROM stdin;
5	Alelo	0.00	0.00
6	Flash	0.00	17.16
3	Nubank Gica	0.00	0.00
2	Nubank Vitor	709.77	0.00
4	Itau 	25.97	0.00
\.


--
-- Data for Name: cartoes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.cartoes (id_cartao, id_banco, nome_cartao, tipo_cartao, dia_vencimento) FROM stdin;
2	4	Cartão Itau Vitor	0	10
4	3	Cartão Nubank Giovanna	0	23
5	5	Cartão VR Alelo	1	5
6	5	Cartão VA Alelo	1	5
7	6	Cartão Flash	1	25
1	2	Cartão Nubank Vitor	0	26
3	4	Cartão Itau Azul Vitor	1	27
\.


--
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categorias (id_categoria, nome_categoria, tipo) FROM stdin;
1	Pessoal	SAIDA
2	Pet	SAIDA
3	Mercado	SAIDA
4	Carro	SAIDA
5	Farmacia	SAIDA
6	Vestuario	SAIDA
8	Estudo	SAIDA
9	Refeição	SAIDA
10	Nany	SAIDA
11	Gica	SAIDA
12	Uber	SAIDA
7	Casa	SAIDA
13	Saude	SAIDA
14	Jogo	SAIDA
15	Streams	SAIDA
16	Viagem	SAIDA
17	Presentes	SAIDA
18	Lazer	SAIDA
19	Salario	ENTRADA
20	Beneficio	ENTRADA
21	Pix	ENTRADA
\.


--
-- Data for Name: compras_cartao; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.compras_cartao (id_compra_cartao, id_cartao, data_compra, estabelecimento, id_categoria, valor_compra, observacoes, numero_parcelas, parcela_atual, created_at) FROM stdin;
367	1	2026-03-19	Skyfit Jd Saira	13	30.00	Day use da gica	1	1	2026-03-23 20:21:20.470702
374	1	2026-03-22	Peixaria Casa grande	9	62.60	Jantar na peixaria com a gica e a nany	1	1	2026-03-23 20:26:28.261429
381	2	2026-03-25	Microsoft	15	51.00	Assinatura do microsoft	1	1	2026-03-26 22:38:02.365859
388	1	2026-03-27	Claudemir Carlos pIza	4	200.00	Troca de oleo, filtros e lampada do carro	1	2	2026-03-27 19:08:40.599803
395	1	2026-03-29	ITu SP Restaurante Lii	9	47.80	Almoco do Vitor no Catarina	1	1	2026-03-31 18:54:43.488089
10	3	2025-06-07	OPHICINA ESPLA	11	61.69	Compra do tenis da giovanna	6	6	2026-03-23 18:11:52.120727
11	3	2025-06-11	MERCADOMOVEIS	7	53.28	Compra de cobertores em curitiba	6	6	2026-03-23 18:11:52.120727
12	3	2025-06-19	DROGARIA COOP	10	51.84	Compra dos rem�dios da anny na farmacia, a nany paga uma parte	6	6	2026-03-23 18:11:52.120727
13	3	2025-06-20	OTICA NICOLAU	6	68.00	Novo oculos do vitor	10	6	2026-03-23 18:11:52.120727
14	3	2025-06-20	OTICA NICOLAU	6	68.00	Novo oculos do vitor	10	7	2026-03-23 18:11:52.120727
15	3	2025-06-20	OTICA NICOLAU	6	68.00	Novo oculos do vitor	10	8	2026-03-23 18:11:52.120727
368	1	2026-03-19	Padaria Jd Goncalves	9	53.50	Café da tarde pós treino	1	1	2026-03-23 20:22:18.279749
375	1	2026-03-23	49723590maria	3	22.67	compra no mercadinho do condominio	1	1	2026-03-26 22:29:54.872927
382	7	2026-03-25	Padaria Real	9	62.80	Compras de itens de café na Real	1	1	2026-03-26 22:39:45.859631
389	1	2026-03-28	49723590maria	3	24.48	Compra no mercadinho do condominio	1	1	2026-03-31 18:49:23.334132
396	1	2026-03-29	Cpq Catarina comercio	9	15.00	compra de 1 unidade de coca zero na casa do pão de queijo	1	1	2026-03-31 18:55:29.597142
75	1	2025-11-17	49723590maria	3	22.68	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
369	1	2026-03-20	Terezinhadejesus	9	54.55	Almoco no cachorrao do bruno	1	1	2026-03-23 20:22:55.604661
376	1	2026-03-24	Apple	15	39.90	Valor assinatura runna	1	1	2026-03-26 22:30:33.737022
383	7	2026-03-25	49723590Maria	3	24.95	Compra de refrigerante e doces no mercadinho do condominio	1	1	2026-03-26 22:40:26.890659
390	1	2026-03-28	Vetstecnologia	9	118.00	Almoco na feira koreana	1	1	2026-03-31 18:50:02.892298
397	1	2026-03-29	Food to save	9	49.95	Compra de cholote da dengo pelo food to save	1	1	2026-03-31 18:56:14.894313
148	3	2025-12-21	DECATHLONSOROC	11	80.59	Compra de novo tenis para gica	6	1	2026-03-23 18:11:52.120727
150	3	2025-12-21	DECATHLONSOROC	11	80.59	Compra de novo tenis para gica	6	2	2026-03-23 18:11:52.120727
151	3	2025-12-23	49723590MariaSOROCABABR	3	23.79	Mercadinho do condominio	1	\N	2026-03-23 18:11:52.120727
370	1	2026-03-20	Pao de acucar	3	117.54	Compra de itens de mercado	1	1	2026-03-23 20:23:28.288097
377	1	2026-03-24	Apple	15	5.90	Assinatura de mais armazenamento do icloud vitor	1	1	2026-03-26 22:31:39.852639
384	7	2026-03-25	Supermercado Confianca	3	737.44	Compra da quinzena no mercado	1	1	2026-03-26 22:41:23.145202
391	1	2026-03-28	Vetstecnologia	9	43.00	Compra do hotdog koreano e refri	1	1	2026-03-31 18:51:10.814022
398	1	2026-03-29	Casa suica	9	78.35	Compra de itens na casa suica	1	1	2026-03-31 18:57:09.051932
219	3	2026-01-18	LOJAS AMERICANAS 1163SO	9	14.99	Compra de docinhos na lojas americanas depois do aniversario do thiago	1	1	2026-03-23 18:11:52.120727
231	3	2026-01-27	TOTALPASSSAO PAULOB	15	89.90	Totalpass da gica	1	1	2026-03-23 18:11:52.120727
371	1	2026-03-21	Pet Mendes	2	109.70	Compra da areia e churu para marie	1	1	2026-03-23 20:24:28.445184
378	\N	2026-03-24	Padaria Jardim Goncal	9	47.50	Café da tarde na padaria	1	1	2026-03-26 22:32:21.666198
385	7	2026-03-26	Ifood	9	65.78	Compra de sorvete no ifood	1	1	2026-03-26 22:42:30.852086
392	1	2026-03-28	Vetstecnologia	9	32.00	Compra da raspadinha koreana	1	1	2026-03-31 18:51:51.984332
399	1	2026-03-30	Confianca supermercado	3	209.20	Compra de mercado no confianca	1	1	2026-03-31 18:57:45.052499
288	1	2026-02-14	Botquim da Francisca	9	181.50	Almoco no botequim da francisca	1	1	2026-03-23 18:11:52.120727
372	1	2026-03-22	AutopostoMairinque	4	150.00	Abastecimento do carro	1	1	2026-03-23 20:25:13.534554
379	1	2026-03-24	49723590maria	3	16.78	Compra no mercadinho do condominio	1	1	2026-03-26 22:33:10.896096
386	7	2026-03-26	Casa e Canela Cofee L	9	21.95	Salgado e café na cantina da uniso	1	1	2026-03-26 22:43:17.20513
393	1	2026-03-28	49723590	9	45.38	Compra no mercadinho do condominio	1	1	2026-03-31 18:52:37.325587
400	1	2026-03-31	Autopostoboavista	4	150.00	Abastecendo o onix	1	1	2026-03-31 18:58:32.463065
16	3	2025-07-09	O PRECINHO LO	10	27.48	Compra da bota da anny em aguas de lindoia (nany paga)	12	5	2026-03-23 18:11:52.120727
17	3	2025-07-09	O PRECINHO LO	10	27.48	Compra da bota da anny em aguas de lindoia (nany paga)	12	6	2026-03-23 18:11:52.120727
18	3	2025-07-09	O PRECINHO LO	10	27.48	Compra da bota da anny em aguas de lindoia (nany paga)	12	7	2026-03-23 18:11:52.120727
19	3	2025-08-24	MARAVILHAS DO	7	24.31	Compras de produtos para casa na maravilhas do lar	6	4	2026-03-23 18:11:52.120727
20	3	2025-08-24	MARAVILHAS DO	7	24.31	Compras de produtos para casa na maravilhas do lar	6	5	2026-03-23 18:11:52.120727
21	3	2025-08-24	MARAVILHAS DO	7	24.31	Compras de produtos para casa na maravilhas do lar	6	6	2026-03-23 18:11:52.120727
22	3	2025-09-13	MAGALU*Magalu	6	86.24	N�o lembro	4	3	2026-03-23 18:11:52.120727
23	3	2025-09-13	MAGALU*Magalu	6	86.24	N�o lembro	4	3	2026-03-23 18:11:52.120727
24	3	2025-09-19	AIRBNB PAGAM*	16	135.41	Hospedagem no airbnb em parati	6	3	2026-03-23 18:11:52.120727
25	3	2025-09-19	AIRBNB PAGAM*	16	135.41	Hospedagem no airbnb em parati	6	4	2026-03-23 18:11:52.120727
26	3	2025-09-19	AIRBNB PAGAM*	16	135.41	Hospedagem no airbnb em parati	6	5	2026-03-23 18:11:52.120727
27	3	2025-09-25	DROGASIL4226CA	5	44.63	Compra de v�rios rem�dios	3	3	2026-03-23 18:11:52.120727
28	3	2025-09-26	LOJA MATA ATLA	6	89.66	Compra do meu chinelo da reserva	3	3	2026-03-23 18:11:52.120727
29	3	2025-10-08	DROGASIL1245SO	5	105.96	Compra de v�rios rem�dios	3	2	2026-03-23 18:11:52.120727
30	3	2025-10-20	DROHGARIA JDGS 	10	14.98	Remedio nany	6	3	2026-03-23 18:11:52.120727
31	3	2025-10-20	DROHGARIA JDGS 	5	14.98	Compra de v�rios rem�dios	6	2	2026-03-23 18:11:52.120727
32	3	2025-10-20	DROHGARIA JDGS 	5	14.98	Compra de v�rios rem�dios	6	4	2026-03-23 18:11:52.120727
33	1	2025-11-04	Gh Fitness Eireli	13	101.98	Ghimper Gica (precisa cancelar)	12	10	2026-03-23 18:11:52.120727
34	1	2025-11-04	Blumo Mecnica Utomoti	4	100.00	N�o lembro dessa compra	10	10	2026-03-23 18:11:52.120727
35	1	2025-11-04	Glaciane de Moraes Si	14	86.66	Ae Games, desbloqueio do switch	6	6	2026-03-23 18:11:52.120727
36	1	2025-11-04	Mercadopago *Ofertaat	10	69.67	Bicicleta ergometrica da nany	12	6	2026-03-23 18:11:52.120727
37	1	2025-11-04	Drogasil4226	5	35.25	Algum rem�dio	1	1	2026-03-23 18:11:52.120727
38	1	2025-11-04	49723590maria	3	35.79	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
39	1	2025-11-04	Memorial Adm Emp	10	310.00	Tumulo do neno	12	11	2026-03-23 18:11:52.120727
40	1	2025-11-04	Hm Recepcao e Eventos	16	595.00	Hotel mantovani meu e da nany	12	11	2026-03-23 18:11:52.120727
41	1	2025-11-05	Mp *Cafenoponto	9	38.00	n�o lembro qual caf� � esse	1	1	2026-03-23 18:11:52.120727
42	2	2025-11-06	IFD*IFOOD CLUB	9	9.90	Clube ifoode de vantagens 	1	\N	2026-03-23 18:11:52.120727
43	3	2025-11-06	PatriciaDeVOTORANTIMBR	6	33.50	Acho que � uma compra de alguma roupa mas n�o lembro	1	1	2026-03-23 18:11:52.120727
44	3	2025-11-06	PAO DE ACUCAR-0014SOROC	3	41.18	Mercado	1	1	2026-03-23 18:11:52.120727
45	1	2025-11-07	Jumbo Estacionamento	4	11.00	Estacionamento da nutricionista	1	1	2026-03-23 18:11:52.120727
46	3	2025-11-07	SUPERMERCADO CONFIANCA	3	385.67	Mercado da semana	1	1	2026-03-23 18:11:52.120727
47	3	2025-11-07	NUTRISAVOUR DSOSOROCABA	9	10.90	Caf�	1	1	2026-03-23 18:11:52.120727
48	1	2025-11-08	Nutrifresh Comercio de	9	143.70	McDonalds afonso vergueiro	1	1	2026-03-23 18:11:52.120727
49	3	2025-11-09	SUPERMERCADO CONFIANCA	3	300.50	Mercado da semana	1	1	2026-03-23 18:11:52.120727
50	3	2025-11-10	49723590maria	3	8.90	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
51	1	2025-11-11	Apple.Com/Bill	13	47.90	Yazzio pro, 1 vez por ano	1	1	2026-03-23 18:11:52.120727
52	3	2025-11-11	HORTENCIA GONCALVES DAS	9	25.00	N�o sei 	1	1	2026-03-23 18:11:52.120727
53	3	2025-11-11	SelectPhonesSO	11	171.56	Iphone Gica	18	1	2026-03-23 18:11:52.120727
54	3	2025-11-11	O BEM SABOROSOSOROCABAB	9	83.62	Almoco antes de comprar o iphone da gica	1	1	2026-03-23 18:11:52.120727
55	3	2025-11-11	SelectPhonesSO	11	171.54	Iphone Gica	18	2	2026-03-23 18:11:52.120727
56	3	2025-11-11	SelectPhonesSO	11	171.54	Iphone Gica	18	3	2026-03-23 18:11:52.120727
57	3	2025-11-12	JIM.COM BOSS BARBER SHO	1	55.00	Cabelereiro Vitor	1	1	2026-03-23 18:11:52.120727
58	1	2025-11-13	Nutty Bavarian	9	36.00	Amendoim no shooping	1	1	2026-03-23 18:11:52.120727
59	1	2025-11-13	Drogaria Jdg	5	6.88	Algum rem�dio	1	1	2026-03-23 18:11:52.120727
60	1	2025-11-14	Applebees	9	240.12	Jantar no applebees	1	1	2026-03-23 18:11:52.120727
61	1	2025-11-14	Lavah Confianca	7	128.00	Lavagem do tapete da sala	1	1	2026-03-23 18:11:52.120727
62	1	2025-11-14	Supermercado Confianca	3	228.49	Mercado da semana	1	1	2026-03-23 18:11:52.120727
63	3	2025-11-14	TOTALPASSSAO	13	29.00	Totalpass giovanna	1	1	2026-03-23 18:11:52.120727
64	3	2025-11-14	TOTALPASSSAO	13	79.90	Totalpass giovanna	1	1	2026-03-23 18:11:52.120727
65	3	2025-11-14	GITHUB, INC.GITHUB.COMU	8	56.02	Creditos na api do GitHub	1	1	2026-03-23 18:11:52.120727
66	1	2025-11-15	Padaria Real	9	115.40	Caf� da manha na padaria real	1	1	2026-03-23 18:11:52.120727
67	1	2025-11-15	49723590maria	3	23.89	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
68	3	2025-11-15	DROGASIL1324SOROCABABR	5	34.68	Algum rem�dio	1	1	2026-03-23 18:11:52.120727
69	3	2025-11-15	MERCADOLIVRE*M 	10	49.69	Bota de trabalho para anny (nany paga)	4	1	2026-03-23 18:11:52.120727
360	1	2026-03-17	Pao de acucar	9	45.50	Cafe da tarde no pao de acucar	1	1	2026-03-23 18:11:52.120727
70	3	2025-11-15	MERCADOLIVRE*M 	10	49.66	Bota de trabalho para anny (nany paga)	4	2	2026-03-23 18:11:52.120727
71	3	2025-11-15	MERCADOLIVRE*M 	10	49.66	Bota de trabalho para anny (nany paga)	4	3	2026-03-23 18:11:52.120727
72	1	2025-11-16	Cobasi - Parcela 1/2	2	94.10	Compras para a marie de areia e comida	2	1	2026-03-23 18:11:52.120727
73	1	2025-11-16	Minuto Pa-5107	3	43.79	Compra pq a gica estava com hipo	1	1	2026-03-23 18:11:52.120727
74	1	2025-11-17	Apple.Com/Bill	15	14.99	Assinatura Crunchroll pelo prime video	1	1	2026-03-23 18:11:52.120727
76	1	2025-11-17	Supermercado Confianca	3	210.38	Compra no confianca	1	1	2026-03-23 18:11:52.120727
77	1	2025-11-17	Gebaile e Gurgel Comer	9	274.76	Compra das carnes assadas de quandos meus pais vieram em casa	1	1	2026-03-23 18:11:52.120727
78	1	2025-11-18	Drogaria Jdg	5	48.99	Algum rem�dio	1	1	2026-03-23 18:11:52.120727
79	1	2025-11-18	Apple.Com/Bill	14	19.90	Valor mensal da expans�o do icloud do meu celular	1	\N	2026-03-23 18:11:52.120727
80	1	2025-11-19	Girasoli Dolceria	9	35.00	Cookies na uniso	1	1	2026-03-23 18:11:52.120727
81	1	2025-11-19	Gelato Churros	9	18.50	Compra de salgado na cantina do F da uniso	1	1	2026-03-23 18:11:52.120727
82	1	2025-11-19	49723590maria	3	48.28	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
83	1	2025-11-20	49723590maria	3	10.49	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
84	1	2025-11-20	Drogaria Jdg	5	96.84	Algum rem�dio	1	1	2026-03-23 18:11:52.120727
85	1	2025-11-20	Vaninha Joias	11	66.00	Compra da pulseira da giovanna	1	1	2026-03-23 18:11:52.120727
86	1	2025-11-20	Casa e Canela Coffee L	9	35.95	Caf� na cafeteria ultrcoffe na uniso	1	1	2026-03-23 18:11:52.120727
87	1	2025-11-21	Gebaile e Gurgel Comer	9	136.57	Compras de carnes para churrasco na casa dos meus pais	1	1	2026-03-23 18:11:52.120727
88	1	2025-11-22	Hospital Oftalmologico	13	180.00	Consulta oftalmologica da nany	1	1	2026-03-23 18:11:52.120727
89	1	2025-11-22	Mercadodias	3	40.28	Compra no mercado do seu paulo no wanel	1	1	2026-03-23 18:11:52.120727
90	1	2025-11-22	Drogaria Sao Paulo	11	85.97	Compra de rem�dio e sabonete de rosto da Gica	1	1	2026-03-23 18:11:52.120727
91	1	2025-11-22	Rb Marsala Distribuido	9	184.14	Caf� da manha no caf� marsala depois da consulta da nany	1	1	2026-03-23 18:11:52.120727
92	1	2025-11-22	Pao de Acucar-0014	3	139.11	Compra de p�o no p�o de acucar	1	1	2026-03-23 18:11:52.120727
93	1	2025-11-22	49723590maria	3	26.98	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
94	1	2025-11-23	Sorveteria Maga	9	90.00	Compras de sorvete na casa dos meus pais	1	1	2026-03-23 18:11:52.120727
95	2	2025-11-24	Microsoft*Microsoft 36	15	51.00	Mensal do microsoft 360	1	1	2026-03-23 18:11:52.120727
96	1	2025-11-25	49723590maria	3	15.98	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
97	1	2025-11-25	Padaria Real	9	83.65	Caf� na padaria real	1	1	2026-03-23 18:11:52.120727
98	1	2025-11-27	Drogasil4226	5	77.73	Algum rem�dio	1	1	2026-03-23 18:11:52.120727
99	1	2025-11-27	Chimar Supermercados	3	103.24	compras de mercado no chimar	1	1	2026-03-23 18:11:52.120727
100	1	2025-11-27	49723590maria	3	42.79	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
101	3	2025-11-27	TOTALPASSSAO PAULOBR	13	119.90	Academia Vitor	1	1	2026-03-23 18:11:52.120727
102	1	2025-11-29	Patriciade	1	8.50	N�o lembro	1	1	2026-03-23 18:11:52.120727
103	1	2025-11-29	Uber* Trip 	12	27.95	Uber para academia	1	1	2026-03-23 18:11:52.120727
104	1	2025-11-30	Uber* Trip	12	37.96	Uber para academia	1	1	2026-03-23 18:11:52.120727
105	1	2025-11-30	49723590maria	3	25.09	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
106	2	2025-11-30	EBN *Spotify	15	31.90	Mensal do spotify	1	1	2026-03-23 18:11:52.120727
107	1	2025-12-01	ifd*Nutrisavour Comerc	9	105.68	Lanche do Mac	1	1	2026-03-23 18:11:52.120727
108	1	2025-12-01	Mercadodias	3	81.21	Compra no mercado do seu paulo no wanel	1	1	2026-03-23 18:11:52.120727
109	1	2025-12-02	49723590maria	3	30.47	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
110	3	2025-12-04	AutopostoboavistaSOROCA	4	150.00	Abastecimento do carro	1	\N	2026-03-23 18:11:52.120727
111	1	2025-12-04	Mercadopago *Ofertaat	10	69.67	Compra da bicileta ergometrica da nany	12	7	2026-03-23 18:11:52.120727
112	1	2025-12-04	Cobasi	2	94.10	Compra dos produtos da Marie	2	2	2026-03-23 18:11:52.120727
113	1	2025-12-04	Gh Fitness Eireli	13	101.98	Assinatura Ghimper Gica	12	11	2026-03-23 18:11:52.120727
114	1	2025-12-04	Memorial Adm Emp	10	310.00	Tumulo do neno	12	12	2026-03-23 18:11:52.120727
115	1	2025-12-04	Hm Recepcao e Eventos	16	595.00	Hotel mantovani meu e da nany	12	12	2026-03-23 18:11:52.120727
116	2	2025-12-06	IFD*IFOOD CLUB	9	7.95	Club ifood	1	1	2026-03-23 18:11:52.120727
117	1	2025-12-06	Ebn *Tiktok Shop	7	69.99	Compra do fiiltro no tiktok shop	1	1	2026-03-23 18:11:52.120727
118	1	2025-12-06	Syscashticket	1	104.00	N�o lembro dessa compra	1	1	2026-03-23 18:11:52.120727
119	3	2025-12-07	47.227.694 ARENITA DANS	9	107.00	Torta na betina	1	1	2026-03-23 18:11:52.120727
120	1	2025-12-07	NUTRISAVOUR DSOSOROCABA	9	106.80	Caf� na Padaria real	1	1	2026-03-23 18:11:52.120727
121	3	2025-12-09	BOALI IGUATEMI SOROCABS	9	115.70	jantar no restaurante boali no shopping	1	1	2026-03-23 18:11:52.120727
122	3	2025-12-09	ESTAC DO ESPLANADA SHSO	4	20.00	Estacionamento shopping sorocaba	1	1	2026-03-23 18:11:52.120727
123	3	2025-12-09	49723590maria	3	37.47	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
124	3	2025-12-09	DROGARIA JDG	5	65.98	Compra rem�dio vitor	1	1	2026-03-23 18:11:52.120727
125	1	2025-12-09	Jim.Com * 47774648 Ale	1	125.00	N�o lembro dessa compra	2	1	2026-03-23 18:11:52.120727
126	3	2025-12-10	ALTENBURG S�O	7	216.38	Nova colcha da nossa cama	3	1	2026-03-23 18:11:52.120727
127	3	2025-12-10	DFG MONTENEGRO	1	23.35	Capinha do celular vitor	6	1	2026-03-23 18:11:52.120727
128	3	2025-12-10	ALTENBURG S�O	7	216.38	Nova colcha da nossa cama	3	2	2026-03-23 18:11:52.120727
129	3	2025-12-10	DFG MONTENEGRO	1	23.35	Capinha do celular vitor	6	2	2026-03-23 18:11:52.120727
130	3	2025-12-11	PADARIA GRAO DE TRIGOSO	9	89.39	Compra na padaria perto de casa porque meus pais estavam vindo	1	1	2026-03-23 18:11:52.120727
131	3	2025-12-12	PAYGOS]o PauloBR	9	63.60	N�o sei 	1	1	2026-03-23 18:11:52.120727
132	3	2025-12-12	SUPERMERCADO CONFIANCA	3	302.44	Compra da semana	1	1	2026-03-23 18:11:52.120727
133	3	2025-12-13	IFD*IFOOD CLUB	9	143.90	Pedido no primatas	1	1	2026-03-23 18:11:52.120727
134	3	2025-12-14	GITHUB, INC.GITHUB.COMU	15	57.14	Github copilot	1	1	2026-03-23 18:11:52.120727
135	1	2025-12-15	Uber Uber	10	51.76	Uber para casa da nany	1	1	2026-03-23 18:11:52.120727
136	3	2025-12-16	Lavah Confianca	7	75.00	Lavagem da colcha	1	1	2026-03-23 18:11:52.120727
137	1	2025-12-17	Uber Uber	11	26.93	Uber para Gica	1	1	2026-03-23 18:11:52.120727
138	1	2025-12-18	Apple.Com/Bill	16	19.90	Assinatura icloud 	1	1	2026-03-23 18:11:52.120727
139	1	2025-12-18	Apple.Com/Bill	16	19.90	Assinatura Prime Video	1	1	2026-03-23 18:11:52.120727
140	3	2025-12-20	0026 SH ESPL 	11	76.60	Compras de roupas da gica no C&A	3	1	2026-03-23 18:11:52.120727
141	1	2025-12-20	Apple.Com/Bill	16	19.90	Assinatura Max	1	1	2026-03-23 18:11:52.120727
142	3	2025-12-20	0026 SH ESPL 	11	76.60	Compras de roupas da gica no C&A	3	2	2026-03-23 18:11:52.120727
143	3	2025-12-21	JIN JIN - SHOPPING IGUS	9	108.71	Almo�o no shopping	1	1	2026-03-23 18:11:52.120727
144	3	2025-12-21	RIACHUELO FILI	11	70.00	Compra de novas roupas giovanna	3	1	2026-03-23 18:11:52.120727
145	3	2025-12-21	CEA SOR 175	11	89.99	Compras de roupas da gica no C&A	1	1	2026-03-23 18:11:52.120727
147	3	2025-12-21	PURO GELATOVOTORANTIMBR	9	59.49	Sorvete no shopping	1	\N	2026-03-23 18:11:52.120727
152	3	2025-12-23	DROGASIL4226CAMPINASBR	11	90.77	Remedios gica	1	1	2026-03-23 18:11:52.120727
153	2	2025-12-24	Microsoft*Microsoft 36	15	51.00	Assinatura microsoft	1	1	2026-03-23 18:11:52.120727
154	3	2025-12-25	SORVETES URLASOROCABABR	9	61.38	Compra de sorvete pq meus pais vinham em casa	1	1	2026-03-23 18:11:52.120727
155	3	2025-12-25	49723590MariaSOROCABABR	3	67.35	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
157	3	2025-12-26	COBASISOROCABABR	2	139.19	Compras da marie, arreia e comida	1	1	2026-03-23 18:11:52.120727
158	3	2025-12-27	THE ROCK BOA VISTASOROC	9	144.80	Restaurante de almoco no boa vista	1	1	2026-03-23 18:11:52.120727
159	3	2025-12-27	GIRASOLISOROCABABR	9	33.40	Cookies girasoli no boa vista	1	1	2026-03-23 18:11:52.120727
160	1	2025-12-28	Gelato Madre	9	24.00	Gelato l� nos conteiners do boa vista	1	1	2026-03-23 18:11:52.120727
161	3	2025-12-29	DROGASIL1324SOROCABABR	11	75.99	Remedios gica	1	1	2026-03-23 18:11:52.120727
162	3	2025-12-29	OBA HORTIFRUTISOROCABAB	3	334.21	Compra de frutas para o final do ano	1	1	2026-03-23 18:11:52.120727
163	3	2025-12-29	SUPERMERCADO CONFIANCAS	3	166.05	Compra no mercado de final de ano	1	1	2026-03-23 18:11:52.120727
164	3	2025-12-29	DROGARIA JDGSOROCABABR	5	85.43	Compra de remedios anny	1	1	2026-03-23 18:11:52.120727
165	1	2025-12-29	Pag*Steam	14	47.58	Jogo para Gica	1	1	2026-03-23 18:11:52.120727
166	3	2025-12-30	SUPERMERCADO CONFIANCAS	3	70.87	Compra de mercado final de ano	1	1	2026-03-23 18:11:52.120727
167	3	2025-12-30	SUCO BAGACOSOROCABABR	9	37.98	Suco no iguatemi	1	1	2026-03-23 18:11:52.120727
168	3	2025-12-30	LOJA AMERICANAS	9	23.99	Compra do champanhgne do final do ano	1	1	2026-03-23 18:11:52.120727
169	3	2025-12-30	CARREFOUR	10	58.58	Ventilador para nany	6	1	2026-03-23 18:11:52.120727
170	2	2025-12-30	SPOTFY	15	31.90	Assinatura spotfy	1	1	2026-03-23 18:11:52.120727
171	3	2025-12-30	CARREFOUR	10	58.58	Ventilador para nany	6	2	2026-03-23 18:11:52.120727
172	3	2025-12-31	SUPERMERCADO CONFIANCA	3	52.51	Compra de mercado final de ano	1	1	2026-03-23 18:11:52.120727
173	1	2025-12-31	C e C Comercio de Prod	9	35.49	Caf� no dona baunilha do shopping	1	1	2026-03-23 18:11:52.120727
174	1	2025-12-31	Rosana Presentes	1	39.70	Impress�o e compras na loja de presentes	1	1	2026-03-23 18:11:52.120727
175	1	2025-12-31	Naturaehperfumaria	11	28.40	Compra de itens de unha para gica	1	1	2026-03-23 18:11:52.120727
177	3	2026-01-04	PAO DE ACUCAR-0014SOROC	3	128.40	Compra de caf� no pao de acucar	1	1	2026-03-23 18:11:52.120727
178	1	2026-01-04	Mercadopago *Ofertaat	10	69.67	Bicicleta ergometrica da nany	12	8	2026-03-23 18:11:52.120727
179	1	2026-01-04	Jim.Com * 47774648 Ale	1	125.00	N�o lembro dessa compra	2	2	2026-03-23 18:11:52.120727
180	1	2026-01-04	Gh Fitness Eireli	11	101.98	Ghimper Gica (precisa cancelar)	12	12	2026-03-23 18:11:52.120727
181	1	2026-01-04	Europag*Grecco Trattor	9	320.98	Restaurante Grecco de almoco de aniversario de casamento	1	\N	2026-03-23 18:11:52.120727
182	1	2026-01-04	49723590maria	3	34.55	Mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
184	3	2026-01-05	TOTALPASSSAO PAULOBR	13	109.90	totalpass vitor	1	1	2026-03-23 18:11:52.120727
185	3	2026-01-05	MAIS QUE CAFESOROCABABR	9	45.50	Caf� da tarde no hospital	1	1	2026-03-23 18:11:52.120727
186	1	2026-01-05	Ifd*Real Alimentos	9	70.79	Caf� na real	1	1	2026-03-23 18:11:52.120727
187	1	2026-01-05	Pao de Acucar	3	50.79	Salgado para dona Gica	1	1	2026-03-23 18:11:52.120727
188	1	2026-01-07	Yummy Salgaderia	9	48.00	Caf� da tarde no confianca	1	1	2026-03-23 18:11:52.120727
189	1	2026-01-09	Apple.Com/Bill	1	0.99	N�o sei 	1	1	2026-03-23 18:11:52.120727
190	1	2026-01-09	Padaria real	9	85.40	Caf� da tarde na padaria real	1	1	2026-03-23 18:11:52.120727
191	1	2026-01-10	Mercadolivre*Mercado	11	293.48	Secador de cabelo da gica	1	1	2026-03-23 18:11:52.120727
192	1	2026-01-11	Marilcesilveira	1	17.00	N�o sei 	1	1	2026-03-23 18:11:52.120727
193	1	2026-01-12	Pizzaria Martinez	9	101.76	Pizza depois do culto com a familia	1	1	2026-03-23 18:11:52.120727
194	1	2026-01-12	Saldaoinformatica	10	350.73	Compra do notebook da nany	6	1	2026-03-23 18:11:52.120727
195	1	2026-01-14	Estrela Padaria	9	129.79	Caf� da tarde padaria estrela	1	1	2026-03-23 18:11:52.120727
196	3	2026-01-07	DrhogariaJDG	11	103.80	Remedios gica	1	1	2026-03-23 18:11:52.120727
198	3	2026-01-10	Supermercado Confianca	3	539.30	Compra de mercado da semana	1	1	2026-03-23 18:11:52.120727
199	3	2026-01-11	Perfumaria princesa	11	54.65	Compra de shampoo da gica	2	1	2026-03-23 18:11:52.120727
200	3	2026-01-11	Fgdoceriasorocaba	9	73.15	Caf� no dona baunilhana rua	1	1	2026-03-23 18:11:52.120727
201	3	2026-01-12	AutopostoboavistaSOROCA	4	186.77	completando alcool no onix	1	1	2026-03-23 18:11:52.120727
202	3	2026-01-12	Padaria Jardim Goncalves	9	97.00	itens de caf� para meus pais que estavam vindo	1	1	2026-03-23 18:11:52.120727
203	3	2026-01-13	ifd*brosascobr	9	52.94	Milkshake da gica	1	1	2026-03-23 18:11:52.120727
204	1	2026-01-18	Apple.Com/Bill	15	19.90	PrimeVideo Assinatura	1	1	2026-03-23 18:11:52.120727
205	1	2026-01-23	Chimar Supermercados	3	69.23	Compra de itens para café da tarde no chimar	1	1	2026-03-23 18:11:52.120727
206	1	2026-01-31	49723590maria	3	24.89	Compra no mercado do condominio	1	1	2026-03-23 18:11:52.120727
197	3	2026-01-08	P.m.a alimentossorcaba	9	75.70	Subway	1	1	2026-03-23 18:11:52.120727
207	3	2025-12-21	RIACHUELO FILI	11	69.99	Compra de roupas da gica na riachuelo	3	2	2026-03-23 18:11:52.120727
208	3	2026-01-14	ifd*brosascobr	9	32.66	Compra de comida no ifood	1	1	2026-03-23 18:11:52.120727
210	3	2026-01-15	ROSANA PRESENTESSOROCAB	1	5.00	Impressão dos relatorios da igreja	1	1	2026-03-23 18:11:52.120727
211	3	2026-01-16	49723590MariaSOROCABABR	3	29.88	Compra no mercado do condomínio	1	1	2026-03-23 18:11:52.120727
212	3	2026-01-15	SUPERMERCADO CONFIANCAS	3	136.01	Compras de misturas no confianca	1	1	2026-03-23 18:11:52.120727
213	3	2026-01-16	SUPERMERCADO DO BAIRROS	3	106.17	Compra para a nany	1	1	2026-03-23 18:11:52.120727
214	3	2026-01-16	SUPERMERCADO DO BAIRROS	3	1.16	Um salgado veio estragado tive que voltar devolver	1	1	2026-03-23 18:11:52.120727
215	3	2026-01-17	TOTALPASSSAO PAULOBR	15	89.90	pagamento totalpass	1	1	2026-03-23 18:11:52.120727
216	3	2026-01-17	BRUNO DOGSOROCABABR	9	81.70	Alomoço no restaurante da pracinha	1	1	2026-03-23 18:11:52.120727
217	3	2026-01-17	FarmaCondeSASOROCABABR	5	76.85	Compra dos remédios na farmacia	1	1	2026-03-23 18:11:52.120727
218	3	2026-01-18	OUTBACK STEAKHOUSESOROC	9	146.37	aniversário do thiago no outback	1	1	2026-03-23 18:11:52.120727
156	3	2025-12-26	RECANTO DOS VERDESSOROC	18	128.50	Pesqueiro em tatui com os meninos	1	1	2026-03-23 18:11:52.120727
220	3	2026-01-18	IFD*BROSASCOBR	9	97.78	compra de ifood para o almoco	1	1	2026-03-23 18:11:52.120727
221	3	2026-01-19	49723590MariaSOROCABABR	3	44.88	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
222	3	2026-01-19	49723590MariaSOROCABABR	3	28.48	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
223	3	2026-01-19	49723590MariaSOROCABABR	3	10.38	Compra mercadinho do condominio	1	\N	2026-03-23 18:11:52.120727
224	3	2026-01-21	BOM LUGAR LJ WANE VILLS	3	62.19	Compra de itens de café da tarde para ir na tatinha	1	1	2026-03-23 18:11:52.120727
225	3	2026-01-21	COOPSOROCABABR	10	43.40	Compra que a nany fez no me cartão dos remédios da anny	6	1	2026-03-23 18:11:52.120727
226	3	2026-01-22	IFD*TOTEM BLACKOUT BURS	9	88.00	Jantar no hamburguer podrero	1	1	2026-03-23 18:11:52.120727
227	3	2026-01-22	49723590MariaSOROCABABR	3	7.99	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
228	3	2026-01-24	COBASISOROCABABR	2	136.62	Compra de ração e areia da Marie	1	1	2026-03-23 18:11:52.120727
229	3	2026-01-26	TAMMY PASTELARIA LTDASO	9	37.00	Almoco antes da consulta na tammy do campolim	1	1	2026-03-23 18:11:52.120727
230	3	2026-01-26	DROHGARIA JDGS	5	103.30	Compra das vitaminas e injecao do vitor bariatrico	3	1	2026-03-23 18:11:52.120727
232	3	2026-01-27	BhlCafeteriaESOROCABABR	9	89.00	Café da tarde na era uma vez	1	1	2026-03-23 18:11:52.120727
233	3	2026-01-29	PADARIA REALSOROCABABR	9	98.90	cafe da tarde na real	1	1	2026-03-23 18:11:52.120727
234	3	2026-01-30	PADARIA JARDIM GONCALVS 	9	48.18	Compra de itens de cafe da tarde	1	\N	2026-03-23 18:11:52.120727
235	3	2026-01-31	SUPERMERCADO CONFIANCAS 	3	149.90	Compra de mistura e frutas no confiança	1	1	2026-03-23 18:11:52.120727
236	3	2026-02-01	REINALDO CHICAROLLI MAM	3	37.00	Compra de refrigerante no chimar de mairinque	1	1	2026-03-23 18:11:52.120727
237	3	2026-02-01	LOJAS ESTRELA DO LAR LV 	7	89.94	Compra de 4 jogos americanos na loja estreala do lar	1	1	2026-03-23 18:11:52.120727
238	3	2026-02-01	KaoriNakanishiVOTORANTI	9	199.87	Jantar no Kaori com a gica	1	1	2026-03-23 18:11:52.120727
239	3	2026-02-03	49723590MariaSOROCABABR	3	45.37	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
240	3	2026-02-03	BOM LUGAR LJ WANE VILLS 	3	55.60	Compra no wanel para tomar cafe na anny	1	1	2026-03-23 18:11:52.120727
241	3	2026-02-04	IFD*BROSASCOBR	9	38.97	Almoco panela express	1	1	2026-03-23 18:11:52.120727
242	3	2026-02-04	PRIMATAS HAMBURGUERIASO	9	124.78	Jantar no primatas com a gica	1	1	2026-03-23 18:11:52.120727
243	3	2026-01-14	GITHUB, INC.GITHUB.COMU	15	59.20	Assinatura github copilot	1	1	2026-03-23 18:11:52.120727
244	2	2026-01-31	SPOTFY	15	31.90	assinatura spotfy	1	1	2026-03-23 18:11:52.120727
245	2	2026-01-07	IFD*IFOOD CLUB	15	7.95	assinatura ifood	1	1	2026-03-23 18:11:52.120727
246	3	2025-06-20	OTICA NICOLAU	1	68.00	Parcela do oculos do vitor	10	9	2026-03-23 18:11:52.120727
247	3	2026-07-09	O PRECINHO	10	27.48	Compra da bota da anny	12	8	2026-03-23 18:11:52.120727
248	3	2025-12-18	Airbnb pagam	16	135.41	Parcela do Airbnb de paraty	6	6	2026-03-23 18:11:52.120727
279	1	2026-02-11	Daniel Ataide dallava	9	49.00	Pães de fermetação natural 	1	1	2026-03-23 18:11:52.120727
249	3	2026-10-20	DHROGARIA JDG	5	14.98	Pagamento de parcela de compra de remedio	6	5	2026-03-23 18:11:52.120727
250	3	2025-11-11	SELECTPHONE	11	171.54	Parcela do iphone da gica	18	4	2026-03-23 18:11:52.120727
251	3	2025-11-15	MERCADOLIVRE	10	49.66	Parcela da bota da anny	4	4	2026-03-23 18:11:52.120727
252	3	2026-12-10	ALTENBURG	7	216.66	parcela do nosso novo edredom	3	3	2026-03-23 18:11:52.120727
253	3	2026-12-10	DFG MONTENEGRO	1	23.31	Parcela capinha do vitor	6	3	2026-03-23 18:11:52.120727
254	3	2025-12-20	0026 SH ESPL 	11	76.60	Compras de roupas da gica no C&A\n	3	3	2026-03-23 18:11:52.120727
255	3	2025-12-21	RIACHUELO FILI\n	11	69.99	Compra de roupas para Gica na Riachuelo	3	3	2026-03-23 18:11:52.120727
257	3	2025-12-21	DECATHLONSOROC\n	11	80.57	Compra de novo tenis para gica\n	6	3	2026-03-23 18:11:52.120727
258	3	2025-12-30	CARREFOUR\n	10	58.55	Ventilador para nany\n	6	3	2026-03-23 18:11:52.120727
259	3	2026-01-11	Perfumaria princesa\n	11	54.65	Compra de shampoo da gica\n	2	2	2026-03-23 18:11:52.120727
260	3	2026-01-21	Coopsorocaba	10	43.39	Compra dos remédios da anny 	6	2	2026-03-23 18:11:52.120727
261	3	2026-01-26	103.28	5	103.28	Compra dos remedios de bariatrico do Vitor	3	2	2026-03-23 18:11:52.120727
262	3	2026-02-07	Totalpass	15	109.90	Assinatura do totalpass\n	1	1	2026-03-23 18:11:52.120727
263	3	2026-02-08	Fazenda esplanada food	9	77.52	Almoco no restaurante no shopping	1	1	2026-03-23 18:11:52.120727
264	1	2026-02-04	Saldaodainformatica	10	350.70	Parcela notebook da nany	6	2	2026-03-23 18:11:52.120727
265	1	2026-02-04	Mercadopago *Ofertaat\n	10	69.67	Bicicleta ergometrica da nany	12	9	2026-03-23 18:11:52.120727
266	1	2026-02-06	Supermercado Confianca	3	219.84	Compra de mercado no supermercado	1	1	2026-03-23 18:11:52.120727
267	1	2026-02-07	Pis Restaurante	9	167.24	Nao sei qual que é	1	1	2026-03-23 18:11:52.120727
268	1	2026-02-07	Cabocafe	9	64.35	Cafe da tarde no cabo cafe com a gica	1	1	2026-03-23 18:11:52.120727
269	1	2026-02-08	Espetinhos do Zan	9	278.04	comemoracao do aniversario vitor	1	1	2026-03-23 18:11:52.120727
270	1	2026-02-08	Mp *Deliciusbolo	9	158.14	pagamento do bolo do aniversario do vitor	1	1	2026-03-23 18:11:52.120727
271	1	2026-02-08	49723590maria\n	3	35.38	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
272	1	2026-02-09	Mp*Taynara	10	100.00	Nany comprou uma flor para a anny 	1	1	2026-03-23 18:11:52.120727
273	1	2026-02-09	Daiso Brasil	1	49.96	Compra da luz do setup do vitor e produtos da gica	1	1	2026-03-23 18:11:52.120727
275	1	2026-02-10	Padaria Jardim Goncalv	9	54.55	Café da tarde com o pai eliel	1	1	2026-03-23 18:11:52.120727
276	1	2026-02-10	Terezinhajeus	9	54.55	Almoco no restaurante da praca	1	1	2026-03-23 18:11:52.120727
277	1	2026-02-11	Jumbo Estacionamento	4	20.00	Estacionamento no predio da nutricionesta	1	1	2026-03-23 18:11:52.120727
278	1	2026-02-11	Porquilo Restaurante	9	140.00	Almoço no restaurante porquilo	1	1	2026-03-23 18:11:52.120727
280	1	2026-02-11	Skyfit Jd.Saira	9	12.00	Compra de energetico na academia	1	1	2026-03-23 18:11:52.120727
281	1	2026-02-12	Uber	12	17.95	Uber para a endoscopia	1	1	2026-03-23 18:11:52.120727
282	1	2026-02-12	Itu Sp restaurante li	9	39.40	Almoco no shopping no tacobel	1	1	2026-03-23 18:11:52.120727
283	1	2026-02-12	Tbb Gestao de Restaurant	9	44.90	Almoco no shopping spoletto	1	1	2026-03-23 18:11:52.120727
284	1	2026-02-12	Daiso	1	17.98	Compra de coisas na Daiso	1	1	2026-03-23 18:11:52.120727
285	1	2026-02-13	Auto Posto SB Sorocaba	4	67.00	Completando o óleo do carro	1	1	2026-03-23 18:11:52.120727
286	1	2026-02-13	Luciano Duarte	7	14.00	Compra de um novo rodo	1	1	2026-03-23 18:11:52.120727
287	1	2026-02-13	49723590maria	3	11.90	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
289	1	2026-02-14	CacauShow	9	39.97	Docinhos na cacaushow	1	1	2026-03-23 18:11:52.120727
290	1	2026-02-14	Bom Lugar Wanel Vili	3	84.61	Compra de itens de café para ir na nany	1	1	2026-03-23 18:11:52.120727
291	1	2026-02-15	Droga Raia	5	71.77	Compra do remédio da Gica antes de viajar	1	1	2026-03-23 18:11:52.120727
292	1	2026-02-15	Rest Frangoassado Jag	9	138.97	Almoco no frango assado indo para monte santo	1	1	2026-03-23 18:11:52.120727
293	1	2026-02-16	Du massas	9	58.00	Compra de sorvete em Monte Santo	1	1	2026-03-23 18:11:52.120727
294	1	2026-02-17	Picorautoposto	4	169.23	Abastecendo o carro saindo de montesanto	1	1	2026-03-23 18:11:52.120727
295	1	2026-02-17	Apple	15	19.90	Assinatura do PrimeVideo	1	1	2026-03-23 18:11:52.120727
296	1	2026-02-17	Oma Beppie	9	142.51	compra de itens na loja holandesa em holambra	1	1	2026-03-23 18:11:52.120727
297	1	2026-02-18	Parmeggio Grlhados	9	53.90	Almoco no shopping	1	1	2026-03-23 18:11:52.120727
298	1	2026-02-18	Food to Save	9	66.94	compra de itens de cafe com food to save	1	1	2026-03-23 18:11:52.120727
299	1	2026-02-19	49723590maria	3	44.47	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
300	1	2026-02-19	Bruno Dog	9	73.55	Almoço no bruno dog	1	1	2026-03-23 18:11:52.120727
301	1	2026-02-20	Confianca Supermercado	9	69.51	Almoco no Confianca	1	1	2026-03-23 18:11:52.120727
302	1	2026-02-20	Confianca supermercado	3	325.67	Compra no mercado	1	1	2026-03-23 18:11:52.120727
303	1	2026-02-20	McDonalds	9	97.80	Jantar no mc	1	1	2026-03-23 18:11:52.120727
304	1	2026-02-21	TikTok Shop	1	99.40	Compra dos dois fones meu e da gica	1	1	2026-03-23 18:11:52.120727
305	1	2026-02-22	Reinaldo Chicarolli	3	114.73	Compra de itens para comer na casa dos meus pais	1	1	2026-03-23 18:11:52.120727
306	1	2026-02-23	Mp*Patcy	9	90.20	Cafe da tarde na patcy	1	1	2026-03-23 18:11:52.120727
308	3	2026-02-12	Pietro pieroti cafe	9	41.50	Café da tarde na Mr black	1	1	2026-03-23 18:11:52.120727
309	3	2026-02-13	49723590maria	3	29.48	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
310	3	2026-02-14	GITHUB, INC.GITHUB.COMU	15	55.50	Assinatura do github	1	1	2026-03-23 18:11:52.120727
311	3	2026-02-14	Coopsorocabr	5	88.89	Compra na farmacia de remedios	1	1	2026-03-23 18:11:52.120727
312	3	2026-02-25	Padaria real	9	67.40	café da tarde com a gica na real	1	1	2026-03-23 18:11:52.120727
314	3	2026-02-25	Padaria Jardim Goncalves	9	38.50	Salgados na padaria antes de ir para mãe	1	1	2026-03-23 18:11:52.120727
315	2	2026-02-06	IFD*IFOOD CLUB	15	7.95	Assinatura club ifood	1	1	2026-03-23 18:11:52.120727
316	2	2026-02-25	*microsoft	15	51.00	Assinatura do pacote office	1	1	2026-03-23 18:11:52.120727
317	3	2026-02-27	Drohgaria jdgsorocababr	5	181.70	Compra dos remédios do Vitor\n	1	1	2026-03-23 18:11:52.120727
318	3	2026-02-27	Totalpass paulobr	15	89.90	Assinatura do totalpass	1	1	2026-03-23 18:11:52.120727
319	3	2026-02-28	Pty*restaurantekostelasorocaba	9	331.00	Almoço no costela do japones com a nany	1	1	2026-03-23 18:11:52.120727
320	3	2026-03-03	Supermercado Confianca	3	258.19	Complementando o valor do flahs na compra do mercado	1	1	2026-03-23 18:11:52.120727
321	1	2026-03-05	Food To Save	9	43.97	Compra no food to save da cacaushow	1	1	2026-03-23 18:11:52.120727
322	1	2026-03-06	Boss Barber	1	70.00	Corte de cabelo vitor	1	1	2026-03-23 18:11:52.120727
323	1	2026-02-07	Nfpl Calcados e Acesso	6	199.90	Compra do presente de aniversario do pai	1	1	2026-03-23 18:11:52.120727
324	1	2026-03-07	Vororantim Maquiag	11	40.00	Compra de maquiagem da gica	1	1	2026-03-23 18:11:52.120727
325	1	2026-03-07	Panetteria e Cafeteria	9	46.60	Cafe e panetoni no shopping	1	1	2026-03-23 18:11:52.120727
326	1	2026-03-08	Google one	15	1.00	Aumento de armazenamento do google	1	1	2026-03-23 18:11:52.120727
328	1	2026-03-08	Cachorrao do Abner	9	80.50	Lanche no abner a noite	1	1	2026-03-23 18:11:52.120727
329	1	2026-03-09	49723590maria	3	24.39	Compras no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
330	1	2026-03-09	Drogasil	5	53.77	pomada para assadura	1	1	2026-03-23 18:11:52.120727
331	1	2026-03-10	Drogaria Jdg	5	51.00	Remedio do vitor	1	1	2026-03-23 18:11:52.120727
332	1	2026-03-10	Autopostoboavista	4	196.49	Completando o tanque com alcool	1	1	2026-03-23 18:11:52.120727
333	1	2026-03-10	Pao de acucar	3	473.18	Compra de itens de casa no pao de acucar	1	1	2026-03-23 18:11:52.120727
334	3	2026-03-07	Itau	1	262.35	Encargos refinanciamento	1	1	2026-03-23 18:11:52.120727
335	3	2026-03-07	Itau	1	17.37	Juros de mora	1	1	2026-03-23 18:11:52.120727
336	3	2026-03-07	Itau	1	94.77	Multa atraso de pagamento	1	1	2026-03-23 18:11:52.120727
327	1	2026-03-08	Veraantonia	3	36.00	Compra de itens de café	1	1	2026-03-23 18:11:52.120727
337	2	2026-04-06	Ifd*ifood club	15	7.95	Assinatura club ifood	1	1	2026-03-23 18:11:52.120727
338	3	2026-04-20	Otica nicolau scarpa	6	68.00	Parcela do oculos vitor	10	10	2026-03-23 18:11:52.120727
339	3	2026-06-09	O PRECINHO	10	27.48	Compra da bota da anny	12	9	2026-03-23 18:11:52.120727
340	3	2026-04-20	Drohgaria jdgsorocaba	5	14.98	Compra de remedios na farmacia do bairro	6	6	2026-03-23 18:11:52.120727
341	3	2026-04-11	SelectphoeSorocaba	11	171.54	Compra do iphone da Gica	18	5	2026-03-23 18:11:52.120727
342	3	2026-04-10	Dfg montenegrosaovicente	1	23.31	Parcela capa de celular vitor	6	4	2026-03-23 18:11:52.120727
344	3	2026-04-21	Decathlonsorocaba	11	80.57	Compra de itens pra gica na decathlon	6	4	2026-03-23 18:11:52.120727
345	3	2026-04-30	Carrefoursorocaba	10	58.55	Compra do ventilador da nany	6	4	2026-03-23 18:11:52.120727
346	3	2026-04-21	CoopSorocaba	10	43.39	Compra dos remedios da nany	6	3	2026-03-23 18:11:52.120727
347	3	2026-04-26	Dhrogariajdg	5	103.28	Compra dos remedios do vitor	3	3	2026-03-23 18:11:52.120727
348	3	2026-04-25	Conteudo0a90	11	116.56	Compra dos itens do tratamento da gica	3	2	2026-03-23 18:11:52.120727
349	1	2026-03-10	49723590maria	3	38.88	Compra no mercadinho do condominio	1	1	2026-03-23 18:11:52.120727
350	1	2026-03-11	Nubank	1	493.62	Parcelamento da fatura	6	1	2026-03-23 18:11:52.120727
351	1	2026-03-11	Consultorio medico	11	250.00	Pagamento do Dr marcos da Gica	2	1	2026-03-23 18:11:52.120727
352	1	2026-03-11	Panificador Cepam	9	187.69	Almoco na Cepam	1	1	2026-03-23 18:11:52.120727
353	1	2026-03-11	Ifood	9	97.98	Pizza da noite	1	1	2026-03-23 18:11:52.120727
354	1	2026-03-13	Carolina Pane Gusto	9	72.76	Cafeteria na Cafeteria Carolina	1	1	2026-03-23 18:11:52.120727
355	1	2026-03-13	McDonalds	9	63.80	Jantar no mc	1	1	2026-03-23 18:11:52.120727
356	1	2026-03-14	Pao de acucar	3	148.57	Compra no mercado	1	1	2026-03-23 18:11:52.120727
357	1	2026-03-13	Ifood	9	148.18	Esfihas para o irmao ezequiel	1	1	2026-03-23 18:11:52.120727
358	1	2026-03-15	Oba hortifruti	3	171.93	Compras de mercado	1	1	2026-03-23 18:11:52.120727
359	1	2026-03-16	Confianca supermercado	3	163.16	Compras de mercado	1	1	2026-03-23 18:11:52.120727
307	1	2026-02-27	Apple	18	9.90	Alugando clube do cinco no prime video	1	1	2026-03-23 18:11:52.120727
313	3	2026-02-25	Conteudo0a90	11	116.58	Compra dos itens do tratamento da gica	3	1	2026-03-23 18:11:52.120727
361	1	2026-03-17	Mcdonalds	9	112.70	Jantar com os pai	1	1	2026-03-23 18:11:52.120727
362	1	2026-03-18	Apple	15	19.90	Pagamento do amazn prime	1	1	2026-03-23 18:11:52.120727
363	1	2026-03-18	Real Gastronomia Serv	9	131.20	Almoco na real	1	1	2026-03-23 18:11:52.120727
364	1	2026-03-18	Padaria real	9	59.80	Itens de padaria da real	1	1	2026-03-23 18:11:52.120727
366	1	2026-03-18	Cinepolis	9	89.00	Compra de pipoca no cinema	1	1	2026-03-23 18:11:52.120727
146	3	2025-12-21	PBKIDS BRINQUE	17	31.69	Compra de um presente para aurora	6	1	2026-03-23 18:11:52.120727
149	3	2025-12-21	PBKIDS BRINQUE	17	31.69	Compra de um presente para aurora	6	2	2026-03-23 18:11:52.120727
176	1	2025-12-31	Daiso Brasil	17	119.43	Compra dos presentes para o jogo do final do ano	2	1	2026-03-23 18:11:52.120727
183	1	2026-01-04	Daiso Brasil	17	119.42	Compra dos presentes para o jogo do final do ano	2	2	2026-03-23 18:11:52.120727
256	3	2025-12-21	PBKIDS BRINQUE\n	17	31.66	Compra de um presente para aurora\n	6	3	2026-03-23 18:11:52.120727
274	1	2026-02-09	Maravilha do Lar	17	83.95	Compra dos presentes do chá de cozinha da Mayara	1	1	2026-03-23 18:11:52.120727
343	3	2026-04-21	PBkids brinquedos	17	31.66	Compra do presente da lola	6	4	2026-03-23 18:11:52.120727
365	1	2026-03-18	Ingresso.com	18	39.52	Ingressos do cinema	1	1	2026-03-23 18:11:52.120727
373	1	2026-03-22	Wagnerbernado	18	20.00	Estacionamento do restaurante	1	1	2026-03-23 20:25:56.144602
380	1	2026-03-26	Otica Nicolau Scarpa	11	126.50	Compra do oculos da gica de 1265	1	10	2026-03-26 22:34:40.926537
387	1	2026-03-26	Oca Burguer	9	78.00	Jantar com o thales	1	1	2026-03-27 19:07:49.998166
394	1	2026-03-29	The Steak Outlote Catar	9	48.80	Almoco da gica no catarina	1	1	2026-03-31 18:53:57.495036
\.


--
-- Data for Name: entradas_config; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.entradas_config (id_entrada, id_banco, nome_entrada, valor_entrada, dia_entrada, id_categoria) FROM stdin;
1	4	Salario IQVIA	3200.00	9	19
2	4	Salario IQVIA 2	2789.68	25	19
4	3	Salario Uniso	960.00	5	19
5	5	VR Uniso	450.00	5	20
6	5	VA Uniso	180.00	5	20
3	6	VR/VA IQVIA	900.00	25	20
\.


--
-- Data for Name: entradas_realizadas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.entradas_realizadas (id_entrada, id_banco, id_categoria, data_entrada, valor, descricao, created_at) FROM stdin;
1	4	19	2025-12-09	3200.00	Salario IQVIA	2026-03-23 18:11:52.120727
2	4	19	2025-12-25	2789.68	Salario IQVIA 2	2026-03-23 18:11:52.120727
3	6	20	2025-12-25	865.00	VR/VA IQVIA	2026-03-23 18:11:52.120727
4	3	19	2025-12-05	960.00	Salario Uniso	2026-03-23 18:11:52.120727
5	5	20	2025-12-05	450.00	VR Uniso	2026-03-23 18:11:52.120727
6	5	20	2025-12-05	180.00	VA Uniso	2026-03-23 18:11:52.120727
7	4	19	2026-01-09	3200.00	Salario IQVIA	2026-03-23 18:11:52.120727
8	4	19	2026-01-25	2789.68	Salario IQVIA 2	2026-03-23 18:11:52.120727
9	6	20	2026-01-25	865.00	VR/VA IQVIA	2026-03-23 18:11:52.120727
10	3	19	2026-01-05	960.00	Salario Uniso	2026-03-23 18:11:52.120727
11	5	20	2026-01-05	450.00	VR Uniso	2026-03-23 18:11:52.120727
12	5	20	2026-01-05	180.00	VA Uniso	2026-03-23 18:11:52.120727
13	4	19	2026-02-09	3200.00	Salario IQVIA	2026-03-23 18:11:52.120727
14	4	19	2026-02-25	2789.68	Salario IQVIA 2	2026-03-23 18:11:52.120727
15	6	20	2026-02-25	865.00	VR/VA IQVIA	2026-03-23 18:11:52.120727
16	3	19	2026-02-05	960.00	Salario Uniso	2026-03-23 18:11:52.120727
17	5	20	2026-02-05	450.00	VR Uniso	2026-03-23 18:11:52.120727
18	5	20	2026-02-05	180.00	VA Uniso	2026-03-23 18:11:52.120727
19	4	19	2026-03-09	3200.00	Salario IQVIA	2026-03-23 18:11:52.120727
20	4	19	2026-03-25	2789.68	Salario IQVIA 2	2026-03-23 18:11:52.120727
21	6	20	2026-03-25	865.00	VR/VA IQVIA	2026-03-23 18:11:52.120727
22	3	19	2026-03-05	960.00	Salario Uniso	2026-03-23 18:11:52.120727
23	5	20	2026-03-05	450.00	VR Uniso	2026-03-23 18:11:52.120727
24	5	20	2026-03-05	180.00	VA Uniso	2026-03-23 18:11:52.120727
25	6	20	2026-03-25	900	VR/VA da IQIA	2026-03-26 22:45:08.402492
26	2	21	2026-03-20	200	Pix de 200 da consulta da gica que a minha mãe fez	2026-03-26 22:47:45.470235
27	2	21	2026-03-22	38	Pagamento do peixe da anny	2026-03-26 22:48:46.239682
28	2	21	2026-03-24	539.15	Dinheiro resgatdado da XP investimentos	2026-03-26 22:49:33.754944
29	2	21	2026-03-26	540	Pagamento das coisas da nany que estao no meu cartao	2026-03-26 22:50:17.669748
30	2	21	2026-03-26	550	Ajuda da minha mãe para pagar as contas	2026-03-26 22:50:51.992422
\.


--
-- Data for Name: faturas_cartoes_de_credito; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.faturas_cartoes_de_credito (id_fatura_cartao_credito, id_cartao, valor_fatura, paga, data_fatura, data_vencimento) FROM stdin;
2	4	0.00	t	2025-12-31	2026-01-23
4	2	90.85	t	2025-12-31	2026-01-10
6	4	79.95	t	2026-01-31	2026-02-23
8	2	39.85	t	2026-01-31	2026-02-10
9	3	4738.35	t	2026-02-28	2026-03-27
5	3	4405.05	t	2026-01-31	2026-02-27
13	3	783.32	f	2026-04-30	2026-05-27
7	1	2034.34	t	2026-02-28	2026-03-26
3	1	2408.97	t	2026-01-31	2026-02-26
12	2	90.85	t	2026-02-28	2026-03-10
11	3	3110.50	t	2026-03-31	2026-04-27
16	1	3613.78	f	2026-03-31	2026-04-26
18	2	58.95	f	2026-04-30	2026-05-10
17	1	3496.91	f	2026-04-30	2026-05-26
\.


--
-- Data for Name: historico_de_mensagens; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.historico_de_mensagens (mensagem_id, numero_telefone, tipo_mensageiro, conteudo_mensagem, data_criacao) FROM stdin;
1	+55119782848304	user	gAAAAABpVGN2kSEeTA6QhEBOo12CS-hbkRCp5NKI28pmPD_ajzHeSDolTlF9zcrs3MI4G9x28-y_5tkrLPzEONb3cj2a8aZF5Q==	2025-12-30 20:42:52.156122
2	+55119782848304	assistant	gAAAAABpVGOUpy38Jvks_KidgMFOJ23ztCLhbTRLi_-2XqIWyFJ7OMgb8G6_SwtGxIeKjbchRPwXkwQ1VIxHXasPYRcp79SqXFB6Y78PLZWQcxZgNLoenpKD9InHWUU-X47vbzDBkeTTeMq_CsBaV6cO5ezDwVciHw==	2025-12-30 20:43:16.545978
3	+55119782848304	user	gAAAAABpVGRD8fDVoTnqrwkq8NrRN-CIdHi1Fg0W_vyoFOiw5O3oAEBE05_UwtQl2xSUsuhrRxXpeymZNylyRX0J11_sffGKwlIpRKl1MnLC8YmvgMTM3B0=	2025-12-30 20:46:11.807034
4	+55119782848304	assistant	gAAAAABpVGRKnquz6HFotiTshnrj52A_feVhf51nPNuD2h8rXaN_wb8V3TzQKwF8CxT-slkZESmRTkB2NmhQkgOY8e0_TGYZ2_vozqV6dtzNYZbQK04ZLQSW33Xk3CELL04YbVTINRJP2nNiVwr0Pd5FYi8y6N001J8CTdGrEFOyLew9l9jARqH7zWH1iblxMZSuB_hCL0LbG93S58uuM0vpQpSj0HjaYQ==	2025-12-30 20:46:18.523031
5	+55119782848304	user	gAAAAABpVGS0Am_9g-zJa9UuL2TnzbhugdE36xBQrtrW5Qo7AHn_JLYGClDJf00NHPCSiLG0lbh2hUn4GmML5tsuNnmmnhq8JEvxLYOeXC5eRCE6DUl72wKVpWiVL5wFBFyY7nXqSQwbH1Oz429PivdlRELuFcInow==	2025-12-30 20:48:04.02239
6	+55119782848304	assistant	gAAAAABpVGS51Pe0Lh4znJrO4rw6mcKLPXjiKtYmg9xHLtNMumi2eVU_DtwKnkViTKmFj3_A8pBJeTo6rXD-Z3WdNp9JGJL7TEgTvNOvXos2VU3vIFJ4fhjH85_7xrKN6745-Dt1bo1GiSGrtNoB7rtPYdk2XNY_Q4UP_Fh8Xhw0SDUL9M-JZAMmhjkEmE2OGmIi9RkFBZ-4Vx7p9obi6MgmAFncifpbwfphcb5GsBuHFMZ6YrKF1rHFP9DmFo9-QYNRf-L1GshFKEiLXl2IxYEP-FncgyiKsPfmSOVEIm2i-LidCd0pYMGNolvym9PX6BoAq-x-9MLGwibluObDV1GmJ89DhxPnjNNqlqTeKGSQ-Ma4T9nghVDB4Um-Cuwm-7sXJLJHpXo9	2025-12-30 20:48:09.292006
7	+55119782848304	user	gAAAAABpVGVFygkqehhaSGLGnnbsN8IdtbUoih4EarDBVSpE6rjv5HSB9iX0ScIpyIHofXlOeaUbPB0LQKxw8MyRht_ihRYlvOpXtwK0x3m3Wzlw6aRG3fklanaYN_X26eSxD1-bzmET	2025-12-30 20:50:29.56282
8	+55119782848304	assistant	gAAAAABpVGVef1Qp4E8yFSCPRQfWxeHquITsirUy67OeBwfEjXv3zj61CcSq8lIjDfyzdK-23RbXyNzuNK_euPYQz4rhdBOV3MOd6_lk4JOPQ6y_XD0YKWhLUnDPuBFSNMeWkGQF1ZMvGfC2EHBv-0fXzF7teQlpOMo-mBTFnCN-f81yALMEJcr58-iXbQoPVS7_Me1zbH8bw__AXswmxm9246SM9p92LQ==	2025-12-30 20:50:54.382663
9	+55119782848304	user	gAAAAABpVUra6RfEVErTrbzAdhGptBFoxe2D02GU80OsRunSVBvnwLiCEE4PkQgxLHpz6XwfFuITNXdcDDT7m2VwZlEQhCn-8w==	2025-12-31 13:10:02.203862
10	+55119782848304	user	gAAAAABpVUsh7DDjRGZDR0vNkVvt2M8-5Olan79Nyj1dtsfLrjIGHfLTnXaU_hxJr3cXnYCxvRKvfUOnObTrwHHinb75GZRa1A==	2025-12-31 13:11:13.531244
11	+55119782848304	user	gAAAAABpVUunqYLyUuYGUJ4Q8jiaWWxxITzkkczcTsTCA_J-KUOJnvmit2ksutSk-lIRxXF50r5QsXX4HhpnkbmTmI3RinDc9A==	2025-12-31 13:13:27.184633
12	+55119782848304	assistant	gAAAAABpVUvRQwiXnnx-b532VzHzWQr5fPlH7ooa3pF67jdlIohmz4RohnF5AOSPpIwxLW_vKfUiRbnARtdXUAarXEFjkXqRXPjB_G-1RvQFgtPWDnBRZy7Dj0XWtSjkbmS0osJM9Rkek7YRFIHs97aSYNCXqA8jkCF3Z1iacWmQnhFB2XYovZc=	2025-12-31 13:14:09.655971
13	+55119782848304	user	gAAAAABpVU9GbsNb53zdYUFlYP9EBdENNyWOtE39b-n1mPOGFJxNSI3qcSkq56IRb4CVg_y1XvJ22XnU4KF6w2loT_3wOK_mIrUsYH-fWydpPp0umn0tqxemqrESLhKneYGgfNQh3U3FnAFWW3Ce3YiGcmp088Q-jPuVoGQuEh0WJ0fCL6EIwHt2SiSmszNmxeOB4oIQrsZy_9_0vpYvjAusq9lVSr-cwgr603b0EKQoLRvKOAFsBLC2X2tum4SXksKSXJFKjLM0iappP7N1qCfAMM-nE95PwA==	2025-12-31 13:28:54.634437
14	+55119782848304	assistant	gAAAAABpVU9M9SbodoGDaP49CTAj_4svgvzg-lT-ornl-9cfn4PaqjSTFtH8WoVAXUqJAj71XMGVqRM7FmNRo4bKEfRzQm-YT-Nfq5TP8K59EpRN0iJnOycRyB2Mw031WmNjyxJBCRnjCthTCIhYohGp-PCPbbjr9eMkiODIfVVM6KsJlkGqc0iS58jc8RYSDWEFlW8b89q3WmbSsSiuuEsy6jCrX71XG4YTbO43lbaIjaK_ZDSvhSncJCJmyv2mxdYlhv8tdC8d	2025-12-31 13:29:00.233597
15	+55119782848304	user	gAAAAABpVVHD8pL1XQrZt_zEz3IOmOjtqQ7jaXSGPpPE_bHBWI6xmznCqgA2MbD1mWd8mhbqbFs4t5pcDGowsZX1UGV1Va2EiZtoL91kmK5IzvSc0Qf3aivUS6da25cYuYRKTCkE7j_X0uvCIBEB4entImeKmrkiAvNrIKsNz94AEUqctCtK8l_CWRtsZFwADAI6VMXpGkXozQ0YubGqg2-kDOV-izICgoiGNYFF7cG92tg43fGYvlc=	2025-12-31 13:39:31.298989
16	+55119782848304	assistant	gAAAAABpVVHIvialQpeLfxl5e3lkr7qnGRtcozVfxR76fw_oEpcAC61iAVJWEwq_9fLprWGUK-_103sRHvY_hP0hpkgKfySG-4T7HRoVTbcklrUSxtZ4q9nVcscDALynE60Aed9upxmlio_EhZLC74j_JAw8aVzDFPtX2y_O5VO7RcR_Bn126Ne1-rxrm0eLkGDc58WmvqLLMmEfMT7tV1cRdWk0GS5p5Z9o5seq4TMm6sq_8uH--VJTDcEFwd_8SXJ9JuO7VyWDUYnQyGitWpZ9q2dbWNkDO4Vscct0JRWMcWlAJORtcHwGVSJv5Sz-SIk_MtN9UFAV	2025-12-31 13:39:36.227362
17	+55119782848304	user	gAAAAABpVVHatXUxHA0osORi-VdMzETzTIwKBjZNmyBf3JHAXbJafiMNOnBOoKW64QAHJbl1yjEEeNBkOQYtc28icJpvFO4SPfP3ADFMr8ZPJx2HC3JGM2OFzbSk70B0D6_G4Y8WX1p2Cl8D7baPuI0vjz0m7-IMgPCtTOMTaqVWc9xxslzjs98gUwIHnMkDVVLysjEEDs7lSV4OJz_4BPr59rcd0YgOPCnh2u7JNx7-QVsKCF9HP6Y=	2025-12-31 13:39:54.048555
18	+55119782848304	user	gAAAAABpVVIJp54wXOZy_8AlO4zw7SBUd0lpsAtiNfOSC-nNbNG4oRBbcIBR1ahOdAqYtT8cDK54zi96uvF_asCe4XvGe1q7j4Q9xTd8aJNTinmqrQhHhXCGhPQW3kqGyondbVxr5GFGwHjLHCWhkikO1Yvu6hokTyThhZYyGTAG74QS3oA6Kz0pSotgu7xF4a68c_mOgNk-yboPgoZ8ZfMfSwojzM7GSw==	2025-12-31 13:40:41.766318
19	+55119782848304	user	gAAAAABpVVI0Du35u2m_PSw3RiVeiBNMX7x6zKUCqmkOjHDXHQJeU5fvyusiRNRC8ZXTR6rmvFTTeeCvPmgoaU2ELPqNmCItd54O1wQvOFP-OB0J1VJIcW9lHwJaFArGphshO_yNYNqbML29GwO8GwgxMb2gFtaMBp-E-IW8WaYaHw1ztio4hYvwOmgE4vmv87DCPAMHsbMvCkQY2_x7F8amb9YLWdivzg==	2025-12-31 13:41:24.47029
20	+55119782848304	user	gAAAAABpVVNHLq2jPEmVEh1bMJ3p9muOcyYrEHYGuBFY3P6r6ibfSLSsaGCVhG4OU8yNCjcBL9QBRT45ZbUmA-OnZG9lu_89Av13pchXrsG8wnAr6vqSZ-IPNQGDlD8_kOZ3haRGuh3-ODJZwcEtBI9ihG24E7q0MjjR1QqDbZE1qE0cFAr2HljNJBMwcICABhqMeA8wRfosLo8DunNrbZOpsk6h6uvZuA==	2025-12-31 13:45:59.280031
21	+55119782848304	user	gAAAAABpVVSOVErmrBqzC4sHy8GDeGwPnXZZH8wNCXgjunUDr8qFecMD6VwlF2HaLHxss4wSdCnjsBvMVOLVhXCYCSr9olT-Iw0aMEKoB83sc2t0b-d1VCRDi2XnIQrqdNSF3Pl6hKOEP2r42YkhiETb9wkytAqeULx-O-cRYHKUiQlyO6CKj3RikL037TOOYVZqPLYPgkZ2vCZuQrsMCgiSAXyCAvVhGw==	2025-12-31 13:51:26.726868
22	+55119782848304	assistant	gAAAAABpVVSbEHn04ydXLldp-GbDVMEyISW8wCES2u-L05Ecyxogxrv7TJ7e7CX3ym2FatTPmR_0xon2eatQ-KIxK5JceDfevYjSd8OdASXjYe3D5n34N3RoVKP4o2zMFNbsEMrCmGSH4aHvQw5UeFl-tC_-L8LXbCuKdmHuIl0mEaFlhE_Zi091ngcuV1HL5jENPQ_ldYb3PUBAdM8IfoAu-QYxmFRj9CGPMifwORmD2Ux7ggbDkpYiFcSk6Pj-AwONL2RXYkxGMF_JCRAHIfO9YY8871TV_KpaHG6r0bJDXHPcwfwAPyejxkZOISWCT-XYS_7fJYKPIrG0nZ4lqeSPILTAzCkuSw==	2025-12-31 13:51:39.721907
23	+55119782848304	user	gAAAAABpVVVXjSC2RNcQ9A9atzk2sb6aDkP9GRqooG1i6tIYXPBlMNI3oVZjy5TAsz7fNEpjXf2b7Pjx4hlPAML7eXKNGDAMKbrbAPzte8gFt3-tBONG5gL_OooJCkRr3Ow-EAs08sYleQuFixGQbjD7rziT2Z_3b0VWXeP3-o3Ex79p1fh0rziA2IqOl-dkir53HQqGNYlNDzz3NJXC5-WIhB_PkjLeF3q2s6FfSWKha6_UGBmLc_7iXo6rA3A2LeaqxskLnD5M	2025-12-31 13:54:50.645169
24	+55119782848304	assistant	gAAAAABpVVVs2EMSN119QQPRjPW-pe1jArQ1Fk2l16zTUHPfJy0i5F3wEd8e9AHRdiq5YmHBYmq81jiyOaBu0UtacxHfLGWcn9U9GYuNvkFxhB1DtA_smg3fDqYrKPh7s1gjDACAH0QvRYPF7KGN_z1tdRRrBjlaeZYSqskthdq6O5Az195I--DkKrPAYoe3N8F0Y8wE730kB6UGXzW99OvCSWRRO3x2-cJW8c-nchCy_wjoKbZvoDKOKVNT_b9Pi8mBILIIWs45sd7jlzGcZRXtudpqKTDSYk8BWGjIQjGf3yhN2fVtfOYi_Kk6X1Mf3kJ7jeV_3ba1DFUKmpazuxvTOxhFMfg2tg==	2025-12-31 13:55:08.457292
25	+55119782848304	user	gAAAAABpVWDmKQSidwHPqxRT6GapBXBNyZmc2SAccIYvjVtCzZijcm2jRgxUxh8ppRbiu-ITnDKSVqJ5_Fz5pMHFRizojt_CeV6uoJOXpI_8jJiE2IN-jcm-V_r6Ej1qlmqKE7O59k3MLEzKOdAn5aE3zFmXbVw_VMTsFYJzxDKD-bjKAoS0v1tqxbSINzC5ZMqD_SZiL6Mvbpz6jmPveYxDrJOd-KFogR6JqlL_7N0NYs1IcSMbZoq0Rm4tvuMka1kXVUmrcuap	2025-12-31 14:44:06.024908
26	+55119782848304	user	gAAAAABpVWIdKsYSWmdeP35B_HP7cwX_X88gh4p58xbqGgv46KvIGLvcKtaPJAnSjw1t8S6B6ZQNgo-5g0xPiKHcv-YM_jOciessS5hy9BaYdsv_-lVu9I-6XPw9ejJzzVZPgvE0_Vjo49_f3xZ6F-C35epUV9mhUkb7NXHZkHphy9vly3guq7khfuK8aBzN9C2GTaQjFvD9Mptqs11r0V_-TUA7pe1ILDIoyVwN-kShGm-wxsibSJ7r75OB_23k7bPKD0JKM2PN	2025-12-31 14:49:17.427299
27	+55119782848304	user	gAAAAABpVWP-PnaW4vHenZ-wHsnUvv-Xd2eIhtP-P8GRCO2Eb2GPJ7FCHNT5OcnHyn904-SmommPu0T7WjllkNjdpPLzmyR5lPndW8_b-ZQFhSnnEN1emd70GlU0F8sZT1iSPFr1OTQXwa7UmGiC4kEjyfDwj6zHBsvAuPfED-RtlLCpaR59D8Tib7lpaEyZp6UUnDs3t4igJLPVEBWN0vg18aDPVrdL0iJmCjsT2ry02tIeP_bNSx6H4yx2F3IIzcLGapd0bZgt	2025-12-31 14:57:18.524017
28	+55119782848304	assistant	gAAAAABpVWQERMHVs7gLBUVIapHLpJebmwCtLcxM7TgPWwzY0JK1S9-eh3nuN4wgOoXjtY_yc0VPcEwHNgB16cC-CL2-05_QF9LwNA4qpPusIdGeObNFjF-SuqJFoWm4oE2zuDOyElPF-uCkQDjvHfToQRM70fuS-dzkTIK6q4K9FhyCJG6YyW2PrEM_lZ6ay48iGDJAkR5FhkISHEIZGwzuGG7YuxS9JAt763AnaJClHOmZ0uwfIQUMkPYNehpsWET2I_xWVFK8sq77kZE6lCRDbR_Q6069CpS1Vo9K9zSZQ0TYTt5TrGvJ5qSoMnoAFMM7gDqBTu2zmtWFZGUh2V5oXdvyVBZCfoBNz3YkL4vtoOJ83gcicO_EL_LjysjrNROnb8qBj7U4Qi1GgFXGLzp1OgekF3Ea2crbE1Y6zZHyIJSugD1Bqg-_pfr-SWoU5muRQHoM1wHriotD6J5_i4tZxPKcoI9nvD-claclTxd-gu4MAt3KZoaKC46b5tYokXZa7W7bUFIoFmuKrilkzaW_vnqNOXIu9XoF7PN63_c6Y5DAqZtxwiOZwGRfsar2t5heQMHcbfbh5y5aAKV3xYKy8BZEepsRFF9rkSLqPQ5kZoS4aZzXeuUYmUZUe9n8wDnz8I8FpoDDGdnI8kL6vHDCr3-QCQV55A==	2025-12-31 14:57:24.583297
29	+55119782848304	user	gAAAAABpVWQp38tNDoW7o2bUWDJENspfgk2I7sBF2GMEk8M4mf7i2P5-CKi0aNZtH7fBs6x5RwKLz9olrGK41rRvCr_i5HkN8zioYfnUBv5yIRLbXS_M049O7nhRSopucuWsQpieZkRN	2025-12-31 14:58:01.550824
30	+55119782848304	assistant	gAAAAABpVWQsJdUyhEhk5FXZOMqwOQPMBLXdLYCnA_BkQhBPJ2HeIYoVYUEJZ-Eox1_RYr0GhhyZFKufQJ9JeVEgKRyncqiliaOIKg8AUrRNNiADR2LH7I3ZqJ1UMGIAJhW8Ne5bGbA2nVxRGr9vx2iM2vg1R5L97Wg4RGZmml4UnAqbFNWMhW-x14feudLBSXSByGwsKaT-K-iOmCDnYVbfLVzLWRbT8knK2rHBJdKhIsDO5UWZOZZ73ofe5E50L0gHQSP1Z0REjPbsMZEpm_yWp3P4CX-OWdoARp_VPdyznfLJDUo1ufiYSXLnzRxbvcCqD-4lwwR2wqpuge5FP9Azq1sQBCt6I7NDEGv7dAcIV4sbLCaqMB8R0acA4lLw74q6hdKHAjH0ZheCkXUV_Nat_ckULKmS298flrwgDWKf4RNAg_5CRNNKZjkhxgw_0mgFVbaHTH69zUdFKLKTSag9K4f5lG7rmmrs_EHUxi6f0fnCReW9RNE=	2025-12-31 14:58:04.218501
31	+55119782848304	user	gAAAAABpWt7j2dM3welmeHy02UH0PSQqLtKnekka04QFMhPlu160qHGgKzflYP828BUsI30NFTdiUyLtQ-Mth2SbOYeh90M7AxJUGKpuqbmnGb4hWxZFNPhVPWT2sAsh6WRCZ1jXfsMSLQlMQcGSK6u3Pdx5O2E_vQ==	2026-01-04 18:42:59.444564
32	+55119782848304	assistant	gAAAAABpWt7wnV3FZNKZToaNAn2xExCWp1UUJm2E9lFoUrGUv3kHG4Qwe6rQzUf0EClXr0ezpHD20hSjJj0uqYX9MDlMHtogo-ZB6mlMP_ilmMgGrlK5WJ-gww0caK1KcDdDc-YMelQ5Yio3f1yhfpHrVOmDOnYQCDf0niXR2RRBDPh-HAmtPsd7pSU0THVGXui5T9C-Yl72KC1g23blfiQ8OR-Z3m33oAhFDP5bROyPvKL1WIRF11ZzpX64F7Ainx40Jp8JSzYyYHZs2K9NO34MsihwTLGEZe8s8oewyBSgeIijx0aT9oV1z9Anclt6sGY8QmlKMXaS	2026-01-04 18:43:12.422355
33	+55119782848304	user	gAAAAABpWt8wsenSBawXIAcYg-9YVpl8706tqgmaE4MdxxE4vNY7NOmd_2wNfHbPKjl9FgswNIFs3x4728Yn2GpPzADfXeJynGPh0dfQbf-7nfXR7CRgNT-OeU0Ggu8tV8WUiWDo4y8hN8ABGeZzFb14PDU_N8amvP-Ro6ekg5iLC2PJSrEWh47ACF9K0d61plQSTOZ_rn4es8K1ViWKMnQIqdJPupySFA==	2026-01-04 18:44:16.811538
34	+55119782848304	user	gAAAAABpWuLz7Yq9KGRqGd5VR3sc5isw8S6_qYI8_qTFylUBkXTXuB0QdRf1BMuW6y2_Zln8rzFMfDrN5XZPFqo5kS84njVJZrw9TMG0J3IRwyUpeWuNxMjQRXFgwn_9HQFIQfkTIg0kxy2bexstXLO8N40m20pyZUS6Yqk5a3Q26pdaSX1AwI3Hs57bGkj5CorJFD4awgBN-ihsfJWFW1NtL9ujE702aQ==	2026-01-04 19:00:19.766021
35	+55119782848304	user	gAAAAABpWuORP1GFbpIEACEfvqbXxeofxxBXwiLK0SsU5vRXf4Lah2ohCzs3hobzHwaUbaSsOnOB4juCkYDPIh8CzFooKvc58Y6B-LA73upiUySdwHG5aJbMWpo8HSVvRQWzPRuuYyHtsS4sXX7xvUnY6vhFpft6Q6WLx1kMCwBXKOiJZKllswdNxdC11kwEAqlXOE0Kw9ym5_Dt_tfQbrvLiSQSEMK0r50LR4p5ZsuIDvqMpM_0KcY=	2026-01-04 19:02:57.637823
36	+55119782848304	assistant	gAAAAABpWuPHqAuFgdbRtUyN1YlFMhknxmqLdTTGNTv2FUddxVGDVfvAh5e-dTvEuM7-1bKywYGOZ5T4LswM2ew-GLnWsDaCaCXcQoNSQdwnuJtGGmYXLsaHA2oeE_ZpF6W5OrNFcWS-sQfcVQrPxTVqvqsdo8lt-zv8PEwbjShAsASA2iws3LZOhuDTVB8oxsb1rt9H6PVM2oGO8SglMnXc5iDqvXKLH3bHzOb2QwrsLOqhaRlTetQ=	2026-01-04 19:03:51.059034
37	+55119782848304	user	gAAAAABpWuP0QWTvnsfgSPa0jhCOLng3HHF27ibI_W1UqgnlzzUgw91y6zwEtCNR4WOnVv2pZpdtsIeQM1QsoxkknDOHOhB7bqzdIr8tO2lZBSzEJRkE756VWLIOudoeEMqQOonAtShntDVlCt7tJcaaibHLwTRpRqXqfhq2doLDgMJ-k_1HhEWelqqUclLDmkVkp_yFHOQFfRV6286nPbs2B-eItplX4S7HtTv7_HuYj4pBdkYaAEw=	2026-01-04 19:04:36.948638
38	+55119782848304	user	gAAAAABpWuSeA2QclXBcvfFSA792VSNNuKKFDqeyU-8ryBoRbozhc7pD4UWO4SBwDvQF52Gq3l-QbkxhOdyjbLWgWhVAHanYrts4VPDVNqU7YRnXxohq4jmUNP14k5IMod45rHAalF8zh4oICCkJyuHszLuJJOeQXkiPGKj124qZRST7OpKtpAZyvrkfNRvAISbvuYQPUfBb56jnRdDprPzdAWpX-ZGxWLzMt_veTAjgyQDh7MM_HSk=	2026-01-04 19:07:26.995122
39	+55119782848304	user	gAAAAABpWuZ4146wxhwuW-lIi0HkAbiwZhXcoVTQhNRbPKcikEhqgBkcvtilBZ8olM1DfV7PfwruVqXKjICRFgj0Ply_HvyTK9tLGIr9_2blrA3_ubwTvBnOveIDGZ6ELf95zoQB3vq7PXV7256cjO-geYMSX1RkiQDoFPhjg1T6f-Q-0GezsKjOYw43Wq0RAv9EMv26TC5faIxuJx9JHtctVqpvWD5-Hf45iH_5DwixUxmVa74gObMfzHbxe7YA9-84SFU_KI_o4KP8nKEo3Ogq1zPUf2oHMbi90a9LrO5gIdicl-6fbx4hIK2GOfDiv3MNTEzHWohNXOBZhZh22pl9bBWwJG9CcxuD3oGOwdBHAjzcIdYnVmU=	2026-01-04 19:15:20.9905
40	+55119782848304	user	gAAAAABpWugFGS4U1jliJn7_zPj-_45y16hZr2mS_hXmhCyTlFrg8FhJ_pCewyKZktkYFl9Gih1AnKrfwdDsA6y2kuX4MDlkghGg30ZjP-EPhr0yHO8FmxuxHGpXxXvcwicFs6urU9Nb69FwdBN2ZMXrOkHoGPa6AtRGu1AujBfHr7imldA-0ZJdxDke0kThXSXOBSvoIpMTxkdpAUqU5nh5ANwrmcj2oTRLzpofW4RSf86jtK2xpKp4E1mN57jLUwwgXtSg3nJe0yDGZZ63kIukbbeGncaBq65XUxwtLdHh7iNO0mgd6XPPmaJ5yHprehzSYWEDxgQgi5QcBLSnwakpZjRV5PIiyqJr5QHO2d-C4yaKIF1hW5pdX0oZFI-9uXe_k1X4C-fYMSssPlS0Ack_dH-j2rJtDg==	2026-01-04 19:21:57.443616
41	+55119782848304	user	gAAAAABpWuirjT8Li85mEw1sR9wtZ83FdyuHbTsNUupjMtG8xlJ_5WcvHOf-ByMyGKWr3mbxwyvXaeFKL7MXDR2K8EifCz7QIYA2yxVaYg7Q1LsJ8noAm0Sedy0EAgKT__VXgDUYT37lrc1UNoCahrh-Uz8ezsoPbw90LiGOWd9xDvEkAbPNs0yPdRp1WzJLwASzi0mmHVT7KC-18ngeVV3PG3wB60h7thsVA7YIcOnlt9jeNoomM4_x-bQ_-BbA_K3lXZRiE8SwJtdLi1QIcUEFrkQM88-UXg==	2026-01-04 19:24:43.33663
42	+55119782848304	user	gAAAAABpWumADEt9C6P3Z-BnSWtg6630JbrBc4xb4snvqKcW7UZipTDhduPottFYoiRn5u79jhnn8gCFsX997yFTeBQXB6DHe9i79nS_wcDWQ21WMfWYJwIARYc1u6LkXdsTxXaZs1rv8xHWtjE1zbBXjgKeH-XoywldeGj0ysqgfSJdtRDIyOmX_rJxcNSxkxYlZUxPwbXphwKMwQ0Nk6cF9uBW84YS3jeTGNc1vMBJRlovZ4PEIEPOAST_c0wI2R9xSXb3oQFJWMc1GtTQPPrahoOgjlx0Mg==	2026-01-04 19:28:16.149613
43	+55119782848304	assistant	gAAAAABpWumXD2PdsynbrR2ZqUJFg_LLJt__NTvDwVBohuJIZgQQUe48P7fGdlB9vZY7f40nM_5Xpil7IAgQFzV3QMJqPnSq8BpG-SOt87OJCFsBiTa6_EFBtRnLzjGsXeW-r0meBhDCys8RI2Gy2arsVS7dF7vZ72NFLyPGnEy0yuhb9i0P2LN6qepU1LzIkLma6SjUeNQa6hxFakxQWgycfY2ZqhOf978y4jp2WzpdFd8GLKyAhS8=	2026-01-04 19:28:39.558681
44	+55119782848304	user	gAAAAABpWumrGRvKdFkWylAEmiAk72h1VbdhqgnbKNw-eUiXuQdoibuBkhIzzBF_k871U9mDbvnBY21oJSaE9DsRG536Oe4FT9ECZJB_eAovkAjNmSuk115hky35qjmDHikriGM9mP-yJM-x1c_b5Kp-XMG85wSiiw==	2026-01-04 19:28:59.132903
45	+55119782848304	assistant	gAAAAABpWum9xMlBLPpL8Y3YNdkc02y06IdpPSBBTLSbuIs3q8DXjtOHc4oBIEaCFmBsr6OwYOKE1sd-9aJUUlx8Px5p1w7UMYh7uUJYcerH2GJ-qeQpzhnsP7WsTb-0oznz_qG7U03ATu5KlVHelv2LAVNF97P5jwdu2EXqPjqu7Jol3y09elrDXx4Ujl7owOEndfqnE8tImfcjW61vSC9eyNLo4JDMRvXDBhpQN0-Y6aVFc5Vr7QyL_X4Bo-t4OPI0b2lC71cTkXXGPN0spL9yadCxxkSSIlFwCKgBQG7ekaenIu5U1500CCUAeUWKBQyOIqqHX9Q3Ba5d81FpS7zeAbE-Xs4u6_wYIJoCJV7kJ9TUSUj2iMyzVfqFALwdP67mbj2OZNKMuKKuyeb9KChMP9BixyNzag==	2026-01-04 19:29:17.638712
46	+55119782848304	user	gAAAAABpWunkl5kXJTnT_-EeARIlvnE11-KzmCRwNn7dpM9VcC1-1yAhDfi8HSBs1rSto4GZQwkmv6DXExAz6zbuXwqdU0DGYtWggxQxoYZSgeu2FqkdEjg7SLa-SpENGywE1xVz4eep	2026-01-04 19:29:56.127433
47	+55119782848304	assistant	gAAAAABpWun_r63jO5u8ItuXcJrpMvIam924EJtHGFOalqh3oEWP_7AVFHE6h1itJIa5_fTwbFR09DAqi99O400s4aITQNFnOPXMMjSDNQxf6Igzo5dRpQdMteGq8Hp1KFj15Wk2Fbuwfv5zKsQUQ7iMpyJdS0mFP6naqMl1JXERsSVJc7rE-lCZTz4LvNWhEZBS6vLRBUTBIsIgVCh4sI0iF_W13jynRwbah9g285BVqekVxe_XRH6gFO91tt2U02HwUFcF83xm-KgbIveSTnHP1E8Wd629NhkeGLpLvYOxvF1xMxikLS8=	2026-01-04 19:30:23.159889
48	+55119782848304	user	gAAAAABpWupJMQM1s5rrE0HwgD4uURQUNmiJ4ZryAzsVnTCoMo9vjalf0CW21g2xmdvK586ZdfsdaatQ_UwlXwJe6XtEc6GFMiw5riDqFi_IPtQoboEZqR1Px78g-y2uqfuCrme1IM_XNrzp8HLrCP56_wQ3I-KQgA==	2026-01-04 19:31:37.917475
49	+55119782848304	assistant	gAAAAABpWupQwuc3tqFWMzih8QdJ0uB0dhoSMCDMyWzuKV_qQMzzVO_ZQ9mm8brVaKklsvmm6ga0Uc9oCrDbD7Iz5FPa7UE2JgdDHIR212sSfSZTS2nAnIG-6xE5DuMPFd9nBROIL6l4RMsGiA0Eh3-tqhkNltHSUh42O4l_MDUjqMnU7QQXL2LkJQF31xkvme8Q0mWSfZxFdlxQGq3XLhSW0Th_dU-FrQ==	2026-01-04 19:31:44.29553
50	+55119782848304	user	gAAAAABpWupybWVkEKs2NbHVN6oapWdKbngWB3bhg5y47erX3rerkfbbG-FhOkxjblmbdMGTxUjVrZdjdWtBVLll9NNtnq0JS9y6dVFWbeKzQVNFo6F-LSAFKF17KCJDhLTUyF-wepfjOyPKOThPEA_2rOBV1E2gVA==	2026-01-04 19:32:18.917641
51	+55119782848304	assistant	gAAAAABpWup4gnxnHDLn-BAFpTqxXGshLG5KppoVQpo8LHGgdGyOgTGCcoI1sTlJFCAZTBicUCDr0ISq6NBW14HPOQJc1RmYxgWHRxOBSgq61ppWQhIU8pGmewZa1UNqBk7pPgpx8VPCyouDeiiuABKAYTrcA5a84f-AB5K1ON2SBjeQ0i_vWJnRw3G8kJisLAAj2U4tyl4W	2026-01-04 19:32:24.594203
52	whatsapp:+5511972848304	user	gAAAAABpWuuYGkXShNEyfhPdVFlsDY5uQ8w4EHr1aRGyWZFXxIyvV5D0mNgDX2FIo2jxkk9bEai0WrnfKZTa37h840viKV96Bg==	2026-01-04 19:37:12.37842
53	whatsapp:+5511972848304	assistant	gAAAAABpWuuaKD_kVIQk7Ggw-XbwVdJpmaaI_MNB0U5owuoaUC-DqutFtB5qXzrmfoxlcs3FdGt8xV3-1R2BTN4n0QU41mTwVDJBES_BXszTikGVcwUiscobmcWHNz9Qqx55qwPQj-7FVZ1jlLZhf9tTbSMO_1osqA==	2026-01-04 19:37:14.158464
54	whatsapp:+5511972848304	user	gAAAAABpWuww3uUaKlc9KrQ_z7b2ddj_AOwTJn6KjF-RoVNmcLavts9hDmcLoFG37iAA-rpuCTWBiZrFi5nvXCqF-GOq0tzN4A==	2026-01-04 19:39:44.189933
55	whatsapp:+5511972848304	user	gAAAAABpWuzqEOiFJNDjNWxDx7lqHd4GD75MN2vP_EKMtFzhwu1BNAKzMnV-gl-3sdSJXoKnQ9lXaP9V5XtGbuGUf4hMUPDjKg==	2026-01-04 19:42:50.190216
56	whatsapp:+5511972848304	assistant	gAAAAABpWuzsiVlFfxyHisjMookIoAIm2ZrYeOinJSCQGyLtuy2VuhHowmYBVB--8IcBOSIYroM-H0UsmtenybvTDI0NeIMDdSehYZbaVAjG1F8RgaMwbe1oe2I3BCj3ma_O4bM6OxeuBthF3dJld9_Eq-1UCrzBTusEAP-zO_69et2k2emWszGL77gmSUlqCC2IRlWtkqW9	2026-01-04 19:42:52.20007
57	whatsapp:+5511972848304	user	gAAAAABpWu3WVjNYqHJKuh1kQkcSC3MzkGNKQntWqgmzvtMo7P9R2IiTXNaO7WEepNf18l6JduymICUvi3uVhKzDp34em9Fhiw==	2026-01-04 19:46:46.559773
58	whatsapp:+5511972848304	user	gAAAAABpWvAai5ZAHR3_ykanR3ckSBLhiwoR93qcQ-4E3mGCBdfOXivVb-Wv5Kt0rMoxZm0mReu118Q1v2kgidvgBPJUDkgNDg==	2026-01-04 19:56:26.00392
59	whatsapp:+5511972848304	user	gAAAAABpankcoOrNEloe2VAo_PK_RxE2KKE09LsOcpXB8ORGGxJcBeI0wM1yn-yCIjsGolMkh57AsODPMKUdPjtd6Aa-Ch5QYw==	2026-01-16 14:45:00.819281
60	whatsapp:+5511972848304	assistant	gAAAAABpankgL0iXsVnZpK1drEI8uDPmfishv9UgpQ02iAO3AwtF3XfD0PZR5-ikNkKUh9BiZsrgrMN1BO5KzL4AhA-wSB65KDeadxK3tQ3OxLVJ07esQ7E1BOLPPpHz90shVt5xxfZTCTVj57GD_URLv740yGLaOQ==	2026-01-16 14:45:04.454789
61	whatsapp:+5511972848304	user	gAAAAABpank0Z-SeN29D23WSClN8whsaZUQVnlEjs-AXO2D0bH1wNRWmo-wzjV1dy7pjijm2Z6ERMQjXXahd1AkEXxGuyWvr20SrPNBDWOXZ4G88AC8k9PxC6_WQnQqJAt9wNWkTES9udkLCwH7TT2i6vkns1EK30naiERYGkZbnxo5eEkh9sIQ=	2026-01-16 14:45:24.341209
62	whatsapp:+5511972848304	assistant	gAAAAABpank__Qr2adV7eVp44ln2GHDckivC2i5fmL3jjNgWENTvzrXUj9E3sgfXZHxI1vf2sFHfBX_N5-JdXpr6DMtWqXez40CD7tw3LyLvFEK7aknJYUyeHVd4VeGq22zMegUFS5PWhQF9wa1VVVEC74Y_v9jypgB7vEXGXSAroaisZpnBrgpO1qWkF2xzkv_qZRQQtb3jdDo07-HDZEQ2IbpRrQXGbcUdO9Ye2WHhS-LtbnaTGC3HbYz6WlyA-Sx83Hd26aNZmwsiC2ENfpJFPUmaXLjhg-zWYiLJNnqS2-EEJScxTz-QioiC8Kn-dtkOV5IC8iXC	2026-01-16 14:45:35.014733
63	whatsapp:+5511972848304	user	gAAAAABpanln34DjV1bKui1HjJWFr2YB_jA4s-M6LvYoY3iGWFisMoXfYAU6BqH4wpGGUgMyJBQNCpr1h5Euqr8VXMclNNb4aAHoanx4Y90UDv_Rn4zYwCUiaPyBposYsklOchMLH1BbDjhcffctMu_Lb5zKhues0g==	2026-01-16 14:46:15.332541
64	whatsapp:+5511972848304	assistant	gAAAAABpanltIks22wBaluln1jvytBarIrtW7zQDY_Rq8VoUphCV9y0DYTOyZftKPo_M3VGKJVbzXZW48H9H-nXCBCgtjA5iwSnQ5jA4UvWwvEOenAJXCeLXCbecntLwN7DxZU5QlYx1UTiqj8xRvYp1GLHM9YMW1Xa_cZPt9CkjW3GK1IUieFcJS5SzGbcUUiLNwuhXv5iraYEpJeaGl_q7YmVO8evO679Ko-tPzVtyJFvK1OKHc-1FDRh8-zfaEIqCph1mmtw0MOu5pV9ssGKc0XYhz4xwBZ4v3saNu4b8E_f08fL2akr83_erVcghJgbt9Z-Qj1LqJeb9mGUO_yovdv4EbUuinsitrI5fIxdDgUlV_i8qxv9eporw2HgvwRd-P3v1NQRiBgx5cmX9j4UB6u4kWSP_yHDC5Sxx3fEhL1LzdYMuOPLRqw-NHhbcHHsge_gVtJWrv299wrnsplZ0ZBzuYE82k0Em0jWvp_8NxG9-Ce5BGLU=	2026-01-16 14:46:21.266482
65	whatsapp:+5511972848304	user	gAAAAABpanmd0LqQBwUPiXOHuNg7Y3d6Y7qOS7QLfd1-gdD04bzl15NMMx3XyZ638ObZF075xh-PdPXy09kEZJx9029DGSqdGWF9eDman-P6dlvZ8yqmAD7waKhPqm3K--gBDNN_sOv_nKPmJri__VpWHghSHG672IWS0R0pA0uhBcx3o9LhoAuKA8-fC4td3_T27AO9A0gq4EHfEOD3fs3XW_x6x23tBg==	2026-01-16 14:47:09.912762
66	whatsapp:+5511972848304	user	gAAAAABpannNqIYekm-otcJWcyOFItcdbfBiQ-k3fAr-Ei2YRv-m8tnHBTU8iNDU-jmv8FAY6fJ2Z4RlQXx_AQFfFp2fUvosYrHQbXM3tdq5TLGsyNxhvEEG8ayeaqVtOtXbjWdSF-aWlMXkEYelJibzu94NptobcQ==	2026-01-16 14:47:57.267779
67	whatsapp:+5511972848304	assistant	gAAAAABpannd0B1Wr-NdgfbVDWRcYd_pyiIwl7ZWTlwcRSjXJTezbcBE15w5dcQb08RSBS_8imQtJSz5xrkmm87WOyrjSVOsnz5FfOVPR1ysZFVaVaGtqnKo9bL_0pZllfFht35_B4yiopG6fldYH0TFL-wG13c12kkyr8N3ot6qeTFPamv2wwzhm_ZyTISvvpz2ckBBDyrCcbSM8d5MmzTRhcBYo-89xj-sBrYOAKQ872NRDhWqXY_9xudTfOzM6hNj9zcxyYokD9-VtZe421RBpAVK9t-jthxkjDfNapcRpvZkdjibYcSAvySD8Mmf4YFxZrKOxU3a7LRNDNV_hw54r69a3d0G8afWMH5nEYmhsgrXqrbgKTY3Tey5FnL5i1pQoCy-biGonSYG8TWhtj5z0ao04GEBP2x6QclA4l6jVUqGpm_-zvLF9XCGk7sO2tQqEWY6PMe0JTAK2kK6phfI5ax_GTR29jXbYIfbS26FEC1s7tsR5bUTXWepLhqcQHT3oTlF0-29AONv3XGxxVAObpNx3ip5xMXsI83UfkjyWKlOofv7Koo_W8C53h88cM4Qb9HMjgMUnzzRWcJAi4Evwfp5Zk1V8tbJOMA7Ct1P85iXM8sIUUcSkQxMdM_uJJu5fzQKGOPt7glezNbh3XPowNHLv0kOdw==	2026-01-16 14:48:13.100366
68	whatsapp:+5511972848304	user	gAAAAABpanpQ1auq7KzXQ1uHsUyJq4359twFnfU1xw6KYsrlMZW8O7G0HIHx3oOVleMzkNVWCT4dTeKX6KROS3LeIEjlqBgxIg72RJMUwr-d5IcFxAwR6hA=	2026-01-16 14:50:08.523639
69	whatsapp:+5511972848304	assistant	gAAAAABpanpUuaEqgrY_fbzB9jLeYVUKc18M9Io0HPbKsfyyfnzxeFk4omQJVcxC6azwtBI-Ys6X6UP5EC5IUMrPOyZ5fSs2F8FmyAXFYzgGEvrXLbgOsazu7dvEERteUm_Tx5eJAt--GZLOUdOfU10QiH2p-od4Q9BBSV679wCrDSHZVkqXsSWqyXNICcuEHVXtHqUIPhoYM8FChQqW9iVhxLRGlo1-I0knoxdGJCqgNwJQVwPZ1vG-enfs_0N4kcFwzafVhvwm5PQqvIX6xbO_fmuUauh9STh2IuzMzPYWzzjI9sPvD5OX-ERgvMTWAkkMC3MoSWmyOCwQ7o1znxBN3eCBezlzOkaXuq9XUrt7SsQi_IIlLXcNiiy5IbKTLyD7zrlM0gBiiE9kEpJ6yz-Hoxdtyuxgnp_m9rtCe7KGOT81oqtvUbt3OfepUjH1BT94mpAewH-kVBjy3Gv94veP_npQzR002ud52S5I_kv8X98Uj9qCbt5NtnNtuzFwABDfydN_wTtLLdzuHEb8tfLjZuFJr13-6A==	2026-01-16 14:50:12.75426
70	whatsapp:+5511972848304	user	gAAAAABpanreHVjfXDcPczIhDsOBuoPSKUVtMtCmYrTQ-VvJ1GHBXtZeHdPmUbTR-4uT77TnTnb4Ti0i9Jh-JsvUwGuoXamH0RqNwcTMIQ_ZRdQPsCxcSPVUhdb0by9WCGSqYkHZv9qA5Cg--OYuuYOqJ7L3fYOjxTyNiDJuorUCwWAaOeeeRC09PucNamIO07ZIswjkIfkx	2026-01-16 14:52:30.990109
71	whatsapp:+5511972848304	user	gAAAAABpbk0wWXr2hVQcs0x9GB2yROc1k_w32VGfPUHqM0ZAhs-AW46GM_By9IJy6fa5f0NEodjcfcg8KVmlOnL-F6SMjiFAB7Qj0YsjvsisnuESyJjOFM0=	2026-01-19 12:26:40.091072
72	whatsapp:+5511972848304	assistant	gAAAAABpbk0zj9il9zpii_kAes_Aqin41MRLVOgOtouan_HihFapQEwp_kQjguhjlGO9ESJnePgeLeQNm2CGaaq9K-uFPrnFzIopAcBHsXNoNMxhkEgYpIha_1cnX83sceWZNqfIfyt4j63WmMmrbsle9kvOuqLQPB0Bhg_-1Nnyt5eqZOxitr4D0V2v3h_f7RueUD5a6O1AE77B7KwTUxFC4lfskzNytgyGR7AE3LR5-GnsdLMt7Vo3xNTBz1Yh2hVahunpVizXBh5pDKntQSaSAVCGZsOwosg3ekMAe6uge7St7mE3BpGS8iN7N1KiSCLUlysZ4xg-SaqhnUZAQssPWeu12tRG6iQhtHKjQIsVfMzfEj_K-XyYITe_vgM3w3ldIHRLjY-g4c2wZUX3-oA-vnpnkTezhg==	2026-01-19 12:26:43.894842
73	whatsapp:+5511972848304	user	gAAAAABpbk1WiK8PN5a2kO1cWqu9B0HCwFPRhZdK82Z8JUH34glRy-zFfzhygS5lgQAMIqutlxWKhPhays0qkvPYxiGKjzIC4E0oi0Egdfg0l7tsBs8B6XoFcXWcpP7wjOdwNfjfKeK9	2026-01-19 12:27:18.988968
74	whatsapp:+5511972848304	assistant	gAAAAABpbk1gqP-zHTLXbhY9JUan7cGMiYNYtmZXXXx7JFI9KPpo5JF_-RVxl_9_uFCPLP_tcaSos3HcuzZSKZCf49CrxySaluRV_QPJGJ1F8gbOrK5m179KgPHMg3oIVaXQiqUe9brbxm96VTbzgPwsPGLMtabPobhguEjNJOvag2F-lXy35PonAnJb9PrkTtN1IfVws3x1wc-yWLhxWKYFrhQYqIkOfpbZde4us_5tvFbYT2mPbF-DLxCI2jSTVZJlOImySQXqeUggF5OH0qKY6HuEObC7OfJPG2wJlExTM7KNDm-AWQlFzeMh1BbAUjsTy2vC7FLs	2026-01-19 12:27:28.680774
75	whatsapp:+5511972848304	user	gAAAAABpbk8JXqk1qSLZYIcBu_2eI4M2MUgUePvh34KFsAx5VUBNi6TFam_M6NRYC2LzWtYXlgfLxEGPzVZxPerIv9z_qJoswA==	2026-01-19 12:34:33.502979
76	+55119782848304	user	gAAAAABpbk87kUA3kZkpRc_vRAK6PTrijK5gIy0T4b6y1u-aSnl6TFahY42dQ4UbA6iPOKltVAq_TWyEa52y5qjsLXxUx6uMGw==	2026-01-19 12:35:23.258237
77	+55119782848304	assistant	gAAAAABpbk9A8FXHK31llTEa25ZMfhUKkYaUnI69AVDalbfNyaEBColzdpyE3jWpe82klCQI1cDm-Gnmsb1yzLrs2PT_ndxeNPHAuBCBGucYpmwdzNBBqcCMr0c9WW3NO6V5QkGOxOu7SLQlJ9hOjuqpLBJFn9Tz2aCvCreWietdnCRvznT0QvvQ7iSjLmYHypkpXLzAV8E1pXQv9naA-orbTKPdprjfy8yz_Sp2F1Xc4nsoU0m3Sbz4DnSM9rOGWzIcsD8SOxuWN_WPWgBl7-0FYACLZ6ZsRL1iIog6ai9Z7hqmLcl2sGsIJQxe69dgauD3Lgm6rSogbUbCKEp17Hk7k_N7aUsfxf-gsm8IycU6GUGQLxw4M1vkDCAGjHoeZ8q_XolxLz2w	2026-01-19 12:35:28.000718
78	+55119782848304	user	gAAAAABpbk99TZFKNl8k8vpHcOi6FxQHFPz_sUP1e943tXm9A4aGiHJ1_NICitzBai1iQZhTZ57BbFk4PCYfd47w6O0GP5oa0aGIaxTHhu9vk1uhXFDIwvs=	2026-01-19 12:36:29.122622
79	+55119782848304	assistant	gAAAAABpbk-GHUQBm2T4ZC8O49vdEOVtoNAzjyEO_fUCgzyzeYJXSGscpUl_JKny5ZVvK4RaPQxNk5mRe18JkFG_-OejzUPrl9jMubOo0otv0-fClX8eEXmDUHGM-xs6o_5eyBePRZ9smAFo-O8AHqOiUbXzNRDEVDZY5tP2KJX_W7ygtbIeoLbgggIuDE0CSvpR31zLEJBCF9-mtgg2A1S4EZ-V10JRiOF82NxdMPDTxhJdUnnesBStHAighGAwqph__BJT6pkQ_d5zNrSHZyC3ztkRCCLWPKvtR0w3y9vx12kmzSBvYxw=	2026-01-19 12:36:38.195754
80	+55119782848304	user	gAAAAABpxuCHAeK37e096HkXfz-Ui1ujkmKLpgnrGNUmcFH-kXteXPtIGWgiKKlGYBY3VyHT-ZCaDenO06TTr0tDvjQS8x-6fQ==	2026-03-27 16:54:47.04544
81	+55119782848304	assistant	gAAAAABpxuCKckRxCtF3snUIhva0AH-pAPH5Q_mB07DT0KbK7D8pivp2gCJWC4etpQGqfJCT9eLqSHj6U868pgLemMe4pA6mQMWg9T3bt3msDCuDsviXwG7S_DcUihHW0rt7OW6kMLaBrvO5Pq8O6o7pF5aJ9rMwKw==	2026-03-27 16:54:50.302716
82	+55119782848304	user	gAAAAABpxuCn_uzs8dOMPaXLa5pokENCokziMa75wbT4VZN7ZyIZ3P4P6alGluT3u9qqefVtSCVCD5iHbfwAs6OAfgnjvONwjOn5irml02x4vf2QCX4_2MZqPrkxqMyED_4gChXdM28p	2026-03-27 16:55:19.620375
83	+55119782848304	assistant	gAAAAABpxubHGjso9N97oZ58KaOPfVgZLtGk9b2L6AQZ7jG984zSWls5cmSAnKH-XeNkgXHazPST0SafgZSqq0VOhmbyyqWNNI9ZqC0o6q8orHHLoytdG69KV3bU62o2bfDnuO9K3ZVd2m6d8n2nS-Ii4KYXr7wcEpjfLoTXqbYCHuvJTh0akkc7DdftgPOMwf04sX7CBHV5t9adb6MQHf_rq6uyOGoDQeID_o0ACEZtoH0GuLWes8MTzMCXN_EYuah5U290vHWE	2026-03-27 17:21:27.217481
84	+55119782848304	user	gAAAAABpxubcuuMAMj1G9k8H6ohzDk31FWzlZ-m5cKIihPl7lM0B98djCq0zHMotd0vDeaBV_pqRczso-6g5Avo0lejey1EiTK6s6y-V-qqF5ScFgV2wZalE8h3FXyS3iuD90AQVlam6	2026-03-27 17:21:48.87267
85	+55119782848304	user	gAAAAABpxuhOKEhn4AgQOkKErnIW_viJsBafxa2vZ7X4zSpCdWOoqzNPrLf4p9lwSTMUzgER1m2nbwNf34rrnSAV8fcwuEOL8qR9qDCWaCk1MQbMLgNv-HEodnt766a5JtdLCPWOUy9a	2026-03-27 17:27:58.018717
86	+55119782848304	user	gAAAAABpxujxasjDvBz3KE58oloFDb949oSnQuaV28lJw3Xe0DIdUro7C1zCvW01JV7S39mZ9gBegUOEhjhwocByQTsDQo_9Bq_WRnuHbruc0ij4oTosZ4yN1GWcIpR53B9JRCnB4IY1	2026-03-27 17:30:41.005069
87	+55119782848304	user	gAAAAABpxumdUJUQ7kTUGNy_X2LMLjqaeEhvMRZcwkrG3XBCvzxpYe0xQc6tsW3iv4WTn51HO01cSxAHzGQ0hLEYHwxNbHp2knnwuw1brG-DQ2h6qJemLhjjoL3Xm21o-YN9qr_9wzCa	2026-03-27 17:33:33.074813
88	+55119782848304	user	gAAAAABpxuqMWseCjLtZ1T1i1HomdbKqKEzKZgOChpf3AjhwI7ZVbCWsxTwZcubYe_2323gRlOkVJ6Dhw7CrtZDtzwyZbNGq2BiTEgiIMNXpn4QQHhCFiq2LQBLt8_Nn2Uxr5cT2Q-bB	2026-03-27 17:37:32.085068
89	+55119782848304	user	gAAAAABpxusYWZQoHdeDoreKOasK58DHDTe8mpSA9aKBb-Ovu4E2nOVlSPRJkAK51RkVO9k9OpLIF_lLdlXUoQG-YW6IOb13aplNm8fkMRD5FOK0uB6u7rvhFWcBgV3sIkT6fsesBuuT	2026-03-27 17:39:52.294899
90	+55119782848304	user	gAAAAABpxutvxzo6Jas-N8mb_WvXX2LQCwLCfPpg_FUJjYmCY8I7NvfiAWuUJToBk3GMbkMLWel_UeJeqtNsxUUyGIuaxiyiaB-WdJWwuigvN5I9rRnP8MAwWlfWeVaOxxVFY6SzCCzL	2026-03-27 17:41:19.98617
91	+55119782848304	user	gAAAAABpxuveGgaRVbpqAE2rNKddS30fmFx9y2ZBakQCgT9Wb-R9S1So6qKLQbHOIunqHDh19YnSc6FlzaqgxNTef0yKtJUAwFMgj4t_5LFk9n8gY9XoPHuujPXbDH1_HD0nu2RFMoRN	2026-03-27 17:43:10.616322
92	+55119782848304	user	gAAAAABpxuwUjBCIHg2r9SGeBq42gPtQ9-dkZqVlkbnj6G6LH__OEdnME1kUG3lXSMw4YtZeyNJ_lvRuLfEwJ5R2GnaHiBW_PuveSyJS9xwldIuxt0Fx2kH-aU-NCrUC7Lr6qlq65Ljo	2026-03-27 17:44:04.801432
93	+55119782848304	assistant	gAAAAABpxuxs9k27OxKm7kc56-ym7YMCdZtGkcNp-SXcwyF3Z4hJAhj4qQmNilvyJhdF3E6tN_frOBS2f_Jh2oMpweTxtmRgmb0DzMkdshy_GYoH87DNlxmEs__7m5l-PJ3piC3TkdKn__rsJD88JmqOHDQQ4pDw-0w5-fJdaCYxxmqQ12k2wlSNNuhV3ky9k8R3PrHH4Acgk9clFAs2aMNbTsZ-XHP_NgcRQsMigxiYMrj614N29TVSd0QypnnPAL31wOILKzWKg75y4xjCHx1G67DBX2HJL_xYG9FoDczKj4vV7Yy3S_nh79rILpXttt1BuzVqQm2a	2026-03-27 17:45:32.951312
94	+55119782848304	user	gAAAAABpxux_kzpKSJwnsoGQYao4KJobY92V-_L8SgR3dF4UNBUsiNC9HfdXd8ubG48L3yOzf89Ado09LPPpAOoBSuFA8A59KMxGcv6d2qi1qd3yUa1L-bj13rSV8UI37anjb1AFmjw6	2026-03-27 17:45:51.263742
95	+55119782848304	user	gAAAAABpzDJ-1ngKRUx8v0BCT-XoiBhbsj6e0m7MNGBBl06CEmYGRkTb9zHLTh4Mlkv5Jwn3T-SjB53Lb_uAAsXpoQ6Z6JOPl9pD3UYczhKVF8fUOjFOPo_mtHCUYy7ptSkYoY5p-L7z	2026-03-31 17:45:50.321493
96	+55119782848304	assistant	gAAAAABpzDKLXesvZo65o_EIKdw__fZzmNNfRIVk9ZRgbl7u2QPa1Pj8AN735PP_HPiZ52N_jePAmL_8HH8GUChQ9Duf8QGzbMERZ1X4CzJNgDfuEYMaYdx7YMPkQl5v9FeK6eZTLBtcdpVdta4uOeEK9I3pAsj_8AlcLN8fzgZf2SdEDjMk6jbYTD5gv9up0zBtdWt7Ky9NGUFuoIJd68VKPaEuFjFIjrqZub9B4BN3SlPCoOBnTO30a4Aqi6bJ1DNADSq_GvmB	2026-03-31 17:46:03.525083
97	+55119782848304	user	gAAAAABpzDKtCmBGh0C_UbJnE_SB6OPj9_cjktE-GWTfu4Q4moLT3CP8V3bOONNumytCPEsKzP3pui1KUkf03gDGh2UztvfBm9aw5wM5qEgCpdZhDXr3AYkj-YNWMuKLl8Y0E8YIDPYM	2026-03-31 17:46:37.200105
98	+55119782848304	assistant	gAAAAABpzDK3xPaD2HbdjQIUxfSV1ebM9G-1YNYcJ0aZ9TZP8gBY0XYOKlmWXr8n0b30iGV6PGuLU6AvZIXiubl-cahVyRbxXjZ1_20pGf_AOuycqYDImyaIdcYj2uqO-pyjWI5w2wUM97qlR7EvMWVIoZaLMwUPbsWXZhva7pYC_h0WuLCVt0gZnDCU9CuAErr7G9ujXFPsa43rxt4Pge_E0xGRcFT3M51-bWW-PPOWf7L92NlGOyHCsnb8Dmd6sbVglkXj7QRsztEpWdQzejG2JAyPR-ciElxa6nPNZ46KstNsSWkKWaUj4w4XKX9AUQ96B8ssEUt_wKc6OCKIb9fD1QdqML7a9ZZnS4zu4UiPk4xOQrxsHAU=	2026-03-31 17:46:47.615393
99	+55119782848304	user	gAAAAABpzDLWd7z0Ma0UNxD3_2GXl6OWWhfeJJrilJEDVDOvnGL1TaI9y1H3vLpm-Sva4_o9d5nNvprHoPRKg__5-YPSWvecXzR2GOXnHIiR4cNsQDM-wIlQaLeFSP8jEUQfv33dE5T4	2026-03-31 17:47:18.068538
100	+55119782848304	assistant	gAAAAABpzDLkjsjgVKPSgUHyJhmEhSeJPNKFVA8mSD5fNuMNAv2n7RB8UI8R0mbMV9Yyk-v0pFjLSp_Z-zyrGRdB7UwXIPieHQe78xGXB8azi6rBfGdAYLWP6TCyAlOD3XdZztp9FAiJ8urgVIVZnwYhHUINGDdOEF79L_V5rgv5taxdM9OFq4oOZYFiuaAxKUZdeCBmffZux1BPkXFF7WucAsiHsyhV6LGBaLc7I8_wRD-kA-8v85qUFMALCTbUr7ynbyPvdd_aEwFg0GLg0xTGUnWnVazA8CfHAyROn0w_e6H-EabDGwFl0BcYwqQzwteP9nzkpMnyBY99M-w_4bko3FUv68QAp7IpSFa70D7x2mcQ7OP0T38=	2026-03-31 17:47:32.968343
101	+55119782848304	user	gAAAAABpzDSKYmcmaOEH8RsE5Y8ifp8GA1XcRMV44RlCPBJlKZDGwLMHHgab_UfcCxKkS84fP7-PONxGigfCtm67z89QmiOh_FGMzXmTYO_xC-WkZ7Xmj3ucA09t39RhNvm2i8IniR3E	2026-03-31 17:54:34.288101
102	+55119782848304	assistant	gAAAAABpzDUUJ5caipzsoQmQn-4A6XFGbS5CCCtZd05V4gc-2pqERh7T3Dd9HEIWKajFZAcJ2CrgjU9GNiV8jXuuv47Eb-rVWfscSklDbVb5W-n9UDiOK8qZAxtPxdg8scGn24KkShi6_m25RkCt-59C3LghUHdmFRphzNDOQBNqPmGJMChEMHA1Ya0G01nqQM46SKoML2PrLqxdVh9XQIaNvlzv8dMEI8EMjNjZvcA9yRjDHTgW0rPj8KoVw3bzQBRaDz2MsIVE52dvqJ4CYXZMi41rmgmE1yAnTZdvibrJi828k_OMGgw=	2026-03-31 17:56:52.227674
\.


--
-- Data for Name: limites_compras; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.limites_compras (id_limite_compra, id_categoria, limite_categoria) FROM stdin;
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.logs (id, nivel, mensagem, modulo, funcao, linha, traceback, created_at) FROM stdin;
1	INFO	Recuperadas 8 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 13:09:54.282655+00
2	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:10:02.676681+00
3	INFO	Recuperadas 9 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 13:11:12.820254+00
4	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:11:14.007018+00
5	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 13:13:26.560074+00
6	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:13:27.65081+00
7	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:14:10.177904+00
8	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 13:45:58.623285+00
9	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:45:59.747248+00
10	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Para registrar a compra, preciso saber a categoria. Você gostaria de classificar essa compra como "Alimentação", "Lazer", ou outra categoria? Se preferir, posso criar uma nova categoria para você.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	35	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 33, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Para registrar a compra, preciso saber a categoria. Você gostaria de classificar essa compra como "Alimentação", "Lazer", ou outra categoria? Se preferir, posso criar uma nova categoria para você.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2025-12-31 13:46:34.128988+00
11	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 13:51:26.108764+00
12	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:51:27.192369+00
13	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:51:40.207668+00
14	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:54:55.446232+00
15	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 13:55:09.433119+00
16	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 14:44:05.363174+00
17	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 14:44:06.488043+00
18	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 14:49:16.8028+00
19	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 14:49:17.899768+00
20	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Houve um erro ao registrar a compra porque o campo "parcelas" não foi informado. Você poderia me dizer se essa compra será parcelada? Se sim, em quantas vezes? Se for à vista, posso registrar como 1 parcela.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	35	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 33, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Houve um erro ao registrar a compra porque o campo "parcelas" não foi informado. Você poderia me dizer se essa compra será parcelada? Se sim, em quantas vezes? Se for à vista, posso registrar como 1 parcela.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2025-12-31 14:49:54.113343+00
21	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 14:57:17.810323+00
22	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 14:57:18.987717+00
23	WARNING	Falha no parsing estruturado: Invalid json output: O cartão "Nubank Vitor" cadastrado no sistema é do tipo débito, não crédito. Você gostaria de registrar essa compra como débito mesmo, ou deseja adicionar em outro cartão de crédito? Por favor, confirme para que eu possa prosseguir corretamente. \n\nstatus='pergunta', topic='adicionar compra', summary='O cartão Nubank Vitor é do tipo débito. Deseja registrar a compra como débito ou escolher outro cartão de crédito?'\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	45	\N	2025-12-31 14:57:24.126238+00
24	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 14:57:25.05375+00
25	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2025-12-31 14:58:00.927142+00
26	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 14:58:02.01745+00
27	WARNING	Falha no parsing estruturado: Invalid json output: status='pergunta', topic='adicionar compra cartão Nubank', summary='Para registrar a compra no cartão Nubank, preciso das seguintes informações: valor da compra, estabelecimento onde foi realizada e o banco vinculado ao cartão Nubank. Por favor, informe esses dados para prosseguirmos.' \nsources=[]\ntools_used=[]\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	45	\N	2025-12-31 14:58:03.744431+00
28	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2025-12-31 14:58:04.676365+00
29	INFO	Recuperadas 0 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 18:42:58.726435+00
30	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 18:42:59.940791+00
31	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 18:43:12.886727+00
32	INFO	Recuperadas 2 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 18:44:16.191325+00
33	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 18:44:17.277792+00
34	INFO	Recuperadas 3 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:00:19.143036+00
35	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:00:20.250593+00
36	INFO	Recuperadas 4 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:02:56.992061+00
37	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:02:58.109699+00
38	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:03:51.610918+00
39	INFO	Recuperadas 6 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:04:36.306714+00
40	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:04:37.454002+00
41	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Compra de R$ 250,00 no Posto São Bartolomeu, categoria Carro, realizada hoje no cartão Itau Vitor, foi registrada com sucesso. \n\nSe precisar adicionar mais alguma compra ou consultar seus gastos, é só avisar! \n\nsources=[]\ntools_used=["GetCartoesInfo","GetBancosInfo","GetCurrentDateTime","InsertCompraCartao"]\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Compra de R$ 250,00 no Posto São Bartolomeu, categoria Carro, realizada hoje no cartão Itau Vitor, foi registrada com sucesso. \n\nSe precisar adicionar mais alguma compra ou consultar seus gastos, é só avisar! \n\nsources=[]\ntools_used=["GetCartoesInfo","GetBancosInfo","GetCurrentDateTime","InsertCompraCartao"]\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:04:50.427108+00
42	INFO	Recuperadas 7 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:07:26.352026+00
43	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:07:27.475043+00
44	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: As duas compras foram registradas com sucesso:\n\n1. Posto São Bartolomeu, categoria Carro, valor R$ 250,00, no cartão Itau Vitor, realizada hoje.\n2. Carrefour, categoria Pessoal, valor R$ 228,88, parcelada em 3 vezes, no cartão Itau Vitor, realizada ontem.\n\nSe precisar de mais alguma coisa, é só avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: As duas compras foram registradas com sucesso:\n\n1. Posto São Bartolomeu, categoria Carro, valor R$ 250,00, no cartão Itau Vitor, realizada hoje.\n2. Carrefour, categoria Pessoal, valor R$ 228,88, parcelada em 3 vezes, no cartão Itau Vitor, realizada ontem.\n\nSe precisar de mais alguma coisa, é só avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:07:59.238428+00
45	INFO	Recuperadas 8 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:15:20.360009+00
46	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:15:21.477452+00
47	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: A compra na Cobasi, categoria PET, no cartão Nubank Vitor, parcelada em 5 vezes, com observação "compras para Marie", foi registrada com sucesso para ontem. No entanto, o valor da compra não foi informado corretamente. Por favor, me informe o valor para que eu possa corrigir o registro, se necessário. \n\nSe precisar ajustar, só avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: A compra na Cobasi, categoria PET, no cartão Nubank Vitor, parcelada em 5 vezes, com observação "compras para Marie", foi registrada com sucesso para ontem. No entanto, o valor da compra não foi informado corretamente. Por favor, me informe o valor para que eu possa corrigir o registro, se necessário. \n\nSe precisar ajustar, só avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:15:58.046374+00
48	ERROR	'str' object has no attribute 'summary'	app.core.config	log_error_to_file	17	Traceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\api\\financial_agent_endpoint.py", line 62, in bot\n    response_text = result.summary\n                    ^^^^^^^^^^^^^^\nAttributeError: 'str' object has no attribute 'summary'\n	2026-01-04 19:15:58.521718+00
49	INFO	Recuperadas 9 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:21:56.8099+00
50	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:21:57.912886+00
51	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Compra registrada com sucesso: Cobasi, R$ 300,00, categoria PET, no cartão Nubank Vitor, parcelada em 5 vezes, com observação "compras para Marie", realizada ontem.\n\nstatus='resposta', topic='inserção de compra', summary='Compra na Cobasi de R$ 300,00 registrada com sucesso no cartão Nubank Vitor, categoria PET, 5 parcelas, observação: compras para Marie.', sources=[], tools_used=["GetCartoesInfo", "GetBancosInfo", "GetCurrentDateTime", "InsertCompraCartao"]\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Compra registrada com sucesso: Cobasi, R$ 300,00, categoria PET, no cartão Nubank Vitor, parcelada em 5 vezes, com observação "compras para Marie", realizada ontem.\n\nstatus='resposta', topic='inserção de compra', summary='Compra na Cobasi de R$ 300,00 registrada com sucesso no cartão Nubank Vitor, categoria PET, 5 parcelas, observação: compras para Marie.', sources=[], tools_used=["GetCartoesInfo", "GetBancosInfo", "GetCurrentDateTime", "InsertCompraCartao"]\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:22:23.310617+00
52	ERROR	'str' object has no attribute 'summary'	app.core.config	log_error_to_file	17	Traceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\api\\financial_agent_endpoint.py", line 62, in bot\n    # Se result for ResearchResponse, pega o summary\nAttributeError: 'str' object has no attribute 'summary'\n	2026-01-04 19:22:23.904603+00
53	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:24:42.714093+00
54	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:24:43.799481+00
55	ERROR	Erro na conexão com o banco: duplicate key value violates unique constraint "categorias_de_compras_pkey"\nDETAIL:  Key (id_categoria)=(9) already exists.\n	app.services.postgres_service	get_connection	52	Traceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\postgres_service.py", line 45, in get_connection\n    yield conn\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\categorias_service.py", line 45, in insert_categoria\n    cur.execute(\n    ~~~~~~~~~~~^\n        'INSERT INTO "categorias_de_compras" ("nome_categoria") VALUES (%s) RETURNING "id_categoria"',\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        (nome_categoria,)\n        ^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\psycopg2\\extras.py", line 236, in execute\n    return super().execute(query, vars)\n           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^\npsycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "categorias_de_compras_pkey"\nDETAIL:  Key (id_categoria)=(9) already exists.\n\n	2026-01-04 19:24:51.679635+00
56	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Houve um erro ao registrar a compra devido a um problema interno com a categoria "Refeição". Recomendo revisar as categorias cadastradas ou tentar novamente em instantes. Se preferir, posso listar as categorias disponíveis para você escolher outra. Deseja tentar novamente ou consultar as categorias?\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Houve um erro ao registrar a compra devido a um problema interno com a categoria "Refeição". Recomendo revisar as categorias cadastradas ou tentar novamente em instantes. Se preferir, posso listar as categorias disponíveis para você escolher outra. Deseja tentar novamente ou consultar as categorias?\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:25:35.506678+00
57	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:28:15.526124+00
58	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:28:16.612284+00
59	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:28:40.100864+00
60	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:28:58.500274+00
61	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:28:59.600411+00
62	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:29:18.107896+00
63	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:29:55.501295+00
64	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:29:56.590458+00
65	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:30:23.624983+00
66	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:31:37.25872+00
67	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:31:38.528401+00
68	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:31:44.761908+00
69	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:32:18.296147+00
70	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:32:19.380561+00
71	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:32:25.078128+00
72	INFO	Recuperadas 0 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:37:11.759134+00
73	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:37:12.859672+00
74	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:37:14.618177+00
75	INFO	Recuperadas 2 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:39:43.560446+00
76	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:39:44.667928+00
77	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Estou bem, obrigado por perguntar! E você, como posso ajudar nas suas finanças hoje? Se quiser consultar saldos, registrar uma compra ou analisar seus gastos, é só me avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Estou bem, obrigado por perguntar! E você, como posso ajudar nas suas finanças hoje? Se quiser consultar saldos, registrar uma compra ou analisar seus gastos, é só me avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:39:46.107316+00
78	INFO	Recuperadas 3 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:42:49.574406+00
79	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:42:50.653337+00
80	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:42:52.6595+00
81	INFO	Recuperadas 5 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:46:45.822628+00
82	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:46:47.044372+00
83	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Olá! Como posso te ajudar com suas finanças hoje? Se quiser consultar saldos, registrar uma compra ou analisar seus gastos, é só me dizer!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Olá! Como posso te ajudar com suas finanças hoje? Se quiser consultar saldos, registrar uma compra ou analisar seus gastos, é só me dizer!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:46:48.824443+00
84	INFO	Recuperadas 6 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-04 19:56:25.347044+00
85	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-04 19:56:26.485684+00
86	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Olá! Como posso ajudar você com suas finanças hoje? Se precisar consultar saldos, registrar uma compra ou analisar seus gastos, é só me avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Olá! Como posso ajudar você com suas finanças hoje? Se precisar consultar saldos, registrar uma compra ou analisar seus gastos, é só me avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-04 19:56:27.941753+00
87	INFO	Recuperadas 0 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-16 14:44:59.862353+00
88	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:45:01.603491+00
89	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:45:04.928857+00
90	INFO	Recuperadas 2 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-16 14:45:23.721488+00
91	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:45:24.900657+00
92	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:45:35.604819+00
93	INFO	Recuperadas 4 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-16 14:46:14.513549+00
94	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:46:15.946033+00
95	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:46:21.886051+00
96	INFO	Recuperadas 6 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-16 14:47:09.185374+00
97	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:47:10.526988+00
119	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:35:28.457276+00
120	INFO	Recuperadas 2 mensagens para +55119782848304	app.services.conversation_history_service	get_history	138	\N	2026-01-19 12:36:28.486862+00
121	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:36:29.581527+00
98	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Com base nas suas entradas, saídas frequentes e faturas pendentes, você ainda pode gastar aproximadamente R$ 902,66 neste mês sem comprometer seu orçamento. Se precisar de uma análise mais detalhada ou quiser simular novos gastos, é só avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Com base nas suas entradas, saídas frequentes e faturas pendentes, você ainda pode gastar aproximadamente R$ 902,66 neste mês sem comprometer seu orçamento. Se precisar de uma análise mais detalhada ou quiser simular novos gastos, é só avisar!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-16 14:47:21.499606+00
99	INFO	Recuperadas 7 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-16 14:47:56.5499+00
100	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:47:57.847592+00
101	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:48:13.708043+00
102	INFO	Recuperadas 9 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-16 14:50:07.631674+00
103	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:50:09.125139+00
104	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:50:13.522914+00
105	INFO	Recuperadas 10 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	135	\N	2026-01-16 14:52:30.328282+00
106	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	65	\N	2026-01-16 14:52:31.65897+00
107	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: No momento, não tenho acesso direto ao detalhamento por estabelecimento, apenas por categoria. Se desejar, posso listar as categorias em que você mais gastou ou ajudar a consultar compras recentes em estabelecimentos específicos, caso informe o nome. Se quiser um relatório detalhado por estabelecimento, posso verificar se há essa opção disponível. Deseja tentar algo assim?\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: No momento, não tenho acesso direto ao detalhamento por estabelecimento, apenas por categoria. Se desejar, posso listar as categorias em que você mais gastou ou ajudar a consultar compras recentes em estabelecimentos específicos, caso informe o nome. Se quiser um relatório detalhado por estabelecimento, posso verificar se há essa opção disponível. Deseja tentar algo assim?\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-16 14:52:41.300227+00
108	INFO	Recuperadas 0 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	138	\N	2026-01-19 12:26:39.42518+00
109	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:26:40.55259+00
110	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:26:44.351939+00
111	INFO	Recuperadas 2 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	138	\N	2026-01-19 12:27:18.380683+00
112	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:27:19.496996+00
113	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:27:29.142344+00
114	INFO	Recuperadas 4 mensagens para whatsapp:+5511972848304	app.services.conversation_history_service	get_history	138	\N	2026-01-19 12:34:32.798033+00
115	INFO	Mensagem salva para whatsapp:+5511972848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:34:33.96488+00
116	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Oi! 😄 Estou aqui! Precisa de alguma orientação sobre suas finanças, quer registrar uma compra ou conferir algum resumo? Me diga como posso ajudar você hoje!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	44	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 42, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Oi! 😄 Estou aqui! Precisa de alguma orientação sobre suas finanças, quer registrar uma compra ou conferir algum resumo? Me diga como posso ajudar você hoje!\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-01-19 12:34:36.46197+00
117	INFO	Recuperadas 0 mensagens para +55119782848304	app.services.conversation_history_service	get_history	138	\N	2026-01-19 12:35:22.624781+00
118	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:35:23.709436+00
122	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	67	\N	2026-01-19 12:36:38.65604+00
123	INFO	Recuperadas 0 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 16:54:46.379222+00
124	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 16:54:47.550583+00
125	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 16:54:50.745887+00
126	INFO	Recuperadas 2 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 16:55:19.053167+00
127	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 16:55:20.046499+00
128	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:21:27.740369+00
129	INFO	Recuperadas 4 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:21:48.253316+00
130	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:21:49.355313+00
131	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Não consegui recuperar a lista de cartões cadastrados devido a um erro temporário no sistema. Você gostaria de tentar novamente ou deseja consultar outra informação financeira? Se preferir, posso ajudar com bancos, despesas, receitas ou configuração do sistema.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	65	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 63, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Não consegui recuperar a lista de cartões cadastrados devido a um erro temporário no sistema. Você gostaria de tentar novamente ou deseja consultar outra informação financeira? Se preferir, posso ajudar com bancos, despesas, receitas ou configuração do sistema.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-03-27 17:22:04.932361+00
132	INFO	Recuperadas 5 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:27:57.422497+00
133	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:27:58.444984+00
134	INFO	Recuperadas 6 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:30:40.38567+00
135	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:30:41.450919+00
136	ERROR	Database connection error: 0	app.services.postgres_service	get_connection	72	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\postgres_service.py", line 65, in get_connection\n    yield conn\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\tools\\dynamic_query_tool.py", line 54, in get_db_schema\n    table_name = line[0]\n                 ~~~~^^^\nKeyError: 0\n	2026-03-27 17:30:55.781032+00
137	INFO	Recuperadas 7 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:33:32.476342+00
138	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:33:33.499037+00
139	ERROR	Database connection error: 'list' object has no attribute 'items'	app.services.postgres_service	get_connection	72	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\postgres_service.py", line 65, in get_connection\n    yield conn\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\tools\\dynamic_query_tool.py", line 53, in get_db_schema\n    for _, table_name in tables.items():\n                         ^^^^^^^^^^^^\nAttributeError: 'list' object has no attribute 'items'\n	2026-03-27 17:33:49.429698+00
140	ERROR	Erro ao parsear resposta do OpenAI: Invalid json output: Houve um erro ao tentar acessar a lista de cartões cadastrados. Você gostaria de tentar novamente ou deseja realizar outra consulta financeira? Se preferir, posso ajudar com outras informações sobre suas finanças.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 	app.services.opena_ai_service	run	65	Traceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 82, in parse_result\n    return parse_json_markdown(text)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 150, in parse_json_markdown\n    return _parse_json(json_str, parser=parser)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 166, in _parse_json\n    return parser(json_str)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\utils\\json.py", line 123, in parse_partial_json\n    return json.loads(s, strict=strict)\n           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\__init__.py", line 359, in loads\n    return cls(**kw).decode(s)\n           ~~~~~~~~~~~~~~~~^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 345, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^\n  File "C:\\Users\\vitor\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\json\\decoder.py", line 363, in raw_decode\n    raise JSONDecodeError("Expecting value", s, err.value) from None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\opena_ai_service.py", line 63, in run\n    return self.parser.parse(raw_response["output"])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 77, in parse\n    return super().parse(text)\n           ~~~~~~~~~~~~~^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 96, in parse\n    return self.parse_result([Generation(text=text)])\n           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\pydantic.py", line 61, in parse_result\n    json_object = super().parse_result(result)\n  File "c:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\.venv\\Lib\\site-packages\\langchain_core\\output_parsers\\json.py", line 85, in parse_result\n    raise OutputParserException(msg, llm_output=text) from e\nlangchain_core.exceptions.OutputParserException: Invalid json output: Houve um erro ao tentar acessar a lista de cartões cadastrados. Você gostaria de tentar novamente ou deseja realizar outra consulta financeira? Se preferir, posso ajudar com outras informações sobre suas finanças.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE \n	2026-03-27 17:34:04.296932+00
141	INFO	Recuperadas 8 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:37:31.497308+00
142	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:37:32.513899+00
143	ERROR	Database connection error: not enough values to unpack (expected 2, got 1)	app.services.postgres_service	get_connection	72	Traceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\postgres_service.py", line 65, in get_connection\n    yield conn\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\tools\\dynamic_query_tool.py", line 53, in get_db_schema\n    for _, table_name in tables:\n        ^^^^^^^^^^^^^\nValueError: not enough values to unpack (expected 2, got 1)\n	2026-03-27 17:37:58.960221+00
144	INFO	Recuperadas 9 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:39:51.693971+00
145	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:39:52.752705+00
146	ERROR	Database connection error: 0	app.services.postgres_service	get_connection	72	Traceback (most recent call last):\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\services\\postgres_service.py", line 65, in get_connection\n    yield conn\n  File "C:\\Users\\vitor\\OneDrive\\Documentos\\Projects\\ControleFinanceiro\\app\\tools\\dynamic_query_tool.py", line 55, in get_db_schema\n    table_name = line['table_name']\n                 ^^^^^^^\nKeyError: 0\n	2026-03-27 17:41:01.687008+00
147	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:41:19.409868+00
148	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:41:20.411536+00
149	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:43:10.056127+00
150	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:43:11.063436+00
151	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:44:04.178069+00
152	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:44:05.218178+00
154	INFO	Recuperadas 10 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-27 17:45:50.700249+00
155	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-27 17:45:51.69644+00
156	INFO	Recuperadas 0 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-31 17:45:49.681986+00
157	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:45:50.77033+00
158	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:46:03.955637+00
159	INFO	Recuperadas 2 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-31 17:46:36.633849+00
160	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:46:37.621486+00
161	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:46:48.047925+00
162	INFO	Recuperadas 4 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-31 17:47:17.500907+00
163	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:47:18.496528+00
164	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:47:33.392555+00
165	INFO	Recuperadas 6 mensagens para +55119782848304	app.services.conversation_history_service	get_history	167	\N	2026-03-31 17:54:33.606661+00
166	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:54:34.718414+00
167	INFO	Mensagem salva para +55119782848304	app.services.conversation_history_service	save_message	86	\N	2026-03-31 17:56:52.673612+00
\.


--
-- Data for Name: saidas_frequentes_config; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.saidas_frequentes_config (id_saida_frequente, nome_saida, valor_saida, dia_saida, id_categoria) FROM stdin;
1	Conta de Luz	234.17	8	7
2	Conta Internet/Cel Vitor/Cel Gica	250.00	6	7
3	Condominio/Agua/Gas	460.00	15	7
4	Seguro do carro	247.94	14	4
5	FIES GIca Caixa	46.00	15	11
6	Parcela Divida Gica	144.00	15	11
8	Psicologa Gica	500.00	8	11
9	Sexologa Gica	1200.00	8	11
\.


--
-- Data for Name: saidas_realizadas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.saidas_realizadas (id_saida, id_categoria, id_banco, data_saida, valor, descricao, created_at) FROM stdin;
1	7	2	2025-12-08	234.17	Conta de Luz	2026-03-23 18:11:52.120727
2	7	2	2025-12-06	250.00	Conta Internet/Cel Vitor/Cel Gica	2026-03-23 18:11:52.120727
3	7	2	2025-12-15	460.00	Condominio/Agua/Gas	2026-03-23 18:11:52.120727
4	4	2	2025-12-14	247.94	Seguro do carro	2026-03-23 18:11:52.120727
5	11	2	2025-12-15	46.00	FIES GIca Caixa	2026-03-23 18:11:52.120727
6	11	2	2025-12-15	144.00	Parcela Divida Gica	2026-03-23 18:11:52.120727
7	11	2	2025-12-08	500.00	Psicologa Gica	2026-03-23 18:11:52.120727
8	11	2	2025-12-08	1200.00	Sexologa Gica	2026-03-23 18:11:52.120727
9	7	2	2026-01-08	234.17	Conta de Luz	2026-03-23 18:11:52.120727
10	7	2	2026-01-06	250.00	Conta Internet/Cel Vitor/Cel Gica	2026-03-23 18:11:52.120727
11	7	2	2026-01-15	460.00	Condominio/Agua/Gas	2026-03-23 18:11:52.120727
12	4	2	2026-01-14	247.94	Seguro do carro	2026-03-23 18:11:52.120727
13	11	2	2026-01-15	46.00	FIES GIca Caixa	2026-03-23 18:11:52.120727
14	11	2	2026-01-15	144.00	Parcela Divida Gica	2026-03-23 18:11:52.120727
15	11	2	2026-01-08	500.00	Psicologa Gica	2026-03-23 18:11:52.120727
16	11	2	2026-01-08	1200.00	Sexologa Gica	2026-03-23 18:11:52.120727
17	7	2	2026-02-08	234.17	Conta de Luz	2026-03-23 18:11:52.120727
18	7	2	2026-02-06	250.00	Conta Internet/Cel Vitor/Cel Gica	2026-03-23 18:11:52.120727
19	7	2	2026-02-15	460.00	Condominio/Agua/Gas	2026-03-23 18:11:52.120727
20	4	2	2026-02-14	247.94	Seguro do carro	2026-03-23 18:11:52.120727
21	11	2	2026-02-15	46.00	FIES GIca Caixa	2026-03-23 18:11:52.120727
22	11	2	2026-02-15	144.00	Parcela Divida Gica	2026-03-23 18:11:52.120727
23	11	2	2026-02-08	500.00	Psicologa Gica	2026-03-23 18:11:52.120727
24	11	2	2026-02-08	1200.00	Sexologa Gica	2026-03-23 18:11:52.120727
25	7	2	2026-03-08	234.17	Conta de Luz	2026-03-23 18:11:52.120727
26	7	2	2026-03-06	250.00	Conta Internet/Cel Vitor/Cel Gica	2026-03-23 18:11:52.120727
27	7	2	2026-03-15	460.00	Condominio/Agua/Gas	2026-03-23 18:11:52.120727
28	4	2	2026-03-14	247.94	Seguro do carro	2026-03-23 18:11:52.120727
29	11	2	2026-03-15	46.00	FIES GIca Caixa	2026-03-23 18:11:52.120727
30	11	2	2026-03-15	144.00	Parcela Divida Gica	2026-03-23 18:11:52.120727
31	11	2	2026-03-08	500.00	Psicologa Gica	2026-03-23 18:11:52.120727
32	11	2	2026-03-08	1200.00	Sexologa Gica	2026-03-23 18:11:52.120727
\.


--
-- Name: bancos_id_banco_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.bancos_id_banco_seq', 6, true);


--
-- Name: cartoes_de_credito_id_cartao_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cartoes_de_credito_id_cartao_seq', 7, true);


--
-- Name: categorias_de_compras_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categorias_de_compras_id_categoria_seq', 10, true);


--
-- Name: compras_cartoes_de_credito_id_compra_cartao_credito_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.compras_cartoes_de_credito_id_compra_cartao_credito_seq', 400, true);


--
-- Name: entradas_id_entrada_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.entradas_id_entrada_seq', 6, true);


--
-- Name: entradas_realizadas_id_entrada_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.entradas_realizadas_id_entrada_seq', 30, true);


--
-- Name: faturas_cartoes_de_credito_id_fatura_cartao_credito_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.faturas_cartoes_de_credito_id_fatura_cartao_credito_seq', 18, true);


--
-- Name: historico_de_mensagens_mensagem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.historico_de_mensagens_mensagem_id_seq', 102, true);


--
-- Name: limites_compras_id_limite_compra_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.limites_compras_id_limite_compra_seq', 1, false);


--
-- Name: logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.logs_id_seq', 167, true);


--
-- Name: saidas_frequentes_id_saida_frequente_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.saidas_frequentes_id_saida_frequente_seq', 10, true);


--
-- Name: saidas_realizadas_id_saida_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.saidas_realizadas_id_saida_seq', 32, true);


--
-- Name: bancos bancos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bancos
    ADD CONSTRAINT bancos_pkey PRIMARY KEY (id_banco);


--
-- Name: cartoes cartoes_de_credito_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cartoes
    ADD CONSTRAINT cartoes_de_credito_pkey PRIMARY KEY (id_cartao);


--
-- Name: categorias categorias_de_compras_nome_categoria_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_de_compras_nome_categoria_key UNIQUE (nome_categoria);


--
-- Name: categorias categorias_de_compras_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_de_compras_pkey PRIMARY KEY (id_categoria);


--
-- Name: compras_cartao compras_cartao_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compras_cartao
    ADD CONSTRAINT compras_cartao_pkey PRIMARY KEY (id_compra_cartao);


--
-- Name: entradas_config entradas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entradas_config
    ADD CONSTRAINT entradas_pkey PRIMARY KEY (id_entrada);


--
-- Name: entradas_realizadas entradas_realizadas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entradas_realizadas
    ADD CONSTRAINT entradas_realizadas_pkey PRIMARY KEY (id_entrada);


--
-- Name: faturas_cartoes_de_credito faturas_cartoes_de_credito_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.faturas_cartoes_de_credito
    ADD CONSTRAINT faturas_cartoes_de_credito_pkey PRIMARY KEY (id_fatura_cartao_credito);


--
-- Name: historico_de_mensagens historico_de_mensagens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historico_de_mensagens
    ADD CONSTRAINT historico_de_mensagens_pkey PRIMARY KEY (mensagem_id);


--
-- Name: limites_compras limites_compras_id_categoria_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.limites_compras
    ADD CONSTRAINT limites_compras_id_categoria_key UNIQUE (id_categoria);


--
-- Name: limites_compras limites_compras_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.limites_compras
    ADD CONSTRAINT limites_compras_pkey PRIMARY KEY (id_limite_compra);


--
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- Name: saidas_frequentes_config saidas_frequentes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saidas_frequentes_config
    ADD CONSTRAINT saidas_frequentes_pkey PRIMARY KEY (id_saida_frequente);


--
-- Name: saidas_realizadas saidas_realizadas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saidas_realizadas
    ADD CONSTRAINT saidas_realizadas_pkey PRIMARY KEY (id_saida);


--
-- Name: idx_cartoes_banco; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_cartoes_banco ON public.cartoes USING btree (id_banco);


--
-- Name: idx_compras_cartao; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_compras_cartao ON public.compras_cartao USING btree (id_cartao);


--
-- Name: idx_compras_categoria; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_compras_categoria ON public.compras_cartao USING btree (id_categoria);


--
-- Name: idx_compras_data; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_compras_data ON public.compras_cartao USING btree (data_compra);


--
-- Name: idx_data_criacao; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_data_criacao ON public.historico_de_mensagens USING btree (data_criacao);


--
-- Name: idx_entradas_banco; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_entradas_banco ON public.entradas_config USING btree (id_banco);


--
-- Name: idx_entradas_data; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_entradas_data ON public.entradas_realizadas USING btree (data_entrada);


--
-- Name: idx_faturas_cartao; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_faturas_cartao ON public.faturas_cartoes_de_credito USING btree (id_cartao);


--
-- Name: idx_logs_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_logs_created_at ON public.logs USING btree (created_at);


--
-- Name: idx_logs_modulo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_logs_modulo ON public.logs USING btree (modulo);


--
-- Name: idx_logs_nivel; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_logs_nivel ON public.logs USING btree (nivel);


--
-- Name: idx_logs_nivel_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_logs_nivel_created_at ON public.logs USING btree (nivel, created_at);


--
-- Name: idx_numero_data; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_numero_data ON public.historico_de_mensagens USING btree (numero_telefone, data_criacao DESC);


--
-- Name: idx_numero_telefone; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_numero_telefone ON public.historico_de_mensagens USING btree (numero_telefone);


--
-- Name: idx_saidas_data; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_saidas_data ON public.saidas_realizadas USING btree (data_saida);


--
-- Name: cartoes cartoes_de_credito_id_banco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cartoes
    ADD CONSTRAINT cartoes_de_credito_id_banco_fkey FOREIGN KEY (id_banco) REFERENCES public.bancos(id_banco) ON DELETE CASCADE;


--
-- Name: compras_cartao compras_cartoes_de_credito_id_cartao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compras_cartao
    ADD CONSTRAINT compras_cartoes_de_credito_id_cartao_fkey FOREIGN KEY (id_cartao) REFERENCES public.cartoes(id_cartao) ON DELETE CASCADE;


--
-- Name: compras_cartao compras_cartoes_de_credito_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compras_cartao
    ADD CONSTRAINT compras_cartoes_de_credito_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria) ON DELETE SET NULL;


--
-- Name: entradas_config entradas_id_banco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entradas_config
    ADD CONSTRAINT entradas_id_banco_fkey FOREIGN KEY (id_banco) REFERENCES public.bancos(id_banco) ON DELETE CASCADE;


--
-- Name: entradas_realizadas entradas_realizadas_id_banco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entradas_realizadas
    ADD CONSTRAINT entradas_realizadas_id_banco_fkey FOREIGN KEY (id_banco) REFERENCES public.bancos(id_banco);


--
-- Name: faturas_cartoes_de_credito faturas_cartoes_de_credito_id_cartao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.faturas_cartoes_de_credito
    ADD CONSTRAINT faturas_cartoes_de_credito_id_cartao_fkey FOREIGN KEY (id_cartao) REFERENCES public.cartoes(id_cartao) ON DELETE CASCADE;


--
-- Name: entradas_config fk_categoria; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entradas_config
    ADD CONSTRAINT fk_categoria FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria);


--
-- Name: saidas_frequentes_config fk_categoria; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saidas_frequentes_config
    ADD CONSTRAINT fk_categoria FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria);


--
-- Name: limites_compras limites_compras_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.limites_compras
    ADD CONSTRAINT limites_compras_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria) ON DELETE CASCADE;


--
-- Name: saidas_realizadas saidas_realizadas_id_banco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saidas_realizadas
    ADD CONSTRAINT saidas_realizadas_id_banco_fkey FOREIGN KEY (id_banco) REFERENCES public.bancos(id_banco);


--
-- Name: saidas_realizadas saidas_realizadas_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saidas_realizadas
    ADD CONSTRAINT saidas_realizadas_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria);


--
-- PostgreSQL database dump complete
--

\unrestrict wGcIDNs9ExccIsuYFkUPseLmhkEp5VcxwOTcLpqtGkD42hVyHXpGzqeMFGiASGe

