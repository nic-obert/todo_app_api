
DATABASE = 'database.db'

DB_INIT = 'CREATE TABLE todos (\
    title VARCHAR (32) NOT NULL, \
    desc VARCHAR (1024) NOT NULL, \
    dateCreated VARCHAR (10) NOT NULL\
    );'

DB_FETCH = 'SELECT rowid, title, desc, dateCreated FROM todos'

DB_EDIT = 'UPDATE todos SET title=?, desc=? WHERE rowid=?'

DB_DELETE = 'DELETE FROM todos WHERE rowid=?'

DB_ADD = 'INSERT INTO todos VALUES (?,?,?)'
