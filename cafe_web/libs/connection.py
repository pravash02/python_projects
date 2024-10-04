from abc import abstractmethod


class DBConnection:

    __slots__ = ()

    def __init__(self, config):
        """
        Initializes the values for DBConnection class.

        :param config:
        """
        pass

    def __call__(self, *args, **kwargs):
        """
        Returns the connection object.

        :param args:
        :param kwargs:

        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def get_postgre_connection(cls):
        """
        create postgre connection

        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def get_mysql_connection(cls):
        """
        create mysql connection

        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def get_oracle_connection(cls):
        """
        create oracle connection

        :return:
        """
        pass

    @abstractmethod
    def get_dataframe(self):
        """
        Get the dataframe from Datasource

        :return:
        """
        pass



if __name__ == '__main__':
    con = DBConnection
