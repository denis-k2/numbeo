create table month (
  month_id integer CONSTRAINT PK_month PRIMARY KEY,
  month_name varchar(9)
);

insert into month (month_id, month_name) values (1, 'january');
insert into month (month_id, month_name) values (2, 'february');
insert into month (month_id, month_name) values (3, 'march');
insert into month (month_id, month_name) values (4, 'april');
insert into month (month_id, month_name) values (5, 'may');
insert into month (month_id, month_name) values (6, 'june');
insert into month (month_id, month_name) values (7, 'july');
insert into month (month_id, month_name) values (8, 'august');
insert into month (month_id, month_name) values (9, 'september');
insert into month (month_id, month_name) values (10, 'october');
insert into month (month_id, month_name) values (11, 'november');
insert into month (month_id, month_name) values (12, 'december');

