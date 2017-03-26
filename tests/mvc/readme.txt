Implementation of mvc with pyqt, qdesigner, python, sqlite

Our model derived from QAbstractTableModel

1. We pass an sqlite3 database nad a table to our model.
2. We get field names and data
3. First column must always be id. This is a read only column.
4. We implement a slot save2db who actually inserts or updates data to db
