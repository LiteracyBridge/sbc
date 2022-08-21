-- Database export via SQLPro (https://www.sqlprostudio.com/allapps.html)
-- Exported by cliff at 21-08-2022 07:36.
-- WARNING: This file may contain descructive statements such as DROPs.
-- Please ensure that you are running the script at the proper location.


-- BEGIN TABLE public.activities
DROP TABLE IF EXISTS public.activities CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.activities (
	id integer DEFAULT nextval('activities_sampleid_seq'::regclass) NOT NULL,
	parent_id integer,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
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

-- Inserting 7 rows into public.activities
-- Insert batch #1
INSERT INTO public.activities (id, parent_id, prj_id, user_id, name, intervention_id, owner_id, status_id, notes, url, driver_ids) VALUES
(3, NULL, 1, 1, 'Psycho-Social Support', 11, NULL, NULL, NULL, NULL, '{4}'),
(5, NULL, 1, 1, 'Direct Capacity Building', 13, NULL, NULL, NULL, NULL, '{4}'),
(26, NULL, 1, 1, 'Reevaluation exercises', 9, NULL, NULL, NULL, NULL, '{3}'),
(29, NULL, 1, 1, 'Gender-transformative programming', 39, NULL, NULL, NULL, NULL, '{10}'),
(28, 26, 1, 1, 'Early Childhood Development123', 38, 1, 2, 'some bnte\nasdasda\n', 'sadsdsa', '{10}'),
(27, NULL, 1, 1, 'Elaboration likelihood approach', 6, NULL, NULL, NULL, NULL, '{1,5,3,4,2,66,47}'),
(30, 3, 1, 1, 'test one', 3, 2, 2, 'notes\nhere', 'url here', '{2,66}');

-- END TABLE public.activities

-- BEGIN TABLE public.driver_graph
DROP TABLE IF EXISTS public.driver_graph CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.driver_graph (
	id integer DEFAULT nextval('driver_graph_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	driver_id integer NOT NULL,
	driver_influenced_id integer NOT NULL,
	importance_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.driver_graph contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.driver_graph


-- END TABLE public.driver_graph

-- BEGIN TABLE public.drivers_in_prj
DROP TABLE IF EXISTS public.drivers_in_prj CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.drivers_in_prj (
	id integer DEFAULT nextval('prj_drivers_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	lu_driver_id integer NOT NULL,
	importance_id integer,
	notes_context text,
	notes_gap text,
	notes_goal text,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 8 rows into public.drivers_in_prj
-- Insert batch #1
INSERT INTO public.drivers_in_prj (id, prj_id, user_id, lu_driver_id, importance_id, notes_context, notes_gap, notes_goal) VALUES
(2, 2, 1, 31, 3, NULL, 'gap notes here', NULL),
(4, 1, 3, 47, 1, NULL, NULL, NULL),
(6, 1, 3, 66, 2, NULL, NULL, NULL),
(7, 1, 3, 5, 1, NULL, NULL, NULL),
(8, 1, 99, 2, 1, NULL, NULL, NULL),
(3, 1, 1, 4, 2, NULL, NULL, NULL),
(0, 1, 1, 1, 3, 'context', 'gap', 'goal'),
(9, 1, 1, 3, 2, NULL, NULL, NULL);

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
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.gaps contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.gaps


-- END TABLE public.gaps

-- BEGIN TABLE public.indicators
DROP TABLE IF EXISTS public.indicators CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.indicators (
	id integer DEFAULT nextval('indicators_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
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

-- Table public.indicators contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.indicators


-- END TABLE public.indicators

-- BEGIN TABLE public.languages
DROP TABLE IF EXISTS public.languages CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.languages (
	id integer DEFAULT nextval('languages_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	private boolean DEFAULT true NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.languages contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.languages


-- END TABLE public.languages

-- BEGIN TABLE public.library
DROP TABLE IF EXISTS public.library CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.library (
	id integer DEFAULT nextval('library_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	library_type_id integer NOT NULL,
	author text,
	url text NOT NULL,
	url_label text,
	private boolean DEFAULT true NOT NULL,
	notes text,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.library contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.library


-- END TABLE public.library

-- BEGIN TABLE public.locations
DROP TABLE IF EXISTS public.locations CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.locations (
	id integer DEFAULT nextval('locations_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
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

-- Table public.locations contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.locations


-- END TABLE public.locations

-- BEGIN TABLE public.lu_access_types
DROP TABLE IF EXISTS public.lu_access_types CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_access_types (
	id integer DEFAULT nextval('roles_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"sequence" integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 3 rows into public.lu_access_types
-- Insert batch #1
INSERT INTO public.lu_access_types (id, name, "sequence") VALUES
(1, 'owner', 1),
(3, 'editor', 2),
(2, 'viewer', 3);

-- END TABLE public.lu_access_types

-- BEGIN TABLE public.lu_activity_status
DROP TABLE IF EXISTS public.lu_activity_status CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_activity_status (
	id integer DEFAULT nextval('activity_statuses_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"sequence" integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 4 rows into public.lu_activity_status
-- Insert batch #1
INSERT INTO public.lu_activity_status (id, name, "sequence") VALUES
(1, 'proposed', 1),
(2, 'planned', 2),
(3, 'in progress', 3),
(4, 'completed', 4);

-- END TABLE public.lu_activity_status

-- BEGIN TABLE public.lu_countries
DROP TABLE IF EXISTS public.lu_countries CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_countries (
	id integer DEFAULT nextval('countries_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"sequence" integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 249 rows into public.lu_countries
-- Insert batch #1
INSERT INTO public.lu_countries (id, name, "sequence") VALUES
(1, 'Afghanistan', 1),
(2, 'Åland Islands', 2),
(3, 'Albania', 3),
(4, 'Algeria', 4),
(5, 'American Samoa', 5),
(6, 'Andorra', 6),
(7, 'Angola', 7),
(8, 'Anguilla', 8),
(9, 'Antarctica', 9),
(10, 'Antigua and Barbuda', 10),
(11, 'Argentina', 11),
(12, 'Armenia', 12),
(13, 'Aruba', 13),
(14, 'Australia', 14),
(15, 'Austria', 15),
(16, 'Azerbaijan', 16),
(17, 'Bahamas', 17),
(18, 'Bahrain', 18),
(19, 'Bangladesh', 19),
(20, 'Barbados', 20),
(21, 'Belarus', 21),
(22, 'Belgium', 22),
(23, 'Belize', 23),
(24, 'Benin', 24),
(25, 'Bermuda', 25),
(26, 'Bhutan', 26),
(27, 'Bolivia (Plurinational State of)', 27),
(28, 'Bonaire, Sint Eustatius and Saba', 28),
(29, 'Bosnia and Herzegovina', 29),
(30, 'Botswana', 30),
(31, 'Bouvet Island', 31),
(32, 'Brazil', 32),
(33, 'British Indian Ocean Territory', 33),
(34, 'British Virgin Islands', 34),
(35, 'Brunei Darussalam', 35),
(36, 'Bulgaria', 36),
(37, 'Burkina Faso', 37),
(38, 'Burundi', 38),
(39, 'Cabo Verde', 39),
(40, 'Cambodia', 40),
(41, 'Cameroon', 41),
(42, 'Canada', 42),
(43, 'Cayman Islands', 43),
(44, 'Central African Republic', 44),
(45, 'Chad', 45),
(46, 'Chile', 46),
(47, 'China', 47),
(48, 'China, Hong Kong Special Administrative Region', 48),
(49, 'China, Macao Special Administrative Region', 49),
(50, 'Christmas Island', 50),
(51, 'Cocos (Keeling) Islands', 51),
(52, 'Colombia', 52),
(53, 'Comoros', 53),
(54, 'Congo', 54),
(55, 'Cook Islands', 55),
(56, 'Costa Rica', 56),
(57, 'Côte d’Ivoire', 57),
(58, 'Croatia', 58),
(59, 'Cuba', 59),
(60, 'Curaçao', 60),
(61, 'Cyprus', 61),
(62, 'Czechia', 62),
(63, 'Democratic People''s Republic of Korea', 63),
(64, 'Democratic Republic of the Congo', 64),
(65, 'Denmark', 65),
(66, 'Djibouti', 66),
(67, 'Dominica', 67),
(68, 'Dominican Republic', 68),
(69, 'Ecuador', 69),
(70, 'Egypt', 70),
(71, 'El Salvador', 71),
(72, 'Equatorial Guinea', 72),
(73, 'Eritrea', 73),
(74, 'Estonia', 74),
(75, 'Eswatini', 75),
(76, 'Ethiopia', 76),
(77, 'Falkland Islands (Malvinas)', 77),
(78, 'Faroe Islands', 78),
(79, 'Fiji', 79),
(80, 'Finland', 80),
(81, 'France', 81),
(82, 'French Guiana', 82),
(83, 'French Polynesia', 83),
(84, 'French Southern Territories', 84),
(85, 'Gabon', 85),
(86, 'Gambia', 86),
(87, 'Georgia', 87),
(88, 'Germany', 88),
(89, 'Ghana', 89),
(90, 'Gibraltar', 90),
(91, 'Greece', 91),
(92, 'Greenland', 92),
(93, 'Grenada', 93),
(94, 'Guadeloupe', 94),
(95, 'Guam', 95),
(96, 'Guatemala', 96),
(97, 'Guernsey', 97),
(98, 'Guinea', 98),
(99, 'Guinea-Bissau', 99),
(100, 'Guyana', 100),
(101, 'Haiti', 101),
(102, 'Heard Island and McDonald Islands', 102),
(103, 'Holy See', 103),
(104, 'Honduras', 104),
(105, 'Hungary', 105),
(106, 'Iceland', 106),
(107, 'India', 107),
(108, 'Indonesia', 108),
(109, 'Iran (Islamic Republic of)', 109),
(110, 'Iraq', 110),
(111, 'Ireland', 111),
(112, 'Isle of Man', 112),
(113, 'Israel', 113),
(114, 'Italy', 114),
(115, 'Jamaica', 115),
(116, 'Japan', 116),
(117, 'Jersey', 117),
(118, 'Jordan', 118),
(119, 'Kazakhstan', 119),
(120, 'Kenya', 120),
(121, 'Kiribati', 121),
(122, 'Kuwait', 122),
(123, 'Kyrgyzstan', 123),
(124, 'Lao People''s Democratic Republic', 124),
(125, 'Latvia', 125),
(126, 'Lebanon', 126),
(127, 'Lesotho', 127),
(128, 'Liberia', 128),
(129, 'Libya', 129),
(130, 'Liechtenstein', 130),
(131, 'Lithuania', 131),
(132, 'Luxembourg', 132),
(133, 'Madagascar', 133),
(134, 'Malawi', 134),
(135, 'Malaysia', 135),
(136, 'Maldives', 136),
(137, 'Mali', 137),
(138, 'Malta', 138),
(139, 'Marshall Islands', 139),
(140, 'Martinique', 140),
(141, 'Mauritania', 141),
(142, 'Mauritius', 142),
(143, 'Mayotte', 143),
(144, 'Mexico', 144),
(145, 'Micronesia (Federated States of)', 145),
(146, 'Monaco', 146),
(147, 'Mongolia', 147),
(148, 'Montenegro', 148),
(149, 'Montserrat', 149),
(150, 'Morocco', 150),
(151, 'Mozambique', 151),
(152, 'Myanmar', 152),
(153, 'Namibia', 153),
(154, 'Nauru', 154),
(155, 'Nepal', 155),
(156, 'Netherlands', 156),
(157, 'New Caledonia', 157),
(158, 'New Zealand', 158),
(159, 'Nicaragua', 159),
(160, 'Niger', 160),
(161, 'Nigeria', 161),
(162, 'Niue', 162),
(163, 'Norfolk Island', 163),
(164, 'North Macedonia', 164),
(165, 'Northern Mariana Islands', 165),
(166, 'Norway', 166),
(167, 'Oman', 167),
(168, 'Pakistan', 168),
(169, 'Palau', 169),
(170, 'Panama', 170),
(171, 'Papua New Guinea', 171),
(172, 'Paraguay', 172),
(173, 'Peru', 173),
(174, 'Philippines', 174),
(175, 'Pitcairn', 175),
(176, 'Poland', 176),
(177, 'Portugal', 177),
(178, 'Puerto Rico', 178),
(179, 'Qatar', 179),
(180, 'Republic of Korea', 180),
(181, 'Republic of Moldova', 181),
(182, 'Réunion', 182),
(183, 'Romania', 183),
(184, 'Russian Federation', 184),
(185, 'Rwanda', 185),
(186, 'Saint Barthélemy', 186),
(187, 'Saint Helena', 187),
(188, 'Saint Kitts and Nevis', 188),
(189, 'Saint Lucia', 189),
(190, 'Saint Martin (French Part)', 190),
(191, 'Saint Pierre and Miquelon', 191),
(192, 'Saint Vincent and the Grenadines', 192),
(193, 'Samoa', 193),
(194, 'San Marino', 194),
(195, 'Sao Tome and Principe', 195),
(196, 'Sark', 196),
(197, 'Saudi Arabia', 197),
(198, 'Senegal', 198),
(199, 'Serbia', 199),
(200, 'Seychelles', 200),
(201, 'Sierra Leone', 201),
(202, 'Singapore', 202),
(203, 'Sint Maarten (Dutch part)', 203),
(204, 'Slovakia', 204),
(205, 'Slovenia', 205),
(206, 'Solomon Islands', 206),
(207, 'Somalia', 207),
(208, 'South Africa', 208),
(209, 'South Georgia and the South Sandwich Islands', 209),
(210, 'South Sudan', 210),
(211, 'Spain', 211),
(212, 'Sri Lanka', 212),
(213, 'State of Palestine', 213),
(214, 'Sudan', 214),
(215, 'Suriname', 215),
(216, 'Svalbard and Jan Mayen Islands', 216),
(217, 'Sweden', 217),
(218, 'Switzerland', 218),
(219, 'Syrian Arab Republic', 219),
(220, 'Tajikistan', 220),
(221, 'Thailand', 221),
(222, 'Timor-Leste', 222),
(223, 'Togo', 223),
(224, 'Tokelau', 224),
(225, 'Tonga', 225),
(226, 'Trinidad and Tobago', 226),
(227, 'Tunisia', 227),
(228, 'Turkey', 228),
(229, 'Turkmenistan', 229),
(230, 'Turks and Caicos Islands', 230),
(231, 'Tuvalu', 231),
(232, 'Uganda', 232),
(233, 'Ukraine', 233),
(234, 'United Arab Emirates', 234),
(235, 'United Kingdom of Great Britain and Northern Ireland', 235),
(236, 'United Republic of Tanzania', 236),
(237, 'United States Minor Outlying Islands', 237),
(238, 'United States of America', 238),
(239, 'United States Virgin Islands', 239),
(240, 'Uruguay', 240),
(241, 'Uzbekistan', 241),
(242, 'Vanuatu', 242),
(243, 'Venezuela (Bolivarian Republic of)', 243),
(244, 'Viet Nam', 244),
(245, 'Wallis and Futuna Islands', 245),
(246, 'Western Sahara', 246),
(247, 'Yemen', 247),
(248, 'Zambia', 248),
(249, 'Zimbabwe', 249);

-- END TABLE public.lu_countries

-- BEGIN TABLE public.lu_driver_categories
DROP TABLE IF EXISTS public.lu_driver_categories CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_driver_categories (
	id integer DEFAULT nextval('lu_driver_categories_sampleid_seq'::regclass) NOT NULL,
	framework_id integer NOT NULL,
	name text NOT NULL,
	color text,
	"sequence" integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 4 rows into public.lu_driver_categories
-- Insert batch #1
INSERT INTO public.lu_driver_categories (id, framework_id, name, color, "sequence") VALUES
(0, 0, 'Psychology', '#A9D18E', 0),
(1, 0, 'Sociology', '#F4B183', 1),
(2, 0, 'Environment', '#9DC3E6', 2),
(3, 0, 'Personal and Contextual', '#D0CECE', 3);

-- END TABLE public.lu_driver_categories

-- BEGIN TABLE public.lu_drivers
DROP TABLE IF EXISTS public.lu_drivers CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_drivers (
	id integer DEFAULT nextval('drivers_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"group" text,
	parent_id integer,
	"sequence" integer,
	sem_id integer,
	text_short text,
	text_long text,
	url_description text,
	category_id integer,
	framework_id integer,
	intervention_ids integer[],
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 133 rows into public.lu_drivers
-- Insert batch #1
INSERT INTO public.lu_drivers (id, name, "group", parent_id, "sequence", sem_id, text_short, text_long, url_description, category_id, framework_id, intervention_ids) VALUES
(9, 'Community dynamic', 'Social-Environment', 0, 10, 3, 'The group’s collective capacity to change.', 'Community dialogue and collective action are key processes to produce change within a community. Members of a community acting collectively to deal with a shared problem\nand improve their lives will be a critical condition of success when issues to be addressed\nare social (in particular driven by social norms). The success of such processes increases\nthe community’s collective capacity to solve future problems. The existence of such a dynamic (shared recognition of a problem with ongoing collective discussion or action), or\nin its absence, the collective capacity to engage in it, is a critical condition for social change. However, some groups or societies are more individualistic: there could be a social norm of staying out of other people’s business, and a low recognition of the existence and value of the ‘public good’.', '', 1, 0, '{26,27}'),
(109, 'Living conditions', '', 15, 2, 0, '', 'The circumstances of a person’s life, such as geographic isolation, living in an active conflict zone, in areas with high criminality rates or even being incarcerated amongst other factors, are often strong barriers to adopting new practices. Lack of access to a job market, to food supplies or other basic needs plays a similar role.', '', 2, 0, NULL),
(123, 'Household composition', '', 7, 6, 0, '', '', '', 3, 0, NULL),
(6, 'Limited Rationality', 'Psychology', 0, 6, 1, 'The reasons why I don’t do what I should.', 'People do not always make decisions that are in their best interest. There are instances where we don’t really know why we do or don’t do things. A reason may be because it has always been done like this, even if it seems irrational. Several psychological traits (e.g., feeling more comfortable in a set routine, finding inaction to be easier, feeling overly positive about a choice previously made, etc.) are part of ‘human nature’ and can be used to explain why people don’t behave the way we would predict from a rational perspective. Limited or bounded rationality refers to this characteristic of human cognition that it is restricted in its resources (thinking capacity, available input information, and the amount of time allotted). As a consequence, people have a tendency to find simpler and easier ways to make decisions and act, regardless of intelligence. The concept of bounded rationality is very close to that of cognitive miser.', '', 0, 0, '{15,16}'),
(16, 'Information avoidance', '', 1, 1, 0, '', 'Individuals might actively and/or unconsciously avoid information if this information can threaten their beliefs, or force them to act, or upset them, or simply because they are already overloaded with information. One can choose not to recognize and consider certain details about a subject matter, even when there is no cost to obtaining such details and there is a benefit to doing so.', '', 0, 0, NULL),
(15, 'Structural barriers', 'Social-Environment', 0, 16, 4, 'Concrete things that prevent me from acting.', 'Structural barriers are bottlenecks that are not related to people’s willingness to change, or the legal and social environment, but often link to infrastructure, services and types of livelihoods, and are commonly consequences of poverty and underdevelopment.', '', 2, 0, '{33,34,35,36,37}'),
(99, 'Positive deviants', '', 13, 5, 0, '', 'The existence of individuals or small groups who confront similar challenges and constraints to their peers but who employ uncommon yet successful behaviours or strategies that enable them to find better solutions. They can be important role models.', '', 2, 0, NULL),
(124, 'Income / poverty level', '', 7, 7, 0, '', '', '', 3, 0, NULL),
(125, 'Religious affiliation', '', 7, 8, 0, '', '', '', 3, 0, NULL),
(126, 'Lifestyle', '', 7, 9, 0, '', '', '', 3, 0, NULL),
(127, 'Physiological attributes', '', 7, 10, 0, '', '', '', 3, 0, NULL),
(128, 'Alcohol/drug use', '', 7, 11, 0, '', '', '', 3, 0, NULL),
(91, 'Public figures, public discourse', '', 12, 5, 0, '', 'The messages most commonly spread in the communication environment; the ongoing public debates; the position of persons that have a significant effect on influencing the opinion of the general public.', '', 2, 0, NULL),
(108, 'Trust in service providers', '', 15, 1, 0, '', 'A critical condition for people to use services is trust in the person or entity providing them. Trust can be measured based on how respectful, competent and compassionate the provider is perceived to be, but can also derive from her/his profile (right ethnicity, right gender, etc.). The quality of the relationship as perceived by the ‘client’ is also extremely important in driving the use of a service – measured by the ‘user experience’.', '', 2, 0, NULL),
(130, 'Migration, displacement', '', 11, 1, 0, '', '', '', 3, 0, NULL),
(73, 'Sense of ownership', '', 9, 2, 0, '', 'The degree to which community members think the problem is important, perceive themselves as contributing to and responsible for the success of the collective change, and think they will benefit from the results.', '', 1, 0, NULL),
(131, 'Emergency vs. development context', '', 11, 2, 0, '', '', '', 3, 0, NULL),
(75, 'Equity of participation', '', 9, 4, 0, '', 'The degree to which marginalized members of the community (women, poor, ethnic groups, youth, elderly, etc.) can access spaces were issues are discussed, speak up and be involved in decision-making.', '', 1, 0, NULL),
(12, 'Communication environment', 'Mini-Environment', 0, 13, 4, 'The information and opinions I can be exposed to.', 'The information, opinions, arguments and stories we are exposed to have a significant role in shaping our attitudes and interests, and down the line our behaviours. This communication environment is formed by multiple channels and sources. Theories and analyses have long proven the influence of mass and social media on many aspects of our lives, but our views and beliefs are also conditioned by other sources such as the movies we watch, the songs we listen to, or the word on the street.', '', 2, 0, '{1,2,3,4,5}'),
(13, 'Emerging alternatives', 'Mini-Environment', 0, 14, 3, 'Those who don’t think or behave like the majority; new things out there.', 'People’s exposure to and awareness of those who have already chosen a different option, of voices carrying a different message and of influences which can trigger change is important, since dialogue in a community and personal action are rarely initiated spontaneously. The dynamic of change within a group usually starts with a catalyst or stimulus. Emerging alternatives can induce individual and collective actions.', '', 2, 0, '{1,2,3,4,5}'),
(111, 'Traditional services', '', 15, 4, 0, '', 'Existence and accessibility of alternative and traditional services, where behaviours considered harmful could be practiced and even encouraged.', '', 2, 0, NULL),
(112, 'Infrastructure', '', 15, 5, 0, '', 'Existence and usability of facilities, roads, water and sewage systems, electrical grids, phone, Internet, etc.', '', 2, 0, NULL),
(113, 'Availability, access to and quality of services/technology', '', 15, 6, 0, '', 'The demand for services cannot always be appropriately met for several reasons regarding their provision or impaired access for reasons such as financial difficulties, lack of transport, language barriers, low capacity of service providers, etc.', '', 2, 0, NULL),
(133, 'Natural events and weather', '', 11, 4, 0, '', '', '', 3, 0, NULL),
(11, 'Context', '', 0, 12, 5, 'The context in which I live.', 'Contextual factors include social, cultural and religious backgrounds; emergency and development contexts; migration and displacement conditions; and natural events and weather. These overarching situational elements will largely condition all other drivers: for example, being in humanitarian situations strongly impacts people’s decisions on a wide range of behaviours; similarly, socio-economic backgrounds partly explain the standard behaviours within given groups.', '', 3, 0, NULL),
(24, 'Representativeness heuristic', '', 1, 9, 0, '', 'We fill in characteristics from stereotypes, generalities and prior histories. As a result, we make judgements about people and events based on how much they resemble others.', '', 0, 0, NULL),
(4, 'Self-Efficacy', 'Psychology', 0, 4, 1, 'What I think I can do.', 'Self-efficacy combines a person’s objective capability to perform a change and her belief about this ability. Positive self-efficacy is a necessary precondition to taking steps towards new practices. As with attitude, individual characteristics are usually a key driver of a person’s self-efficacy. Poverty, for example, has a significant cognitive burden that makes it difficult for the poorest to think deliberately, see themselves as capable, have faith in the possibility of change and seize opportunities. On top of more classic empowerment efforts, interventions on self-perceptions can be powerful sources of change.', '', 0, 0, '{10,11,12,13,14}'),
(5, 'Intent', 'Psychology', 0, 5, 1, 'What I plan on doing; what I am ready for.', 'The readiness to change is the factor at the centre of the individual change process. When an individual is no longer reluctant to try a new practice, and more importantly willing to try it, the likelihood of change increases dramatically. But for intent to be converted into action, motivation is not enough: external and social factors must align in a supportive way.', '', 0, 0, NULL),
(72, 'Collective self-efficacy', '', 9, 1, 0, '', 'The confidence of community members that together they can succeed. This includes the perceived capability of other community members.', '', 1, 0, NULL),
(31, 'Efforts needed', '', 2, 5, 0, '', 'How practical and easy the change to a new behaviour is. The difficulty is not proportional to the likelihood of adoption: minor inconveniences (also known as ‘hassle factors’) might prevent us from acting in accordance with our intentions.', '', 0, 0, NULL),
(7, 'Personal Characteristics', '', 0, 8, 2, 'Who I am.', 'As a factor driving behaviours, personal characteristics involve the influence of a wide\nset of physiological and socio-demographical determinants, and relate to lifestyles. The\nmain attributes include age, gender, ethnicity, life-cycle stage (regardless of age, certain moments in a person’s growth trajectory have strong influence on their behaviours, such as transitions from childhood to adolescence to adulthood), education level, social status (level of respect, competence, authority position, etc.), poverty level, religious affiliation, household composition, possible disorders and alcohol/drug use. These are overarching background elements with direct influence on all the psychological drivers, which we will unpack in the following sections of the document.', '', 3, 0, NULL),
(100, 'Recognition of the issue', '', 14, 1, 0, '', 'The extent to which the authorities acknowledge the existence of a problem and are willing to act upon it.', '', 2, 0, NULL),
(132, 'Social, cultural and religious context', '', 11, 3, 0, '', '', '', 3, 0, NULL),
(63, 'Reference network’s attitudes and behaviours', '', 8, 1, 0, '', 'Social influence is primarily based on the attitudes and behaviours of those whose opinion we value the most, who we consult regarding certain issues, and those whose perception of us matters. Members of this ‘reference network’ include family and peers as well as influencers and role models who exert some form of influence over us. People tend to imitate the behaviours of their reference network frequently, and sometimes automatically. But who are the members of the group will depend on the situation and the behaviour. For example, in a new situation or a foreign country, most would align their behaviour to what complete strangers are doing. People end up having several reference networks, such as their close family, groups of friends and colleagues, online communities, etc.', '', 1, 0, NULL),
(114, 'Other external factors', '', 15, 7, 0, '', 'As relevant to the problem at hand and local context (e.g., natural obstacles, age barriers, climate change, currency and market changes, etc.).', '', 2, 0, NULL),
(129, 'Disorders', '', 7, 12, 0, '', '', '', 3, 0, NULL),
(64, 'Injunctive norms', '', 8, 2, 0, '', 'A rule of behaviour that people engage in because they think others in their group expect them to do so. This belief about socially approved behaviour is sometimes called ‘normative expectations’. There might be a silent majority of people disapproving of certain practices but still complying with them based on a widespread and wrong perception of what others think. This discrepancy between the majority of individual attitudes and a given practice is called ‘pluralistic ignorance’.', '', 1, 0, NULL),
(25, 'Cognitive dissonance', '', 1, 10, 0, '', 'People experience psychological tension when they realize that they engage in behaviours inconsistent with the type of person they would like to be. The natural reaction is to reduce this tension, either by changing attitudes and behaviours or accepting a different self-image (which can be much harder).', '', 0, 0, NULL),
(26, 'Memory bias', '', 1, 11, 0, '', 'What and how one remembers things is never objective. We edit and reinforce some memories after events, store memories differently based on how they were experienced (e.g., we better remember information we produce ourselves), are more likely to regard as accurate memories associated with significant events or emotions, and we notice things already memorized or repeated often. In summary, cognitive biases affect – both negatively and positively – the content and/or recollection of a memory.', '', 0, 0, NULL),
(30, 'Perceived risks', '', 2, 4, 0, '', 'The possibility that something bad might happen as a result of an action or a change, including, but not limited to, in terms of safety and satisfaction of basic needs. People desire certainty even when it is counterproductive. Being overly risk-averse is a natural human bias.', '', 0, 0, NULL),
(122, 'Education', '', 7, 5, 0, '', '', '', 3, 0, NULL),
(107, 'Voice and participation', '', 14, 8, 0, '', 'The ability of all actors – particularly those that are poor, marginalized, underrepresented, or disproportionately affected by policies – to elevate their voices and contribute to dialogue and decision-making processes that affect their lives. This not only includes direct engagement but also links to political representation.', '', 2, 0, NULL),
(42, 'Emotions', '', 3, 7, 0, '', 'Similarly, emotions are generated subconsciously and are designed to appraise and summarize an experience and inform action. It is a feeling process in which cognitive, physiological and behavioural reactions come together to respond to a stimulus. A number of decisions are informed by our emotional responses, which can constitute a barrier to rational thinking. Phobias and aversions, for example, are important mechanisms in everyday life. Another example of the power of emotions is that exactly similar information will trigger different attitudes if it is presented positively or negatively.', '', 0, 0, NULL),
(44, 'Agency', '', 4, 1, 0, '', 'The sense of control a person feels toward an action and its consequences. If the intention to perform an action appears to precede, guide and exclusively cause the action, an individual will have a sense of agency over what she has just done. If not, the resulting mismatch will prevent the individual from feeling a sense of control over what has just happened. Feeling of agency is the overall feeling of control without any explicit thinking about a specific action. Judgement of agency speaks to the conceptual level of control, when an individual explicitly thinks about initiating an action.', '', 0, 0, NULL),
(32, 'Affordability', '', 2, 6, 0, '', 'The extent to which a person considers a change of practice to be within her financial means, combining costs and possible monetary incentives.', '', 0, 0, NULL),
(33, 'Enjoyment', '', 2, 7, 0, '', 'How much someone likes or might like doing something, a cognitive and affective state that follows an activity where a sense of pleasure was experienced. This covers basic amusement as well as other forms of gratification and thrill, such as the feeling of power. Being passionate about something is a powerful driver for action. In economics, satisfaction and happiness are sometimes referred to as ‘utility’.', '', 0, 0, NULL),
(17, 'Availability heuristic', '', 1, 2, 0, '', 'We tend to overestimate the importance of information available to us. As a result, we refer to immediate examples that come to mind when making judgments, instead of acknowledging the need for more evidence.', '', 0, 0, NULL),
(21, 'Simplicity bias', '', 1, 6, 0, '', 'We discard specifics to form generalities, reduce events and lists to their key elements, and favour simple-looking options over complex, ambiguous ones. We favour the immediate, reliable and tangible things in front of us, simplify probabilities and numbers to make them easier to comprehend, and think we know what others are thinking, as it tends to make life easier. We also simplify our vision of life by projecting our current mindset and assumptions onto the past and future.', '', 0, 0, NULL),
(87, 'Factual/scientific information', '', 12, 1, 0, '', 'The availability, accessibility and dissemination of accurate and unbiased knowledge about the issue and practices at hand; understandable evidence conveyed without feelings or opinions about it.', '', 2, 0, NULL),
(22, 'Recency bias', '', 1, 7, 0, '', 'Favouring the latest information, we tend to make wrong conclusions by emphasizing and overestimating the importance of recent events, experiences and observations, over those in the near or distant past.', '', 0, 0, NULL),
(46, 'Physical capacity', '', 4, 3, 0, '', 'Strength and ability to perform essential physical actions.', '', 0, 0, NULL),
(118, 'Age', '', 7, 1, 0, '', '', '', 3, 0, NULL),
(38, 'Awareness and knowledge', '', 3, 3, 0, '', 'These concepts are interdependent but not interchangeable. Awareness is the consciousness of a fact (e.g., being conscious that violent discipline has negative consequences, and being cognizant that there are alternatives to it), whereas knowledge is associated with a deeper understanding of this information (e.g., understanding the reasons why violent discipline is hurtful, and being able to explain alternatives to it). It is important to keep in mind that people tend to ignore ‘negative’ information related to what they are doing, and can sometimes favour prior ‘evidence’ that reaffirms their actions. Perception is very selective.', '', 0, 0, NULL),
(27, 'Attention', '', 2, 1, 0, '', 'We might or might not notice what is put in front of us. We often wrongly assume that people are properly informed about existing options because these options have been communicated to them. But making sure that people are informed and paying attention to what is suggested, or that promoters of behaviours manage to capture the attention of their audience, are key steps for a new behaviour to be considered. This is made harder by the fact that people tend to only listen to information that confirms their preconceptions (confirmation bias).', '', 0, 0, NULL),
(34, 'Appeal', '', 2, 8, 0, '', 'Characterizes how attractive something is on a more emotional level. As understood in psychology, appeal is a stimulus – visual or auditory – that influences its targets’ attitude towards a subject. Many types of psychological appeals have been exploited by the advertising and marketing industry, such as fear appeal, sex appeal, genetic fallacy, or guilt by association.', '', 0, 0, NULL),
(37, 'Aspirations', '', 3, 2, 0, '', 'Personal goals and dreams, vision for future-self and hopes and ambitions for achieving things. Examples of these include aspiring to be the best parent possible; to be an independent woman; to be a successful student; etc. It reflects what someone truly desires in life.', '', 0, 0, NULL),
(45, 'Emotional wellbeing', '', 4, 2, 0, '', 'The emotional quality of someone’s everyday experience, the frequency and intensity of positive and negative feelings that make one’s life pleasant or unpleasant. High levels of stress can impair our ability to make choices and to perceive ourselves positively and as capable, and can paralyze change and adoption of positive practices, and, in some instances, result in adoption of negative coping mechanisms. Anxiety and mental distress are particularly frequent in emergency contexts. Trauma is a significant barrier to action.', '', 0, 0, NULL),
(104, 'Fiscal measures and incentives', '', 14, 5, 0, '', 'The use of taxes, expenditures or direct incentives to influence people’s actions and achieve social, economic and political objectives (e.g., conditional cash transfers in development and humanitarian situations).', '', 2, 0, NULL),
(36, 'Values', '', 3, 1, 0, '', 'What we perceive as good, right or acceptable, including our inner convictions of right and wrong, and of what good conscience requires. These principles are strong drivers of standard behaviours. Individual values are directly influenced by moral norms, and can be liberal or conservative. Some powerful values include individual and collective honour, caring for the family, loyalty, authority and respect, sanctity and purity, and liberty.', '', 0, 0, NULL),
(62, 'Decision context/frame', '', 6, 8, 0, '', 'The context in which a decision is made (including the physical place) as well as the way a decision is framed (e.g., how options are presented) have a strong influence on choosing a course of action, regardless of the rational analysis of these options. This concept is often referred to as ‘choice architecture’.', '', 2, 0, NULL),
(18, 'Anchoring', '', 1, 3, 0, '', 'Over-reliance on one trait of a subject or piece of information when making decisions. Anchoring often refers to people’s initial exposure to a piece of information (commonly a number) that serves as a reference point that influences subsequent opinions and judgements.', '', 0, 0, NULL),
(50, 'Social mobility', '', 4, 7, 0, '', 'A socio-economic process in which an individual, family, or group move to a new position within a social hierarchy, from job to job, or from one social class or level to another. Social mobility is also understood as the movement of certain categories of people from place to place. In many societies, mobility is an issue for women, in both senses of the term: they are blocked from rising to positions of power, but might also not be free or able to leave the household, interact with certain people, or get access to commodities and services, for cultural or safety reasons.', '', 0, 0, NULL),
(52, 'Confidence', '', 4, 9, 0, '', 'A person’s belief that she can succeed in creating change; feeling of trust in one’s own ability.', '', 0, 0, NULL),
(53, 'Self-image', '', 4, 10, 0, '', 'Many of our choices are impacted by the perception we have of ourselves and our role in our family, community and society. This perceived identity will often make us behave according to common stereotypes associated with our dominant identity (see meta-norms). This might prevent people from doing things that they are completely capable of, because they underestimate their abilities in accordance to the stereotype of their group.', '', 0, 0, NULL),
(54, 'Emotional intelligence', '', 4, 11, 0, '', 'The ability to recognize and process one’s own emotions and use these to assist thinking.', '', 0, 0, NULL),
(55, 'Self-control/Willpower', '', 6, 1, 0, '', 'Temptations and impulses affect our decisions and actions, including those that go against the path we had decided to follow and the goals we had set. We all face these struggles but we do not always have equal capacity when it comes to restraining or regulating these urges. When our mental resources are depleted (by stress, fatigue, etc.) our willpower goes down. Certain behaviours have a higher addictiveness than others.', '', 0, 0, NULL),
(56, 'Present bias', '', 6, 2, 0, '', 'People generally favour a smaller gain in the short run over a larger gain in the future, even sometimes consciously when considering trade-offs. We overvalue immediate rewards, which impairs our ability to make decisions to pursue longer-term interests that would benefit us more. This has multiple consequences, including the need to create rapid and small gains for people on the way to what can be a deeper change of behaviour with bigger rewards – bringing pieces of future benefit closer to the present.', '', 0, 0, NULL),
(35, 'Desire', '', 2, 9, 0, '', 'A powerful feeling of craving something, or of wishing for something to happen. This sense of longing follows a variety of core human drives, such as the need to bond, to possess what we do not have, to love and reproduce, to dominate, etc. Desire can be both conscious and unconscious.', '', 0, 0, NULL),
(39, 'Beliefs', '', 3, 4, 0, '', 'Convictions of what is true. There are multiple types of beliefs influencing attitudes, the main ones being:\n1) Effect beliefs: considering a causality chain to be true (X leads to Y); e.g., physically disciplining a child will make her/him a good adult.\n2) Holding personal convictions about what ‘needs’ to be done in a given situation, e.g., if a woman is seen walking with a man who is not her husband or relative, she needs to be punished.\n3) Personal normative beliefs: beliefs about what should be, what should happen, e.g., men should be primarily responsible for the honour of the family; women should report intimate partner violence to the police, etc.\nBeliefs are individual, but highly influenced by others. The probability of one person adopting a belief increases with the number of people already holding that belief.', '', 0, 0, NULL),
(19, 'Messenger effect', '', 1, 4, 0, '', 'The value we give to a piece of information is largely conditioned by its source. The level of trust, familiarity and credibility of a communication channel is a key driver of our receptiveness. An individual can be influenced in her judgement of a subject by the representative of that subject rather than by the subject itself.', '', 0, 0, NULL),
(20, 'Confirmation and belief bias', '', 1, 5, 0, '', 'People easily ignore or criticize information that contradicts their existing beliefs and assumptions, and filter it in a way that supports their preconceptions and fits their thinking. This is an automatic process we use naturally to seek affirmation of our views, which can draw us to focus on details that are irrelevant in the larger picture.', '', 0, 0, NULL),
(65, 'Descriptive norms', '', 8, 3, 0, '', 'A rule of behaviour that people engage in because they think other people in their reference group do the same thing. This belief about what other people do and what are typical behaviours is called ‘empirical expectations’. This is often ground for misconceptions and similar ‘pluralistic ignorance’.', '', 1, 0, NULL),
(43, 'Mindset', '', 3, 8, 0, '', 'A person’s way of thinking, a default attitude for addressing various situations that create a pre-disposition to adopt or reject certain behaviours, such as an innovative mindset, conservative mindset, a learning and growth mindset, etc.', '', 0, 0, NULL),
(10, 'Meta-norms', 'Social-Environment', 0, 11, 4, 'What defines and maintains the stratification, roles and power in a society.', 'Meta-norms are underlying ideologies and unwritten rules, deeply entrenched in people’s culture and identity, cutting across sectors and conditioning a large number of behaviours. These meta-norms have a direct and strong influence on individual drivers (e.g., a person’s attitude or self-efficacy) as well as an indirect one as they are expressed through several derivative social norms and practices (e.g., gender inequity and patriarchy expressed through female genital mutilation (FGM), gender-based violence (GBV), child marriage, etc.) and structural elements (e.g., gender ideologies and power differentials institutionalized in laws and systems).\nFor the distinction between social norms and meta-norms, the Behaviour Drivers Model borrows the terminology and extends the concept from Robert Axelrod’s work in the 1980s on social cooperation (Axelrod, 1986), in which he developed a theory that there is an upper norm ruling the fact that transgressors of lower-level norms are punished. In other words, a norm about norms. For him, this norm of enforcement is a ‘meta-norm’, and its existence is\na condition for norms to emerge and remain stable. His work is still explored and improved\nby various scientists today (for example Eriksson et al., 2017). In the BDM, following Axelrod’s idea, we extend this original concept to other second-order, deeper or overarching norms that also influence a range of social norms, but not simply by contributing to enforcing them (which is the case for the meta-norms related to the rule of law, the conflict resolution modalities and the decision-making patterns in families), but also sometimes by generating social norms (e.g., socialization processes, gender ideologies and perceptions of a child). So, we consider meta-norms as playing a role in both creating and maintaining social norms, and through these mechanisms, in preserving social organization, stratification, reproduction and power differentials among groups.', '', 1, 0, '{39,40,42,41,43,44,38}'),
(76, 'Quality of leadership', '', 9, 5, 0, '', 'The existence of effective leadership is necessary to steer the group in the right direction and sustain the community development process. A ‘good’ leader will be popular and trusted, supportive of dialogue and change, innovative, and foster inclusion.', '', 1, 0, NULL),
(77, 'Trigger/stimulus', '', 9, 6, 0, '', 'Community dynamics usually stem from a triggering factor, including the emerging alternatives we describe below, but also from more exogenic factors, such as the visit or interest of external agents of change, who can be from civil society, authorities or the international cooperation.', '', 1, 0, NULL),
(40, 'Past experience', '', 3, 5, 0, '', 'Researchers have shown that past experience helps form complex decisions. Memories of experiences, such as past failure and frustration with a behaviour, or negative experiences such as poor treatment by a service provider, will shape our attitude towards trying new things. At a deeper level, experiences as a child also drive behaviours of adults, including negative, violent or abusive behaviours. This replication concept is paramount in most psychological schools of thought. There is ample evidence of a link between perpetuating multiple forms of violence as an adult, and experiencing and/or witnessing violence, including domestic violence, as a child.', '', 0, 0, NULL),
(41, 'Intuitions', '', 3, 6, 0, '', 'Instinctive feelings regarding a situation or an idea, often formed from past experience. Intuitions involve emotionally charged, rapid, unconscious processes that contribute to immediate attitudes or decisions that don’t stem from reasoning. In other words, our brain might have already decided what to do in a situation before analysing options. Intuitions are one of the elements of automatic thinking. Laws and rules target our rational brain, whereas many decisions are made intuitively. Hunches drive many of our actions and we often rely more on guesses than facts.', '', 0, 0, NULL),
(51, 'Support', '', 4, 8, 0, '', 'The availability of trusted relatives or friends to encourage, aid and protect someone when needed.', '', 0, 0, NULL),
(88, 'Media agenda and narrative', '', 12, 2, 0, '', 'The way media outlets present what is newsworthy, and how the facts and stories are framed to cover a given topic. Narratives are rarely neutral, and considerably influence the audience’s attitude.', '', 2, 0, NULL),
(90, 'Marketing, brand messaging', '', 12, 4, 0, '', 'Companies promote messages and ideas in favour of their economic success, and develop campaigns to create more appeal. The most popular and trusted brands, with large audiences and benefiting from a positive image, can significantly influence the way consumers perceive certain products, ideas and situations, changing their decisions and behaviours.', '', 2, 0, NULL),
(95, 'Publicized change and stories', '', 13, 1, 0, '', 'People’s achievements made public. Human-interest stories of transformation told to inspire and promote similar change through exposure to successes and failures.', '', 0, 0, NULL),
(57, 'Procrastination', '', 6, 3, 0, '', 'We can be as good at delaying positive actions as we are at indulging sudden negative impulses (‘today is not the right day, there is still time’). Putting off decisions can be explained by the desire to use the present time for more satisfying actions, or by the complexity of making a change. In both cases, emotions are taking over and we forget about the longer-term plan, despite the cost of delayed action. Magnifying the consequences of action or inaction in respect to what will happen for our future-self is a classic programmatic answer to this problem.', '', 0, 0, NULL),
(119, 'Gender', '', 7, 2, 0, '', '', '', 3, 0, NULL),
(120, 'Lifecycle stage', '', 7, 3, 0, '', '', '', 3, 0, NULL),
(93, 'Word of mouth', '', 12, 7, 0, '', 'In advertising and marketing, word of mouth refers to the phenomenon that occurs following the introduction and ascendancy of a product or subject matter that has attracted the attention of a certain number of individuals. In societies where word of mouth is the main means for transferring information (e.g., certain nomadic groups), it demonstrates how significant passing information from person to person by oral communication can be.', '', 2, 0, NULL),
(83, 'Decision-making patterns', '', 10, 6, 0, '', 'How and by whom a course of action is selected in a family or a community will have a significant impact on people’s options for alternative behaviours. These processes can be simple or complex depending on who voices opinions, is consulted and valued, can oppose a decision, and who makes the final call. On certain issues, elder family members can play a significant role. In various religious and traditional societies, the preservation of the family’s reputation is seen as the responsibility of the man; but as a woman’s honour is directly tied to family honour, it is considered the men’s right to make important decisions about women’s lives, including controlling the access of their female kin to the outside world.', '', 1, 0, NULL),
(94, 'Exposure', '', 12, 8, 0, '', 'The availability of information is not synonymous with access to it. Depending on the means of communication, coverage by mass media, penetration of technology and occupation, people will have very different levels of access to information. Campaigns are designed to proactively expose a target audience to certain content and narratives, but the success in reaching the target audience varies.', '', 0, 0, NULL),
(58, 'Hassle factors', '', 6, 4, 0, '', 'Minor inconveniences that prevent people from acting. Sometimes, a step that requires a little time, paperwork to fill out, or a small investment are perceived as major complications that can disproportionately prevent us from acting.', '', 0, 0, NULL),
(71, 'Sensitivity to social influence', '', 8, 9, 0, '', 'Reflects the level of autonomy of a person. In a similar social environment, individuals are affected differently by the pressure coming from the group or the need to comply with collective identity and claim to membership.', '', 0, 0, NULL),
(102, 'Enforcement/security apparatus', '', 14, 3, 0, '', 'System enforcing the observance of law and order (justice, criminal and police systems), and in conflict situations, elements of control and repression (e.g., administration by an occupying power). In some countries, policing of what people do (e.g., policing water usage, religious practices, etc.).', '', 2, 0, NULL),
(103, 'Grievances against authorities', '', 14, 4, 0, '', 'Citizens who consider themselves in conflict with the government, who criticize the State’s capacity or willingness to deliver services, who criticize the authorities’ motives or legitimacy, who feel that their demands are not met or consider that the social contract has collapsed might all adapt their grievance practices accordingly (e.g., refusal to get their children vaccinated, refusal to vote, civil disobedience, violence, etc.).', '', 2, 0, NULL),
(28, 'Feasibility', '', 2, 2, 0, '', 'The extent to which the adoption of a new behaviour is perceived as feasible or not by a person in her actual situation (this is an individual self-assessment, non-objective).', '', 0, 0, NULL),
(47, 'Fatigue', '', 4, 4, 0, '', 'Being tired (and hungry) depletes cognitive resources and significantly affects our decision-making.', '', 0, 0, NULL),
(48, 'Skills', '', 4, 5, 0, '', 'Particular abilities and capacities to do something. Most skills are acquired through experience and/or deliberate learning. Examples of skills include parenting techniques and positive discipline, as well as life skills such as critical thinking, negotiation, conflict resolution and active citizenship.', '', 0, 0, NULL),
(49, 'Decision autonomy', '', 4, 6, 0, '', 'The ability to make one’s own decision.', '', 0, 0, NULL),
(66, 'Social pressure, rewards, sanctions, exceptions', '', 8, 4, 0, '', 'Several social norms exist because of the consequences of behaving in certain ways (anticipated opinion or reaction of others). What defines these norms is the social ‘obligation’ behind them and people’s belief that compliance will condition their acceptance or rejection by the group. On the negative side, sanctions can take many forms, such as stigma, avoidance, gossip, insults, violence, exile, etc. On the other side, when we follow the rules, we are socially rewarded (e.g., praised, honored). Exceptions are a set of circumstances under which breaking the norm would be acceptable.', '', 1, 0, NULL),
(67, 'Influence by powerholders/gatekeepers', '', 8, 5, 0, '', 'Those who benefit from a norm which helps consolidate their position of power can be directly involved in enforcing the norm to maintain the social status quo. A typical example of that is men’s domination over women, and its multiple expression through socially accepted forms of violence enforced by males. The subordinate group might not have the resources, such as authority, credibility, visibility, money, strength, or relational network, required to challenge the norm and its enforcement.', '', 1, 0, NULL),
(78, 'Socialization process', '', 10, 1, 0, '', 'The process of learning to behave in a way that is acceptable to the group based on societal beliefs, values, attitudes and examples, through which norms are learned and internalized by individuals. A person’s acquisition of habits, whether positive or negative, is due to their exposure to models that display certain traits when solving problems and coping with the world. Early gender socialization, for example, starts at birth and is a process of learning cultural roles according to one’s sex. Right from the beginning, boys and girls are treated differently and learn the differences between them, and between women and men. Parents and families are the initial agents who affect the formation of behaviours during childhood (children are told how to dress, which activities are for them or not, what role they should play as a boy or a girl, etc.). Peers are an additional source of influence during adolescence and play a key role in solidifying socially accepted gender norms: boys usually enforce toughness, competition and heterosexual prowess, whereas girls are pressured around appearance, proper behaviour and marriage, with an emphasis on their reproductive roles. This happens in home, school and discreet settings alike. Socialization may also occur more passively through role modelling: as an example of negative behaviours, boys may adopt abusive behaviours after witnessing domestic violence, or lose respect for their mother (and women at large) after witnessing violence against her. These day-to-day interactions as children and adolescents are one of the key drivers of social norms reproduction. As they are learned in developmental stages and important milestones in the life cycle, norms become connected to feelings of shame and guilt that become triggers of appropriate behaviour. As a result, compliance with norms often becomes automatic, rather than the result of internal rational deliberation.', '', 1, 0, NULL),
(79, 'Gender ideologies', '', 10, 2, 0, '', 'Gender roles are expressed at all levels and in all segments of society, and are reproduced through daily interactions. Concepts of masculinity and femininity are underlying ideologies translating into behavioural expectations for men, women, girls and boys. Manhood is sometimes used as justification for different forms of violent behaviours. Girls and women may be considered vulnerable and, therefore seen to need protection, which may translate into lower access to education, restrictions in travelling, and higher unemployment. Gender discrimination is often deeply rooted and perpetuated by leaders and communities, and can result in behaviours related to domestic violence, sexual harassment and abuse, child marriage, female genital mutilation and trafficking.', '', 1, 0, NULL),
(110, 'Cues to action', '', 15, 3, 0, '', 'Factors or devices that activate readiness to change. When the environment or the structural context in which decisions are made or practices are reproduced is altered, it can often result in a change of behaviour.', '', 2, 0, NULL),
(86, 'Legal compliance', '', 10, 9, 0, '', 'The enforcement of laws and regulations does not only rely on formal organisms: the respect of these rules requires a social norm of legal obedience. If the belief that nobody respects the laws is widespread, legal disobedience might be the norm. The term ‘meta-norm’ was created by Robert Axelrod specifically to designate the fact that there is an upper norm ruling the fact that transgressors of lower-level norms are punished: a norm about norms.', '', 1, 0, NULL),
(92, 'Entertainment industry', '', 12, 6, 0, '', 'The roles played by characters in movies, books and radio shows, as well as the overall narratives of these entertainment pieces, affect the mental models of viewers. Entertainment can carry messages and values (sometimes purposively in the case of entertainment education, or ‘edutainment’) that influence the decisions made by the audience. This influence is based on how relatable and/or inspiring the characters and situations are, and what consequences these fictional characters face.', '', 2, 0, NULL),
(98, 'Social movements', '', 13, 4, 0, '', 'Large-scale collective actions and campaigns based on shared identity and grievances, people engaged in a fight to change the social or political order (e.g., the early stages of the Arab Spring; Black Lives Matter in the Unites States; the #metoo movement; etc.).', '', 2, 0, NULL),
(80, 'Power dynamics', '', 10, 3, 0, '', 'Power is the ability to control and access resources, opportunities, privileges and decision- making processes. Power can be based on many distinctions including wealth, ethnicity, religion, class, caste, age or gender. Who controls or retains power over ‘subordinate’ family and community members dictates the practices of many in households and communities. Many protection and developmental issues are associated with male authority over women, and men’s desire to control women’s sexuality. Violence against women and violence against children often co-occur in families with a patriarchal family structure, featuring rigid hierarchies linked to gender and age. In other cases, positive relationships centred on listening, respect and empathy offer contexts in which dominance is not the governing factor.', '', 1, 0, NULL),
(82, 'Moral norms', '', 10, 5, 0, '', 'Principles of morality that people are supposed to follow. They are learned socially. Human rights, for example, as a global doctrine, represent the moral norms that the United Nations is trying to ensure are supported universally. The important question here is what individuals perceive as women’s and children’s rights, as this will condition the classification of certain practices as being inherently immoral or not (e.g., beating a woman).', '', 1, 0, NULL),
(1, 'Cognitive biases', 'Psychology', 0, 1, 1, 'The information my brain is willing to consider.', 'Cognitive biases refer to the use of mental models for filtering and interpreting information, often to make sense of the world around us. The human mind is lazy, and cognition requires all sorts of shortcuts to make sense of things. These shortcuts lead to errors: we make mistakes in reasoning, evaluating, remembering, and, as a result, choices are almost always based on imperfect information. Shortcuts are part of Automatic Thinking (as opposed\nto Deliberative Thinking), which is when someone draws conclusions based on limited information. Most of the time, people consider what automatically comes to mind to fill in missing information, associate the situation with what they already know, make assumptions, jump to conclusions, and eventually decide through a narrow frame depicting a biased picture of a situation. This brain process is widespread and implies less effort.\nFrom a social perspective, these mental models are linked to ways of thinking, often passed down across generations, which include stereotypes and ideologies.', '', 0, 0, '{6,7,8}'),
(3, 'Attitude', 'Psychology', 0, 3, 1, 'My opinion about a behaviour; how I feel about it.', 'An attitude is what someone thinks or feels about something. Mixing cognitive and emotional elements, attitude defines people’s predisposition to respond positively or negatively to an idea, a situation, or a suggested change. It is one of the key drivers of an individual’s choice of action, and probably the most crucial factor shaping behaviour change among psychological elements.\nSocio-economic background, religion and other individual characteristics are important drivers of an attitude. When measuring attitude during surveys, the ‘demographics’ questions will help to cross-reference these respondents’ characteristics and allow for a better understanding of their influence.', '', 0, 0, '{9}'),
(29, 'Potential gains/avoided losses', '', 2, 3, 0, '', 'The benefits that the person thinks she might get from change, especially in the short term (rapid gains tend to matter more in decision-making). These gains are not only material, but can be in terms of relationships, image, etc. Gains should also be understood as ‘avoided losses’, since a loss is often seen as much worse than its equivalent in gain is perceived as positive (human ‘loss aversion’).', '', 0, 0, NULL),
(81, 'Conflict resolution', '', 10, 4, 0, '', 'Typical ways of solving family and community disagreements, from listening and trying to reach mutual understanding to practices of coercion.', '', 1, 0, NULL),
(101, 'Policies and regulations', '', 14, 2, 0, '', 'Set of principles and rules established by the authorities to regulate how people behave in society, which may prompt the community and its members to act and change (e.g., law criminalizing marital rape). The rule of law might or might not exist according to the context.', '', 2, 0, NULL),
(117, 'Action', '', 0, 7, 1, '', '', '', 0, 0, NULL),
(59, 'Habits and status quo', '', 6, 5, 0, '', 'The default option for humans is usually the status quo. We often feel more comfortable in a set routine, find inaction easier, feel overly positive about a choice previously made, and are averse to change because it can be risky. Many of these feelings will drive us towards inertia even if it is not in our best interest. Also, a significant share of our lives is habitual, and related actions are often automatic and driven by specific parts of the brain, associated with a context or a moment, following a ritual, and the very purpose of these actions loses importance. Bringing novelty into these mental patterns doesn’t come without friction and disruption.', '', 0, 0, NULL),
(60, 'Heuristics', '', 6, 6, 0, '', 'Heuristics are cognitive shortcuts or rules of thumb that simplify decisions. They are often grounded in similar cognitive biases our brains use to filter information (see cognitive biases), and make questions easier to answer. Since choosing can be difficult and requires effort, we use our intuition, make guesses, stereotype, or use what we describe as ‘common sense’ to avoid decision fatigue.', '', 0, 0, NULL),
(61, 'Inconsistent commitment', '', 6, 7, 0, '', 'Behavioural consistency tends to make us feel compelled to stick to a decision we have made, and keep on engaging in associated actions to maintain a positive self-image. Inconsistency can result in negative feelings towards ourselves. Nevertheless, in many situations our commitment may fade for several reasons, including insufficient willpower, opposition from other people, or a low cost of breaking the commitment. The existence of a more public, official commitment often supports continuity.', '', 0, 0, NULL),
(121, 'Social Status', '', 7, 4, 0, '', '', '', 3, 0, NULL),
(96, 'Innovations and opportunities', '', 13, 2, 0, '', 'A new vaccine made available, an agent of change visiting the community and offering support, a new method of contraception stimulating community discussion on family planning, or the renewal of political leadership, are examples.', '', 2, 0, NULL),
(23, 'Optimism bias', '', 1, 8, 0, '', 'People tend to overestimate the probability of positive events and underestimate the probability of negative ones, including the risks they face in comparison to other people. Similarly, we notice flaws in others more easily than we notice flaws in ourselves (also referred to as self-serving bias). We also imagine things and people we are familiar with or fond of as better.', '', 0, 0, NULL),
(97, 'Opinion trends', '', 13, 3, 0, '', 'How people’s views on a topic are changing; new directions taken by general beliefs and judgments. Public opinion is evolving continuously, at different paces.', '', 2, 0, NULL),
(8, 'Social Influence', 'Social-Environment', 0, 9, 3, 'How others affect what I think, feel and do.', 'Individual behaviours and decision-making are often driven by social factors. People are almost never fully autonomous thinkers, but rather influenced by, and concerned about others’ opinions and actions. We act as members of groups. How supportive a social environment\nis of individual change will sometimes condition the very possibility of change, in particular (but not only) when social norms are at play. Social norms are informal group rules influenced by the beliefs that members hold about what others in the group do and approve. Even in\nthe absence of sanctions, which can be central to several norms, such beliefs usually exist and influence individual practices, because people seek to comply with the group’s identity. Norms can be both positive and negative.', '', 1, 0, '{17,18,19,20,21,22,23,24,25}'),
(69, 'Social identity, compliance and display', '', 8, 7, 0, '', 'Complying with norms can be driven by an individual’s desire to belong to the group and manifest affiliation, even in the absence of actual sanctions. Adherence to the rules is then seen as a way to be recognized as a full member of the group. This can affect behaviours and other external signs such as ways to dress, to talk, etc.', '', 1, 0, NULL),
(70, 'Stigma and discrimination/societal views on minorities', '', 8, 8, 0, '', 'The negative and/or incorrect collective views and beliefs regarding certain groups of people strongly condition their practices and the majority’s behaviour towards them, often for the worst, leading to rejection and deprivation; e.g., in some instances rearing practices for children with disabilities.', '', 1, 0, NULL),
(74, 'Social cohesion', '', 9, 3, 0, '', 'The sense of belonging and feeling part of the group; the extent to which community members want to cooperate to solve collective issues; the level of interconnection between community members (density of the social network); the level of division into factions; and the level of trust for other members.', '', 1, 0, NULL),
(115, 'Contemplation', '', 5, 1, 0, '', 'Stage where a person is conscious of both the problem and option for change, and is considering switching to the new practice, but still has not acted.', '', 0, 0, NULL),
(116, 'Experience', '', 117, 0, 0, '', 'When an individual is acting and trying a new practice out; a change of behaviour in the short term, with a risk to abandon it.', '', 0, 0, NULL),
(84, 'Family roles and relationships', '', 10, 7, 0, '', 'Social norms related to what it means to be a grandparent, an elder sibling or a mother or father, and to how spouses communicate between themselves and interact with their children are important drivers of behaviours, in particular parenting practices and the provision of care, household chores and financial responsibilities, among others. These can impact girls and boys differently.', '', 1, 0, NULL),
(85, 'Perception of the child', '', 10, 8, 0, '', 'Different societies will have different perceptions of when a human being starts and stops being considered a child, and what this means in terms of her/his rights and needs. The overall understanding and value of who a child is and what she or he requires drives practices at different stages of the life cycle (child labour, child marriage, participation of children in family and public life, child enrolment in armed forces, etc.).', '', 1, 0, NULL),
(2, 'Interest', 'Psychology', 0, 2, 1, 'What I want; how appealing change is.', 'Interest characterizes how sympathetic people are to an alternative practice, how much they want to know about it, be involved in activities around it, or try it out. This combines some cost/benefit thinking with a dimension of appeal and desire on a more emotional level.', '', 0, 0, NULL),
(105, 'Religious institutions', '', 14, 6, 0, '', 'Religious institutions are the visible and organized manifestations of practices and beliefs in a group or society. They are translated in structures with specific agendas, power and leadership, and areas of influence, and aim to maintain or spread certain patterns of beliefs and associated actions. They largely influence behaviours of individuals and groups following them.', '', 2, 0, NULL),
(106, 'Education system', '', 14, 7, 0, '', 'The group of institutions (ministries of education and policies, schools and related associations, teachers, private and sometimes religious groups, etc.) that provide education to children and young people in educational settings, which can be public or private. The structure can vary significantly across contexts. Education systems are part of the group of entities influencing behaviours, including, in the longer term, as agents of socialization.', '', 2, 0, NULL),
(68, 'Strength of the norms', '', 8, 6, 0, '', 'The strength of normative influence is the result of multiple factors: how widespread a norm is, the importance of its social role, its alignment with personal attitudes, detectability, the consequences of non-compliance, the reference network structure (how dense and connected it is), etc.', '', 1, 0, NULL),
(14, 'Governing entities', 'Social-Environment', 0, 15, 5, 'How institutions influence what I do.', 'Institutions, ruling bodies, socio-political or armed groups try to structure and organize society through various forms of peaceful or violent interactions with the population in an attempt\nto control them. As a result, these governing entities play a paramount role in shaping individual behaviours, through several institutional features (laws, systems, enforcers, etc.), and at various levels – from local authorities to international institutions through national governments.', '', 2, 0, '{28,29,30,31,32}'),
(89, 'Social media', '', 12, 3, 0, '', 'Social media is an unpredictable and unregulated space where the audience is not only in a passive position, but can also be a content creator, and users can interact and collaborate with each other. Contrary to ‘mainstream media’, authoritative voices, previously unknown and sometimes without proven expertise, can emerge organically and generate large opinion trends and groups. Opinions relayed on social media fall within an individual’s own social network (group of individuals within the user’s ‘bubble’), which can distort the perception of what the most prevalent opinion is.', '', 2, 0, NULL);

-- END TABLE public.lu_drivers

-- BEGIN TABLE public.lu_frameworks
DROP TABLE IF EXISTS public.lu_frameworks CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_frameworks (
	id integer DEFAULT nextval('lu_frameworks_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	url text,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 1 row into public.lu_frameworks
-- Insert batch #1
INSERT INTO public.lu_frameworks (id, name, url) VALUES
(0, 'UNICEF Behavioural Drivers Model', 'https://www.unicef.org/mena/reports/behavioural-drivers-model');

-- END TABLE public.lu_frameworks

-- BEGIN TABLE public.lu_importance
DROP TABLE IF EXISTS public.lu_importance CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_importance (
	id integer DEFAULT nextval('importance_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"sequence" integer NOT NULL,
	color text,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 4 rows into public.lu_importance
-- Insert batch #1
INSERT INTO public.lu_importance (id, name, "sequence", color) VALUES
(1, 'Low', 1, 'black'),
(2, 'Medium', 2, 'blue'),
(3, 'High', 3, 'red'),
(0, 'Not relevant', 0, 'white');

-- END TABLE public.lu_importance

-- BEGIN TABLE public.lu_interventions
DROP TABLE IF EXISTS public.lu_interventions CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_interventions (
	id integer DEFAULT nextval('interventions_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	url_description text,
	text_short text,
	text_long text,
	"sequence" integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 44 rows into public.lu_interventions
-- Insert batch #1
INSERT INTO public.lu_interventions (id, name, url_description, text_short, text_long, "sequence") VALUES
(1, 'Multi-media campaigns', '(UNICEF, 2019)', 'consist of using a combination of traditional and non-traditional methods of communication to reach a target audience, deliver messages, educate, entertain, induce specific emotions, increase visibility, amplify the voice of communities and young people, leverage local creativity, or project transitional characters and role models in edutainment. ', 'When traditional financial education was not effective in South Africa, for example, a television soap opera was aired, in which financial messages were delivered through a central character. Following the show, there was a decrease in gambling and expensive instalment purchases (World Bank, 2015, p. 4). Communication channels are very diverse and can include localized options such as community radio, community cinema via mobile audio-visual vans, street theatre, puppet shows, etc. Trans-media approaches are used to reinforce ideas and messages across multiple media platforms, and 360-degree strategies link multimedia engagement with community engagement.', 10),
(2, 'Face-to-face dialogues', '(World Bank, 2015)', 'two-way communication in which partners respond to the concerns and interests of each other so that there is always a connection rather than a separation of unrelated monologues. ', 'This can happen in individual and group settings alike (e.g., listeners or viewers groups, community meetings, inter-generational dialogues, etc.). Exposition, perspective taking, perspective giving and feedback have important effects on behaviour change. During door-to-door activities, the quality of individual engagement can span from a simple standard message delivery to active listening approaches, and make or break the efficiency of the intervention.', 20),
(3, 'Digital communication', '(Fertig, Fishbane and Lefkowitz, 2018)', 'a specialized type of campaign that utilizes non-traditional media such as email, mobile phones, websites and online social hubs to reach different types of audiences. ', 'Tactics vary from leveraging the wide reach of social media and online influencers to using purposively created ICT platforms such as U-Report. In an experiment, researchers sent emails, text messages and push notifications to certain Mexican bank users’ mobile phones, with the subject “your future self has a message for you”. The contents all contained a link to a selfie filter that simulated a future old-age picture of the users. Underneath the picture read, “How much would you like to save for him/her to live well?”, coupled with a link to a savings page. The combined use of emails, text messages, and mobile software resulted in increased contributions, both in quantity and quality, toward savings.', 30),
(4, 'Private sector engagement', '(World Bank, 2013)', 'building a strategic and systematic partnership with businesses for development purposes. ', 'These coalitions can help advance and sustain social and behaviour change initiatives with the double purpose of designing solutions to improve our programme delivery and tapping into the popularity and audience of brands that benefit from a trusted image and widespread positive appeal to enhance the visibility and impact of communications. A number of companies embrace heavy digital multi-channel campaigns to engage consumers, with important reach and visibility. A step worth considering for a government that wants to jumpstart such engagement is holding private-sector assessment sessions. Kenya held a Private Health Sector Assessment in 2010, followed by an engagement workshop attended by the Ministries of Health and Medical Services, Public Health and Sanitation, Finance, and Planning, as well as private health training institutions, for-profit health providers and development partners. Similar assessment sessions were held in Guatemala in 2007, and the Republic of Congo in 2012', 40),
(5, 'Social movements', '', '', '', 50),
(7, 'Pre-testing', '', 'implementation of an intervention on a small scale to identify pros and cons of that intervention and the use thereof. ', 'For example, Hartmann and colleagues (2018) recently ran a pilot test of a low-cost, scalable intervention that aimed at reducing alcohol consumption and intimate partner violence (IPV). The intervention consisted of a small incentive for sobriety and cognitive behavioural therapy. The idea is not new in that evidence generated elsewhere is tested in a new context; however, it shows that pre-testing remains critical for efficient development of social and behavioural change interventions. When it comes to communication specifically, given the complexity of perception and appeal and the multiple cognitive biases at play, strong pre-testing approaches with various audience segments are absolutely necessary to maximize the chance of a cognitive and emotional impact.', 70),
(8, 'HCD', '(Wiener and Nagel, 1988)', 'an approach in solution development that focuses on the experience of users, e.g., what they need in a product, service or solution to a problem.', 'For example, research on specific cognitive processes and abilities of pilots has led to dramatic redesign of the cockpits: information is now grouped and displayed in a manner that is most accessible for pilots, thus minimizing ‘friction’ in their decisions-making processes (Wiener and Nagel, 1988). HCD has been increasingly used in the design of audience- driven communications to benefit from a better understanding of the people one is trying to reach, and the social groups and environments in which they live. Engaging communities in designing communications can not only improve the impact of communications but also put some critical voices (marginalized people, positive deviants, etc.) at the forefront. Before going to the public sphere, audience-centred communications will go through a number of quick trial and error iterations.', 80),
(9, 'Reevaluation exercises', '(for example Longmire-Avital et al., 2010 and Crutzen et al. 2017)', 'cognitive and affective assessments of one’s self-image, with and without the current practice, to understand how much behaviours are part of one’s identity – usually followed by training to increase problem-solving ability and self-efficacy. ', 'There are mixed results of this technique. For example, Crutzen et al. (2017) found that self-re-evaluation and anticipated regret did not change attitude or perceived distance in an online context. Others highlighted the importance of such self-reflection exercises in facilitating addictive behaviour change.', 90),
(12, 'Parenting programs', 'Gertler and colleagues (2014)', 'aim to provide parents with the skills, knowledge or resources to raise children to their full potential.', 'They are multi-faceted, and include working with national and local media to get information and effective messages out; training professionals to visit homes; providing guidance to parents and/or caregivers; conducting health or social centre- based activities on a one-to-one basis or in groups; caregivers exchange and peer support; etc. A longitudinal study by Gertler and colleagues (2014) found that growth-stunted Jamaican toddlers earned 25 per cent more as adults than their peers if their mothers received weekly training from community health workers in parenting skills and methods that promoted cognitive and socio-emotional skills in the children.', 120),
(14, 'Frontline workers trainings', '(Timme, 2012)', 'capacity building of frontline workers, such as health service providers, social workers, teachers, community volunteers, and many others, who are in direct contact with the population. ', 'These workers are often the backbone of service delivery outreach, and benefit from opportunities to engage with individuals and families during home visits, community group sessions, or at the point of service provision. Because of their critical role, frontline workers’ training focuses on strengthening their interpersonal communication, social mobilization and facilitation skills. When perceived as competent and compassionate, workers help improve trust in social services and capacity of communities for collective action, reinforce referral systems and influence the processes that lead to behavioural and social change. As an example, in 2011, UNICEF launched a community programme in Madagascar to train social health workers in interpersonal communication. These workers then came back to their communities to successfully engage members on the benefits of vaccination and latrine use for ending preventable under-5 child deaths.', 140),
(15, 'Behavioural Economics', '(World Bank, 2015, p. 4)', 'a field that studies the effects of psychological, emotional, cultural and social factors on the economic decisions of individuals and how those decisions deviate from standard models.', 'For example, with the understanding that human thinking works in two major lanes – fast or automatic, and slow or deliberative – researchers overcame a local challenge of short funding to buy insecticide-treated mosquito nets in Kenya by giving each household a metal box, a padlock and a passbook. While the funding was still short, mentally associating money for mosquito nets with ‘saving’ resulted in a 66 to 75 per cent increase in household investments in these nets.', 150),
(16, 'Behavioural Insights', '(Thaler and Sunstein, 2008 and OECD, 2017)', 'is defined by the Organisation for Economic Co-operation and Development (OECD) as an inductive approach to policymaking that combines insights from psychology, cognitive science and social science with empirically tested results to discover how humans actually make choices.', 'This field of work is based on human behavioural traits and intervention design experiments spread across multiple fields with successful results in education, energy, environment, finance, health and safety, labour, public service delivery, taxes and telecommunications. The term ‘nudging’ is commonly used to describe the use of choice architecture and behavioural tools and levers (prompts, reminders, commitment devices, social influence, etc.) to overcome cognitive biases.', 160),
(17, 'Value deliberations and framing', '(UNICEF, 2010a)', 'discussion of local cultural and social values that can lead to individual and collective empowerment, increase collective efficacy, spark collective action and build local institutions.', 'The organization of safe spaces for deliberations and debates is a key component of social norms interventions, given that norms shift at the group level. As an example, when simply preaching about the health risks that are related to female genital mutilation (FGM) cannot tackle the harmful practice from its roots, advocates should organize sessions to discuss how FGM violates human rights and local protective values such that communities could reassess social norms and local conventions within a broader context. Most importantly, this format of discussion allows communities to reflect on the individual and communal levels about the enduring yet harmful practice, which is most likely to facilitate changes.', 170),
(10, 'Life Skills and Empowerment', '(World Bank, 2015 and UNICEF, 2012)', 'personal development strategies to increase one’s ability to thrive in changing environments, e.g., by knowing how to increase autonomy, set realistic goals and fulfil personal potential.', 'To improve the well-being of stigmatized or marginalized individuals (such as low-caste, minor, poor, or unemployed people), it has been found effective to focus on helping these individuals build and think about their own strengths. In UNICEF, ‘life skills’ are defined as psychosocial abilities for adaptive and positive behaviours that enable individuals to deal effectively with the demands and challenges of everyday life. They are grouped into three broad categories:\ncognitive skills for analysing and using information,\npersonal skills for developing personal agency and managing oneself, and inter-personal skills for communicating and interacting effectively with others.\nThese approaches have been successfully used to empower adolescent girls and boys, including helping them to cope with the challenges of humanitarian situations and build their resilience, increasing self-esteem, self-awareness and self-confidence.', 100),
(11, 'Psycho-Social Support', '(Psychosocial Support, IFRC)', 'programmes provided to help “individuals and communities to heal the psychological wounds and rebuild social structures after an emergency or a critical event.', 'It can help change people into active survivors rather than passive victims” (Psychosocial Support, IFRC). These programmes contribute to the provision of holistic support in humanitarian situations. In terms of parenting in emergencies, for example, psycho-social support and stress-reduction will be key elements for allowing parents to play their role and limit families uptake of violent and negative coping behaviours. Interventions vary from proper counselling and case management to provision and communication of advice, including self- care and self-coping mechanisms.', 110),
(18, 'Positive norms promotion', '', 'leveraging the positive norms and values that exist in a group as a tool for change.', 'When only framed as ‘elimination of harmful practices’, programmes tend to reflect this negativity into the content of engagement on the ground. But this is sensitive: telling people what they do is wrong is not the best starting point, as some of these practices are inextricably tied to their social identity and ability to fit into their reference network. The identification of collective alternatives based on how people might better live their values if things changed, including positive religious, cultural and family values, often offers a better chance of success.', 180),
(19, 'Positive deviants approach', '(Bernard et al., 2014)', 'strategies developed for a community to look for and learn from uncommon yet successful attitudes and behaviours.', 'In 2010, a study was carried out in different villages in Ethiopia, in which individuals watched a one-hour documentary that showcased successful people who had come from similar (low) socio-economic backgrounds. Six months later, surveys showed that watching the examples of success had induced higher aspirations, improved savings, and increased spending on children’s schooling.', 190),
(20, 'Gatekeepers engagement', '(Bryld et al., 2017)', 'certain social practices are actively enforced by those who benefit from the social status quo, as the norm helps consolidate their position of power.', 'Partnering with and reassuring these particular stakeholders is often a condition to make local change possible. In some cases, gatekeepers will literally condition the possibility of accessing and working with a certain community, and their involvement in activities: the recognition of their role and that of the positive aspects of authority systems will be necessary for activities to take place.', 200),
(21, 'Bystanders training', '(Te and Khiev, 2018 and WHO, 2018)', 'programmes and curricula purposed to restrain the bystander effect (i.e., the more witnesses there are, the less likely each witness is to take action), raise awareness of related behaviours, and teach skills to recognize and intervene in intimate partner violence, sexual assault or harassment, sexual abuse of children or peer violence.', 'Examples of interventions include knowledge enrichment to increase understanding of why the bystander effect exists and how to identify implicit victims of covert crimes. Bystander intervention techniques are one of the key implementation strategies to change social norms featured in the INSPIRE handbook to reduce violence against children.', 210),
(22, 'Organized diffusion', '', 'is a pillar of most strategies that aim at scaling up social norms change.', 'Once critical reflection, collective commitment and change have been achieved ‘’privately’’ within a core group, the results of the deliberation are shared more widely amongst people who did not participate in the initial debates and mobilization, to spread the change outside of the initial community. In cases when norms are particularly powerful (actively enforced through social pressure, with guaranteed and significant consequences for deviants), new behaviors are likely to be possible only once a critical mass of people ready to change is reached, AND these people know about each other’s intentions. Communicating the shift of attitudes and expectations outside of the core group, and later outside of the community, is instrumental in reaching this tipping point at different scales. The practice of public commitment can also serve as a catalyst for wider communications efforts that disseminate new beliefs and practices outside of the community, especially when it involves respected influencers. Its organized diffusion is a way of bringing local change to scale, conveying communities’ choices.', 220),
(23, 'Civil Society Alliances', '(SUN Movement, 2017)', 'civil partnerships and organizations that are founded to tackle local harmful conditions or behaviours, and cooperate on a national, regional or global level under the coordination of a broader organization.', 'For example, the Scaling Up Nutrition (SUN) Movement devises and exploits its multi-stakeholder platforms across multiple countries to fight malnutrition. It increasingly engages in high-level politics, involves more sectors and stakeholders, distributes attention according to severity, audits coordinating structures, and strives to maintain momentum.', 230),
(24, 'Social comparison opportunities', '(Allcott, 2011 and Allcott and Rogers, 2014) ', 'provide individuals with opportunities to assess one’s own abilities, opinions and behaviours against others.', 'This process of self-evaluation relative to other people or groups happens automatically and implicitly, whenever we’re exposed to relevant information about others. But these opportunities can be created as a way to influence behaviours. Nudging through social comparison has a simple nature yet marked effect in changing practices. For example, Allcott (2011) and Allcott and Rogers (2014) report that giving individuals information about their neighbours’ energy consumption can reduce individual consumption by 2 per cent.', 240),
(25, 'Training resistance to social pressure', '(Thomas, McLellan and Perera, 2013)', 'training to develop skills to fight back compliance tendency, to commit to initial intentions and to anchor intended behaviour to personal values.', 'Previous academic work (Thomas, McLellan and Perera, 2013) has found that programmes that combine social competence and social influence training yielded positive results in helping school students to resist pressure – from their peers or the media – to start smoking. Social competence trainings aim to improve students’ life skills, such as “problem-solving and decision-making, cognitive skills for resisting interpersonal or media influences, increased self-control and self-esteem, coping strategies for stress, and general social and assertive skills” (Thomas, McLellan and Perera, 2013). Social influence trainings aim to increase awareness of the social influences that promote negative behaviours and teach people how to handle high-risk situations, as well as how to effectively refuse persuasion from any sources.', 250),
(26, 'Community-based approaches', '(UNICEF, 2019)', 'a local process that engages community members, raising their awareness of barriers and opportunities for development, developing a collective analysis of issues that affect them, and engaging them in critical reflection, participatory learning, collaborative action and joint assessment.', 'It is a process of change coming from the community and driven by the community. These participatory problem-solving interventions have been central to a number of SBC initiatives including as core components of programmes implemented at scale, such as the Global Programme on Ending Child Marriage or the global approach to Community-Led Total Sanitation (CLTS). They have had significant measurable effects on outcomes related to health, nutrition, education and child protection.', 260),
(27, 'Empowerment of CSOs, CBOs, FBOs', '(UNICEF, 2019 and UNFPA-UNICEF, 2017)', 'all keep close relationships with the communities and are critical partners that engage in development and humanitarian efforts. ', 'They exist organically within every community and have a strong influence over the local behavioural dynamics and social and moral orientation of their constituencies, thanks to the trust capital they have earned. They include faith based groups, family and parenting organizations, self-help groups, women’s support groups, savings and credit groups, farmers associations, trade unions and youth organizations. They can facilitate a level of dialogue and call to action that is unique to their communities and critical to implementing participatory research, planning, implementation, monitoring and social accountability processes. They also offer points of convergence to engage on issues spanning multiple sectors. For example, FBOs may play a key role by speaking out against child abuse and female genital mutilation while also promoting vaccination. As an example, the United Nations Population Fund (UNFPA) has collaborated with UNICEF to leverage the potential of partnering with CSOs and FBOs in the global programme to end child marriage. CSOs received master trainings to help adolescents (both in and out of school) to gain essential life skills, as well as to use participatory development tools to increase interactions among adolescents and their communities.', 270),
(28, 'Advocacy & Policy', '', 'is an increasingly important function for many non-profit organizations. In the social and economic development context, the aims of advocacy are to create or change policies, laws, regulations, distribution of resources or other decisions that affect people’s lives, and to ensure that such decisions lead to implementation. ', 'Good advocacy and advice helps transmit the message to ensure governments, lawmakers, the media and civil society hear it and act on it.', 280),
(29, 'Sectoral reforms', '(Kishore, 2011)', 'campaigns and programmes to change the current state of one or several aspects of a society/nation, such as public housing, health, education, etc.', 'There is no general formula for undertaking sectoral reforms; the process must start with a systematic analysis of the political economy and thus be case specific. For example, in around 2011, India went through radical changes to regulations of several sectors to address its pressing issues for national growth. For the financial sector, it increased the limits of authorized capital; for insurance, it invited more contractual savings institutions; for agriculture, it broke the state- level monopoly in regulation; for energy, it moved several regulated products to market pricing; for subsidy delivery, it transitioned from food, fertilizer and fuel subsidies to cash transfer and coupons; for foreign direct investment, it relaxed caps across the board; and for land management, it effected a national title registry to ameliorate real estate illiquidity.', 290),
(30, 'Social Mobilization', '(UNICEF, 2019)', 'focuses on uniting partners at the national and/or community levels for a common purpose.', 'It is a process of dialogue, coalition-building and group organization to rally multiple forces around a specific cause, from the public, private and civil-society sectors alike. It emphasizes collective efficacy and empowerment to create an enabling environment.', 300),
(31, 'Institutional partnerships', '', 'action taken by civic organizations, governments and other entities to create relationships between them and increase access to available resources to fulfil goals related to social change.', 'Specifically for social and behaviour change programming, partnerships can involve alliances between donors, academic institutions, practitioners, communities, private-sector entities, civil society and governments to diagnose, design, implement and evaluate interventions to change harmful behaviours. Partnerships are complex, diverse and increasingly vital to tackle development issues by mobilizing and unlocking the power of various stakeholders. Addressing the whole set of factors that drive behaviors can be quite overwhelming and not really fundable: social and behavior change can often only happen at scale through partnerships.', 310),
(32, 'Participation and Social Accountability', '(UNICEF, 2015)', 'policies to engage citizens or their representative agents in a process in which they can question public officials and service providers about their decisions and actions.', 'Examples include the Children’s Budget Clubs in Zimbabwe – an initiative that combined budget analysis, public hearings, and community scorecards to engage Children’s Clubs with policymakers; community scorecards in Kenya – an effort to inform service providers and rights holders of poor water quality; and the Cotton Campaign in Uzbekistan – a coalitional effort to stop forced labour (including children) by the Uzbekistan government in cotton harvesting that called for a boycott of Uzbek cotton.', 320),
(33, 'Systems strengthening', '(USAID, 2015)', 'any efforts that support an existing service structure, with actions to improve the provision, utilization, quality, efficiency and inclusiveness of services delivered through the system, and encourage the adoption of positive practices.', 'For example, the United States Agency for International Development (USAID) has set goals to strengthen health systems in many developing countries by strengthening human resources, health finance, health governance, health information, medical products, vaccines, technologies and service delivery (USAID, 2015). In Bangladesh, USAID started a Program Monitoring and Management Unit to monitor evaluation and reporting processes. In Liberia, it started emergency operations systems and improved disease surveillance and quality control laboratories. In Zimbabwe, it helped with the transition from paper-based records to electronic logistics management.', 330),
(34, 'Equity interventions', '', 'aim to distribute resources and provide access to services to those who have not enjoyed an equal share and are marginalized.', 'Vulnerability assessment and equity-focused data collection and analysis are the basis for developing programmes to meet the needs of people affected by poverty in order to close the attainment gap, but also to address the underlying drivers of inequity, which often appear even before a child is born.', 340),
(35, 'Social Protection', '(UNICEF 2010b)', 'aim to support vulnerable populations and target marginalized groups as participants and beneficiaries of services, goods and activities.', 'UNICEF (2010b) has found many benefits from using social protection mechanisms and approaches in reaching the Millennium Development Goals, i.e., tackling poverty, unemployment and hunger; bettering education and gender outcomes; and improving health care and reducing illness.', 350),
(36, 'Technological innovation', '', 'the development and use of new approaches and technologies to increase access to essential services, communicate life-saving information (e.g., U-Report and RapidPro), engage participants and connect them to institutions and opportunities. ', 'Examples include essential medicines, new communication mechanisms, improved WASH devices and agricultural breakthroughs.', 360),
(37, 'Market Shaping', '', 'the attainment of development goals is inextricably linked to the marketplaces that deliver commodities, including life-saving products to low-income populations.', 'Market shaping consists of influencing policies, manufacturers and distributors to produce and deliver enough high-quality and accessible products. UNICEF, for example, seeks to influence markets to achieve affordable prices, diversify supplier bases, build competitive market landscapes, and increase the availability of quality products, which are fit for purpose and appropriate for use by children. Significant focus has been placed on the sanitation and hygiene market, vaccine procurement (through an extensive market shaping effort with GAVI, the Vaccine Alliance) and nutrition markets. This is a highly strategic endeavour requiring an understanding of market forces, accurate forecasting and analysis, and engagement with various industries and players.', 370),
(38, 'Early Childhood Development', '', 'aim at two objectives: 1) parents and caregivers practicing nurturing care, positive parenting, and stimulating and learning activities; and 2) all young children, from conception up to the age of school entry, having equitable access to quality child care, health, nutrition, protection and early learning services to address their developmental needs.', 'ECD involves the use of comprehensive multi-sectoral programming packages delivered through a range of platforms (UNICEF, 2017) so children can achieve their full developmental potential. ECD helps mitigate the impact of adverse early experiences, which, if not addressed, lead to poor health, low educational attainment, economic dependency, increased violence and crime, and heightened risk of substance abuse and depression – all of which add to the costs and burden to society, and perpetuate cycles of poverty.', 380),
(39, 'Gender-transformative programming', '(UNICEF South Asia, 2018).', 'specifically seek to address harmful gender norms and inequalities, and promote alternative roles and behaviours to achieve outcomes that enable women, men, girls and boys to have equal opportunities and exercise their rights.', 'Such approaches go beyond raising awareness and focus instead on addressing underlying power relations and structural inequalities such as changing institutions and systems. ‘Gender- responsive programming’ is less transformative and refers to programmes in which the different needs of women, men, girls and boys have been considered, and measures have been taken to actively address them. ‘Gender-sensitive programming’ refers to programmes where gender roles and inequalities have been considered, and awareness of these issues has been raised, although appropriate actions may not necessarily have been taken.', 390),
(40, 'Educational Programming', '', 'a vast array of programmatic efforts that aim at improving the accessibility and quality of learning opportunities through strengthening inclusive and equitable education systems.', 'Interventions include the provision of quality learning materials, improvement of accountability systems, capacity development and training for quality teaching, community mobilization and training school management committees, provision of alternative education in emergencies, etc. Education is critical in changing societies not only because it is necessary for children to reach their potential and contribute to change, but also because a significant part of the socialization element, which underpins most social norms and future adults’ behaviours, happens in school where, it is hoped, children spend a large part of their lives.', 400),
(41, 'Rights protection and promotion', '', 'ensuring that the State and communities are able to identify the violation of rights of the most marginalized and enforce respect.', 'A human rights-based approach to programming (HRBAP) is a conceptual framework that is built on international standards of human rights and strives to promote human rights, as well as fight practices that violate these rights. HRBAP is based on four key principles: empowerment, participation, equality and non-discrimination, and accountability. The main focus of the approach is rights-holders and duty-bearers, and their capacities to claim and fulfil their obligations to human rights (HRBAP, UNICEF; see also HRBAP Portal, United Nations). In UNICEF, all programming follows the goal of realizing the rights of children and women as put forth in the Convention on the Rights of the Child (CRC) and Convention on the Elimination of Discrimination Against Women (CEDAW), but more direct strategic interventions include the monitoring and active advocacy for these rights, and approaches addressing the root causes of inequity so that all children, particularly those who suffer the worst deprivations in society, can access services and protection that are responsive to their needs.', 410),
(42, 'Adolescent empowerment', '(UNICEF, 2018)', 'the use of participatory interventions, interpersonal communication, digital innovations and media platforms to build the capacities of adolescents and their families to address harmful social norms and practices; support programmes which engage adolescents in identifying problems or issues which concern them and creating innovative adolescent-led solutions, working closely with adolescents and youth as partners.', '', 420),
(43, 'Social cohesion programming', '(Ortmans and Madsen, 2016, for a case study; and Gercama et al., 2018, for a retrospective study)', 'refers to a combination of various processes, mostly peacebuilding, strengthening democratic governance, fostering social inclusion, promoting social justice and mobility, building of social capital, and supporting access to livelihoods and basic services.', 'refers to a combination of various processes, mostly peacebuilding (solidification of peace, prevention of the continuation or reoccurrence of conflicts, reconciliation efforts, and management of differences and divisions), strengthening democratic governance (support of social dialogue, representation, civic engagement and participation in decision-making, social accountability, transparency and trust), fostering social inclusion (fighting exclusion with inequity-sensitive policies and financing, and protection systems for poor and marginalized people), promoting social justice and mobility (improvement of the distribution of wealth and opportunities for individual growth and participation in the economy), building of social capital (community empowerment to strengthen resources allowing – and resulting from – people’s cooperation toward common ends; these resources include social networks, civil society and community-based organizations, collective ownership of issues, key influencers and positive leadership for change, collective self-efficacy, and capacity capacity to mobilize for action), and supporting access to livelihoods and basic services (efforts to contribute to minimum living standards and welfare and ensure citizens’ satisfaction with service provision).\nAt a more local level, social cohesion programming refers to the development of a response mechanism that can help the factions in a community who are undergoing tension caused by disagreements on a societal issue. With the overwhelming influx of about 1 million Syrian refugees in 2011, Lebanese society faced a petrifying challenge. Search for Common Ground executed a project to create opportunities for interaction between the Lebanese host communities and the refugees, and organized capacity building events to empower individuals and to work on social cohesion.', 430),
(44, 'Stigma and discrimination reduction', '(Awad and Ourfali, 2017 and  Willis, n.d.)', 'at a collective level, programmes to change discriminatory social norms or eliminate structural barriers faced by marginalized people; at a more individual level, activities to help people learn the facts about who is being stigmatized, grow aware of personal attitudes and behaviour, avoid insensitive expressions, focus on the others’ contributions and be more inclusive.', 'UNICEF Syria has a cash transfer programme\nto support, on a bimonthly basis, Syrian families with children with complex disabilities. Zimbabwe’s AfricAid, through its Zvandiri Programme, trains HIV- positive adolescents to deliver counselling, training and advocacy activities that aim to reduce stigma towards children with HIV and help them gain confidence and skills to cope with stigma.', 440),
(13, 'Direct Capacity Building', '(Waterkeyn and Cairncross, 2005) ', 'activities that help individuals or organizations develop and retain skills, knowledge and tools needed to better their life or improve their performance.', 'A field experiment on open defecation in Makoni and Tsholotsho Districts of Zimbabwe set up Community Health Clubs and had trainers support community members with health knowledge and skills-building sessions. After two years, 2,400 latrines had been built by club members in Makoni, and 1,200 in Tsholotsho. Club members also reported practicing significantly better hygiene – including hand washing – than those not in the experiment.', 130),
(6, 'Elaboration likelihood approach', '(Angst and Agarwal, 2009)', 'based on two cognition routes: central route requiring elaboration and the quick and superficial peripheral route.', 'There are two main routes of information processing in human cognition. The central route is ‘persuaded’ by thoughtful elaboration of a topic, and the peripheral route is by quick, superficial ‘selling points’. The Elaboration Likelihood Model (ELM) provides conceptual guidance on how to structure and present a message to attract attention and make it persuasive (Angst and Agarwal, 2009). Multiple guidance tools exist on designing and framing communications so that they can appeal to both cognitive routes and not risk alienating either one, increasing the chances of bypassing certain cognitive biases.', 60);

-- END TABLE public.lu_interventions

-- BEGIN TABLE public.lu_library_types
DROP TABLE IF EXISTS public.lu_library_types CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_library_types (
	id integer DEFAULT nextval('library_types_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"sequence" integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 5 rows into public.lu_library_types
-- Insert batch #1
INSERT INTO public.lu_library_types (id, name, "sequence") VALUES
(1, 'article', 1),
(2, 'case study', 2),
(3, 'template', 3),
(4, 'evaluation', 4),
(5, 'data collection tool', 5);

-- END TABLE public.lu_library_types

-- BEGIN TABLE public.lu_participant_types
DROP TABLE IF EXISTS public.lu_participant_types CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_participant_types (
	id integer DEFAULT nextval('audience_types_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"sequence" integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 33 rows into public.lu_participant_types
-- Insert batch #1
INSERT INTO public.lu_participant_types (id, name, "sequence") VALUES
(1, 'infant', 10),
(2, 'young child', 20),
(3, 'girl child', 30),
(4, 'boy child', 40),
(5, 'adolescent', 50),
(6, 'adolescent girl', 60),
(7, 'adolescent boy', 70),
(8, 'adult', 80),
(9, 'man', 90),
(10, 'woman', 100),
(11, 'mother', 110),
(12, 'father', 120),
(13, 'grandparent', 130),
(14, 'grandmother', 140),
(15, 'grandfather', 150),
(16, 'mother-in-law', 160),
(17, 'father-in-law', 170),
(18, 'chief', 180),
(19, 'elder', 190),
(20, 'community leader', 200),
(21, 'community leader-man', 210),
(22, 'community leader-woman', 220),
(23, 'traditional healer', 230),
(24, 'traditional birth attendant', 240),
(25, 'teacher', 250),
(26, 'headmaster / principal', 260),
(27, 'community health worker', 270),
(28, 'nurse', 280),
(29, 'extension agent', 290),
(30, 'farmer', 300),
(31, 'farmer-woman', 310),
(32, 'farmer-man', 320),
(33, 'entrepreneur', 330);

-- END TABLE public.lu_participant_types

-- BEGIN TABLE public.lu_sem
DROP TABLE IF EXISTS public.lu_sem CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_sem (
	id integer DEFAULT nextval('sem_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	description text,
	"sequence" integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 5 rows into public.lu_sem
-- Insert batch #1
INSERT INTO public.lu_sem (id, name, description, "sequence") VALUES
(1, 'Individual', 'Characteristics of an individual that influence behaviours, including knowledge, attitudes, gender, age, self-efficacy, developmental history, religious identity, racial/ethnic identity, sexual orientation, economic status, financial resources, values, goals, expectations, literacy, stigma and others.', 1),
(2, 'Interpersonal', 'Formal and informal social networks and social support systems that can influence individual behaviours, including family, friends, peers, co-workers, religious networks, customs or traditions.', 2),
(3, 'Community', 'Relationships among organizations and informational networks within defined boundaries, including the built environment, local associations, community leaders, businesses, transportation, as well as social rules applying to the local community.', 3),
(4, 'Organizational', 'Organizations with rules, procedures and regulations to structure everyday life, including for operations that affect how, or how well, for example, services are provided for citizens.', 4),
(5, 'Policy/Enabling environment', 'Local, state, national and global laws and policies affecting the issue of interest, either as the promoters or barriers to interventions and changes.', 5);

-- END TABLE public.lu_sem

-- BEGIN TABLE public.lu_toc_types
DROP TABLE IF EXISTS public.lu_toc_types CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.lu_toc_types (
	id integer DEFAULT nextval('toc_categories_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	"sequence" integer NOT NULL,
	text_short text,
	text_long text,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 5 rows into public.lu_toc_types
-- Insert batch #1
INSERT INTO public.lu_toc_types (id, name, "sequence", text_short, text_long) VALUES
(1, 'input', 1, NULL, NULL),
(2, 'activity', 2, NULL, NULL),
(3, 'output', 3, NULL, NULL),
(4, 'outcome', 4, NULL, NULL),
(5, 'impact', 5, NULL, NULL);

-- END TABLE public.lu_toc_types

-- BEGIN TABLE public.measurements
DROP TABLE IF EXISTS public.measurements CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.measurements (
	id integer DEFAULT nextval('measurements_sampleid_seq'::regclass) NOT NULL,
	indicator_id integer NOT NULL,
	activ_sched_id integer NOT NULL,
	user_id integer NOT NULL,
	date date,
	value_quant real,
	value_text text,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.measurements contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.measurements


-- END TABLE public.measurements

-- BEGIN TABLE public.participants
DROP TABLE IF EXISTS public.participants CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.participants (
	id integer DEFAULT nextval('audiences_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	parent_id integer,
	name text NOT NULL,
	type_id integer NOT NULL,
	language_id integer,
	location_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.participants contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.participants


-- END TABLE public.participants

-- BEGIN TABLE public.project_users
DROP TABLE IF EXISTS public.project_users CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.project_users (
	id integer DEFAULT nextval('prj_users_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	access_id integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 3 rows into public.project_users
-- Insert batch #1
INSERT INTO public.project_users (id, prj_id, user_id, access_id) VALUES
(0, 1, 1, 1),
(1, 1, 2, 2),
(2, 2, 1, 2);

-- END TABLE public.project_users

-- BEGIN TABLE public.projects
DROP TABLE IF EXISTS public.projects CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.projects (
	id integer DEFAULT nextval('projects_sampleid_seq1'::regclass) NOT NULL,
	name text NOT NULL,
	private boolean DEFAULT true NOT NULL,
	country_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 2 rows into public.projects
-- Insert batch #1
INSERT INTO public.projects (id, name, private, country_id) VALUES
(1, 'Project 1', 'True', 89),
(2, 'Project 2', 'False', 120);

-- END TABLE public.projects

-- BEGIN TABLE public.risk_activities
DROP TABLE IF EXISTS public.risk_activities CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.risk_activities (
	id integer DEFAULT nextval('risk_activities_sampleid_seq'::regclass) NOT NULL,
	risk_id integer NOT NULL,
	activity_id integer NOT NULL,
	user_id integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.risk_activities contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.risk_activities


-- END TABLE public.risk_activities

-- BEGIN TABLE public.risks
DROP TABLE IF EXISTS public.risks CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.risks (
	id integer DEFAULT nextval('risks_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
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

-- Table public.risks contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.risks


-- END TABLE public.risks

-- BEGIN TABLE public.schedules
DROP TABLE IF EXISTS public.schedules CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.schedules (
	id integer DEFAULT nextval('activity_schedules_sampleid_seq'::regclass) NOT NULL,
	user_id integer NOT NULL,
	activity_id integer NOT NULL,
	planned_date_from date NOT NULL,
	planned_date_to date,
	actual_date_from date,
	actual_date_to date,
	owner_id integer,
	audience_id integer,
	status_id integer,
	url text,
	dependency_ids integer[],
	prj_id integer NOT NULL,
	notes text,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.schedules contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.schedules


-- END TABLE public.schedules

-- BEGIN TABLE public.test
DROP TABLE IF EXISTS public.test CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.test (
	id integer DEFAULT nextval('test_sampleid_seq'::regclass) NOT NULL,
	name text NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 2 rows into public.test
-- Insert batch #1
INSERT INTO public.test (id, name) VALUES
(1, 'test1'),
(2, 'test2');

-- END TABLE public.test

-- BEGIN TABLE public.toc
DROP TABLE IF EXISTS public.toc CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.toc (
	id integer DEFAULT nextval('theory_of_change_sampleid_seq'::regclass) NOT NULL,
	prj_id integer NOT NULL,
	user_id integer NOT NULL,
	name text NOT NULL,
	activity_id integer,
	toc_type_id integer NOT NULL,
	sem_id integer,
	description text,
	notes text,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.toc contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.toc


-- END TABLE public.toc

-- BEGIN TABLE public.toc_graph
DROP TABLE IF EXISTS public.toc_graph CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.toc_graph (
	id integer DEFAULT nextval('toc_graph_sampleid_seq'::regclass) NOT NULL,
	toc_from_id integer NOT NULL,
	toc_to_id integer NOT NULL,
	user_id integer NOT NULL,
	PRIMARY KEY(id)
);

COMMIT;

-- Table public.toc_graph contains no data. No inserts have been genrated.
-- Inserting 0 rows into public.toc_graph


-- END TABLE public.toc_graph

-- BEGIN TABLE public.users
DROP TABLE IF EXISTS public.users CASCADE;
BEGIN;

CREATE TABLE IF NOT EXISTS public.users (
	id integer DEFAULT nextval('users_sampleid_seq'::regclass) NOT NULL,
	email text NOT NULL,
	name text NOT NULL,
	last_project_id integer,
	PRIMARY KEY(id)
);

COMMIT;

-- Inserting 2 rows into public.users
-- Insert batch #1
INSERT INTO public.users (id, email, name, last_project_id) VALUES
(2, 'lisa@amplio.org', 'Lisa Zook', NULL),
(1, 'cliff@amplio.org', 'Cliff Schmidt', 1);

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
    dp.user_id,
    COALESCE(dp.importance_id, 0) AS importance_id,
    dp.notes_context,
    dp.notes_gap,
    dp.notes_goal
   FROM (public.lu_drivers ld
     LEFT JOIN public.drivers_in_prj dp ON ((ld.id = dp.lu_driver_id)));

DROP VIEW public.user_projects;

CREATE OR REPLACE VIEW public.user_projects AS
 SELECT p.id AS prj_id,
    p.name,
    p.private,
    p.country_id,
    pu.access_id,
    pu.user_id
   FROM (public.projects p
     JOIN public.project_users pu ON ((pu.prj_id = p.id)));

DROP VIEW public.users_in_project;

CREATE OR REPLACE VIEW public.users_in_project AS
 SELECT u.id,
    u.email,
    u.name,
    pu.access_id,
    pu.prj_id
   FROM (public.users u
     JOIN public.project_users pu ON ((u.id = pu.user_id)));

