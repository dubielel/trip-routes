import { Button, CircularProgress } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { useMemo, useRef, useEffect } from 'react';
import { setIsRouteCalculating } from '../store/reducers/tripSlice';

export const CalculateTripButton = () => {
  const {
    trip,
    trip: {
      placesToVisit,
      routeCalculations: { isCalculating: isRouteCalculating },
    },
  } = useSelector((state: RootState) => state);
  const dispatch = useDispatch();

  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  useEffect(() => {
    return () => {
      clearTimeout(timer.current);
    };
  }, []);

  const handleCalculateTrip = () => {
    dispatch(setIsRouteCalculating({ isCalculating: true }));
    // TODO communicate with backend
    timer.current = setTimeout(() => {
      dispatch(setIsRouteCalculating({ isCalculating: false }));
    }, 5000);
    console.log('Calculate Trip');
  };

  const disabled = useMemo(() => {
    return (
      isRouteCalculating ||
      Object.values(trip).some((v) => v === null) ||
      placesToVisit.features.length === 0 ||
      placesToVisit.features.some((feature) => feature.properties.isNew)
    );
  }, [trip, placesToVisit.features, isRouteCalculating]);

  return (
    <Button
      onClick={handleCalculateTrip}
      disabled={disabled}
      sx={{ position: 'relative' }}
    >
      Calculate Trip
      {isRouteCalculating && (
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
