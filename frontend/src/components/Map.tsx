import { useEffect, useRef } from 'react';

import { Map as MaplibreMap, Marker, type MapRef } from 'react-map-gl/maplibre';

import { useSelector } from 'react-redux';
import { RootState } from '../store/reduxStore';

import { chance } from '../utils/chance';
import { ACCOMMODATION_MARKER_COLOR } from './Accommodation';

type BoundingBox = [number, number, number, number];

const initialViewState = {
  longitude: 12.7058702,
  latitude: 41.1905539,
  zoom: 5,
} as const;

export const Map = () => {
  const {
    accommodation,
    placesToVisit: { features: placesToVisit },
  } = useSelector((state: RootState) => state.trip);

  const mapRef = useRef<MapRef | null>(null);

  useEffect(() => {
    const placesToDisplay = [accommodation, ...placesToVisit].reduce(
      (acc: GeoJSON.Feature<GeoJSON.Point>[], feature) => {
        if (feature) {
          acc.push(feature);
        }
        return acc;
      },
      [],
    );
    if (placesToDisplay.length === 0) {
      mapRef.current?.flyTo({
        center: [initialViewState.longitude, initialViewState.latitude],
        zoom: initialViewState.zoom,
      });
      return;
    }

    const bounds: BoundingBox = placesToDisplay.reduce(
      (bbox, feature) => {
        if (!feature || (feature.geometry.coordinates[0] === 0 && feature.geometry.coordinates[1] === 0)) {
          return bbox;
        }

        const [west, south, east, north] = bbox;
        const [lng, lat] = feature.geometry.coordinates;

        return [Math.min(west, lng), Math.min(south, lat), Math.max(east, lng), Math.max(north, lat)];
      },
      [Infinity, Infinity, -Infinity, -Infinity],
    );

    if (bounds.some((bound) => Math.abs(bound) === Infinity)) {
      return;
    }

    mapRef.current?.fitBounds(bounds, { maxZoom: 15, padding: 50, duration: 1500 });
  }, [accommodation, placesToVisit]);

  return (
    <MaplibreMap
      ref={mapRef}
      id="main-map"
      initialViewState={initialViewState}
      mapStyle="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
    >
      {accommodation && (
        <Marker
          longitude={accommodation.geometry.coordinates[0]}
          latitude={accommodation.geometry.coordinates[1]}
          color={ACCOMMODATION_MARKER_COLOR}
        />
      )}
      {placesToVisit.map((placeToVisit) => {
        return (
          <Marker
            key={chance.guid()} // This is a workaround for changing the color of the marker: component does not re-render when color prop changes
            color={placeToVisit.properties.markerColor}
            longitude={placeToVisit.geometry.coordinates[0]}
            latitude={placeToVisit.geometry.coordinates[1]}
          />
        );
      })}
    </MaplibreMap>
  );
};
