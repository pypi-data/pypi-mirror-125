<h1 align="center">JetORM</h1>
    <blockquote>The simple wrapper for work with databases.</blockquote>
</p>
<hr>

# Get started with JetORM!

# Connect with database
Connecting to the database:

## MySQL
An instance of the **mysql** class accepts **2** **mandatory** and **4** **optional** arguments as input
```python
from jetorm import mysql

mysql("host", "database", port=3306, 
      user="root", password="")
```

For example (*we have a local server and port 3306, database name - test*):

```python
db = mysql("127.0.0.1", "dbname")
```
## SQLite
An instance of the **sqlite** class accepts **1** mendotory argument as input
```python
from jetorm import sqlite

db = sqlite("dbfile.db")
```
P.S *In the form of an instance name of a mysql or sqlite class, we will use the db name*

# MySQL CRUD

## CREATE
In order to create a table, there is method `dispense`

Example:
```python
instance_of_the_mysql_class.dispense("table")
```
This method create table and it's create default field `id`

### Structure of a table
In order to create a table structure, there are several methods, we will analyze each.

#### Method name: *add*
This method takes 4 arguments as input:
`table: str, name_of_the_field: str, type: str, unsigned=True`

**JetORM MySQL Types:**
 - *int* (INT)
 - *varchar* (VARCHAR)
 - *text* (TEXT)
 - *dt:ct* (datetime current timestamp)
 - *id* (INDEX)
 - *bit* (BIT)
 - *bool* (BOOLEAN)
 - *tint* (TINYINT)
 - *bint* (BIGINT)
 
**Q**: *How to specify the field types correctly?*
**A**: A colon is placed after the type and the length of the values of this field is written. That is, if you have a VARCHAR field type, specify the length of values for it, for example, 255:
```python
db.add('table', 'name_of_the_field', 'varchar:255')
```
Another Example:
```python
db.add('table', 'log_date','dt:ct') 
``` 
This code will create a field with the **datetime** type and the default value of current timestamp

Example:
```python
db.add('table', 'money', 'bint')
```
This code will create a field with the *BIGINT* type

Example:
```python
db.add('table', 'number', 'int:8')
```
This code will create a field with an *INT* type and a value length of 8

#### Method name: *puts*
This method takes 4 arguments as input:
`table: str, column_values: dict, unsigned=True`
It's **create** and **insert** the data which you inputed

For example:
```python
db.puts('table', {'name': 'Alex', 'age': 18})
```
So it will create fields `name` and `age` and insert data `Alex, 18`

### INSERT
#### Method name: insert
The method responsible for inserting values takes **2** arguments: `table: str, column_values: dict`

For example:
```python
db.insert('table', {'name': 'John', 'age': 25})
```

Also there is method execute your sql:

```python
db.exec("YOUR SQL", values)
```

For example:
```python
db.exec("SELECT * FROM `table` WHERE `password` = %s", "qwerty123")
```

Besides that, if the data is not recorded, use this method:
```python
db.store()
```

## READ

### Load the cells
To get a cell from a table, you can use several methods:

 - `load`
 - `load_all`
 - `read`
 - `read_one`
 - `find`
 - `find_one`

#### Method name: `load`
This method returns a list with data
```python
db.load(table: str, ids: tuple)
```
For example:
```python
user = db.load('some_table', (1, 3))
```

#### Method name: `load_all`
This method returns all the cells
```python
db.load_all(table: str)
```
For example:
```python
all_users = db.load_all('some_table')
```

#### Method name: `read`
This method returns certain fields
```python
db.read(table: str, fields: tuple, sub_sql: str=None, *values)
```
For example:
```python
user = db.read('table', ('name',), "`password` = %s", 'qwerty')
```
or like this:
```python
user = db.read('table', ('age',))
```
#### Method name: `read_one`
This method is similar to the `read` method, but it's adds to the SQL query **`LIMIT 1`**


#### Method name: `find`
This method returns cell
```python
db.find(table: str, sql: str, *values)
```
For example:
```python
users = db.find('some_table', "`age` > 15")
```
or
```python
users = db.find('some_table', "`password` = %s", 'qwerty')
```

#### Method name: `find_one`
This method is similar to the `find` method, but it's adds to the SQL query **`LIMIT 1`**

### Sorting methods
#### Method name: `recent`
This method returns recent field
```python
db.recent(table: str, order_by_field: str)
```
For example:
```python
recently_id_user = db.recent('table', 'id')
```

#### Method name: `count`
This method returns number of entries
```python
db.count(table: str, sub_sql=None, *values)
```
For example:
```python
how_many_users = db.count('table')
```

or like this:
```python
user_exists = db.count('table', 'id = %s', 5)
```

### Viewing tables in the console
#### Method name: **`view`**


For example:
```python
two_users = db.view('table', (1, 2))
print(two_users)
```

#### Method name: **`view_all`**
Similar in meaning to the `load_all` method
For example:
```python
all_users = db.view_all('table')
print(all_users)
```

## UPDATE

#### Method name: **`update`**
This method is similar in syntax to the `puts` method, but unlike it, this method **updates** records

```python
db.update(table: str, column_values: dict, sub_sql=None, *values)
```
For example:
```python
db.update('table', {'name': 'Test'}, "`id` = %s", 10)
```
Then, in the cell with `id = 10`, the `name` field for the **Test** will be updated

or like this:
```python
db.update('table', {'name': 'Test'})
```

## DELETE

#### Method name: **`trash`**
This method deletes an entry
```python
db.trash(table: str, field_ids: tuple)
```
For example:
```python
db.trash('table', (1,4,5))
```
Then, in the cell with `id = 1, 4, 5` will be deleted.

#### Method name: **`trash_sql`**
This method is similar to `trash` method
```python
db.trash_sql(table: str, sub_sql: str, *values)
```
For example:
```python
db.trash_sql('table', "`id` < 5 OR `id` = %s", 6)
```
Then, in the cell with `id < 5` or `id = 6` will be deleted.

#### Method name: **`wipe`**
This method completely removes all records from the table
```python
db.wipe(table: str)
```
For example:
```python
db.wipe('table')
```
Then, all the cells will be deleted.

#### Method name: **`nuke`**
This method deletes the table
```python
db.nuke(table: str)
```
For example:
```python
db.nuke('table')
```
Then, the table will be deleted.

# SQLite CRUD
Uses the same methods as in MySQL CRUD (executes the same query), but the sturcture of the fields some different

### Structure of a table
**JetORM SQite Types:**
 - *int* (INT)
 - *varchar* (VARCHAR)
 - *text* (TEXT)
 - *dt:ct* (datetime current timestamp)
 - *id* (INDEX)
 - *bool* (BOOLEAN)
 - *tint* (TINYINT)
 - *bint* (BIGINT)

Unlike MySQL, the SQLite module does not have a BIT data type, so ***bool*** can be used instead.

CREATE, READ, UPDATE and DELETE methods SQLite module implements in the same way as the MySQL module.

p.s All **methods** and their **names**, **arguments** completely *coincide* with the mysql class.