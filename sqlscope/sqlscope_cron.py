import os
import django
import psycopg2
import mysql.connector

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from sqlscope.models import (
    Server,
    Server_status,
    Engine_mysql_parameter,
    Engine_postgresql_parameter,
    Engine_user,
    Server_database,
)


def open_mysql_connection(host, user, password):
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password)
        if connection.is_connected():
            print("Connection successfully established to the MySQL database.")
            return connection
    except mysql.connector.Error as err:
        print(f"Error during MySQL connection: {err}")
        return None


def open_postgresql_connection(host, user, password, database):
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=database
        )
        if connection:
            print("Connection successfully established to PostgreSQL database.")
            return connection
    except psycopg2.Error as err:
        print(f"Error during PostgreSQL connection: {err}")
        return None


def close_sql_connection(connection, cursor=None, db_type="MySQL"):
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print(f"{db_type} connection closed.")
    except (mysql.connector.Error, psycopg2.Error) as err:
        print(f"Error while closing {db_type} connection: {err}")


def execute_mysql_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except mysql.connector.Error as err:
        print(f"Error during MySQL query execution: {err}")
        return None


def save_server_status(
    server, result_up_or_down, result_engine_version, result_replication_status
):
    new_status = Server_status(
        fk_server=server,
        up_or_down=result_up_or_down,
        engine_version=result_engine_version,
        replication_status=result_replication_status,
    )
    new_status.save()


def save_mysql_engine_parameter(parameter_to_save):
    new_engine_parameter = Engine_mysql_parameter(
        fk_server=parameter_to_save[0],
        datadir=parameter_to_save[1],
        tmpdir=parameter_to_save[2],
        max_connections=parameter_to_save[3],
        innodb_data_file_path=parameter_to_save[4],
        innodb_open_files=parameter_to_save[5],
        innodb_page_size=parameter_to_save[6],
        innodb_read_only=parameter_to_save[7],
        innodb_sort_buffer_size=parameter_to_save[8],
        innodb_temp_data_file_path=parameter_to_save[9],
        innodb_buffer_pool_size=parameter_to_save[10],
        innodb_log_file_size=parameter_to_save[11],
        innodb_flush_method=parameter_to_save[12],
        query_cache_size=parameter_to_save[13],
        max_allowed_packet=parameter_to_save[14],
    )
    new_engine_parameter.save()


def get_mysql_engine_users(connection, server):
    query_result = execute_mysql_query(connection, "select host, user from mysql.user;")
    if query_result:
        for host, username in query_result:
            new_user = Engine_user(fk_server=server, username=username, host=host)
            new_user.save()


def get_mysql_engine_parameters(connection, server):
    result_to_save = [server]
    my_queries = [
        "show global variables like 'datadir';",
        "show global variables like 'tmpdir';",
        "show global variables like 'max_connections';",
        "show global variables like  'innodb_data_file_path';",
        "show global variables like  'innodb_open_files';",
        "show global variables like  'innodb_page_size';",
        "show global variables like  'innodb_read_only';",
        "show global variables like  'innodb_sort_buffer_size';",
        "show global variables like  'innodb_temp_data_file_path';",
        "show global variables like  'innodb_buffer_pool_size';",
        "show global variables like  'innodb_log_file_size';",
        "show global variables like  'innodb_flush_method';",
        "show global variables like  'query_cache_size';",
        "show global variables like  'max_allowed_packet';",
    ]
    for query in my_queries:
        query_result = execute_mysql_query(connection, query)
        if query_result:
            for _ in query_result:
                result = _[1]
                if result == "OFF":
                    result = False
                elif result == "ON":
                    result = True
                result_to_save.append(result)
    save_mysql_engine_parameter(result_to_save)


def get_postgresql_engine_parameters(connection, server):
    result_to_save = [server]
    pg_queries = [
        "SHOW data_directory;",
        "SHOW temp_buffers;",
        "SHOW max_connections;",
        "SHOW shared_buffers;",
        "SHOW work_mem;",
        "SHOW maintenance_work_mem;",
        "SHOW effective_cache_size;",
        "SHOW max_wal_size;",
        "SHOW checkpoint_timeout;",
        "SHOW default_statistics_target;",
        "SHOW random_page_cost;",
        "SHOW effective_io_concurrency;",
        "SHOW max_worker_processes;",
        "SHOW max_parallel_workers;",
    ]

    for query in pg_queries:
        query_result = execute_postgresql_query(connection, query)
        if query_result:
            for row in query_result:
                # PostgreSQL retourne généralement une seule valeur par paramètre
                result = row[0]
                if isinstance(result, str):
                    if result.lower() == "off":
                        result = False
                    elif result.lower() == "on":
                        result = True
                result_to_save.append(result)

    save_postgresql_engine_parameter(result_to_save)


def execute_postgresql_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête PostgreSQL: {str(e)}")
        return None


