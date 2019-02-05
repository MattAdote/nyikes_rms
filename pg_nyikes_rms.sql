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
-- Name: campaign_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.campaign_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: campaign; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campaign (
    id integer DEFAULT nextval('public.campaign_id_seq'::regclass) NOT NULL,
    start_date date,
    end_date date,
    status_id integer NOT NULL,
    target_amount double precision NOT NULL,
    campaign_name character(1) NOT NULL,
    campaign_description character(1),
    notes character(1)
);


ALTER TABLE public.campaign OWNER TO postgres;

--
-- Name: campaign_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.campaign_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_status_id_seq OWNER TO postgres;

--
-- Name: campaign_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.campaign_status (
    id integer DEFAULT nextval('public.campaign_status_id_seq'::regclass) NOT NULL,
    status_name character(1) NOT NULL,
    status_description character(1) NOT NULL
);


ALTER TABLE public.campaign_status OWNER TO postgres;

--
-- Name: credit_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.credit_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.credit_transaction_id_seq OWNER TO postgres;

--
-- Name: credit_transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.credit_transaction (
    id integer DEFAULT nextval('public.credit_transaction_id_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    txn_mode_id integer NOT NULL,
    transacting_member_id integer NOT NULL,
    reference_no character(1),
    amount double precision NOT NULL,
    txn_ts timestamp without time zone NOT NULL
);


ALTER TABLE public.credit_transaction OWNER TO postgres;

--
-- Name: debit_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.debit_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.debit_transaction_id_seq OWNER TO postgres;

--
-- Name: debit_transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.debit_transaction (
    id integer DEFAULT nextval('public.debit_transaction_id_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    txn_mode_id integer NOT NULL,
    campaign_id integer,
    fund_id integer,
    reference_no character(1),
    amount double precision NOT NULL,
    authorized boolean NOT NULL,
    authorized_ts timestamp without time zone,
    txn_ts timestamp without time zone NOT NULL
);


ALTER TABLE public.debit_transaction OWNER TO postgres;

--
-- Name: debit_txn_authorization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.debit_txn_authorization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.debit_txn_authorization_id_seq OWNER TO postgres;

--
-- Name: debit_txn_authorization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.debit_txn_authorization (
    id integer DEFAULT nextval('public.debit_txn_authorization_id_seq'::regclass) NOT NULL,
    debit_txn_id integer NOT NULL,
    holding_acc_signatory_id integer NOT NULL,
    authorization_ts timestamp without time zone NOT NULL,
    authorizes boolean NOT NULL
);


ALTER TABLE public.debit_txn_authorization OWNER TO postgres;

--
-- Name: debit_txn_cost_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.debit_txn_cost_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.debit_txn_cost_id_seq OWNER TO postgres;

--
-- Name: debit_txn_cost; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.debit_txn_cost (
    id integer DEFAULT nextval('public.debit_txn_cost_id_seq'::regclass) NOT NULL,
    debit_txn_id integer NOT NULL,
    cost_name character(1) NOT NULL,
    cost_amount double precision NOT NULL,
    cost_description character(1)
);


ALTER TABLE public.debit_txn_cost OWNER TO postgres;

--
-- Name: fund_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fund_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fund_id_seq OWNER TO postgres;

--
-- Name: fund; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fund (
    id integer DEFAULT nextval('public.fund_id_seq'::regclass) NOT NULL,
    fund_name character(1) NOT NULL,
    fund_description character(1),
    fund_balance double precision NOT NULL,
    balance_last_update_ts timestamp without time zone NOT NULL
);


ALTER TABLE public.fund OWNER TO postgres;

--
-- Name: fund_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fund_account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fund_account_id_seq OWNER TO postgres;

--
-- Name: fund_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fund_account (
    id integer DEFAULT nextval('public.fund_account_id_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    fund_id integer NOT NULL,
    fund_balance double precision NOT NULL
);


ALTER TABLE public.fund_account OWNER TO postgres;

--
-- Name: fund_contrib_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fund_contrib_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fund_contrib_id_seq OWNER TO postgres;

--
-- Name: fund_contrib; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fund_contrib (
    id integer DEFAULT nextval('public.fund_contrib_id_seq'::regclass) NOT NULL,
    welfare_contrib_id integer NOT NULL,
    fund_id integer NOT NULL,
    contrib_amount double precision NOT NULL,
    fund_running_balance double precision NOT NULL
);


ALTER TABLE public.fund_contrib OWNER TO postgres;

--
-- Name: holding_account_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.holding_account_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.holding_account_type_id_seq OWNER TO postgres;

--
-- Name: holding_account_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.holding_account_type (
    id integer DEFAULT nextval('public.holding_account_type_id_seq'::regclass) NOT NULL,
    type_name character(1) NOT NULL,
    description character(1)
);


ALTER TABLE public.holding_account_type OWNER TO postgres;

--
-- Name: member_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.member_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.member_id_seq OWNER TO postgres;

--
-- Name: member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member (
    id integer DEFAULT nextval('public.member_id_seq'::regclass) NOT NULL,
    class_id integer NOT NULL,
    first_name character(1) NOT NULL,
    middle_name character(1) NOT NULL,
    surname character(1) NOT NULL,
    email character(1)
);


ALTER TABLE public.member OWNER TO postgres;

--
-- Name: member_credit_txn_campaign_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.member_credit_txn_campaign_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.member_credit_txn_campaign_id_seq OWNER TO postgres;

--
-- Name: member_credit_txn_campaign; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member_credit_txn_campaign (
    id integer DEFAULT nextval('public.member_credit_txn_campaign_id_seq'::regclass) NOT NULL,
    member_id integer NOT NULL,
    credit_txn_id integer NOT NULL,
    campaign_id integer NOT NULL,
    txn_amount double precision NOT NULL
);


ALTER TABLE public.member_credit_txn_campaign OWNER TO postgres;

--
-- Name: member_credit_txn_welfare_contrib_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.member_credit_txn_welfare_contrib_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.member_credit_txn_welfare_contrib_id_seq OWNER TO postgres;

--
-- Name: member_credit_txn_welfare_contrib; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member_credit_txn_welfare_contrib (
    id integer DEFAULT nextval('public.member_credit_txn_welfare_contrib_id_seq'::regclass) NOT NULL,
    member_id integer NOT NULL,
    credit_txn_id integer NOT NULL,
    welfare_contrib_id integer NOT NULL,
    txn_amount double precision NOT NULL
);


ALTER TABLE public.member_credit_txn_welfare_contrib OWNER TO postgres;

--
-- Name: membership_class_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.membership_class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.membership_class_id_seq OWNER TO postgres;

--
-- Name: membership_class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.membership_class (
    id integer DEFAULT nextval('public.membership_class_id_seq'::regclass) NOT NULL,
    class_name character(1) NOT NULL,
    monthly_contribution_amount double precision NOT NULL
);


ALTER TABLE public.membership_class OWNER TO postgres;

--
-- Name: nyikes_holding_acc_signatory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.nyikes_holding_acc_signatory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nyikes_holding_acc_signatory_id_seq OWNER TO postgres;

--
-- Name: nyikes_holding_acc_signatory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nyikes_holding_acc_signatory (
    id integer DEFAULT nextval('public.nyikes_holding_acc_signatory_id_seq'::regclass) NOT NULL,
    holding_acc_id integer NOT NULL,
    member_id integer NOT NULL
);


ALTER TABLE public.nyikes_holding_acc_signatory OWNER TO postgres;

--
-- Name: nyikes_holding_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.nyikes_holding_account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nyikes_holding_account_id_seq OWNER TO postgres;

--
-- Name: nyikes_holding_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nyikes_holding_account (
    id integer DEFAULT nextval('public.nyikes_holding_account_id_seq'::regclass) NOT NULL,
    account_type_id integer NOT NULL,
    account_number character(1) NOT NULL,
    account_name character(1) NOT NULL,
    account_balance double precision NOT NULL,
    notes character(1) NOT NULL
);


ALTER TABLE public.nyikes_holding_account OWNER TO postgres;

--
-- Name: transaction_mode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_mode_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_mode_id_seq OWNER TO postgres;

--
-- Name: transaction_mode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction_mode (
    id integer DEFAULT nextval('public.transaction_mode_id_seq'::regclass) NOT NULL,
    name character(1) NOT NULL,
    description character(1)
);


ALTER TABLE public.transaction_mode OWNER TO postgres;

--
-- Name: welfare_contrib_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.welfare_contrib_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.welfare_contrib_id_seq OWNER TO postgres;

--
-- Name: welfare_contrib; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.welfare_contrib (
    id integer DEFAULT nextval('public.welfare_contrib_id_seq'::regclass) NOT NULL,
    contrib_month character(1) NOT NULL,
    contrib_year integer NOT NULL
);


ALTER TABLE public.welfare_contrib OWNER TO postgres;

--
-- Name: welfare_contrib_alloc_reference_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.welfare_contrib_alloc_reference_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.welfare_contrib_alloc_reference_id_seq OWNER TO postgres;

--
-- Name: welfare_contrib_alloc_reference; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.welfare_contrib_alloc_reference (
    id integer DEFAULT nextval('public.welfare_contrib_alloc_reference_id_seq'::regclass) NOT NULL,
    fund_id integer NOT NULL,
    percent_to_allocate double precision NOT NULL
);


ALTER TABLE public.welfare_contrib_alloc_reference OWNER TO postgres;

--
-- Name: campaign pk_campaign_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT pk_campaign_id PRIMARY KEY (id);


--
-- Name: campaign_status pk_campaignstatus_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.campaign_status
    ADD CONSTRAINT pk_campaignstatus_id PRIMARY KEY (id);


--
-- Name: credit_transaction pk_credittransaction_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction
    ADD CONSTRAINT pk_credittransaction_id PRIMARY KEY (id);


--
-- Name: debit_transaction pk_debittransaction_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT pk_debittransaction_id PRIMARY KEY (id);


--
-- Name: debit_txn_authorization pk_debittxnauthorization_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_txn_authorization
    ADD CONSTRAINT pk_debittxnauthorization_id PRIMARY KEY (id);


--
-- Name: debit_txn_cost pk_debittxncost_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_txn_cost
    ADD CONSTRAINT pk_debittxncost_id PRIMARY KEY (id);


--
-- Name: fund pk_fund_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund
    ADD CONSTRAINT pk_fund_id PRIMARY KEY (id);


--
-- Name: fund_account pk_fundaccount_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_account
    ADD CONSTRAINT pk_fundaccount_id PRIMARY KEY (id);


--
-- Name: fund_contrib pk_fundcontrib_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_contrib
    ADD CONSTRAINT pk_fundcontrib_id PRIMARY KEY (id);


--
-- Name: holding_account_type pk_holdingaccounttype_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holding_account_type
    ADD CONSTRAINT pk_holdingaccounttype_id PRIMARY KEY (id);


--
-- Name: member pk_member_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT pk_member_id PRIMARY KEY (id);


--
-- Name: member_credit_txn_campaign pk_membercredittxncampaign_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_campaign
    ADD CONSTRAINT pk_membercredittxncampaign_id PRIMARY KEY (id);


--
-- Name: member_credit_txn_welfare_contrib pk_membercredittxnwelfarecontrib_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_welfare_contrib
    ADD CONSTRAINT pk_membercredittxnwelfarecontrib_id PRIMARY KEY (id);


--
-- Name: membership_class pk_membershipclass_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membership_class
    ADD CONSTRAINT pk_membershipclass_id PRIMARY KEY (id);


--
-- Name: nyikes_holding_account pk_nyikesholdingaccount_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_account
    ADD CONSTRAINT pk_nyikesholdingaccount_id PRIMARY KEY (id);


--
-- Name: nyikes_holding_acc_signatory pk_nyikesholdingaccsignatory_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_acc_signatory
    ADD CONSTRAINT pk_nyikesholdingaccsignatory_id PRIMARY KEY (id);


--
-- Name: transaction_mode pk_transactionmode_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_mode
    ADD CONSTRAINT pk_transactionmode_id PRIMARY KEY (id);


--
-- Name: welfare_contrib pk_welfarecontrib_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contrib
    ADD CONSTRAINT pk_welfarecontrib_id PRIMARY KEY (id);


--
-- Name: welfare_contrib_alloc_reference pk_welfarecontriballocreference_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.welfare_contrib_alloc_reference
    ADD CONSTRAINT pk_welfarecontriballocreference_id PRIMARY KEY (id);


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
-- Name: campaign_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_id_index ON public.campaign USING btree (id);


--
-- Name: campaign_status_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX campaign_status_id_index ON public.campaign_status USING btree (id);


--
-- Name: credit_transaction_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX credit_transaction_id_index ON public.credit_transaction USING btree (id);


--
-- Name: debit_transaction_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX debit_transaction_id_index ON public.debit_transaction USING btree (id);


--
-- Name: debit_txn_authorization_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX debit_txn_authorization_id_index ON public.debit_txn_authorization USING btree (id);


--
-- Name: debit_txn_cost_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX debit_txn_cost_id_index ON public.debit_txn_cost USING btree (id);


--
-- Name: fund_account_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_account_id_index ON public.fund_account USING btree (id);


--
-- Name: fund_contrib_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_contrib_id_index ON public.fund_contrib USING btree (id);


--
-- Name: fund_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fund_id_index ON public.fund USING btree (id);


--
-- Name: holding_account_type_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX holding_account_type_id_index ON public.holding_account_type USING btree (id);


--
-- Name: member_credit_txn_campaign_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX member_credit_txn_campaign_id_index ON public.member_credit_txn_campaign USING btree (id);


--
-- Name: member_credit_txn_welfare_contrib_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX member_credit_txn_welfare_contrib_id_index ON public.member_credit_txn_welfare_contrib USING btree (id);


--
-- Name: nyikes_holding_acc_signatory_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX nyikes_holding_acc_signatory_id_index ON public.nyikes_holding_acc_signatory USING btree (id);


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
-- Name: welfare_contrib_id_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX welfare_contrib_id_index ON public.welfare_contrib USING btree (id);


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
-- Name: credit_transaction fk_credittransaction_transactionmode_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_transaction
    ADD CONSTRAINT fk_credittransaction_transactionmode_id FOREIGN KEY (txn_mode_id) REFERENCES public.transaction_mode(id);


--
-- Name: debit_transaction fk_debittransaction_campaign_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT fk_debittransaction_campaign_id FOREIGN KEY (campaign_id) REFERENCES public.campaign(id);


--
-- Name: debit_transaction fk_debittransaction_fund_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.debit_transaction
    ADD CONSTRAINT fk_debittransaction_fund_id FOREIGN KEY (fund_id) REFERENCES public.fund(id);


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
-- Name: fund_contrib fk_fundcontrib_welfarecontriballocreference_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fund_contrib
    ADD CONSTRAINT fk_fundcontrib_welfarecontriballocreference_id FOREIGN KEY (welfare_contrib_id) REFERENCES public.welfare_contrib_alloc_reference(id);


--
-- Name: nyikes_holding_account fk_holdingaccounttype_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nyikes_holding_account
    ADD CONSTRAINT fk_holdingaccounttype_id FOREIGN KEY (account_type_id) REFERENCES public.holding_account_type(id);


--
-- Name: member_credit_txn_campaign fk_membercredittxncampaign_campaign_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_campaign
    ADD CONSTRAINT fk_membercredittxncampaign_campaign_id FOREIGN KEY (campaign_id) REFERENCES public.campaign(id);


--
-- Name: member_credit_txn_campaign fk_membercredittxncampaign_credittransaction_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_campaign
    ADD CONSTRAINT fk_membercredittxncampaign_credittransaction_id FOREIGN KEY (credit_txn_id) REFERENCES public.credit_transaction(id);


--
-- Name: member_credit_txn_campaign fk_membercredittxncampaign_member_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_campaign
    ADD CONSTRAINT fk_membercredittxncampaign_member_id FOREIGN KEY (member_id) REFERENCES public.member(id);


--
-- Name: member_credit_txn_welfare_contrib fk_membercredittxnwelfarecontrib_credittransaction_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_welfare_contrib
    ADD CONSTRAINT fk_membercredittxnwelfarecontrib_credittransaction_id FOREIGN KEY (credit_txn_id) REFERENCES public.credit_transaction(id);


--
-- Name: member_credit_txn_welfare_contrib fk_membercredittxnwelfarecontrib_member_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_welfare_contrib
    ADD CONSTRAINT fk_membercredittxnwelfarecontrib_member_id FOREIGN KEY (member_id) REFERENCES public.member(id);


--
-- Name: member_credit_txn_welfare_contrib fk_membercredittxnwelfarecontrib_welfarecontrib_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member_credit_txn_welfare_contrib
    ADD CONSTRAINT fk_membercredittxnwelfarecontrib_welfarecontrib_id FOREIGN KEY (welfare_contrib_id) REFERENCES public.welfare_contrib(id);


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
-- PostgreSQL database dump complete
--

