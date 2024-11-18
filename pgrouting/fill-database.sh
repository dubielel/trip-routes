set -e

echo DATA_DIR=${DATA_DIR:="/osm-data"}

DB_NAME="routing"

createdb $DB_NAME
psql --dbname $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql --dbname $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS pgRouting;"

for OSM_FILE in "$DATA_DIR"/*.osm; do
    echo "Processing $OSM_FILE"
    osm2pgrouting \
        --f $OSM_FILE \
        --conf $DATA_DIR/mapconfig.xml \
        --host /var/run/postgresql \
        --port 5432 \
        --dbname $DB_NAME \
        --username $POSTGRES_USER \
        --password $POSTGRES_PASSWORD

    # rm $OSM_FILE
done