def save_postgresql_engine_parameter(parameters):
    """
    Sauvegarde les paramètres PostgreSQL dans la base de données.
    :param parameters: Liste contenant [server, data_directory, temp_buffers, max_connections, ...]
    """
    new_engine_parameter = Engine_postgresql_parameter(
        fk_server=parameters[0],
        data_directory=parameters[1],
        temp_buffers=parameters[2],
        max_connections=parameters[3],
        shared_buffers=parameters[4],
        work_mem=parameters[5],
        maintenance_work_mem=parameters[6],
        effective_cache_size=parameters[7],
        max_wal_size=parameters[8],
        checkpoint_timeout=parameters[9],
        default_statistics_target=parameters[10],
        random_page_cost=parameters[11],
        effective_io_concurrency=parameters[12],
        max_worker_processes=parameters[13],
        max_parallel_workers=parameters[14],
    )
    new_engine_parameter.save()


# main loop on all servers
servers = Server.objects.all()
for server in servers:
    if server.enabled:
        if server.engine_type == "MySQL":
            connection = open_mysql_connection(
                server.dn_or_ip, server.sql_user, server.sql_passwd
            )
            if connection:
                result_up_or_down = True
                engine_version = execute_mysql_query(
                    connection, "show variables like 'version'"
                )
                for _ in engine_version:
                    result_engine_version = _[1]

                # Slave or master?
                query_result = execute_mysql_query(connection, "show slave status")
                server_is_slave = False
                if query_result:
                    for _ in query_result:
                        server_is_slave = True
                        Slave_IO_Running = _[10]
                        Slave_SQL_Running = _[11]
                        Seconds_Behind_Master = _[32]
                        if (
                            Slave_IO_Running == "Yes"
                            and Slave_IO_Running == "Yes"
                            and Seconds_Behind_Master == 0
                        ):
                            # Slave is OK
                            result_replication_status = 2
                        else:
                            # Replication not working!
                            result_replication_status = 3
                if server_is_slave is False:
                    # The server is master or alone.
                    result_replication_status = 0

                # Get engine parameter
                get_mysql_engine_parameters(connection, server)
                get_mysql_engine_users(connection, server)

                # Get databases list and save it
                databases = execute_mysql_query(connection, "show databases;")
                # Delete all existing databases for this server
                Server_database.objects.filter(fk_server=server).delete()
                # Create new database entries
                for database in databases:
                    new_database = Server_database(
                        fk_server=server, database_name=database[0]
                    )
                    new_database.save()

                close_sql_connection(connection, db_type="MySQL")

            else:
                # Unable to connect
                result_up_or_down = False
                result_engine_version = None
                result_replication_status = None

            # Save in database
            save_server_status(
                server,
                result_up_or_down,
                result_engine_version,
                result_replication_status,
            )
        else:  # PostgreSQL
            pg_connection = open_postgresql_connection(
                server.dn_or_ip,
                server.sql_user,
                server.sql_passwd,
                "postgres",
            )
            if pg_connection:
                result_up_or_down = True
                pg_cursor = pg_connection.cursor()

                # Get PostgreSQL version
                pg_cursor.execute("select version();")
                engine_version = pg_cursor.fetchall()
                for row in engine_version:
                    str_row = str(row[0])
                    result_engine_version = " ".join(str_row.split()[:2])

                # Get replication status for master
                # state = streaming -> replication OK
                pg_cursor.execute("select * from pg_stat_replication;")
                pg_stat_replication = pg_cursor.fetchall()
                if not pg_stat_replication:
                    # maybe do not execute this part if we are on a master.
                    # Get replication status for slave
                    pg_cursor.execute("select * from pg_stat_wal_receiver;")
                    pg_stat_wal_receiver = pg_cursor.fetchall()
                    if not pg_stat_wal_receiver and not pg_stat_replication:
                        result_replication_status = 0
                    else:
                        if not pg_stat_wal_receiver:
                            result_replication_status = 3
                        else:
                            if "streaming" in pg_stat_wal_receiver[0]:
                                result_replication_status = 2
                            else:
                                result_replication_status = 3
                else:
                    if "streaming" in pg_stat_replication[0]:
                        result_replication_status = 0
                    else:
                        result_replication_status = 1

                # Get engine parameter
                get_postgresql_engine_parameters(pg_connection, server)

                # Save in database
                save_server_status(
                    server,
                    result_up_or_down,
                    result_engine_version,
                    result_replication_status,
                )

                # GET databases list and save it
                pg_cursor.execute("select datname from pg_database;")
                databases = pg_cursor.fetchall()
                # Delete all existing databases for this server
                Server_database.objects.filter(fk_server=server).delete()
                # Create new database entries
                for database in databases:
                    new_database = Server_database(
                        fk_server=server, database_name=database[0]
                    )
                    new_database.save()

            close_sql_connection(pg_connection, db_type="PostgreSQL")
            if pg_cursor:
                close_sql_connection(None, pg_cursor, db_type="PostgreSQL")
