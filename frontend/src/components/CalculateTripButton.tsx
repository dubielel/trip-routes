import { Button, CircularProgress } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { useMemo } from 'react';
import { CalculateTripResponse } from '../types/CalculateTripResponse';
import { setCalculations, setIsCalculating } from '../store/reducers/routeSlice';

export const CalculateTripButton = () => {
  const trip = useSelector((state: RootState) => state.trip);
  const { isCalculating, moveMethod, algorithm } = useSelector((state: RootState) => state.route);
  const dispatch = useDispatch();

  const handleCalculateTrip = () => {
    dispatch(setIsCalculating({ isCalculating: true }));
    const url = new URL('http://localhost:8000/calculate-trip');
    url.searchParams.append('move', moveMethod ?? '');
    url.searchParams.append('algorithm', algorithm ?? '');
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(trip),
    }).then((response) => {
      response
        .json()
        .then((data: CalculateTripResponse) => {
          dispatch(setCalculations(data));
        })
        .finally(() => {
          dispatch(setIsCalculating({ isCalculating: false }));
        });
    });
  };

  const disabled = useMemo(() => {
    return (
      isCalculating ||
      Object.values(trip).some((v) => v === null) ||
      trip.placesToVisit.features.length === 0 ||
      trip.placesToVisit.features.some((feature) => feature.properties.isNew)
    );
  }, [trip, isCalculating]);

  return (
    <Button
      onClick={handleCalculateTrip}
      disabled={disabled}
      sx={{ position: 'relative' }}
    >
      Calculate Trip
      {isCalculating && (
        <CircularProgress
          size={24}
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            marginTop: '-12px',
            marginLeft: '-12px',
          }}
        />
      )}
    </Button>
  );
};
