drop table if exists messages;
create table messages (
  id integer primary key autoincrement,
  plate text not null,
  state text not null,
  message text not null,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

drop table if exists subscribers;
create table subscribers (
    plate text not null,
    state text not null,
    phone_number text not null
);

insert into messages (plate, state, message) values ('CA', '123ABC', 'You are awesome');
insert into messages (plate, state, message) values ('CA', '123ABC', 'You are awesome :heart:');
insert into subscribers (state, plate, phone_number) values ('CA', '123ABC', '4081234567')

