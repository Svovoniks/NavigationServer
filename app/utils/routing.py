import psycopg2 as ps
import os

closest_query = """SELECT id FROM result_2po_4pgr
    ORDER BY ST_Distance(geom_way, ST_SetSRID(ST_MakePoint({}, {}), 4326))
    LIMIT 1;"""

route_a_star = """SELECT r.x1, r.y1, r.x2, r.y2 FROM result_2po_4pgr AS r JOIN pgr_astar(
    'SELECT id, source, target, cost, reverse_cost, x1, y1, x2, y2 FROM result_2po_4pgr',
    {}, {},
    directed := true
) AS p ON r.id = p.node;"""

rouring_DB_name = os.environ['ROUTING_DB_NAME']
DB_user_name = os.environ['POSTGRES_USER']
DB_password = os.environ['POSTGRES_PASSWORD']
DB_host = os.environ['POSTGRES_HOST']
DB_port = os.environ['POSTGRES_PORT']

def get_route_a_star(start, dest):
    conn = ps.connect(f"dbname='{rouring_DB_name}' user='{DB_user_name}' host='{DB_host}' password='{DB_password}' port='{DB_port}'")
    with conn.cursor() as cursor:
        cursor.execute(closest_query.format(*start))
        point1 = cursor.fetchone()[0]

        cursor.execute(closest_query.format(*dest))
        point2 = cursor.fetchone()[0]

        cursor.execute(route_a_star.format(point1, point2))
        return cursor.fetchall()