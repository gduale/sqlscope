from django.db import models
from django_cryptography.fields import encrypt


class Server(models.Model):
    ENGINE_CHOICES = [
        ("MySQL", "MySQL"),
        ("PostgreSQL", "PostgreSQL"),
    ]
    dn_or_ip = models.CharField(
        max_length=100, verbose_name="Domain name or IP address"
    )
    sql_user = models.CharField(max_length=100)
    sql_passwd = encrypt(models.CharField(max_length=100))
    creation_date = models.DateTimeField(auto_now_add=True)
    engine_type = models.CharField(
        max_length=10, choices=ENGINE_CHOICES, default="MySQL"
    )
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.dn_or_ip


class Server_status(models.Model):
    fk_server = models.ForeignKey(Server, on_delete=models.CASCADE)
    up_or_down = models.BooleanField()
    engine_version = models.CharField(max_length=200, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    # 0 -> master OK
    # 1 -> master KO
    # 2 -> slave OK
    # 3 -> slave KO
    replication_status = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Server_status"
        verbose_name_plural = "Server_status"


class Server_database(models.Model):
    fk_server = models.ForeignKey(Server, on_delete=models.CASCADE)
    database_name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)


class Engine_mysql_parameter(models.Model):
    fk_server = models.ForeignKey(Server, on_delete=models.CASCADE)
    datadir = models.CharField(max_length=200, null=True, blank=True)
    tmpdir = models.CharField(max_length=200, null=True, blank=True)
    max_connections = models.IntegerField(null=True)
    innodb_data_file_path = models.CharField(max_length=200, null=True, blank=True)
    innodb_open_files = models.IntegerField(null=True)
    innodb_page_size = models.IntegerField(null=True)
    innodb_read_only = models.BooleanField()
    innodb_sort_buffer_size = models.IntegerField(null=True)
    innodb_temp_data_file_path = models.CharField(max_length=200, null=True, blank=True)
    innodb_buffer_pool_size = models.IntegerField(null=True)
    innodb_log_file_size = models.IntegerField(null=True)
    innodb_flush_method = models.CharField(max_length=200, null=True, blank=True)
    query_cache_size = models.IntegerField(null=True)
    max_allowed_packet = models.IntegerField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class Engine_postgresql_parameter(models.Model):
    fk_server = models.ForeignKey(Server, on_delete=models.CASCADE)
    data_directory = models.CharField(max_length=200, null=True, blank=True)
    temp_buffers = models.CharField(max_length=200, null=True, blank=True)
    max_connections = models.IntegerField(null=True, blank=True)
    shared_buffers = models.CharField(max_length=200, null=True, blank=True)
    work_mem = models.CharField(max_length=200, null=True, blank=True)
    maintenance_work_mem = models.CharField(max_length=200, null=True, blank=True)
    effective_cache_size = models.CharField(max_length=200, null=True, blank=True)
    max_wal_size = models.CharField(max_length=200, null=True, blank=True)
    checkpoint_timeout = models.CharField(max_length=200, null=True, blank=True)
    default_statistics_target = models.IntegerField(null=True, blank=True)
    random_page_cost = models.FloatField(null=True, blank=True)
    effective_io_concurrency = models.IntegerField(null=True, blank=True)
    max_worker_processes = models.IntegerField(null=True, blank=True)
    max_parallel_workers = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)


class Engine_user(models.Model):
    fk_server = models.ForeignKey(Server, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
