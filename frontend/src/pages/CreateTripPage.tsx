import { Divider, Stack, Grid2 as Grid } from '@mui/material';

import { TravelDates } from '../components/TravelDates';
import { Accommodation } from '../components/Accommodation';
import { TravelTime } from '../components/TravelTime';
import { Map } from '../components/Map';
import { PlacesToVisit } from '../components/PlacesToVisit';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { useCallback, useEffect, useMemo } from 'react';
import { TripDetailsModal } from './TripDetailsModal';
import { clearCalculations, setAlgorithm, setAvailableParameters, setMoveMethod } from '../store/reducers/routeSlice';
import { CalculateTrip } from '../components/CalculateTrip';
import { AvailableParametersResponse } from '../types/AvailableParametersResponse';

export const CreateTripPage = () => {
  const { routePoints, routeGeometry } = useSelector((state: RootState) => state.route);
  const dispatch = useDispatch();

  const isRouteCalculated = useMemo(() => routePoints !== null && routeGeometry !== null, [routePoints, routeGeometry]);
  const closeTripDetailsModal = useCallback(() => {
    dispatch(clearCalculations());
  }, [dispatch]);

  useEffect(() => {
    fetch('http://localhost:8000/available-parameters', {
      method: 'GET',
    }).then((response) => {
      response.json().then((data: AvailableParametersResponse) => {
        dispatch(setAvailableParameters(data));
        dispatch(setMoveMethod({ moveMethod: data.moves[0] }));
        dispatch(setAlgorithm({ algorithm: data.algorithms[0] }));
      });
    });
    // This effect should run only once
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <Grid
        container
        spacing={4}
      >
        <Grid size={6}>
          <Stack
            direction="column"
            spacing={4}
          >
            <TravelDates />
            <Divider />
            <Accommodation />
            <Divider />
            <TravelTime />
            <Divider />
          </Stack>
        </Grid>
        <Grid size={6}>
          <Map mapId="main-map" />
        </Grid>
        <Grid size={12}>
          <Stack
            direction="column"
            spacing={4}
          >
            <PlacesToVisit />
            <CalculateTrip />
          </Stack>
        </Grid>
      </Grid>
      <TripDetailsModal
        isOpen={isRouteCalculated}
        handleClose={closeTripDetailsModal}
      />
    </>
  );
};
