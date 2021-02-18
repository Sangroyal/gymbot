CREATE TABLE training_plan(
    codename VARCHAR(255),
    user_id INTEGER,
    daily_volume INTEGER,
    PRIMARY KEY(codename)
);

INSERT INTO training_plan(codename, daily_volume) VALUES ('base', 2000);

CREATE TABLE category(
    codename VARCHAR(255),
    name VARCHAR(255),
    is_base_exercise BOOLEAN,
    aliases TEXT,
    PRIMARY KEY(codename)
);

INSERT INTO category (codename, name, is_base_exercise, aliases)
VALUES
    ('bench press', 'жим', TRUE, 'жим штанги лежа, жим, жим лежа'),
    ('squats', 'приседание со штангой', TRUE, 'присед, приседания'),
    ('deadlift', 'становая тяга', TRUE, 'становая, тяга'),
    ('other', 'прочее', FALSE, '');

CREATE TABLE exercises(
    id SERIAL,
    user_id INTEGER,
    weight INTEGER,
    repetitions INTEGER,
    created TIMESTAMP,
    category_codename VARCHAR,
    name VARCHAR(255),
    record_id SERIAL,
    PRIMARY KEY(id),
    FOREIGN KEY (category_codename) REFERENCES category (codename)
);

--CREATE TABLE individual_plan(
--    user_id INTEGER PRIMARY KEY REFERENCES training_plan (user_id),
--    training_id INTEGER,
--    week_day TEXT,
--    repetition_id INTEGER,
--    weight INTEGER,
--    numb_of_reps INTEGER,
--    exercise_name TEXT,
--    start_date TIMESTAMP
--);
--
--CREATE TABLE users(
--    user_id INTEGER PRIMARY KEY ,
--    name VARCHAR(30),
--    sex INTEGER,
--    t_number VARCHAR(12),
--    weight INTEGER,
--    age INTEGER,
--    individual_plan_status BOOLEAN,
--    orders_count INTEGER
--
--);







