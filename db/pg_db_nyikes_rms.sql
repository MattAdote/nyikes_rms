--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 10.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: campaign_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.campaign_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: campaign; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campaign (
    id integer DEFAULT nextval('public.campaign_seq'::regclass) NOT NULL,
    start_date date,
    end_date date,
    status_id integer NOT NULL,
    target_amount double precision NOT NULL,
    campaign_name character varying(75) NOT NULL,
    campaign_description character varying(75) DEFAULT NULL::character varying,
    notes character varying(75) DEFAULT NULL::character varying
);


ALTER TABLE public.campaign OWNER TO postgres;

--
-- Name: campaign_contributions_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.campaign_contributions_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_contributions_seq OWNER TO postgres;

--
-- Name: campaign_contributions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campaign_contributions (
    id integer DEFAULT nextval('public.campaign_contributions_seq'::regclass) NOT NULL,
    split_txn_id integer NOT NULL,
    campaign_id integer NOT NULL,
    contrib_amount double precision NOT NULL
);


ALTER TABLE public.campaign_contributions OWNER TO postgres;

--
-- Name: campaign_status_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.campaign_status_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_status_seq OWNER TO postgres;

--
-- Name: campaign_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campaign_status (
    id integer DEFAULT nextval('public.campaign_status_seq'::regclass) NOT NULL,
    status_name character varying(75) NOT NULL,
    status_description character varying(75) NOT NULL
);


ALTER TABLE public.campaign_status OWNER TO postgres;

--
-- Name: credit_transaction_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.credit_transaction_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.credit_transaction_seq OWNER TO postgres;

