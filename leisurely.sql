--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'LATIN1';
SET standard_conforming_strings = on;
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


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE activities (
    act_id integer NOT NULL,
    cat_id integer NOT NULL,
    eb_cat_id integer NOT NULL,
    name character varying(80) NOT NULL,
    act_type character varying(80),
    eb_format_id integer NOT NULL,
    sub_cat character varying(80),
    mu_id integer NOT NULL
);


ALTER TABLE activities OWNER TO vagrant;

--
-- Name: activities_act_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE activities_act_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE activities_act_id_seq OWNER TO vagrant;

--
-- Name: activities_act_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE activities_act_id_seq OWNED BY activities.act_id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE categories (
    cat_id integer NOT NULL,
    name character varying(80) NOT NULL,
    screenname character varying(80) NOT NULL
);


ALTER TABLE categories OWNER TO vagrant;

--
-- Name: categories_cat_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE categories_cat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE categories_cat_id_seq OWNER TO vagrant;

--
-- Name: categories_cat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE categories_cat_id_seq OWNED BY categories.cat_id;


--
-- Name: saved_events; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE saved_events (
    saved_id integer NOT NULL,
    user_id integer,
    event_id bigint NOT NULL,
    event_name character varying(200) NOT NULL,
    event_url character varying(200) NOT NULL
);


ALTER TABLE saved_events OWNER TO vagrant;

--
-- Name: saved_events_saved_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE saved_events_saved_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE saved_events_saved_id_seq OWNER TO vagrant;

--
-- Name: saved_events_saved_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE saved_events_saved_id_seq OWNED BY saved_events.saved_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    user_id integer NOT NULL,
    email character varying(80) NOT NULL,
    password character varying(80) NOT NULL
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: weekday_categories; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE weekday_categories (
    weekday_category_id integer NOT NULL,
    cat_id integer NOT NULL,
    weekday_id integer NOT NULL
);


ALTER TABLE weekday_categories OWNER TO vagrant;

--
-- Name: weekday_categories_weekday_category_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE weekday_categories_weekday_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE weekday_categories_weekday_category_id_seq OWNER TO vagrant;

--
-- Name: weekday_categories_weekday_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE weekday_categories_weekday_category_id_seq OWNED BY weekday_categories.weekday_category_id;


--
-- Name: weekdays; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE weekdays (
    weekday_id integer NOT NULL,
    name character varying(80)
);


ALTER TABLE weekdays OWNER TO vagrant;

--
-- Name: weekdays_weekday_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE weekdays_weekday_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE weekdays_weekday_id_seq OWNER TO vagrant;

--
-- Name: weekdays_weekday_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE weekdays_weekday_id_seq OWNED BY weekdays.weekday_id;


--
-- Name: act_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY activities ALTER COLUMN act_id SET DEFAULT nextval('activities_act_id_seq'::regclass);


--
-- Name: cat_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY categories ALTER COLUMN cat_id SET DEFAULT nextval('categories_cat_id_seq'::regclass);


