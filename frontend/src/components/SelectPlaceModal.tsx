import { Box, Modal } from '@mui/material';

import { Map } from 'react-map-gl/maplibre';

import { GeocoderControl } from './GeocoderControl';

import '@maplibre/maplibre-gl-geocoder/dist/maplibre-gl-geocoder.css';
import { NominatimResultResponse } from '../types/Nominatim';

export type SelectPlaceModalProps = {
  isOpen: boolean;
  handleClose: () => void;

  onGeocoderResult: (evt: { result: NominatimResultResponse }) => void;
};

export const SelectPlaceModal = ({ isOpen, handleClose, onGeocoderResult }: SelectPlaceModalProps) => {
  return (
    <Modal
      open={isOpen}
      onClose={handleClose}
    >
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '80%',
          height: '80%',
          bgcolor: 'background.paper',
          border: '2px solid #000',
          boxShadow: 24,
          p: 4,
        }}
      >
        <Map
          id="select-place-map"
          initialViewState={{
            longitude: 12.7058702,
            latitude: 41.1905539,
            zoom: 5,
          }}
          mapStyle="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
        >
          <GeocoderControl
            position="top-left"
            marker={true}
            onLoading={() => {}}
            onResults={() => {}}
            onResult={onGeocoderResult}
            onError={() => {}}
          />
        </Map>
      </Box>
    </Modal>
  );
};
