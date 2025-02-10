-- public.average_ratings_by_category definition

-- Drop table

-- DROP TABLE public.average_ratings_by_category;

CREATE TABLE public.average_ratings_by_category (
	id bigserial NOT NULL,
	category_name varchar(255) NOT NULL,
	average_rating float8 NOT NULL,
	created_at timestamp(0) NULL,
	updated_at timestamp(0) NULL,
	CONSTRAINT average_ratings_by_category_pkey PRIMARY KEY (id)
);
CREATE INDEX average_ratings_by_category_category_name_index ON public.average_ratings_by_category USING btree (category_name);


-- public.categories definition

-- Drop table

-- DROP TABLE public.categories;

CREATE TABLE public.categories (
	category_id serial4 NOT NULL,
	"name" text NOT NULL,
	CONSTRAINT categories_name_key UNIQUE (name),
	CONSTRAINT categories_pkey PRIMARY KEY (category_id)
);
CREATE INDEX idx_category_name ON public.categories USING btree (name);


-- public.developers definition

-- Drop table

-- DROP TABLE public.developers;

CREATE TABLE public.developers (
	developer_id serial4 NOT NULL,
	developer_name text NOT NULL,
	developer_website text NULL,
	developer_email text NULL,
	privacy_policy text NULL,
	CONSTRAINT developers_developer_name_key UNIQUE (developer_name),
	CONSTRAINT developers_pkey PRIMARY KEY (developer_id)
);


-- public.ratings_distribution definition

-- Drop table

-- DROP TABLE public.ratings_distribution;

CREATE TABLE public.ratings_distribution (
	id bigserial NOT NULL,
	rating float8 NOT NULL,
	count int8 NOT NULL,
	created_at timestamp(0) NULL,
	updated_at timestamp(0) NULL,
	CONSTRAINT ratings_distribution_pkey PRIMARY KEY (id)
);
CREATE INDEX ratings_distribution_rating_index ON public.ratings_distribution USING btree (rating);


-- public.apps definition

-- Drop table

-- DROP TABLE public.apps;

CREATE TABLE public.apps (
	app_id serial4 NOT NULL,
	app_name text NOT NULL,
	app_unique_id text NOT NULL,
	developer_id int4 NULL,
	category_id int4 NULL,
	rating float8 NULL,
	rating_count int8 NULL,
	installs int8 NULL,
	min_installs int8 NULL,
	max_installs int8 NULL,
	"free" bool NULL,
	price float8 NULL,
	currency text NULL,
	"size" text NULL,
	minimum_android_version text NULL,
	released_date text NULL,
	last_updated text NULL,
	content_rating text NULL,
	ad_supported bool NULL,
	in_app_purchases bool NULL,
	editor_choice bool NULL,
	CONSTRAINT apps_app_unique_id_key UNIQUE (app_unique_id),
	CONSTRAINT apps_pkey PRIMARY KEY (app_id),
	CONSTRAINT apps_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id),
	CONSTRAINT apps_developer_id_fkey FOREIGN KEY (developer_id) REFERENCES public.developers(developer_id)
);
CREATE INDEX idx_category ON public.apps USING btree (category_id);
CREATE INDEX idx_content_rating ON public.apps USING btree (content_rating);
CREATE INDEX idx_price ON public.apps USING btree (price);
CREATE INDEX idx_rating ON public.apps USING btree (rating);