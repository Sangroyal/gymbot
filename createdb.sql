CREATE TABLE training_plan(
    codename VARCHAR(255) PRIMARY KEY,
    user_id INTEGER,
    daily_volume INTEGER
);

INSERT INTO training_plan(codename, daily_volume) VALUES ('base', 2000);

CREATE TABLE category(
    codename VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    is_base_exercise boolean,
    aliases text
);

INSERT INTO category (codename, name, is_base_exercise, aliases)
VALUES
    ("bench press", "жим", TRUE, "жим штанги лежа, жим, жим лежа"),
    ("squats", "приседание со штангой", TRUE, "присед, приседания"),
    ("deadlift", "становая тяга", TRUE, "становая, тяга"),
    ("other", "прочее", FALSE, "");

CREATE TABLE exercises(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    weight INTEGER,
    repetitions INTEGER,
    created datetime,
    category_codename INTEGER,
    name TEXT
    record_id INTEGER,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

--CREATE TABLE individual_plan(
--    user_id INTEGER PRIMARY KEY,
--    training_id INTEGER,
--    week_day TEXT,
--    repetition_id INTEGER,
--    weight INTEGER,
--    numb_of_reps INTEGER,
--    exercise_name TEXT
--    start_date,
--);
--
--CREATE TABLE users(
--    user_id INTEGER PRIMARY KEY,
--    name text,
--    sex INTEGER,
--    t_number VARCHAR(12),
--    weight INTEGER,
--    age INTEGER,
--    individual_plan_status text,
--    orders_count INTEGER,
--);



     )



