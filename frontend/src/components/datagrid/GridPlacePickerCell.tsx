import { GridRenderCellParams } from '@mui/x-data-grid';

import { TextField } from '@mui/material';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const GridPlacePickerCell = ({ value }: GridRenderCellParams<any, string | null>) => {
  return (
    <TextField
      value={value}
      slotProps={{ input: { readOnly: true } }}
      sx={{ width: '100%' }}
    />
  );
};
