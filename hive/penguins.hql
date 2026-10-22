-- Section 2 - Hive table and HiveQL

-- 1. Created database  and uploaded table from HDFS.

-- 2. Preview
SELECT * FROM penguins LIMIT 10;

-- 3a. Records per species and island
SELECT species, island, COUNT(*) AS num_records
FROM penguins
GROUP BY species, island
ORDER BY species, island;

-- 3b. Average body mass and flipper length per species
SELECT species,
       ROUND(AVG(body_mass_g), 2)       AS avg_body_mass_g,
       ROUND(AVG(flipper_length_mm), 2) AS avg_flipper_length_mm
FROM penguins
GROUP BY species;

-- 3c. Missing values in selected columns
SELECT
    SUM(CASE WHEN bill_length_mm    IS NULL THEN 1 ELSE 0 END) AS missing_bill_length_mm,
    SUM(CASE WHEN flipper_length_mm IS NULL THEN 1 ELSE 0 END) AS missing_flipper_length_mm,
    SUM(CASE WHEN body_mass_g       IS NULL THEN 1 ELSE 0 END) AS missing_body_mass_g,
    SUM(CASE WHEN sex IS NULL OR sex = '' THEN 1 ELSE 0 END)   AS missing_sex
FROM penguins;
