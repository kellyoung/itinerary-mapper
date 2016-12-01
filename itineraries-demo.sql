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
-- Name: categories; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE categories (
    cat_id character varying(16) NOT NULL
);


ALTER TABLE categories OWNER TO vagrant;

--
-- Name: places; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE places (
    place_id integer NOT NULL,
    place_name character varying(256) NOT NULL,
    place_loc character varying(256) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    day_num integer NOT NULL,
    date date NOT NULL,
    trip_id integer NOT NULL,
    cat_id character varying(16) NOT NULL,
    notes text,
    pic_file character varying(256)
);


ALTER TABLE places OWNER TO vagrant;

--
-- Name: places_place_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE places_place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE places_place_id_seq OWNER TO vagrant;

--
-- Name: places_place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE places_place_id_seq OWNED BY places.place_id;


--
-- Name: trips; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE trips (
    trip_id integer NOT NULL,
    trip_name character varying(256) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    general_loc character varying(256),
    latitude double precision,
    longitude double precision,
    viewport text,
    username character varying(64) NOT NULL,
    published boolean NOT NULL
);


ALTER TABLE trips OWNER TO vagrant;

--
-- Name: trips_trip_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE trips_trip_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE trips_trip_id_seq OWNER TO vagrant;

--
-- Name: trips_trip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE trips_trip_id_seq OWNED BY trips.trip_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    name character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    password character varying(128) NOT NULL
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: place_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY places ALTER COLUMN place_id SET DEFAULT nextval('places_place_id_seq'::regclass);


