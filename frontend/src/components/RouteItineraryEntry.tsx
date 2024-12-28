import { Key as ReactKeyProp } from 'react';

import { Accordion, AccordionSummary, AccordionDetails, Typography, Stack } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import dayjs from 'dayjs';

import { DAY_FORMAT } from '../constants';
import { RoutePlaceToVisitProperties } from '../store/reducers/routeSlice';
import { RouteItineraryEntryTable } from './RouteItineraryEntryTable';
import { MarkerColorBox } from './MarkerColorBox';
import { useDispatch } from 'react-redux';
import { setHoveredDayIndex } from '../store/reducers/internalSlice';

type RouteItineraryEntryProps = {
  places: GeoJSON.FeatureCollection<GeoJSON.Point, RoutePlaceToVisitProperties>;
  dayIndex: number;
  date: dayjs.Dayjs;
  entryKey: ReactKeyProp;
  color: string;
};

export const RouteItineraryEntry = ({ places, dayIndex, date, entryKey, color }: RouteItineraryEntryProps) => {
  const dispatch = useDispatch();
  return (
    <div
      onMouseEnter={() => {
        dispatch(setHoveredDayIndex({ hoveredDayIndex: dayIndex }));
      }}
      onMouseLeave={() => {
        dispatch(setHoveredDayIndex({ hoveredDayIndex: null }));
      }}
    >
      <Accordion defaultExpanded={true}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Stack
            direction="row"
            spacing={2}
            alignItems="center"
          >
            <MarkerColorBox color={color} />
            <Typography variant="h5">{date.format(DAY_FORMAT)}</Typography>
          </Stack>
        </AccordionSummary>
        <AccordionDetails>
          <RouteItineraryEntryTable
            places={places}
            entryKey={entryKey}
          />
        </AccordionDetails>
      </Accordion>
    </div>
  );
};
