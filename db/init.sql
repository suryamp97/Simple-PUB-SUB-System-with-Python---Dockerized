CREATE DATABASE test;
use test;

create table publisher(pid int auto_increment PRIMARY KEY,pname varchar(50));
create table subscriptions (subid int auto_increment PRIMARY KEY, sname varchar(50), email varchar(70), topic varchar(50));

insert into publisher (pid,pname) values(1,"Rainbow6Game");
insert into publisher (pid,pname) values(0,"FarCrygame");
insert into publisher (pid,pname) values(0,"assassinscreed");

insert into subscriptions (subid,sname,email,topic) values(1, "subzy", "suryasathya97@gmail.com", "Rainbow6Game")
