import { useState } from 'react';

import { Box, Stack, Typography } from '@mui/material';
import {
  GridRowModesModel,
  GridRowModes,
  DataGrid,
  GridColDef,
  GridActionsCellItem,
  GridEventListener,
  GridRowModel,
  GridRowEditStopReasons,
} from '@mui/x-data-grid';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';

import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { addPlaceToVisit, removePlaceToVisitByRowId, updatePlaceToVisit } from '../store/reducers/tripSlice';

import { EditToolbar } from './datagrid/EditToolbar';
import { GridEditSliderCell } from './datagrid/GridEditSliderCell';
import { GridSliderCell } from './datagrid/GridSliderCell';
import { GridColorPickerCell } from './datagrid/GridColorPickerCell';
import { GridEditColorPickerCell } from './datagrid/GridEditColorPickerCell';
import { GridPlacePickerCell } from './datagrid/GridPlacePickerCell';
import { GridEditPlacePickerCell } from './datagrid/GridEditPlacePickerCell';

const NoPlacesToVisitOverlay = () => (
  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
    <Typography variant="overline">No places to visit</Typography>
  </Box>
);

export const PlacesToVisit = () => {
  const {
    placesToVisit: { features: placesToVisit },
    routeCalculations: { isCalculating: isRouteCalculating },
  } = useSelector((state: RootState) => state.trip);
  const dispatch = useDispatch();

  const [rowModesModel, setRowModesModel] = useState<GridRowModesModel>({});

  const handleRowEditStop: GridEventListener<'rowEditStop'> = (params, event) => {
    if (params.reason === GridRowEditStopReasons.rowFocusOut) {
      event.defaultMuiPrevented = true;
    }
  };

  const handleEditClick = (rowId: string) => () => {
    setRowModesModel({ ...rowModesModel, [rowId]: { mode: GridRowModes.Edit } });
  };

  const handleSaveClick = (rowId: string) => () => {
    setRowModesModel({ ...rowModesModel, [rowId]: { mode: GridRowModes.View } });
  };

  const handleDeleteClick = (rowId: string) => () => {
    dispatch(removePlaceToVisitByRowId({ rowId, onlyWhenIsNew: false }));
  };

  const handleCancelClick = (rowId: string) => () => {
    setRowModesModel({
      ...rowModesModel,
      [rowId]: { mode: GridRowModes.View, ignoreModifications: true },
    });
    dispatch(removePlaceToVisitByRowId({ rowId, onlyWhenIsNew: true }));
  };

  const processRowUpdate = (newRow: GridRowModel) => {
    const updatedRow = {
      type: 'Feature' as const,
      properties: {
        displayName: newRow.displayName as string,
        timeToSpend: newRow.timeToSpend as number,
        markerColor: newRow.markerColor as string,

        rowId: newRow.properties.rowId as string,
        isNew: false,
      },
      geometry: newRow.geometry,
    };
    dispatch(updatePlaceToVisit({ placeToUpdate: updatedRow }));
    return updatedRow;
  };

  const handleRowModesModelChange = (newRowModesModel: GridRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const columns: GridColDef[] = [
    {
      renderCell: (params) => <GridPlacePickerCell {...params} />,
      renderEditCell: (params) => <GridEditPlacePickerCell {...params} />,
      display: 'flex',
      align: 'left',
      field: 'displayName',
      valueGetter: (_value, row) => row.properties.displayName,
      preProcessEditCellProps: (params) => ({ ...params.props, error: params.row.geometry === null }),
      headerName: 'Location',
      headerAlign: 'center',
      flex: 2,
      editable: true,
    },
    {
      // Workaround to be able to assign a value to the geometry field in GridEditPlacePickerCell
      field: 'geometry',
      editable: true,
    },
    {
      renderCell: (params) => <GridSliderCell {...params} />,
      renderEditCell: (params) => <GridEditSliderCell {...params} />,
      display: 'flex',
      align: 'center',
      field: 'timeToSpend',
      valueGetter: (_value, row) => row.properties.timeToSpend,
      preProcessEditCellProps: (params) => ({ ...params.props, error: params.row.properties.timeToSpend === null }),
      headerName: 'Time',
      headerAlign: 'center',
      type: 'number',
      flex: 2,
      editable: true,
    },
    {
      renderCell: (params) => <GridColorPickerCell {...params} />,
      renderEditCell: (params) => <GridEditColorPickerCell {...params} />,
      field: 'markerColor',
      valueGetter: (_value, row) => row.properties.markerColor,
      preProcessEditCellProps: (params) => ({ ...params.props, error: params.row.properties.markerColor === null }),
      headerName: 'Marker',
      headerAlign: 'center',
      flex: 1,
      editable: true,
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      headerAlign: 'center',
      width: 100,
      cellClassName: 'actions',
      getActions: ({ id: rowId }) => {
        const isInEditMode = rowModesModel[rowId]?.mode === GridRowModes.Edit;
        if (isInEditMode) {
          return [
            <GridActionsCellItem
              icon={<SaveIcon />}
              label="Save"
              sx={{
                color: 'primary.main',
              }}
              onClick={handleSaveClick(rowId as string)}
            />,
            <GridActionsCellItem
              icon={<CancelIcon />}
              label="Cancel"
              className="textPrimary"
              onClick={handleCancelClick(rowId as string)}
              color="inherit"
            />,
          ];
        }

        return [
          <GridActionsCellItem
            icon={<EditIcon />}
            label="Edit"
            className="textPrimary"
            onClick={handleEditClick(rowId as string)}
            color="inherit"
          />,
          <GridActionsCellItem
            icon={<DeleteIcon />}
            label="Delete"
            onClick={handleDeleteClick(rowId as string)}
            color="inherit"
          />,
        ];
      },
    },
  ];

  return (
    <Stack
      direction="column"
      spacing={2}
    >
      <Typography variant="h5">
        Select places you want to visit and approximate the amount of time you want to spend there
      </Typography>

      <Box
        sx={{
          height: 500,
          width: '100%',
          '& .actions': {
            color: 'text.secondary',
          },
          '& .textPrimary': {
            color: 'text.primary',
          },
        }}
      >
        <DataGrid
          onCellKeyDown={(_params, event) => {
            if (event.key === 'Enter') {
              event.defaultMuiPrevented = true;
            }
          }}
          onCellDoubleClick={(_params, event) => {
            event.defaultMuiPrevented = true;
          }}
          rows={placesToVisit}
          getRowId={(row) => row.properties.rowId}
          getRowHeight={() => 'auto'}
          columns={columns}
          initialState={{
            columns: {
              columnVisibilityModel: {
                geometry: false,
              },
            },
          }}
          editMode="row"
          rowModesModel={rowModesModel}
          onRowModesModelChange={handleRowModesModelChange}
          onRowEditStop={handleRowEditStop}
          processRowUpdate={processRowUpdate}
          slots={{
            toolbar: EditToolbar,
            noRowsOverlay: NoPlacesToVisitOverlay,
          }}
          slotProps={{
            toolbar: {
              addNewRow: (newRow) => dispatch(addPlaceToVisit({ placeToVisit: newRow })),
              setRowModesModel,
            },
          }}
          loading={isRouteCalculating}
          autosizeOptions={{
            includeOutliers: true,
            includeHeaders: true,
          }}
        />
      </Box>
    </Stack>
  );
};