--
-- Name: credit_transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.credit_transaction (
    id integer DEFAULT nextval('public.credit_transaction_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    txn_mode_id integer NOT NULL,
    transacting_member_id integer NOT NULL,
    reference_no character varying(75) DEFAULT NULL::character varying,
    amount double precision NOT NULL,
    txn_ts timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    remarks character varying(50) NOT NULL
);


ALTER TABLE public.credit_transaction OWNER TO postgres;

--
-- Name: credit_transaction_split_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.credit_transaction_split_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.credit_transaction_split_seq OWNER TO postgres;

--
-- Name: credit_transaction_split; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.credit_transaction_split (
    id integer DEFAULT nextval('public.credit_transaction_split_seq'::regclass) NOT NULL,
    credit_txn_id integer NOT NULL,
    member_id integer NOT NULL,
    txn_amount double precision NOT NULL,
    remarks character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE public.credit_transaction_split OWNER TO postgres;

--
-- Name: debit_transaction_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.debit_transaction_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.debit_transaction_seq OWNER TO postgres;

--
-- Name: debit_transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.debit_transaction (
    id integer DEFAULT nextval('public.debit_transaction_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    txn_mode_id integer NOT NULL,
    campaign_id integer,
    fund_account_id integer,
    reference_no character varying(75) DEFAULT NULL::character varying,
    amount double precision NOT NULL,
    authorized smallint NOT NULL,
    authorized_ts timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    txn_ts timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.debit_transaction OWNER TO postgres;

--
-- Name: debit_txn_authorization_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.debit_txn_authorization_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.debit_txn_authorization_seq OWNER TO postgres;

--
-- Name: debit_txn_authorization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.debit_txn_authorization (
    id integer DEFAULT nextval('public.debit_txn_authorization_seq'::regclass) NOT NULL,
    debit_txn_id integer NOT NULL,
    holding_acc_signatory_id integer NOT NULL,
    authorization_ts timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    authorizes smallint NOT NULL
);


ALTER TABLE public.debit_txn_authorization OWNER TO postgres;

--
-- Name: debit_txn_cost_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.debit_txn_cost_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.debit_txn_cost_seq OWNER TO postgres;

--
-- Name: debit_txn_cost; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.debit_txn_cost (
    id integer DEFAULT nextval('public.debit_txn_cost_seq'::regclass) NOT NULL,
    debit_txn_id integer NOT NULL,
    cost_name character varying(75) NOT NULL,
    cost_amount double precision NOT NULL,
    cost_description character varying(75) DEFAULT NULL::character varying
);


ALTER TABLE public.debit_txn_cost OWNER TO postgres;

--
-- Name: fund_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fund_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fund_seq OWNER TO postgres;

--
-- Name: fund; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fund (
    id integer DEFAULT nextval('public.fund_seq'::regclass) NOT NULL,
    fund_name character varying(75) NOT NULL,
    fund_description character varying(75) DEFAULT NULL::character varying,
    fund_balance double precision NOT NULL,
    balance_last_update_ts timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.fund OWNER TO postgres;

--
-- Name: fund_account_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fund_account_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fund_account_seq OWNER TO postgres;

--
-- Name: fund_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fund_account (
    id integer DEFAULT nextval('public.fund_account_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    fund_id integer NOT NULL,
    fund_balance double precision NOT NULL
);


ALTER TABLE public.fund_account OWNER TO postgres;

--
-- Name: fund_contributions_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fund_contributions_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fund_contributions_seq OWNER TO postgres;

--
-- Name: fund_contributions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fund_contributions (
    id integer DEFAULT nextval('public.fund_contributions_seq'::regclass) NOT NULL,
    fund_id integer NOT NULL,
    split_txn_id integer,
    welfare_contribution_id integer,
    contrib_amount double precision NOT NULL,
    fund_running_balance double precision NOT NULL
);


ALTER TABLE public.fund_contributions OWNER TO postgres;

--
-- Name: holding_account_type_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.holding_account_type_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.holding_account_type_seq OWNER TO postgres;

--
-- Name: holding_account_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.holding_account_type (
    id integer DEFAULT nextval('public.holding_account_type_seq'::regclass) NOT NULL,
    type_name character varying(75) NOT NULL,
    description character varying(75) DEFAULT NULL::character varying
);


ALTER TABLE public.holding_account_type OWNER TO postgres;

--
-- Name: member_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.member_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.member_seq OWNER TO postgres;

--
-- Name: member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member (
    id integer DEFAULT nextval('public.member_seq'::regclass) NOT NULL,
    class_id integer NOT NULL,
    first_name character varying(75) NOT NULL,
    middle_name character varying(75) NOT NULL,
    surname character varying(75) NOT NULL,
    email character varying(75) DEFAULT NULL::character varying
);


ALTER TABLE public.member OWNER TO postgres;

--
-- Name: membership_class_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.membership_class_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.membership_class_seq OWNER TO postgres;

--
-- Name: membership_class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.membership_class (
    id integer DEFAULT nextval('public.membership_class_seq'::regclass) NOT NULL,
    class_name character varying(75) NOT NULL,
    monthly_contribution_amount double precision NOT NULL
);


ALTER TABLE public.membership_class OWNER TO postgres;

--
-- Name: nyikes_holding_acc_signatory_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.nyikes_holding_acc_signatory_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nyikes_holding_acc_signatory_seq OWNER TO postgres;

--
-- Name: nyikes_holding_acc_signatory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nyikes_holding_acc_signatory (
    id integer DEFAULT nextval('public.nyikes_holding_acc_signatory_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    member_id integer NOT NULL
);


ALTER TABLE public.nyikes_holding_acc_signatory OWNER TO postgres;

--
-- Name: nyikes_holding_account_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.nyikes_holding_account_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nyikes_holding_account_seq OWNER TO postgres;

--
-- Name: nyikes_holding_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nyikes_holding_account (
    id integer DEFAULT nextval('public.nyikes_holding_account_seq'::regclass) NOT NULL,
    account_type_id integer NOT NULL,
    account_number character varying(75) NOT NULL,
    account_name character varying(75) NOT NULL,
    account_balance double precision NOT NULL,
    notes character varying(75) NOT NULL
);


ALTER TABLE public.nyikes_holding_account OWNER TO postgres;

--
-- Name: transaction_mode_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_mode_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_mode_seq OWNER TO postgres;

--
-- Name: transaction_mode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction_mode (
    id integer DEFAULT nextval('public.transaction_mode_seq'::regclass) NOT NULL,
    name character varying(75) NOT NULL,
    description character varying(75) DEFAULT NULL::character varying
);


ALTER TABLE public.transaction_mode OWNER TO postgres;

--
-- Name: welfare_contrib_alloc_reference_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.welfare_contrib_alloc_reference_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.welfare_contrib_alloc_reference_seq OWNER TO postgres;

--
-- Name: welfare_contrib_alloc_reference; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.welfare_contrib_alloc_reference (
    id integer DEFAULT nextval('public.welfare_contrib_alloc_reference_seq'::regclass) NOT NULL,
    fund_id integer NOT NULL,
    percent_to_allocate double precision NOT NULL
);


ALTER TABLE public.welfare_contrib_alloc_reference OWNER TO postgres;

--
-- Name: welfare_contrib_schedule_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.welfare_contrib_schedule_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.welfare_contrib_schedule_seq OWNER TO postgres;

--
-- Name: welfare_contrib_schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.welfare_contrib_schedule (
    id integer DEFAULT nextval('public.welfare_contrib_schedule_seq'::regclass) NOT NULL,
    contrib_month character varying(75) NOT NULL,
    contrib_year integer NOT NULL
);


ALTER TABLE public.welfare_contrib_schedule OWNER TO postgres;

--
-- Name: welfare_contributions_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.welfare_contributions_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.welfare_contributions_seq OWNER TO postgres;

--
-- Name: welfare_contributions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.welfare_contributions (
    id integer DEFAULT nextval('public.welfare_contributions_seq'::regclass) NOT NULL,
    split_txn_id integer NOT NULL,
    welfare_contrib_schedule_id integer NOT NULL,
    contrib_amount double precision NOT NULL
);


ALTER TABLE public.welfare_contributions OWNER TO postgres;

--
-- Data for Name: campaign; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.campaign (id, start_date, end_date, status_id, target_amount, campaign_name, campaign_description, notes) FROM stdin;
\.


--
-- Data for Name: campaign_contributions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.campaign_contributions (id, split_txn_id, campaign_id, contrib_amount) FROM stdin;
\.


--
-- Data for Name: campaign_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.campaign_status (id, status_name, status_description) FROM stdin;
\.


--
-- Data for Name: credit_transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.credit_transaction (id, holding_acc_id, txn_mode_id, transacting_member_id, reference_no, amount, txn_ts, remarks) FROM stdin;
\.


--
-- Data for Name: credit_transaction_split; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.credit_transaction_split (id, credit_txn_id, member_id, txn_amount, remarks) FROM stdin;
\.


--
-- Data for Name: debit_transaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.debit_transaction (id, holding_acc_id, txn_mode_id, campaign_id, fund_account_id, reference_no, amount, authorized, authorized_ts, txn_ts) FROM stdin;
\.


--
-- Data for Name: debit_txn_authorization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.debit_txn_authorization (id, debit_txn_id, holding_acc_signatory_id, authorization_ts, authorizes) FROM stdin;
\.


--
-- Data for Name: debit_txn_cost; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.debit_txn_cost (id, debit_txn_id, cost_name, cost_amount, cost_description) FROM stdin;
\.


--
-- Data for Name: fund; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fund (id, fund_name, fund_description, fund_balance, balance_last_update_ts) FROM stdin;
\.


--
-- Data for Name: fund_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fund_account (id, holding_acc_id, fund_id, fund_balance) FROM stdin;
\.


--
-- Data for Name: fund_contributions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fund_contributions (id, fund_id, split_txn_id, welfare_contribution_id, contrib_amount, fund_running_balance) FROM stdin;
\.


--
-- Data for Name: holding_account_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.holding_account_type (id, type_name, description) FROM stdin;
\.


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.member (id, class_id, first_name, middle_name, surname, email) FROM stdin;
\.


--
-- Data for Name: membership_class; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.membership_class (id, class_name, monthly_contribution_amount) FROM stdin;
\.


--
-- Data for Name: nyikes_holding_acc_signatory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.nyikes_holding_acc_signatory (id, holding_acc_id, member_id) FROM stdin;
\.


--
-- Data for Name: nyikes_holding_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.nyikes_holding_account (id, account_type_id, account_number, account_name, account_balance, notes) FROM stdin;
\.


--
-- Data for Name: transaction_mode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transaction_mode (id, name, description) FROM stdin;
\.


--
-- Data for Name: welfare_contrib_alloc_reference; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.welfare_contrib_alloc_reference (id, fund_id, percent_to_allocate) FROM stdin;
\.


--
-- Data for Name: welfare_contrib_schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.welfare_contrib_schedule (id, contrib_month, contrib_year) FROM stdin;
\.


--
-- Data for Name: welfare_contributions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.welfare_contributions (id, split_txn_id, welfare_contrib_schedule_id, contrib_amount) FROM stdin;
\.


--
-- Name: campaign_contributions_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.campaign_contributions_seq', 1, false);


--
-- Name: campaign_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.campaign_seq', 1, false);


--
-- Name: campaign_status_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.campaign_status_seq', 1, false);


--
-- Name: credit_transaction_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.credit_transaction_seq', 1, false);


--
-- Name: credit_transaction_split_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.credit_transaction_split_seq', 1, false);


--
-- Name: debit_transaction_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.debit_transaction_seq', 1, false);


--
-- Name: debit_txn_authorization_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.debit_txn_authorization_seq', 1, false);


--
-- Name: debit_txn_cost_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.debit_txn_cost_seq', 1, false);


--
-- Name: fund_account_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fund_account_seq', 1, false);


--
-- Name: fund_contributions_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fund_contributions_seq', 1, false);


--
-- Name: fund_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fund_seq', 1, false);


--
-- Name: holding_account_type_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.holding_account_type_seq', 1, false);


--
-- Name: member_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.member_seq', 1, false);


--
-- Name: membership_class_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.membership_class_seq', 1, false);


--
-- Name: nyikes_holding_acc_signatory_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nyikes_holding_acc_signatory_seq', 1, false);


--
-- Name: nyikes_holding_account_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nyikes_holding_account_seq', 1, false);


--
-- Name: transaction_mode_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transaction_mode_seq', 1, false);


--
-- Name: welfare_contrib_alloc_reference_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.welfare_contrib_alloc_reference_seq', 1, false);


--
-- Name: welfare_contrib_schedule_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.welfare_contrib_schedule_seq', 1, false);


--
-- Name: welfare_contributions_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.welfare_contributions_seq', 1, false);


--
-- Name: campaign_contributions campaign_contributions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_contributions
    ADD CONSTRAINT campaign_contributions_pkey PRIMARY KEY (id);


--
-- Name: campaign campaign_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT campaign_pkey PRIMARY KEY (id);


--
-- Name: campaign_status campaign_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_status
    ADD CONSTRAINT campaign_status_pkey PRIMARY KEY (id);


--
-- Name: credit_transaction credit_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction
    ADD CONSTRAINT credit_transaction_pkey PRIMARY KEY (id);


--
-- Name: credit_transaction_split credit_transaction_split_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction_split
    ADD CONSTRAINT credit_transaction_split_pkey PRIMARY KEY (id);


--
-- Name: debit_transaction debit_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT debit_transaction_pkey PRIMARY KEY (id);


--
-- Name: debit_txn_authorization debit_txn_authorization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_txn_authorization
    ADD CONSTRAINT debit_txn_authorization_pkey PRIMARY KEY (id);


--
-- Name: debit_txn_cost debit_txn_cost_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_txn_cost
    ADD CONSTRAINT debit_txn_cost_pkey PRIMARY KEY (id);


--
-- Name: fund_account fund_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_account
    ADD CONSTRAINT fund_account_pkey PRIMARY KEY (id);


--
-- Name: fund_contributions fund_contributions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_contributions
    ADD CONSTRAINT fund_contributions_pkey PRIMARY KEY (id);


--
-- Name: fund fund_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund
    ADD CONSTRAINT fund_pkey PRIMARY KEY (id);


--
-- Name: holding_account_type holding_account_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holding_account_type
    ADD CONSTRAINT holding_account_type_pkey PRIMARY KEY (id);


--
-- Name: member member_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_pkey PRIMARY KEY (id);


--
-- Name: membership_class membership_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membership_class
    ADD CONSTRAINT membership_class_pkey PRIMARY KEY (id);


--
-- Name: nyikes_holding_acc_signatory nyikes_holding_acc_signatory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_acc_signatory
    ADD CONSTRAINT nyikes_holding_acc_signatory_pkey PRIMARY KEY (id);


--
-- Name: nyikes_holding_account nyikes_holding_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_account
    ADD CONSTRAINT nyikes_holding_account_pkey PRIMARY KEY (id);


--
-- Name: transaction_mode transaction_mode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_mode
    ADD CONSTRAINT transaction_mode_pkey PRIMARY KEY (id);


--
-- Name: campaign uq_campaign_campaign_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT uq_campaign_campaign_name UNIQUE (campaign_name);


--
-- Name: campaign_status uq_campaignstatus_status; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_status
    ADD CONSTRAINT uq_campaignstatus_status UNIQUE (status_name);


--
-- Name: fund uq_fund_fund_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund
    ADD CONSTRAINT uq_fund_fund_name UNIQUE (fund_name);


--
-- Name: holding_account_type uq_holdingaccounttype_type_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holding_account_type
    ADD CONSTRAINT uq_holdingaccounttype_type_name UNIQUE (type_name);


--
-- Name: membership_class uq_membershipclass_class_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membership_class
    ADD CONSTRAINT uq_membershipclass_class_name UNIQUE (class_name);


--
-- Name: transaction_mode uq_transactionmode_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_mode
    ADD CONSTRAINT uq_transactionmode_name UNIQUE (name);


--
-- Name: welfare_contrib_alloc_reference welfare_contrib_alloc_reference_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contrib_alloc_reference
    ADD CONSTRAINT welfare_contrib_alloc_reference_pkey PRIMARY KEY (id);


--
-- Name: welfare_contrib_schedule welfare_contrib_schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contrib_schedule
    ADD CONSTRAINT welfare_contrib_schedule_pkey PRIMARY KEY (id);


--
-- Name: welfare_contributions welfare_contributions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contributions
    ADD CONSTRAINT welfare_contributions_pkey PRIMARY KEY (id);


--
-- Name: campaign_campaignstatus_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_campaignstatus_id_index ON public.campaign USING btree (status_id);


--
-- Name: campaign_contributions_campaign_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_contributions_campaign_id_index ON public.campaign_contributions USING btree (campaign_id);


--
-- Name: campaign_contributions_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_contributions_id_index ON public.campaign_contributions USING btree (id);


--
-- Name: campaign_contributions_split_txn_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_contributions_split_txn_id_index ON public.campaign_contributions USING btree (split_txn_id);


--
-- Name: campaign_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_id_index ON public.campaign USING btree (id);


--
-- Name: campaign_status_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_status_id_index ON public.campaign_status USING btree (id);


--
-- Name: credit_transaction_holding_acc_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX credit_transaction_holding_acc_id_index ON public.credit_transaction USING btree (holding_acc_id);


--
-- Name: credit_transaction_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX credit_transaction_id_index ON public.credit_transaction USING btree (id);


--
-- Name: credit_transaction_split_credit_txn_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX credit_transaction_split_credit_txn_id_index ON public.credit_transaction_split USING btree (credit_txn_id);


--
-- Name: credit_transaction_split_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX credit_transaction_split_id_index ON public.credit_transaction_split USING btree (id);


--
-- Name: credit_transaction_transacting_member_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX credit_transaction_transacting_member_id_index ON public.credit_transaction USING btree (transacting_member_id);


--
-- Name: credit_transaction_txn_mode_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX credit_transaction_txn_mode_id_index ON public.credit_transaction USING btree (txn_mode_id);


--
-- Name: debit_transaction_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX debit_transaction_id_index ON public.debit_transaction USING btree (id);


--
-- Name: debit_transaction_txn_mode_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX debit_transaction_txn_mode_id_index ON public.debit_transaction USING btree (txn_mode_id);


--
-- Name: debit_txn_authorization_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX debit_txn_authorization_id_index ON public.debit_txn_authorization USING btree (id);


--
-- Name: debit_txn_cost_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX debit_txn_cost_id_index ON public.debit_txn_cost USING btree (id);


--
-- Name: fk_credittransactionsplit_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_credittransactionsplit_member_id ON public.credit_transaction_split USING btree (member_id);


--
-- Name: fk_debittransaction_campaign_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_debittransaction_campaign_id ON public.debit_transaction USING btree (campaign_id);


--
-- Name: fk_debittransaction_fundaccount_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_debittransaction_fundaccount_id ON public.debit_transaction USING btree (fund_account_id);


--
-- Name: fk_debittransaction_nyikesholdingaccount_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_debittransaction_nyikesholdingaccount_id ON public.debit_transaction USING btree (holding_acc_id);


--
-- Name: fk_debittxnauthorization_debittransaction_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_debittxnauthorization_debittransaction_id ON public.debit_txn_authorization USING btree (debit_txn_id);


--
-- Name: fk_debittxnauthorization_nyikesholdingaccsignatory_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_debittxnauthorization_nyikesholdingaccsignatory_id ON public.debit_txn_authorization USING btree (holding_acc_signatory_id);


--
-- Name: fk_debittxncost_debittransaction_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_debittxncost_debittransaction_id ON public.debit_txn_cost USING btree (debit_txn_id);


--
-- Name: fk_fund_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_fund_id ON public.fund_account USING btree (fund_id);


--
-- Name: fk_nyikesholdingaccsignatory_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_nyikesholdingaccsignatory_member_id ON public.nyikes_holding_acc_signatory USING btree (member_id);


--
-- Name: fk_nyikesholdingaccsignatory_nyikesholdingaccount_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_nyikesholdingaccsignatory_nyikesholdingaccount_id ON public.nyikes_holding_acc_signatory USING btree (holding_acc_id);


--
-- Name: fk_welfarecontriballocreference_fund_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fk_welfarecontriballocreference_fund_id ON public.welfare_contrib_alloc_reference USING btree (fund_id);


--
-- Name: fund_account_holding_acc_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_account_holding_acc_id_index ON public.fund_account USING btree (holding_acc_id);


--
-- Name: fund_account_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_account_id_index ON public.fund_account USING btree (id);


--
-- Name: fund_contributions_fund_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_contributions_fund_id_index ON public.fund_contributions USING btree (fund_id);


--
-- Name: fund_contributions_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_contributions_id_index ON public.fund_contributions USING btree (id);


--
-- Name: fund_contributions_split_txn_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_contributions_split_txn_id_index ON public.fund_contributions USING btree (split_txn_id);


--
-- Name: fund_contributions_welfare_contribution_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_contributions_welfare_contribution_id_index ON public.fund_contributions USING btree (welfare_contribution_id);


--
-- Name: fund_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_id_index ON public.fund USING btree (id);


--
-- Name: holding_account_type_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX holding_account_type_id_index ON public.holding_account_type USING btree (id);


--
-- Name: member_class_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX member_class_id_index ON public.member USING btree (class_id);


--
-- Name: member_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX member_id_index ON public.member USING btree (id);


--
-- Name: membership_class_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX membership_class_id_index ON public.membership_class USING btree (id);


--
-- Name: nyikes_holding_acc_signatory_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX nyikes_holding_acc_signatory_id_index ON public.nyikes_holding_acc_signatory USING btree (id);


--
-- Name: nyikes_holding_account_account_type_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX nyikes_holding_account_account_type_id_index ON public.nyikes_holding_account USING btree (account_type_id);


--
-- Name: nyikes_holding_account_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX nyikes_holding_account_id_index ON public.nyikes_holding_account USING btree (id);


--
-- Name: transaction_mode_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transaction_mode_id_index ON public.transaction_mode USING btree (id);


--
-- Name: welfare_contrib_alloc_reference_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX welfare_contrib_alloc_reference_id_index ON public.welfare_contrib_alloc_reference USING btree (id);


--
-- Name: welfare_contrib_schedule_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX welfare_contrib_schedule_id_index ON public.welfare_contrib_schedule USING btree (id);


--
-- Name: welfare_contributions_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX welfare_contributions_id_index ON public.welfare_contributions USING btree (id);


--
-- Name: welfare_contributions_split_txn_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX welfare_contributions_split_txn_id_index ON public.welfare_contributions USING btree (split_txn_id);


--
-- Name: welfare_contributions_welfare_contrib_schedule_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX welfare_contributions_welfare_contrib_schedule_id_index ON public.welfare_contributions USING btree (welfare_contrib_schedule_id);


--
-- Name: campaign_contributions fk_campaigncontribution_campaign_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_contributions
    ADD CONSTRAINT fk_campaigncontribution_campaign_id FOREIGN KEY (campaign_id) REFERENCES public.campaign(id);


--
-- Name: campaign_contributions fk_campaigncontribution_credittransactionsplit_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_contributions
    ADD CONSTRAINT fk_campaigncontribution_credittransactionsplit_id FOREIGN KEY (split_txn_id) REFERENCES public.credit_transaction_split(id);


--
-- Name: campaign fk_campaignstatus_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT fk_campaignstatus_id FOREIGN KEY (status_id) REFERENCES public.campaign_status(id);


--
-- Name: credit_transaction fk_creditransaction_nyikesholdingaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction
    ADD CONSTRAINT fk_creditransaction_nyikesholdingaccount_id FOREIGN KEY (holding_acc_id) REFERENCES public.nyikes_holding_account(id);


--
-- Name: credit_transaction fk_credittransaction_member_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction
    ADD CONSTRAINT fk_credittransaction_member_id FOREIGN KEY (transacting_member_id) REFERENCES public.member(id);


--
-- Name: credit_transaction fk_credittransaction_transactionmode_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction
    ADD CONSTRAINT fk_credittransaction_transactionmode_id FOREIGN KEY (txn_mode_id) REFERENCES public.transaction_mode(id);


--
-- Name: credit_transaction_split fk_credittransactionsplit_credittransaction_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction_split
    ADD CONSTRAINT fk_credittransactionsplit_credittransaction_id FOREIGN KEY (credit_txn_id) REFERENCES public.credit_transaction(id);


--
-- Name: fund_contributions fk_credittransactionsplit_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_contributions
    ADD CONSTRAINT fk_credittransactionsplit_id FOREIGN KEY (split_txn_id) REFERENCES public.credit_transaction_split(id);


--
-- Name: credit_transaction_split fk_credittransactionsplit_member_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction_split
    ADD CONSTRAINT fk_credittransactionsplit_member_id FOREIGN KEY (member_id) REFERENCES public.member(id);


--
-- Name: debit_transaction fk_debittransaction_campaign_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT fk_debittransaction_campaign_id FOREIGN KEY (campaign_id) REFERENCES public.campaign(id);


--
-- Name: debit_transaction fk_debittransaction_fundaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT fk_debittransaction_fundaccount_id FOREIGN KEY (fund_account_id) REFERENCES public.fund_account(id);


--
-- Name: debit_transaction fk_debittransaction_nyikesholdingaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT fk_debittransaction_nyikesholdingaccount_id FOREIGN KEY (holding_acc_id) REFERENCES public.nyikes_holding_account(id);


--
-- Name: debit_transaction fk_debittransaction_transactionmode_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT fk_debittransaction_transactionmode_id FOREIGN KEY (txn_mode_id) REFERENCES public.transaction_mode(id);


--
-- Name: debit_txn_authorization fk_debittxnauthorization_debittransaction_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_txn_authorization
    ADD CONSTRAINT fk_debittxnauthorization_debittransaction_id FOREIGN KEY (debit_txn_id) REFERENCES public.debit_transaction(id);


--
-- Name: debit_txn_authorization fk_debittxnauthorization_nyikesholdingaccsignatory_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_txn_authorization
    ADD CONSTRAINT fk_debittxnauthorization_nyikesholdingaccsignatory_id FOREIGN KEY (holding_acc_signatory_id) REFERENCES public.nyikes_holding_acc_signatory(id);


--
-- Name: debit_txn_cost fk_debittxncost_debittransaction_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_txn_cost
    ADD CONSTRAINT fk_debittxncost_debittransaction_id FOREIGN KEY (debit_txn_id) REFERENCES public.debit_transaction(id);


--
-- Name: fund_account fk_fund_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_account
    ADD CONSTRAINT fk_fund_id FOREIGN KEY (fund_id) REFERENCES public.fund(id);


--
-- Name: fund_contributions fk_fundcontributions_fund_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_contributions
    ADD CONSTRAINT fk_fundcontributions_fund_id FOREIGN KEY (fund_id) REFERENCES public.fund(id);


--
-- Name: fund_contributions fk_fundcontributions_welfarecontributions_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_contributions
    ADD CONSTRAINT fk_fundcontributions_welfarecontributions_id FOREIGN KEY (welfare_contribution_id) REFERENCES public.welfare_contributions(id);


--
-- Name: nyikes_holding_account fk_holdingaccounttype_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_account
    ADD CONSTRAINT fk_holdingaccounttype_id FOREIGN KEY (account_type_id) REFERENCES public.holding_account_type(id);


--
-- Name: member fk_membershipclass_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT fk_membershipclass_id FOREIGN KEY (class_id) REFERENCES public.membership_class(id);


--
-- Name: fund_account fk_nyikesholdingaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_account
    ADD CONSTRAINT fk_nyikesholdingaccount_id FOREIGN KEY (holding_acc_id) REFERENCES public.nyikes_holding_account(id);


--
-- Name: nyikes_holding_acc_signatory fk_nyikesholdingaccsignatory_member_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_acc_signatory
    ADD CONSTRAINT fk_nyikesholdingaccsignatory_member_id FOREIGN KEY (member_id) REFERENCES public.member(id);


--
-- Name: nyikes_holding_acc_signatory fk_nyikesholdingaccsignatory_nyikesholdingaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_acc_signatory
    ADD CONSTRAINT fk_nyikesholdingaccsignatory_nyikesholdingaccount_id FOREIGN KEY (holding_acc_id) REFERENCES public.nyikes_holding_account(id);


--
-- Name: welfare_contrib_alloc_reference fk_welfarecontriballocreference_fund_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contrib_alloc_reference
    ADD CONSTRAINT fk_welfarecontriballocreference_fund_id FOREIGN KEY (fund_id) REFERENCES public.fund(id);


--
-- Name: welfare_contributions fk_welfarecontributions_credittransactionsplit_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contributions
    ADD CONSTRAINT fk_welfarecontributions_credittransactionsplit_id FOREIGN KEY (split_txn_id) REFERENCES public.credit_transaction_split(id);


--
-- Name: welfare_contributions fk_welfarecontributions_welfarecontrib_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contributions
    ADD CONSTRAINT fk_welfarecontributions_welfarecontrib_id FOREIGN KEY (welfare_contrib_schedule_id) REFERENCES public.welfare_contrib_schedule(id);


--
-- PostgreSQL database dump complete
--

