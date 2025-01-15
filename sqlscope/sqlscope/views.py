from django.shortcuts import render
from django.db.models import Max, OuterRef, Subquery
from .models import (
    Server,
    Server_status,
    Engine_mysql_parameter,
    Server_database,
    Engine_postgresql_parameter,
)


def dashboard(request):
    # Get the IDs of the latest statuses for each server
    latest_status_ids = (
        Server_status.objects.filter(fk_server__enabled=True)
        .values("fk_server")
        .annotate(latest_id=Max("id"))
        .values("latest_id")
    )

    # Retrieve the latest statuses
    latest_statuses = Server_status.objects.filter(id__in=latest_status_ids)

    # Create a list of dictionaries containing the desired information
    server_data = [
        {
            "dn_or_ip": status.fk_server.dn_or_ip,
            "up_or_down": status.up_or_down,
            "engine_version": status.engine_version,
            "replication_status": status.replication_status,
            "sql_user": status.fk_server.sql_user,
            "creation_date": status.creation_date,
        }
        for status in latest_statuses
    ]

    return render(request, "dashboard.html", {"server_data": server_data})


def about(request):
    return render(request, "about.html")


def engine_parameters(request):
    # Subquery to get the latest Server_status by fk_server
    latest_server_status = Server_status.objects.filter(
        fk_server=OuterRef("fk_server")
    ).order_by("-id")

    # Get MySQL parameters
    latest_mysql_parameter = Engine_mysql_parameter.objects.filter(
        fk_server=OuterRef("fk_server")
    ).order_by("-id")

    mysql_parameters = (
        Engine_mysql_parameter.objects.filter(
            fk_server__engine_type="MySQL",
            fk_server__enabled=True,
            id=Subquery(latest_mysql_parameter.values("id")[:1]),
        )
        .annotate(
            latest_engine_version=Subquery(
                latest_server_status.values("engine_version")[:1]
            )
        )
        .select_related("fk_server")
    )

    # Get PostgreSQL parameters
    latest_postgresql_parameter = Engine_postgresql_parameter.objects.filter(
        fk_server=OuterRef("fk_server")
    ).order_by("-id")

    postgresql_parameters = (
        Engine_postgresql_parameter.objects.filter(
            fk_server__engine_type="PostgreSQL",
            fk_server__enabled=True,
            id=Subquery(latest_postgresql_parameter.values("id")[:1]),
        )
        .annotate(
            latest_engine_version=Subquery(
                latest_server_status.values("engine_version")[:1]
            )
        )
        .select_related("fk_server")
    )

    context = {
        "mysql_parameters": mysql_parameters,
        "postgresql_parameters": postgresql_parameters,
    }
    return render(request, "engine_parameters.html", context)


def databases(request):
    # Get all servers that have databases
    servers = Server.objects.filter(server_database__isnull=False).distinct()

    # Create a dictionary of servers and their databases
    server_databases = {}
    for server in servers:
        server_databases[server] = Server_database.objects.filter(fk_server=server)

    context = {"server_databases": server_databases}
    return render(request, "databases.html", context)
