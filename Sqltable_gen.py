import random


class Sql_table_generator:

    def __init__(self, tablename: str = ""):

        self.tablename = tablename
        self.result = ""

    # Possible tables: Name, Surname, Fullname, Email, Company, City, Region
    # only up to 100 recs :(

    def create_table(self, tablename: str, list_of_colnames: [str], list_of_types: [str]) -> str:

        """
        Function creates sql command to create new table with provided params.
        :param tablename: name of table to be created
        :param list_of_colnames: list of strings, containing names of columns to be created
        :param list_of_types:  list of strings, containing types of columns to be created
        :return:
        """
        assert len(list_of_colnames) == len(list_of_types), f' List of column names {len(list_of_colnames)} ' + \
                                                            ' has different length than' + \
                                                            f' list of types {len(list_of_types)}!'
        self.tablename = tablename

        _template = "CREATE TABLE {tablename} (\n\t{rows}\n);"

        list_of_rows = ["{col} {type}".format(col=col, type=type) for col, type in zip(list_of_colnames,list_of_types)]

        query = _template.format(tablename=self.tablename, rows=',\n\t'.join(list_of_rows))

        return query

    def create_inserts(self, values: [[]], amount: int = -1, shuffle=False) -> None:
        """
        Function create insert commands.
        :param values: list of lists with string values to be put into
        :param amount: number of inserts to be created
        :param shuffle: controls if data should be shuffled
        :return:
        """
        inserts = ""  # list of lists
        # check if all lists in values has proper length
        length = len(values[0])
        for i in values:
            if len(i) != length:
                raise Exception("All lists")

        # if amount not set, then going for length
        if amount == -1:
            amount = length
        if amount > length:
            raise Exception("Amount is higher than max length of datatable")

        # shuffling
        if shuffle:
            for d in values:
                random.shuffle(d)

        for i in range(amount):
            inserts += f"INSERT INTO {self.tablename}, VALUES( "
            for val in values:
                inserts += f"'{val[i]}',"

            # deleting last comma
            inserts = inserts[:-1]
            inserts += " );"

        self.result += inserts

    def save(self, path=""):
        newpath = ""
        if path.endswith(".txt"):
            newpath = path
        else:  # path.endswith("/") or path.endswith("\\"):
            newpath = path + f"SQL_buildup-{self.tablename}.txt"

        with open(newpath, "w") as target:
            target.write(self.result)



