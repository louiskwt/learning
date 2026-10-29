CREATE TABLE pizzas (name TEXT, open INTEGER, close INTEGER);

INSERT INTO pizzas VALUES
  ("Artichoke", 12, 15),
  ("La Val's", 11, 22),
  ("Sliver", 11, 20),
  ("Cheeseboard", 16, 23),
  ("Emilia's", 13, 18);

CREATE TABLE meals (meal TEXT, time INTEGER);

INSERT INTO meals VALUES
  ("breakfast", 11),
  ("lunch", 13),
  ("dinner", 19),
  ("snack", 22);

CREATE TABLE opening AS 
    SELECT name FROM pizzas WHERE open < 13 ORDER BY name DESC;

CREATE TABLE study AS
    SELECT name, MAX(14 - open, 0) AS duration FROM pizzas ORDER BY duration DESC;

CREATE TABLE late AS
  SELECT p.name || " closes at " || p.close AS status
  FROM pizzas AS p JOIN meals AS m
  ON p.close >= m.time
  WHERE m.meal = "snack";

CREATE TABLE double AS
  SELECT m1.meal AS first, m2.meal AS second, p1.name
  FROM meals AS m1
  JOIN meals AS m2 ON m2.time > m1.time + 6  
  JOIN pizzas AS p1 ON p1.open <= m1.time AND m1.time <= p1.close AND p1.open <= m2.time AND m2.time <= p1.close;


CREATE TABLE finals AS
  SELECT "RSF" AS hall, "61A" as course UNION
  SELECT "Wheeler"    , "61A"           UNION
  SELECT "Pimentel"   , "61A"           UNION
  SELECT "Li Ka Shing", "61A"           UNION
  SELECT "RSF"        , "61B"           UNION
  SELECT "Wheeler"    , "61B"           UNION
  SELECT "Morgan"     , "61B"           UNION
  SELECT "Wheeler"    , "61C"           UNION
  SELECT "Pimentel"   , "61C"           UNION
  SELECT "Soda 306"   , "10"            UNION
  SELECT "RSF"        , "70";

CREATE TABLE sizes AS
  SELECT "RSF" AS room, 900 as seats    UNION
  SELECT "Wheeler"    , 700             UNION
  SELECT "Pimentel"   , 500             UNION
  SELECT "Li Ka Shing", 300             UNION
  SELECT "Morgan"     , 100             UNION
  SELECT "Soda 306"   , 80              UNION
  SELECT "Soda 310"   , 40              UNION
  SELECT "Soda 320"   , 30;

SELECT f.course, SUM(s.seats) AS total
  FROM finals AS f JOIN sizes AS s ON s.room = f.hall 
  GROUP BY f.course HAVING COUNT(*) > 1;

SELECT f1.course, COUNT(DISTINCT f2.hall) AS shared
  FROM finals AS f1 JOIN finals AS f2
  ON f1.course != f2.course AND f1.hall = f2.hall
  GROUP BY f1.course;