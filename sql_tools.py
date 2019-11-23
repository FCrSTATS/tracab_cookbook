
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return(conn)

    except Error as e:
        print(e)

    return(conn)

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        "table created"
        # print("table created")
    except Error as e:
        print(e)

def convert_datatype_to_sql_type(type_str):
    """ turns a pandas datatype into a SQL datatype
        automatically assigns correct data types to each column.
        :param type_str pandas version
        :return SQL version
    """
    if type_str == "int64":
        return('integer')
    elif type_str == "float64":
        return('real')
    else:
        return('text')

def pandas_to_sql_table_creation(table_name, dat, connection, NOT_NULL_ = True):
    """ turns a pandas dataframe into a sql table
        automatically assigns correct data types to each column.
        :param table_name decide on the name of the SQL table to be created
        :param dat pandas dataframe ready for conversion
        :param connection - database connection created via create_connection(db_file)
        :param NOT_NULL_ blanket assigns all columns to be NOT_NULL or not
        :outcome create the table within the database
    """
    try:

        # convert datatype for each column into the SQL equivilent
        data_types_sql = [convert_datatype_to_sql_type(str(f)) for f in list(dat.dtypes)]

        # create the start of the table create SQL code, creates a Primary Key, as table_name_id
        table_create_str = """ CREATE TABLE """ +
                           table_name +
                           """ (""" +
                           table_name +
                           """_id integer PRIMARY KEY,"""

        # loop through each column and add to 'table_create_str' the column names, types and NULLS
        for c in range(len(dat.columns)):
            if NOT_NULL_:
                table_create_str += dat.columns[c] + " " + data_types_sql[c] + " NOT NULL,"
            else:
                table_create_str += dat.columns[c] + " " + data_types_sql[c] + ","

        # remove the last comma and add the SQL ending.
        table_create_str = table_create_str[:-1] + """ );"""

        # if there is a connection then action the create_table function with the newly formed SQL statements
        if connection is not None:
            create_table(connection, table_create_str)
            print(table_name + " successfully added to database")

    except:
        # error flagging if the above fails
        print(table_name + " ** FAILURE ** when adding table to database")


def create_sql_insert(table_name, column_names):
    """ Create the SQL INSERT base statement without values
        :param table_name previously created SQL table
        :param column_names columns names of the dat dataframe
        :return SQL statement string
    """
    columns_string = ""
    for i in column_names:
        columns_string += i + ","
    columns_string = columns_string[:-1]

    question_string = ""
    for i in column_names:
        question_string += "?,"
    question_string = question_string[:-1]

    sql = ''' INSERT INTO ''' + table_name + '''(''' + columns_string + ''') VALUES(''' + question_string + ''')'''

    return(sql)

def insert_a_row(table_name, dat, connection, row_index, id_to_print):
    """ takes one row of the pandas dataframe and inserts it into the newly created SQL table
        :param table_name previously created SQL table
        :param dat pandas dataframe ready for insertion
        :param connection - database connection created via create_connection(db_file)
        :param row_index row index of the dat dataframe
        :param id_to_print used for progress tracking
        :outcome insert a row into the SQL database
    """
    try:
        # get the raw SQL Statement without the values
        sql = create_sql_insert(table_name, dat.columns)

        # get datatypes to help with proper formatting of values prior to insertion
        data_types_sql = [convert_datatype_to_sql_type(str(f)) for f in list(dat.dtypes)]

        # list of values from the row
        values_raw = list(dat.iloc[row_index].values)

        # create an empty lists to append the correct values to
        values = []

        # loop through the values and datatypes and append the correctly formatted version
        for idx in range(len(values_raw)):
            if data_types_sql[idx] == "text":
                values.append(str(values_raw[idx]))
            elif data_types_sql[idx] == "integer":
                values.append(int(values_raw[idx]))
            elif data_types_sql[idx] == "real":
                values.append(float(values_raw[idx]))
            else:
                values.append(str(values_raw[idx]))

        # create the SQL tuple of values to add
        data_sql = tuple(values);

        # with the connection add the row of data into the SQL database.
        with connection:
            cur = connection.cursor()
            cur.execute(sql, data_sql)

    except:
        # error tracking 
        print(dat.iloc[row_index][id_to_print] + " *** FAILURE *** when adding to database into " + table_name)


