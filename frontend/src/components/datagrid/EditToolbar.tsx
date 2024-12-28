import { Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { GridSlotProps, GridRowModes, GridToolbarContainer, GridRowModesModel } from '@mui/x-data-grid';

import { chance } from '../../utils/chance';

import { useSelector } from 'react-redux';
import { RootState } from '../../store/reduxStore';
import { PlaceToVisitProperties } from '../../store/reducers/tripSlice';

declare module '@mui/x-data-grid' {
  interface ToolbarPropsOverrides {
    addNewRow: (newPlaceToVisit: GeoJSON.Feature<GeoJSON.Point, PlaceToVisitProperties>) => void;
    setRowModesModel: (newModel: (oldModel: GridRowModesModel) => GridRowModesModel) => void;
  }
}

export const EditToolbar = (props: GridSlotProps['toolbar']) => {
  const { addNewRow, setRowModesModel } = props;

  const { isCalculating } = useSelector((state: RootState) => state.route);

  const handleClick = () => {
    const rowId = chance.guid();
    addNewRow({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [0, 0],
      },
      properties: {
        displayName: '',
        timeToSpend: 30,
        markerColor: '#606060',
        rowId: rowId,
        isNew: true,
      },
    });
    setRowModesModel((oldModel) => ({
      ...oldModel,
      [rowId]: { mode: GridRowModes.Edit },
    }));
  };

  return (
    <GridToolbarContainer sx={{ justifyContent: 'center', alignItems: 'center' }}>
      <Button
        fullWidth
        variant="outlined"
        color="primary"
        startIcon={<AddIcon />}
        onClick={handleClick}
        disabled={isCalculating}
      >
        Add place to visit
      </Button>
    </GridToolbarContainer>
  );
};
