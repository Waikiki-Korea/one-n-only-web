create user tester1 with password 'testono';
alter user tester1 with superuser;
alter user tester1 with createdb;
alter user tester1 with createrole;
alter user tester1 with replication;
alter user tester1 with bypassrls;

CREATE DATABASE test_ono;
\c test_ono
alter role tester1 set client_encoding to 'utf-8';
alter role tester1 set timezone to 'Asia/Seoul';
grant all privileges on database test_ono to tester1;
