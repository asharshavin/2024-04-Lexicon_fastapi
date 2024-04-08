-- /** INIT 

DROP TABLE IF EXISTS public.full_names;

CREATE TABLE IF NOT EXISTS public.full_names
(
    name character(100) COLLATE pg_catalog."default",
    status smallint
);


DROP TABLE IF EXISTS public.short_names;

CREATE TABLE IF NOT EXISTS public.short_names
(
    name character(100) COLLATE pg_catalog."default",
    status smallint
);

INSERT INTO short_names (name, status)
SELECT
    LEFT(md5(random()::text), 8),
    CASE WHEN random() < 0.5 THEN 0 ELSE 1 END
FROM generate_series(1, 700000);

INSERT INTO full_names (name)
SELECT
    LEFT(md5(random()::text), 8) || '.' || LEFT(md5(random()::text), 3)
FROM generate_series(1, 500000);

--**/

--/** 1 вариант
-- explain analyze 
UPDATE full_names
SET status = t.status
FROM (SELECT short_names.status, full_names.name as name FROM full_names 
INNER JOIN short_names
ON short_names.name =  LEFT(full_names.name, LENGTH(full_names.name) - POSITION('.' IN REVERSE(full_names.name)))) AS t
WHERE full_names.name = t.name;
--**/

/** 2 вариант 
-- explain analyze 
WITH t AS (
	SELECT short_names.status, full_names.name as name FROM full_names 
	INNER JOIN short_names
	ON short_names.name =  LEFT(full_names.name, LENGTH(full_names.name) - POSITION('.' IN REVERSE(full_names.name)))
)

UPDATE full_names
SET status = t.status
FROM t
WHERE full_names.name = t.name;
**/


SELECT * from full_names WHERE status IS NOT NULL
