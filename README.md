# BOSS直聘爬虫

* __auther__ = 'lcljcbx'

### 首先创建一个数据库，里面建两张表
```python
创建数据库 create database bosszb charset=utf8;
创建表city
create table city(
id int auto_increment primary key not null,
cityname varchar(255));
插入数据
insert into city values(0,'c101010100'),(0,'c101020100'),.....;
创建表job_category
create table job_category(
id int auto_increment primary key not null,
job_name varchar(255));
插入数据
insert into job_category values(0,'i502'),(0,'i503'), ........;
```
### 利用itertools 模块 进行排列组合关键字参数
### 添加代理，随机User-Agent,设置下载延时等反爬措施
### 利用scrapyd 部署

