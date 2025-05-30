CREATE TABLE game(
id int,
name text,
designer text,
publisher text,
artist text,
yearpublished int,
minplayers int,
maxplayers int,
playingtime int,
minplaytime int,
maxplaytime int,
age int,
usersrated float,
average float,
bayesaverage float,
rank int,
rank_wg float,
numcomments int,
numweights int,
averageweight float,
stddev float,
median float,
owned int,
trading int,
wanting int,
wishing int,
userrating float,
image text,
category text,
mechanic text,
comment text,
player1 text,
player2 text,
player3 text,
player4 text,
player5 text,
player6 text,
player7 text,
player8 text,
player9 text,
player10 text,
player11 text,
player12 text,
player13 text,
player14 text,
player15 text,
player16 text,
player17 text,
player18 text,
player19 text,
player20 text,
description text,
exp text,
basegame text,
basegame_name text,
reimplement text,
reimplement_name text,
reimplemented text,
reimplemented_name text,
contains text,
contains_name text,
iscontained text,
iscontained_name text,
integration text,
integration_name text,
accessories text,
accessories_name text,
numplays text,
price float,
userweight text,
wishpriority text,
expansions text,
domain text,
family text,
age_poll text,
name_others text,
comments_GL text,
thumbs_GL text,
sold_GL text,
price_GL text,
currency_GL text,
user_GL text,
tags text,
tags_user text
);
\copy game FROM 'games.csv' DELIMITER ',' CSV NULL AS 'NULL'


CREATE TABLE name(
name text,
id int NOT NULL
);
\copy name FROM 'name.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE designer(
designer text,
id int NOT NULL
);
\copy designer FROM 'designer.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE designer_to_name(
designer_to_nameId int,
nameId int);

\copy designer_to_name FROM 'designer_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE artist(
artist text,
id int NOT NULL
);
\copy artist FROM 'artist.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE artist_to_name(
artist_to_nameId int,
nameId int);
\copy artist_to_name FROM 'artist_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE maxplayers(
maxplayers text,
id int NOT NULL
);
\copy maxplayers FROM 'maxplayers.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE maxplayers_to_name(
maxplayers_to_nameId int,
nameId int);
\copy maxplayers_to_name FROM 'maxplayers_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'


CREATE TABLE maxplaytime(
maxplaytime text,
id int NOT NULL
);
\copy maxplaytime FROM 'maxplaytime.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE maxplaytime_to_name(
maxplayetime_ti_nameId int,
nameId int);
\copy maxplaytime_to_name FROM 'maxplaytime_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE minplayers(
minplayers text,
id int NOT NULL
);
\copy minplayers FROM 'minplayers.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE minplayers_to_name(
minplayers_to_nameId int,
nameId int);
\copy minplayers_to_name FROM 'minplayers_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE minplaytime(
minplaytime text,
id int NOT NULL
);
\copy minplaytime FROM 'minplaytime.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE minplaytime_to_name(
minplaytime_to_nameId int,
nameId int);
\copy minplaytime_to_name FROM 'minplaytime_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE mechanics(
mechanics text,
id int NOT NULL
);
\copy mechanics FROM 'mechanics.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE mechanics_to_name(
mechanics_to_nameId int,
nameId int);
\copy mechanics_to_name FROM 'mechanic_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE age(
age text,
id int NOT NULL
);
\copy age FROM 'age.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE age(
age_to_nameId int,
nameId int);
\copy age_to_name FROM 'age_to_name.csv' DELIMITER ',' CSV NULL AS 'NULL'

