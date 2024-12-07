import { useCallback, useState } from 'react';

import { Button, IconButton, TextField } from '@mui/material';
import { GridRenderEditCellParams, useGridApiContext } from '@mui/x-data-grid';
import ClearIcon from '@mui/icons-material/Clear';

import { SelectPlaceModal } from '../SelectPlaceModal';
import { NominatimResultResponse } from '../../types/Nominatim';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const GridEditPlacePickerCell = ({ id, field, value }: GridRenderEditCellParams<any, string | null>) => {
  const [isMapOpen, setIsMapOpen] = useState<boolean>(false);
  const closeMapModal = useCallback(() => setIsMapOpen(false), [setIsMapOpen]);

  const apiRef = useGridApiContext();

  const handleChange = (newValue: unknown) => {
    if (newValue === null) {
      apiRef.current.setEditCellValue({ id, field, value: null });
      apiRef.current.setEditCellValue({ id, field: 'geometry', value: null });
      return;
    }

    const {
      geometry,
      properties: { display_name: displayName },
    } = newValue as NominatimResultResponse;

    apiRef.current.setEditCellValue({ id, field, value: displayName });
    apiRef.current.setEditCellValue({ id, field: 'geometry', value: geometry });
  };

  if (value) {
    return (
      <TextField
        value={value}
        slotProps={{
          input: {
            readOnly: true,
            endAdornment: (
              <IconButton
                onClick={() => {
                  handleChange(null);
                }}
              >
                <ClearIcon />
              </IconButton>
            ),
          },
        }}
        sx={{ width: '100%' }}
      />
    );
  }

  return (
    <>
      <Button
        variant="outlined"
        onClick={() => setIsMapOpen(true)}
        sx={{ width: '100%' }}
      >
        Select a place
      </Button>
      <SelectPlaceModal
        isOpen={isMapOpen}
        handleClose={closeMapModal}
        onGeocoderResult={(evt) => handleChange(evt.result)}
      />
    </>
  );
};