--
-- Name: trip_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY trips ALTER COLUMN trip_id SET DEFAULT nextval('trips_trip_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY categories (cat_id) FROM stdin;
eat
sleep
explore
transport
\.


--
-- Data for Name: places; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY places (place_id, place_name, place_loc, latitude, longitude, day_num, date, trip_id, cat_id, notes, pic_file) FROM stdin;
1	Hash Land	724 W Maxwell St, Chicago, IL 60607, USA	41.8649118000000016	-87.6460974000000306	1	2016-11-05	1	eat	test	eat.png
25	DoubleTree Hotel	1000 NE Multnomah St, Portland, OR 97232, USA	45.5307071999999877	-122.655557700000031	1	2016-07-07	4	sleep	They serve delicious cookies upon check in.	sleep.png
2	Taipei	Din Tai Fung, City Hall Road, Xinyi District, Taipei City, Taiwan	25.0333347999999987	121.564307099999951	5	2017-02-01	2	eat	din tai fung	eat.png
3	Tainan	No. 82, Guosheng Rd, Anping District, Tainan City, Taiwan 708	23.0015092999999986	120.160624399999961	4	2017-01-31	2	explore	ANPING	explore.png
5	test place sleep	No. 160, Section 3, Ren'ai Rd, Da’an District, Taipei City, Taiwan 106	25.0375815999999993	121.543120300000055	3	2017-01-30	2	sleep		sleep.png
6	Test Place	No. 30, Section 2, Xinguang Rd, Wenshan District, Taipei City, Taiwan 116	24.9988551000000001	121.581058499999926	2	2017-01-29	2	explore		explore.png
26	Menghan and Kelsey's Wedding!	9957 SE 222nd Dr, Damascus, OR 97089, USA	45.4505896999999877	-122.435418499999969	1	2016-07-07	4	explore	Beautiful Wedding Location. Overlooks pastures. Great food too!	26.jpg
9	add second day 2 test	No. 44-46, Kunming St, Wanhua District, Taipei City, Taiwan 108	25.046775199999999	121.505803399999991	2	2017-01-29	2	explore	test	explore.png
10	Add A Picture	Hengchun Township, Pingtung County, Taiwan 946	21.9483306999999996	120.779751600000054	1	2017-01-28	2	transport	test	10.jpg
11	Newly added	No. 151號, Daxue Rd, Sanxia District, New Taipei City, Taiwan 237	24.9426051000000015	121.368381199999931	1	2017-01-28	2	eat		11.jpg
27	Saturday Market	2 SW Naito Pkwy, Portland, OR 97204, USA	45.5226838000000029	-122.66977810000003	2	2016-07-08	4	explore	Great place to enjoy a lunch on Saturday. Also, really cool local artists selling their work.	27.jpg
14	Test Add	Fujian Province	24.4943485999999986	118.416310300000077	1	2017-01-28	2	explore		explore.png
15	test utf 8	Fujian Province	24.4943485999999986	118.416310300000077	1	2017-01-28	2	sleep		sleep.png
16	try encoding	Fujian, China	26.1007800000000003	119.295143999999937	1	2017-01-28	2	sleep		sleep.png
19	PLEAAASe	Fujian Province	24.4943485999999986	118.416310300000077	1	2017-01-28	2	transport		transport.png
20	PLEASE WORK 2	Fujian, China	26.1007800000000003	119.295143999999937	1	2017-01-28	2	explore		explore.png
21	Add A Place for Extra Measure	No. 45, Section 4, Zhongxiao E Rd, Da’an District, Taipei City, Taiwan 106	25.0420291000000006	121.544929899999943	1	2017-01-28	2	explore	grassa	21.jpg
22	Test Place Day 100	Taiwan Province, Taiwan	22.6158014999999999	120.712002299999995	5	2017-02-01	2	explore	test test	explore.png
23	Add Another Place	Kunming St, Wanhua District, Taipei City, Taiwan 108	25.0473932999999995	121.506076699999994	7	2017-02-03	2	explore	Day 7 L	explore.png
29	Oregon Historical Society Museum	203 SW Park Ave, Portland, OR 97205, USA	45.5227746999999994	-122.679306100000019	2	2016-07-08	4	explore	I love this museum! It was super informative. I liked how the history extended to modern day.	29.jpg
24	PDX	7000 NE Airport Way, Portland, OR 97218, USA	45.5897693999999873	-122.595094200000005	3	2016-07-09	4	transport	This airport has super friendly TSA!	transport.png
30	Blue Star Donuts	1237 SW Washington St, Portland, OR 97205, USA	45.5222118000000009	-122.684178999999972	3	2016-07-09	4	eat	Picked up donuts before leaving! I loved the blueberry bourbon basil donut.	eat.png
32	Hackbright Academy	683 Sutter St, San Francisco, CA 94109, USA	37.7887459000000021	-122.41158519999999	1	2016-12-03	5	explore	awesome place!	explore.png
35	Pine State Biscuits	1100 SE Division St #100, Portland, OR 97202, USA	45.5046409000000125	-122.654554899999994	1	2016-07-07	4	eat	great biscuits!	eat.png
28	Grassa Italian Food	1205 SW Washington St, Portland, OR 97205, USA	45.5220640000000003	-122.683594900000003	2	2016-07-08	4	eat	Great, quick Italian food. I really liked the bucatini carbonara.	28.jpg
\.


--
-- Name: places_place_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('places_place_id_seq', 35, true);


--
-- Data for Name: trips; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY trips (trip_id, trip_name, start_date, end_date, general_loc, latitude, longitude, viewport, username, published) FROM stdin;
1	Hash Brown Land	2016-11-05	2016-11-06	731 W Maxwell St, Chicago, IL 60607, USA	41.8646973000000031	-87.6462685999999849	{"south":41.8646517,"west":-87.64632695,"north":41.86483410000001,"east":-87.64624915000002}	hashbrown4	f
3	Test Home Trip	2016-11-27	2016-11-30	Irvine, CA, USA	33.6839472999999998	-117.794694199999981	{"south":33.5995231,"west":-117.87004100000001,"north":33.7744771,"east":-117.67846299999997}	steben	f
2	Taiwan	2017-01-28	2017-02-10	Taiwan	23.6978100000000005	120.960514999999987	{"south":21.8968244,"west":120.03509889999998,"north":25.2996232,"east":122.00716119999993}	steben	f
4	Portland with Paulina	2016-07-07	2016-07-09	Portland, OR, USA	45.5230622000000125	-122.676481599999988	{"south":45.432393,"west":-122.83699519999999,"north":45.6524799,"east":-122.4718489}	kelly	f
5	San Francisco Weekend	2016-12-03	2016-12-04	San Francisco, CA, USA	37.7749294999999989	-122.419415500000014	{"south":37.70339999999999,"west":-122.52699999999999,"north":37.812,"east":-122.34820000000002}	kelly	f
\.


--
-- Name: trips_trip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('trips_trip_id_seq', 6, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (name, username, password) FROM stdin;
Hash Brown	hashbrown	$2b$12$dQUxbKxWIbac8RY0/Kqp0evdlDbLqeaGxeBFY5/Fu0EeSRJFrZG0C
Hash Brown	hashbrown2	$2b$12$qXH7A2AQk2.wy0nUnwJQzeUoNXheqyE16MUgkqLaDL/Q9n3MqoVY2
hashbrown3	hashbrown3	$2b$12$00D5n9C1XbzIgs1NGZDPfOnlsGATw7ffSWrUEt418yKh3p3qcA5QG
Hash Brown	hashbrown4	$2b$12$kn35QDydRGV1WrLHP3WWse7bg8OVQAbb6gFNm6AaFpedQfU/cn19S
Kelly Young	10154799897830087	fb_user
STEBEN	steben	$2b$12$hMtdS5i6cWgNygxbB/ZdCOHyCG7mLB83ykjuR9PCKj3JWeaPD093S
pelligrino	san	$2b$12$sPXzVhZECc9vL4Ob7mt9te8gbtHpSxhRRAPT/bnQkQ7nMJXeIdf2.
Kelly Young	kelly	$2b$12$6QxIaF.AgKY96jjAQ9705.Yxwn.SaM6P7e2TLYMaX4hWJghWpHGw6
\.


--
-- Name: categories_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (cat_id);


--
-- Name: places_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY places
    ADD CONSTRAINT places_pkey PRIMARY KEY (place_id);


--
-- Name: trips_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY trips
    ADD CONSTRAINT trips_pkey PRIMARY KEY (trip_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);


--
-- Name: places_cat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY places
    ADD CONSTRAINT places_cat_id_fkey FOREIGN KEY (cat_id) REFERENCES categories(cat_id);


--
-- Name: places_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY places
    ADD CONSTRAINT places_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES trips(trip_id);


--
-- Name: trips_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY trips
    ADD CONSTRAINT trips_username_fkey FOREIGN KEY (username) REFERENCES users(username);


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

