import { GridRenderEditCellParams, useGridApiContext } from '@mui/x-data-grid';
import { MuiColorInput, MuiColorInputValue } from 'mui-color-input';

export const GridEditColorPickerCell = ({
  id,
  field,
  value,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
}: GridRenderEditCellParams<any, MuiColorInputValue | null, string>) => {
  const apiRef = useGridApiContext();

  const handleChange = (newValue: unknown) => {
    apiRef.current.setEditCellValue({ id, field, value: newValue });
  };

  return (
    <MuiColorInput
      format="hex"
      value={value ?? '#808080'}
      onChange={handleChange}
      sx={{ width: '100%' }}
    />
  );
};
