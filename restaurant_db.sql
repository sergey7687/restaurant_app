create table guests (
  guest_id smallint unsigned not null auto_increment,
  guest_f_name varchar(20) not null,
  guest_l_name varchar(20) not null,
  guest_phone varchar(20) not null,
  guest_email varchar(20) not null,
  guest_address varchar(20) not null,
  guest_note text not null,
  create_date timestamp default current_timestamp,
  constraint pk_guest_id primary key (guest_id)
 );
 
 create table department (
 dept_id smallint unsigned not null auto_increment,
 dept_name varchar(20) not null,
 constraint pk_dept primary key (dept_id)
 );
 
 create table menu (
 pos_id smallint unsigned not null auto_increment,
 pos_name varchar(20) not null,
 pos_price varchar(20) not null,
 constraint pk_pos primary key (pos_id)
 );

  create table employee (
 emp_id smallint unsigned not null auto_increment,
 emp_f_name varchar(20) not null,
 emp_l_name varchar(20) not null,
 dept_id smallint unsigned not null,
 emp_email varchar(20) not null,
 emp_phone varchar(20) not null,
 constraint pk_employee primary key (emp_id),
 constraint fk_dept_name foreign key (dept_id) references department (dept_id)
  );
  
 
 create table orders (
 book_id smallint unsigned not null auto_increment,
 guest_id smallint unsigned not null,
 menu_pos text not null,
 executor_emp smallint unsigned not null,
 create_date timestamp default current_timestamp,
 constraint pk_book primary key (book_id),
 constraint fk_guest foreign key (guest_id) references guests (guest_id),
 constraint fk_executor foreign key (executor_emp) references users (user_id)
  );
  

 create table users (
 user_id smallint unsigned not null auto_increment,
 user_f_name varchar(50) not null,
 user_l_name varchar(50) not null,
 username varchar(50) not null,
 user_phone varchar(50) not null,
 user_email varchar(50) not null,
 password varchar(100) not null,
 register_date timestamp default current_timestamp,
 constraint pk_user primary key (user_id)
  );


 insert into menu (pos_name, pos_price) 
 values ('Позиция_1', 400);
 insert into menu (pos_name, pos_price) 
 values ('Позиция_2', 200);
 insert into menu (pos_name, pos_price) 
 values ('Позиция_3', 150);
 insert into menu (pos_name, pos_price) 
 values ('Позиция_4', 500);
 insert into menu (pos_name, pos_price) 
 values ('Позиция_5', 300);
insert into menu (pos_name, pos_price) 
 values ('Позиция_6', 600);
insert into menu (pos_name, pos_price) 
 values ('Позиция_7', 450);
 insert into menu (pos_name, pos_price) 
 values ('Позиция_8', 400);
 
 
 insert into department (dept_name) 
 values ('Кухня');
 insert into department (dept_name) 
 values ('Бар');
 insert into department (dept_name) 
 values ('Зал');
 insert into department (dept_name) 
 values ('Администрация');
 
 select * from users;
 delete from users where user_id = 1;

 
 