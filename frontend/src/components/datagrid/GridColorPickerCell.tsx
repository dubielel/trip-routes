import { GridRenderCellParams } from '@mui/x-data-grid';
import { MuiColorInput, MuiColorInputValue } from 'mui-color-input';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const GridColorPickerCell = ({ value }: GridRenderCellParams<any, MuiColorInputValue | null, string>) => {
  return (
    <MuiColorInput
      format="hex"
      value={value ?? '#808080'}
      disablePopover={true}
      slotProps={{
        input: {
          readOnly: true,
        },
      }}
      sx={{ width: '100%' }}
    />
  );
};
