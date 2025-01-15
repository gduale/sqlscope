from django.contrib import admin
from django.forms import PasswordInput
from .models import (
    Server,
    Server_status,
    Server_database,
    Engine_mysql_parameter,
    Engine_postgresql_parameter,
    Engine_user,
)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("dn_or_ip", "enabled", "creation_date")
    list_display_labels = {
        "dn_or_ip": "Domain or IP address",
    }
    formfield_overrides = {
        Server.sql_passwd.field.__class__: {"widget": PasswordInput(render_value=True)},
    }
    pass


@admin.register(Server_status)
class Server_status(admin.ModelAdmin):
    list_display = ("fk_server", "up_or_down", "engine_version")
    pass


@admin.register(Engine_mysql_parameter)
class Engine_parameter(admin.ModelAdmin):
    list_display = ("fk_server", "datadir", "tmpdir", "max_connections")
    pass


@admin.register(Engine_postgresql_parameter)
class Engine_postgresql_parameter(admin.ModelAdmin):
    list_display = (
        "fk_server",
        "data_directory",
        "max_connections",
        "shared_buffers",
        "work_mem",
    )
    pass


@admin.register(Engine_user)
class Engine_user(admin.ModelAdmin):
    list_display = ("fk_server", "username", "host")
    pass


@admin.register(Server_database)
class Server_database(admin.ModelAdmin):
    list_display = ("fk_server", "database_name")
    pass
