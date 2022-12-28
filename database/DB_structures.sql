-- CREATE TEST DB
CREATE DATABASE test;
-- CREATE SCHEMA
CREATE SCHEMA aws_ses;

-- GET SEND STATISTICS - SES

DROP VIEW IF EXISTS aws_ses.send_mail_statistics_informations;
DROP TABLE IF EXISTS aws_ses.send_mail_statistics;
CREATE TABLE aws_ses.send_mail_statistics(
	id serial NOT NULL,
	delivery_attempts int4 NULL,
	bounces int4 NULL,
	complaints int4 NULL,
	rejects int4 NULL,
	collect_timestamp timestamptz NULL,
	created timestamp NULL DEFAULT now(),
	CONSTRAINT send_mail_statistics_pkey PRIMARY KEY (id)
);

CREATE VIEW aws_ses.send_mail_statistics_informations AS 
SELECT
	date(sts.collect_timestamp) AS collect_date,
	sum(sts.delivery_attempts) AS delivery_attempts,
	sum(sts.bounces) AS bounces,
	sum(sts.complaints) AS complaints,
	sum(sts.rejects) AS rejects
FROM
	aws_ses.send_mail_statistics AS sts
GROUP BY 
	date(sts.collect_timestamp)
ORDER BY
	1;

-- ################################### -- 

-- GET METRIC STATISTICS

DROP VIEW IF EXISTS aws_ses.get_metric_statistics_informations;
DROP TABLE IF EXISTS aws_ses.get_metric_statistics;
CREATE TABLE aws_ses.get_metric_statistics(
	id serial NOT NULL,
	metric VARCHAR(255),
	statistic VARCHAR(255),
	totalizator DECIMAL(10,2),
	unit VARCHAR(255),
	collect_timestamp timestamptz NULL,
	created timestamp NULL DEFAULT now(),
	CONSTRAINT get_metric_statistics_pkey PRIMARY KEY (id)
);

CREATE VIEW aws_ses.get_metric_statistics_informations AS 
SELECT
	metric, 
	statistic,
	totalizator,
	unit,
	collect_timestamp
FROM
	aws_ses.get_metric_statistics
ORDER BY
	metric,collect_timestamp
;


-- ################################### -- 

-- VIEWS 

SELECT
	*
FROM
	aws_ses.get_metric_statistics_informations
;

SELECT
	*
FROM
	aws_ses.send_mail_statistics_informations 
;
