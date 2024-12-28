import dayjs from 'dayjs';
import { RoutePlaceToVisitProperties } from '../store/reducers/routeSlice';
import { RouteItineraryEntry } from './RouteItineraryEntry';

import { DAY_MILISECONDS } from '../constants';

type RouteItineraryProps = {
  itinerary: GeoJSON.FeatureCollection<GeoJSON.Point, RoutePlaceToVisitProperties>[];
  firstDayTimestamp: number;
  colors: string[];
};

export const RouteItinerary = ({ itinerary, firstDayTimestamp, colors }: RouteItineraryProps) => {
  return itinerary.map((places, index) => (
    <RouteItineraryEntry
      key={`day-route-itinerary-${index}`}
      entryKey={`day-route-itinerary-${index}`}
      places={places}
      dayIndex={index}
      date={dayjs(firstDayTimestamp + index * DAY_MILISECONDS)}
      color={colors[index]}
    />
  ));
};
