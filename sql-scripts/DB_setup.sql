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

CREATE DATABASE user_db;


ALTER DATABASE user_db OWNER TO postgres;

\connect user_db

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

CREATE SCHEMA trail;

ALTER SCHEMA trail OWNER TO postgres;

CREATE SCHEMA "user";

ALTER SCHEMA "user" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE trail.trail_point (
    id integer NOT NULL,
    x double precision NOT NULL,
    y double precision NOT NULL,
    point_index integer NOT NULL
);

ALTER TABLE trail.trail_point OWNER TO postgres;

CREATE TABLE trail.user_trail (
    trail_id SERIAL NOT NULL,
    trail_name text NOT NULL,
    user_id integer NOT NULL
);

ALTER TABLE trail.user_trail OWNER TO postgres;

CREATE TABLE "user".user_data (
    id SERIAL NOT NULL,
    email text NOT NULL,
    username text NOT NULL,
    password_hash text NOT NULL
);

ALTER TABLE "user".user_data OWNER TO postgres;

CREATE TABLE "user".user_session (
    user_id integer NOT NULL,
    session_key text NOT NULL
);

ALTER TABLE "user".user_session OWNER TO postgres;

ALTER TABLE ONLY trail.user_trail
    ADD CONSTRAINT user_trail_pkey PRIMARY KEY (trail_id);

ALTER TABLE ONLY "user".user_data
    ADD CONSTRAINT user_ak_pkey PRIMARY KEY (id);

ALTER TABLE ONLY trail.trail_point
    ADD CONSTRAINT trail_point_id_fkey FOREIGN KEY (id) REFERENCES trail.user_trail(trail_id);

ALTER TABLE ONLY trail.user_trail
    ADD CONSTRAINT user_trail_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user".user_data(id) NOT VALID;

ALTER TABLE ONLY "user".user_session
    ADD CONSTRAINT user_session_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user".user_data(id) NOT VALID;
