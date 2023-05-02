-- Database export via SQLPro (https://www.sqlprostudio.com/allapps.html)
-- Exported by cliff at 02-05-2023 07:37.
-- WARNING: This file may contain descructive statements such as DROPs.
-- Please ensure that you are running the script at the proper location.


-- BEGIN TABLE public.activities
DROP TABLE IF EXISTS public.activities CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.activities (
	id integer DEFAULT nextval('activities_sampleid_seq'::regclass) NOT NULL,
	parent_id integer,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	name text NOT NULL,
	intervention_id integer,
	owner_id integer,
	status_id integer,
	notes text,
	url text,
	driver_ids integer[],
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.activities

-- BEGIN TABLE public.async_cache
DROP TABLE IF EXISTS public.async_cache CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.async_cache (
	id text NOT NULL,
	response text NOT NULL,
	response_time timestamp without time zone DEFAULT now() NOT NULL
);

COMMIT;

-- END TABLE public.async_cache

-- BEGIN TABLE public.driver_graph
DROP TABLE IF EXISTS public.driver_graph CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.driver_graph (
	id integer DEFAULT nextval('driver_graph_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	driver_id integer NOT NULL,
	driver_influenced_id integer NOT NULL,
	importance_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.driver_graph

-- BEGIN TABLE public.drivers_in_prj
DROP TABLE IF EXISTS public.drivers_in_prj CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.drivers_in_prj (
	id integer DEFAULT nextval('prj_drivers_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	lu_driver_id integer NOT NULL,
	importance_id integer,
	notes_context text,
	notes_gap text,
	notes_goal text,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.drivers_in_prj

-- BEGIN TABLE public.gaps
DROP TABLE IF EXISTS public.gaps CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.gaps (
	id integer DEFAULT nextval('gaps_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	created_time timestamp without time zone NOT NULL,
	alert_text text NOT NULL,
	assigned_user_id integer,
	snoozed_by_user_id integer,
	snoozed_time timestamp without time zone,
	resolved_time timestamp without time zone,
	audience_id integer,
	toc_id integer,
	activity_id integer,
	driver_id integer,
	snooze_until date,
	editing_user_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.gaps

-- BEGIN TABLE public.indicators
DROP TABLE IF EXISTS public.indicators CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.indicators (
	id integer DEFAULT nextval('indicators_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	name text NOT NULL,
	is_quant boolean NOT NULL,
	units text,
	target_value real,
	target_text text,
	toc_id integer,
	source text,
	activity_id integer,
	description text,
	url text,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.indicators

-- BEGIN TABLE public.languages
DROP TABLE IF EXISTS public.languages CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.languages (
	id integer DEFAULT nextval('languages_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	private boolean DEFAULT true NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.languages

-- BEGIN TABLE public.library
DROP TABLE IF EXISTS public.library CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.library (
	id integer DEFAULT nextval('library_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	library_type_id integer NOT NULL,
	author text,
	url text NOT NULL,
	url_label text,
	private boolean DEFAULT true NOT NULL,
	notes text,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.library

-- BEGIN TABLE public.locations
DROP TABLE IF EXISTS public.locations CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.locations (
	id integer DEFAULT nextval('locations_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	latitude real,
	longitude real,
	private boolean DEFAULT true NOT NULL,
	notes text,
	country_id integer,
	district text,
	region text,
	language_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.locations

-- BEGIN TABLE public.measurements
DROP TABLE IF EXISTS public.measurements CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.measurements (
	id integer DEFAULT nextval('measurements_sampleid_seq'::regclass) NOT NULL,
	indicator_id integer NOT NULL,
	activ_sched_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	date date,
	value_quant real,
	value_text text,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.measurements

-- BEGIN TABLE public.msgs_received
DROP TABLE IF EXISTS public.msgs_received CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.msgs_received (
	id bigint DEFAULT nextval('msgs_received_sampleid_seq'::regclass) NOT NULL,
	message text NOT NULL,
	user_id integer NOT NULL,
	received_time timestamp without time zone DEFAULT now() NOT NULL,
	related_msg_id bigint,
	channel character(1),
	related_item text,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.msgs_received

-- BEGIN TABLE public.msgs_sent
DROP TABLE IF EXISTS public.msgs_sent CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.msgs_sent (
	id bigint DEFAULT nextval('msgs_sent_sampleid_seq'::regclass) NOT NULL,
	message text NOT NULL,
	sent_time timestamp without time zone DEFAULT now() NOT NULL,
	related_item text,
	user_id_sending integer NOT NULL,
	prj_id integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.msgs_sent

-- BEGIN TABLE public.msgs_sent_users
DROP TABLE IF EXISTS public.msgs_sent_users CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.msgs_sent_users (
	id bigint DEFAULT nextval('msgs_users_sampleid_seq'::regclass) NOT NULL,
	msg_sent_id bigint NOT NULL,
	user_id integer NOT NULL,
	success boolean,
	channel character(1) DEFAULT NULL::bpchar,
	waiting boolean,
	declined boolean,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.msgs_sent_users

-- BEGIN TABLE public.participants
DROP TABLE IF EXISTS public.participants CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.participants (
	id integer DEFAULT nextval('audiences_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	parent_id integer,
	name text NOT NULL,
	type_id integer NOT NULL,
	language_id integer,
	location_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.participants

-- BEGIN TABLE public.project_data
DROP TABLE IF EXISTS public.project_data CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.project_data (
	id bigint DEFAULT nextval('project_data_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	q_id integer NOT NULL,
	"data" text NOT NULL,
	"sequence" integer,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.project_data

-- BEGIN TABLE public.project_users
DROP TABLE IF EXISTS public.project_users CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.project_users (
	id integer DEFAULT nextval('prj_users_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	access_id integer NOT NULL,
	editing_user_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.project_users

-- BEGIN TABLE public.projects
DROP TABLE IF EXISTS public.projects CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.projects (
	id integer DEFAULT nextval('projects_sampleid_seq1'::regclass) NOT NULL,
	name text NOT NULL,
	private_prj boolean DEFAULT true NOT NULL,
	country_id integer,
	editing_user_id integer,
	archived boolean DEFAULT false NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.projects

-- BEGIN TABLE public.risk_activities
DROP TABLE IF EXISTS public.risk_activities CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.risk_activities (
	id integer DEFAULT nextval('risk_activities_sampleid_seq'::regclass) NOT NULL,
	risk_id integer NOT NULL,
	activity_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.risk_activities

-- BEGIN TABLE public.risks
DROP TABLE IF EXISTS public.risks CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.risks (
	id integer DEFAULT nextval('risks_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	name text NOT NULL,
	toc_id integer,
	driver_id integer,
	audience_id integer,
	mitigation_text text,
	description text,
	importance_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.risks

-- BEGIN TABLE public.schedules
DROP TABLE IF EXISTS public.schedules CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.schedules (
	id integer DEFAULT nextval('activity_schedules_sampleid_seq'::regclass) NOT NULL,
	editing_user_id integer NOT NULL,
	activity_id integer NOT NULL,
	planned_date_from date NOT NULL,
	planned_date_to date,
	actual_date_from date,
	actual_date_to date,
	owner_id integer,
	participant_id integer,
	status_id integer,
	url text,
	dependency_ids integer[],
	prj_id integer NOT NULL,
	notes text,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.schedules

-- BEGIN TABLE public.toc
DROP TABLE IF EXISTS public.toc CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.toc (
	id integer DEFAULT nextval('theory_of_change_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	name text NOT NULL,
	activity_id integer,
	toc_type_id integer NOT NULL,
	sem_id integer,
	description text,
	notes text,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.toc

-- BEGIN TABLE public.toc_graph
DROP TABLE IF EXISTS public.toc_graph CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.toc_graph (
	id integer DEFAULT nextval('toc_graph_sampleid_seq'::regclass) NOT NULL,
	toc_from_id integer NOT NULL,
	toc_to_id integer NOT NULL,
	editing_user_id integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.toc_graph

-- BEGIN TABLE public.users
DROP TABLE IF EXISTS public.users CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.users (
	id integer DEFAULT nextval('users_sampleid_seq'::regclass) NOT NULL,
	email text NOT NULL,
	name text,
	last_project_id integer,
	user_id integer,
	editing_user_id integer,
	sms text,
	notify_email boolean,
	notify_sms boolean,
	address_as text,
	whatsapp text,
	notify_whatsapp boolean,
	whatsapp_last_received timestamp without time zone,
	PRIMARY KEY(id)
);

COMMIT;

-- END TABLE public.users

DROP VIEW public.drivers;

CREATE OR REPLACE VIEW public.drivers AS
 SELECT ld.id AS lu_id,
    ld.sequence,
    ld.parent_id,
    ld.category_id,
    ld.text_short,
    ld.text_long,
    ld.name,
    ld.intervention_ids,
    dp.id AS dip_id,
    dp.prj_id,
    dp.editing_user_id AS user_id,
    COALESCE(dp.importance_id, 0) AS importance_id,
    dp.notes_context,
    dp.notes_gap,
    dp.notes_goal
   FROM (lu_drivers ld
     LEFT JOIN drivers_in_prj dp ON ((ld.id = dp.lu_driver_id)));

DROP VIEW public.user_projects;

CREATE OR REPLACE VIEW public.user_projects AS
 SELECT p.id AS prj_id,
    p.name,
    p.private_prj,
    p.country_id,
    pu.access_id,
    pu.user_id,
    p.archived
   FROM (projects p
     JOIN project_users pu ON ((pu.prj_id = p.id)));

DROP VIEW public.users_in_project;

CREATE OR REPLACE VIEW public.users_in_project AS
 SELECT pu.id,
    pu.user_id,
    pu.access_id,
    pu.prj_id,
    u.email,
    u.name,
    u.address_as
   FROM (users u
     JOIN project_users pu ON ((u.id = pu.user_id)));

DROP VIEW public.users_w_numbers;

CREATE OR REPLACE VIEW public.users_w_numbers AS
 SELECT u.id,
    u.address_as,
    u.sms AS phone,
    pu.prj_id,
    NULL::boolean AS in_window
   FROM (users u
     JOIN project_users pu ON ((u.id = pu.user_id)))
  WHERE ((u.sms IS NOT NULL) AND u.notify_sms)
UNION
 SELECT u.id,
    u.address_as,
    concat('whatsapp:', u.whatsapp) AS phone,
    pu.prj_id,
    (u.whatsapp_last_received > (now() - ((24)::double precision * '01:00:00'::interval))) AS in_window
   FROM (users u
     JOIN project_users pu ON ((u.id = pu.user_id)))
  WHERE ((u.whatsapp IS NOT NULL) AND u.notify_whatsapp);

