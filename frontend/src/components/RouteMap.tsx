import { FullscreenControl } from 'react-map-gl/maplibre';

import { Map } from '../components/Map';
import { MapLineLayer } from './MapLineLayer';

import { RouteProperties } from '../store/reducers/routeSlice';
import { chance } from '../utils/chance';

type RouteMapProps = {
  feature: GeoJSON.Feature<GeoJSON.MultiLineString, RouteProperties>;
};

export const RouteMap = ({ feature }: RouteMapProps) => {
  return (
    <Map mapId="route-map">
      <FullscreenControl position="top-left" />
      {feature.geometry.coordinates.map((points, index) => (
        <MapLineLayer
          key={`day-route-layer-${index}`}
          layerId={`day-route-layer-${index}`}
          route={{ type: 'LineString', coordinates: points }}
          dayIndex={index}
          color={feature.properties.colors.at(index) ?? chance.color({ format: 'hex' })}
        />
      ))}
    </Map>
  );
};
