CREATE TABLE parents (parent TEXT, child TEXT);

INSERT INTO parents VALUES
  ('ace', 'bella'),
  ('ace', 'charlie'),
  ('daisy', 'hank'),
  ('finn', 'ace'),
  ('finn', 'daisy'),
  ('finn', 'ginger'),
  ('ellie', 'finn');

CREATE TABLE dogs (name TEXT, fur TEXT, height INTEGER);

INSERT INTO dogs VALUES
  ('ace',     'long',  26),
  ('bella',   'short', 52),
  ('charlie', 'long',  47),
  ('daisy',   'long',  46),
  ('ellie',   'short', 35),
  ('finn',    'curly', 32),
  ('ginger',  'short', 28),
  ('hank',    'curly', 31);

CREATE TABLE sizes (size TEXT, min INTEGER, max INTEGER);

INSERT INTO sizes VALUES
  ('toy',      24, 28),
  ('mini',     28, 35),
  ('medium',   35, 45),
  ('standard', 45, 60);


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT child FROM parents JOIN dogs WHERE dogs.name = parents.parent ORDER BY dogs.height DESC;


-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name, sizes.size FROM dogs JOIN sizes WHERE dogs.height >= sizes.min AND dogs.height <= sizes.max GROUP BY dogs.name;


-- [Optional] Filling out this helper table is recommended
CREATE TABLE siblings AS
  SELECT DISTINCT p1.child AS sibling_1, p2.child AS sibling_2 FROM parents AS p1 JOIN parents AS p2 ON p1.parent = p2.parent WHERE p1.child < p2.child;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || sibling_1 || " and " || sibling_2 || ", have the same size: " || sz1.size FROM siblings AS s JOIN size_of_dogs AS sz1 ON s.sibling_1 = sz1.name JOIN size_of_dogs AS sz2 ON s.sibling_2 = sz2.name WHERE sz1.size = sz2.size;


-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
CREATE TABLE height_stat AS
  SELECT fur, AVG(height) * 0.70 AS lower_bound, AVG(height) AS avg, AVG(height) * 1.30 AS upper_bound, MIN(height) AS min_h, MAX(height) AS max_h FROM dogs GROUP BY fur;

CREATE TABLE low_variance AS
  SELECT fur, max_h - min_h AS height_range FROM height_stat
    WHERE min_h >= lower_bound AND max_h <= upper_bound;