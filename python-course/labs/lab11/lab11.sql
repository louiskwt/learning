CREATE table newest AS
  SELECT title, year FROM titles ORDER BY year DESC LIMIT 10;


CREATE table dog_movies AS 
  SELECT t.title, p.character FROM titles AS t JOIN principals as p ON p.tconst = t.tconst 
    WHERE p.character LIKE "%dog%";


CREATE table leads AS 
  SELECT n.name, COUNT(p.tconst) AS lead_roles FROM names AS n JOIN principals as p ON p.nconst = n.nconst 
    WHERE p.ordering = 1 GROUP BY n.nconst HAVING COUNT(p.tconst) > 10;


CREATE table long_movies AS 
  SELECT ((t.year / 10) * 10) || "s" AS decade, COUNT(t.tconst) AS count FROM titles AS t
    WHERE t.runtime > 180 GROUP BY (t.year / 10) * 10;

