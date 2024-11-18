#!/bin/bash

DATA_DIR=$1; shift
REGION=$1; shift
SUB_REGIONS=("$@")

for subregion in "${SUB_REGIONS[@]}"; do
    echo "Processing $REGION/$subregion"

    OSM_FILE="$DATA_DIR/$subregion-latest.osm"

    PBF_FILE="$OSM_FILE.pbf"
    if [[ ! -f "$PBF_FILE" ]]; then
        echo "Downloading $REGION/$subregion-latest.osm.pbf"
        START_TIME=$(date +%s)
        wget -nv -O "$PBF_FILE" https://download.geofabrik.de/$REGION/$subregion-latest.osm.pbf
        END_TIME=$(date +%s)
        echo "Downloading took $(($END_TIME - $START_TIME)) seconds, $(du -h $PBF_FILE) size"
    fi;

    O5M_FILE="$OSM_FILE.o5m"
    echo "Converting $PBF_FILE to $O5M_FILE"
    START_TIME=$(date +%s)
    osmconvert $PBF_FILE --drop-author --drop-version --out-o5m -o=$O5M_FILE;
    END_TIME=$(date +%s)
    echo "Conversion took $(($END_TIME - $START_TIME)) seconds $(du -h $O5M_FILE) size"
    rm $PBF_FILE;

    echo "Filtering $O5M_FILE by highway=*"
    START_TIME=$(date +%s)
    osmfilter $O5M_FILE --keep="highway=" -o=$OSM_FILE;
    END_TIME=$(date +%s)
    echo "Filtering took $(($END_TIME - $START_TIME)) seconds $(du -h $OSM_FILE) size"
    rm $O5M_FILE;
done
