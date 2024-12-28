import { Modal, Box } from '@mui/material';

import { useSelector } from 'react-redux';
import { RootState } from '../store/reduxStore';
import { RouteMap } from '../components/RouteMap';
import { RouteItinerary } from '../components/RouteItinerary';

export type TripDetailsModalProps = {
  isOpen: boolean;
  handleClose: () => void;
};

export const TripDetailsModal = ({ isOpen, handleClose }: TripDetailsModalProps) => {
  const { firstDayTimestamp } = useSelector((state: RootState) => state.trip);
  const { routePoints, routeGeometry } = useSelector((state: RootState) => state.route);

  if (firstDayTimestamp === null || routePoints === null || routeGeometry === null) {
    return null;
  }

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
        <Box sx={{ height: '50%', pb: 2 }}>
          <Box sx={{ position: 'absolute', width: 'calc(100% - 8 * 8px)', height: 'calc(50% - 8 * 8px)' }}>
            <RouteMap feature={routeGeometry} />
          </Box>
        </Box>
        <Box sx={{ height: '50%', overflowY: 'auto' }}>
          <RouteItinerary
            itinerary={routePoints}
            firstDayTimestamp={firstDayTimestamp}
            colors={routeGeometry.properties.colors}
          />
        </Box>
      </Box>
    </Modal>
  );
};
