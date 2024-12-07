import { useCallback, useState } from 'react';

import { Button, IconButton, Stack, TextField, Typography } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';

import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/reduxStore';

import { SelectPlaceModal } from './SelectPlaceModal';
import { setAccommodation } from '../store/reducers/tripSlice';

export const ACCOMMODATION_MARKER_COLOR = '#48e5ef';
const AccommodationMarkerColor = () => (
  <span
    style={{
      width: 24,
      height: 24,
      borderRadius: 4,
      backgroundColor: ACCOMMODATION_MARKER_COLOR,
      boxShadow: '0 4px 6px rgba(50, 50, 93, 0.11),0 1px 3px rgba(0, 0, 0, 0.08)',
    }}
  />
);

export const Accommodation = () => {
  const {
    accommodation,
    routeCalculations: { isCalculating: isRouteCalculating },
  } = useSelector((state: RootState) => state.trip);
  const dispatch = useDispatch();

  const [isMapOpen, setIsMapOpen] = useState<boolean>(false);
  const closeMapModal = useCallback(() => setIsMapOpen(false), [setIsMapOpen]);

  if (accommodation && !isMapOpen) {
    return (
      <Stack
        direction="column"
        spacing={2}
      >
        <Stack
          direction="row"
          spacing={1}
          justifyContent="center"
          alignItems="center"
        >
          <Typography variant="h5">Accommodation</Typography>
          <AccommodationMarkerColor />
        </Stack>
        <TextField
          value={accommodation.properties?.displayName}
          slotProps={{
            input: {
              readOnly: true,
              endAdornment: (
                <IconButton
                  onClick={() => {
                    dispatch(setAccommodation({ accommodation: null }));
                  }}
                  disabled={isRouteCalculating}
                >
                  <ClearIcon />
                </IconButton>
              ),
            },
          }}
          disabled={isRouteCalculating}
        />
      </Stack>
    );
  }

  return (
    <Stack
      direction="column"
      spacing={2}
    >
      <Stack
        direction="row"
        spacing={1}
        justifyContent="center"
        alignItems="center"
      >
        <Typography variant="h5">Accommodation</Typography>
        <AccommodationMarkerColor />
      </Stack>
      <Button
        variant="outlined"
        onClick={() => setIsMapOpen(true)}
      >
        Select a place
      </Button>
      <SelectPlaceModal
        isOpen={isMapOpen}
        handleClose={closeMapModal}
        onGeocoderResult={(evt) => {
          dispatch(
            setAccommodation({
              accommodation: {
                type: evt.result.type,
                geometry: evt.result.geometry,
                properties: {
                  displayName: evt.result.properties.display_name,
                },
              },
            }),
          );
        }}
      />
    </Stack>
  );
};
