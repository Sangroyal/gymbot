create table training_plan(
    codename varchar(255) primary key,
    user_id integer foreign key,
    daily_volume integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_exercise boolean,
    aliases text
);

create table exercises(
    id integer primary key,
    user_id integer foreign key,
    weight integer,
    reiteration integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_exercise, aliases)
values
    ("bench press", "жим", true, "жим штанги лежа, жим, жим лежа"),
    ("squats", "приседание со штангой", true, "присед, приседания"),
    ("deadlift", "становая тяга", true, "становая, тяга"),
    ("other", "прочее", false, "");

insert into training_plan(codename, daily_volume) values ('base', 2000);
