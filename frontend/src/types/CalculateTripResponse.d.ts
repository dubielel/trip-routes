import type { RoutePlaceToVisitProperties, RouteProperties } from '../store/reducers/routeSlice';

export declare type CalculateTripResponse = {
  route: GeoJSON.FeatureCollection<GeoJSON.Point, RoutePlaceToVisitProperties>[];
  geometry: GeoJSON.Feature<GeoJSON.MultiLineString, RouteProperties>;
};
