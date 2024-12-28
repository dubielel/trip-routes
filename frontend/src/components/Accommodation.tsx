import { useCallback, useState } from 'react';

import { Button, IconButton, Stack, TextField, Typography } from '@mui/material';
import ClearIcon from '@mui/icons-material/Clear';

import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/reduxStore';

import { SelectPlaceModal } from './SelectPlaceModal';
import { setAccommodation } from '../store/reducers/tripSlice';

import { MarkerColorBox } from './MarkerColorBox';
import { ACCOMMODATION_MARKER_COLOR, ACCOMMODATION_ROW_ID } from '../constants';

const AccommodationMarkerColor = () => <MarkerColorBox color={ACCOMMODATION_MARKER_COLOR} />;

export const Accommodation = () => {
  const { accommodation } = useSelector((state: RootState) => state.trip);
  const { isCalculating } = useSelector((state: RootState) => state.route);
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
                  disabled={isCalculating}
                >
                  <ClearIcon />
                </IconButton>
              ),
            },
          }}
          disabled={isCalculating}
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
                  markerColor: ACCOMMODATION_MARKER_COLOR,

                  isNew: false,
                  rowId: ACCOMMODATION_ROW_ID,
                  timeToSpend: 0,
                },
              },
            }),
          );
        }}
      />
    </Stack>
  );
};