--
-- Name: saved_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY saved_events ALTER COLUMN saved_id SET DEFAULT nextval('saved_events_saved_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: weekday_category_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY weekday_categories ALTER COLUMN weekday_category_id SET DEFAULT nextval('weekday_categories_weekday_category_id_seq'::regclass);


--
-- Name: weekday_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY weekdays ALTER COLUMN weekday_id SET DEFAULT nextval('weekdays_weekday_id_seq'::regclass);


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY activities (act_id, cat_id, eb_cat_id, name, act_type, eb_format_id, sub_cat, mu_id) FROM stdin;
1	1	103	Festivals	Festival	5	0	0
2	1	103	Concerts	Performance	6	0	0
3	1	103	Meetups	Music	0	0	21
4	1	103	Dance Parties	Party	11	0	0
5	1	103	Classes	Class	9	0	0
6	2	101	Networking	Networking	10	0	0
7	2	101	Seminars	Seminar	2	0	0
8	2	101	Meetups	Career & Business	0	0	2
9	2	101	Conferences	Conference	1	0	0
10	2	101	Classes	Class	9	0	0
11	3	110	Classes	Class	9	0	0
12	3	110	Festivals	Festival	5	0	0
13	3	110	Meetups	Food & Drink	0	0	10
14	3	110	Beer	NULL	0	10001	0
15	3	110	Wine	NULL	0	10002	0
16	4	105	Performance	Performance	6	0	0
17	4	105	Classes	Class	9	0	0
18	4	105	Meetups	Arts & Culture	0	0	1
19	4	105	Festivals	Festival	5	0	0
20	4	105	Seminars	Seminar	2	0	0
21	5	108	Classes	Class	9	0	0
22	5	108	Running	Race	15	0	0
23	5	108	Meetups	Sports & Recreation	0	0	32
24	5	108	Games & Matches	Game	14	0	0
25	5	108	Special Events	Party	11	0	0
26	6	102	Classes	Class	9	0	0
27	6	102	Conferences	Conference	1	0	0
28	6	102	Meetups	Tech	0	0	34
29	6	102	Networking	Networking	10	0	0
30	6	102	Seminars	Seminar	2	0	0
31	7	109	Hiking	NULL	0	9001	0
32	7	109	Tours	Tour	16	0	0
33	7	109	Meetups	Outdoors & Adventure	0	0	23
34	7	109	Classes	Class	9	0	0
35	7	109	Retreats	Retreat	18	0	0
36	8	111	Education	NULL	0	11008	0
37	8	111	The Environment	NULL	0	11002	0
38	8	111	Poverty Alleviation	NULL	0	11006	0
39	8	111	Animal Welfare	NULL	0	11001	0
40	8	111	Human Rights	NULL	0	11004	0
\.


--
-- Name: activities_act_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('activities_act_id_seq', 1, false);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY categories (cat_id, name, screenname) FROM stdin;
1	Music	Jamming Out
2	Business & Professional	Getting Ahead
3	Food & Drink	Grubbing
4	Performing & Visual Arts	Being Artsy
5	Sports & Fitness	Getting Swoll
6	Science & Technology	Nerding Out
7	Travel & Outdoors	Being Outdoorsy
8	Charity & Causes	Getting Involved
\.


--
-- Name: categories_cat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('categories_cat_id_seq', 1, false);


--
-- Data for Name: saved_events; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY saved_events (saved_id, user_id, event_id, event_name, event_url) FROM stdin;
2	1	25181536654	Euphoria Music & Camping Festival 2017	https://www.eventbrite.com/e/euphoria-music-camping-festival-2017-tickets-25181536654?aff=ebapi
\.


--
-- Name: saved_events_saved_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('saved_events_saved_id_seq', 6, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (user_id, email, password) FROM stdin;
1	test@gmail.com	$2b$12$cK.F.I6ZSZNhlsbsPMdpC.Yuxp0QV/Vii5SqRiLQzO3EhmzEJKyaO
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('users_user_id_seq', 1, true);


--
-- Data for Name: weekday_categories; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY weekday_categories (weekday_category_id, cat_id, weekday_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	1	5
6	1	6
7	1	7
8	2	1
9	2	2
10	2	3
11	2	4
12	3	1
13	3	2
14	3	3
15	3	4
16	3	5
17	3	6
18	3	7
19	4	5
20	4	6
21	4	7
22	5	1
23	5	2
24	5	3
25	5	4
26	5	5
27	5	6
28	5	7
29	6	1
30	6	2
31	6	3
32	6	4
33	7	5
34	7	6
35	7	7
36	8	5
37	8	6
38	8	7
\.


--
-- Name: weekday_categories_weekday_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('weekday_categories_weekday_category_id_seq', 1, false);


--
-- Data for Name: weekdays; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY weekdays (weekday_id, name) FROM stdin;
1	Monday
2	Tuesday
3	Wednesday
4	Thursday
5	Friday
6	Saturday
7	Sunday
\.


--
-- Name: weekdays_weekday_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('weekdays_weekday_id_seq', 1, false);


--
-- Name: activities_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (act_id);


--
-- Name: categories_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (cat_id);


--
-- Name: saved_events_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY saved_events
    ADD CONSTRAINT saved_events_pkey PRIMARY KEY (saved_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: weekday_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY weekday_categories
    ADD CONSTRAINT weekday_categories_pkey PRIMARY KEY (weekday_category_id);


--
-- Name: weekdays_name_key; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY weekdays
    ADD CONSTRAINT weekdays_name_key UNIQUE (name);


--
-- Name: weekdays_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY weekdays
    ADD CONSTRAINT weekdays_pkey PRIMARY KEY (weekday_id);


--
-- Name: activities_cat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY activities
    ADD CONSTRAINT activities_cat_id_fkey FOREIGN KEY (cat_id) REFERENCES categories(cat_id);


--
-- Name: saved_events_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY saved_events
    ADD CONSTRAINT saved_events_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: weekday_categories_cat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY weekday_categories
    ADD CONSTRAINT weekday_categories_cat_id_fkey FOREIGN KEY (cat_id) REFERENCES categories(cat_id);


--
-- Name: weekday_categories_weekday_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY weekday_categories
    ADD CONSTRAINT weekday_categories_weekday_id_fkey FOREIGN KEY (weekday_id) REFERENCES weekdays(weekday_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

