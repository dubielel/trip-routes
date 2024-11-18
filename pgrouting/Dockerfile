# Based on:
#   https://github.com/postgis/docker-postgis/blob/master/Dockerfile.template
#   https://github.com/pgRouting/docker-pgrouting/blob/master/Dockerfile.template

FROM postgres:16-bookworm

ENV DEBIAN_FRONTEND noninteractive

ENV PG_MAJOR 16
ENV POSTGIS_MAJOR 3

# TODO how to properly set the region from the docker-compose file?
ENV REGION europe/italy

RUN apt update

RUN apt-mark manual postgresql-$PG_MAJOR

# PostGIS part start
RUN apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR

RUN apt install -y --no-install-recommends \
    # ca-certificates: for accessing remote raster files;
    #   fix: https://github.com/postgis/docker-postgis/issues/307
    ca-certificates \
    postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
    postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts

WORKDIR /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh 10_postgis.sh
COPY ./update-postgis.sh /usr/local/bin
# PostGIS part end

WORKDIR /

# pgRouting part start
RUN apt install -y \
    postgresql-$PG_MAJOR-pgrouting \
    osm2pgrouting \
    osmctools

# pgRouting part end

RUN apt install -y wget

# Script for populating the database
WORKDIR /docker-entrypoint-initdb.d
COPY ./fill-database.sh .

# Copy the OSM data and mapconfig.xml
WORKDIR /osm-data
COPY ./osm-data/* .
RUN chmod -R a+rw *
RUN chmod a+x prepare-data.sh

RUN useradd -ms /bin/bash worker
RUN chown -R worker:worker /osm-data
USER worker

RUN ./prepare-data.sh /osm-data europe/italy "centro" "isole" "nord-est" "nord-ovest" "sud"

USER root
RUN rm prepare-data.sh
RUN chmod -R a+rw *

RUN rm -rf /var/lib/apt/lists/*