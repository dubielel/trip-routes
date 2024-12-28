import { Key as ReactKeyProp, useMemo } from 'react';

import { TableContainer, Paper, Table, TableHead, TableCell, TableRow, TableBody } from '@mui/material';

import dayjs from 'dayjs';

import { RoutePlaceToVisitProperties } from '../store/reducers/routeSlice';
import { ACCOMMODATION_ROW_ID, TIME_FORMAT } from '../constants';
import { MarkerColorBox } from './MarkerColorBox';

const RouteItineraryEntryTableHeader = () => (
  <TableHead>
    <TableRow>
      <TableCell>Location</TableCell>
      <TableCell sx={{ width: '1px', whiteSpace: 'nowrap' }}>Arrival</TableCell>
      <TableCell sx={{ width: '1px', whiteSpace: 'nowrap' }}>Departure</TableCell>
      <TableCell
        align="right"
        sx={{ width: '1px', whiteSpace: 'nowrap' }}
      >
        Marker color
      </TableCell>
    </TableRow>
  </TableHead>
);

type RouteItineraryEntryTableRowProps = {
  location: GeoJSON.Feature<GeoJSON.Point, RoutePlaceToVisitProperties>;
};

const RouteItineraryEntryTableRow = ({ location }: RouteItineraryEntryTableRowProps) => {
  const { displayName, markerColor, arrivalTimestamp, departureTimestamp } = location.properties;

  const arrivalTime = useMemo(
    () => (arrivalTimestamp !== null ? dayjs(arrivalTimestamp).format(TIME_FORMAT) : ''),
    [arrivalTimestamp],
  );

  const departureTime = useMemo(
    () => (departureTimestamp !== null ? dayjs(departureTimestamp).format(TIME_FORMAT) : ''),
    [departureTimestamp],
  );

  return (
    <TableRow>
      <TableCell>{displayName}</TableCell>
      <TableCell align="center">{arrivalTime}</TableCell>
      <TableCell align="center">{departureTime}</TableCell>
      <TableCell
        align="center"
        sx={{ display: 'flex', justifyContent: 'center' }}
      >
        <MarkerColorBox color={markerColor} />
      </TableCell>
    </TableRow>
  );
};

type RouteItineraryEntryTableProps = {
  places: GeoJSON.FeatureCollection<GeoJSON.Point, RoutePlaceToVisitProperties>;
  entryKey: ReactKeyProp;
};

export const RouteItineraryEntryTable = ({ places, entryKey }: RouteItineraryEntryTableProps) => {
  const isEmptyRoute = useMemo(
    () =>
      places.features.length === 2 &&
      places.features[0].properties.rowId === ACCOMMODATION_ROW_ID &&
      places.features[1].properties.rowId === ACCOMMODATION_ROW_ID,
    [places.features],
  );

  return (
    <TableContainer component={Paper}>
      <Table>
        <RouteItineraryEntryTableHeader />
        <TableBody>
          {isEmptyRoute ? (
            <RouteItineraryEntryTableRow
              key={`${entryKey}-location-0`}
              location={places.features[0]}
            />
          ) : (
            places.features.map((location, index) => (
              <RouteItineraryEntryTableRow
                key={`${entryKey}-location-${index}`}
                location={location}
              />
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
