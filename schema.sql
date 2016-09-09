drop table if exists passwords;
create table passwords (
    id integer primary key autoincrement,
    title text not null,
    username text,
    password text,
    website text,
    description text
);

