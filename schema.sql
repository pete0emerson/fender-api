drop table if exists messages;
create table messages (
  id integer primary key autoincrement,
  plate text not null,
  message text not null
);

drop table if exists subscribers;
create table subscribers (
    plate text not null,
    phone_number text not null
);
