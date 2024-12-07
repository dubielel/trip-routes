import { Slider } from '@mui/material';
import { GridRenderEditCellParams, useGridApiContext } from '@mui/x-data-grid';

import { sliderMarks } from '../../utils/sliderMarks';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const GridEditSliderCell = ({ id, field, value }: GridRenderEditCellParams<any, number | null>) => {
  const apiRef = useGridApiContext();

  const handleChange = (evt: unknown) => {
    if (evt instanceof Event && evt.target && 'value' in evt.target) {
      apiRef.current.setEditCellValue({ id, field, value: evt.target.value });
    }
  };

  return (
    <Slider
      value={value ?? 30}
      onChange={handleChange}
      min={30}
      step={30}
      max={360}
      marks={sliderMarks}
      valueLabelDisplay="auto"
      sx={{ width: '90%' }}
    />
  );
};
