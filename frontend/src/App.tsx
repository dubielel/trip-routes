import { MapProvider } from 'react-map-gl/maplibre';

import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

import { Provider as ReduxProvider } from 'react-redux';
import { reduxStore } from './store/reduxStore';

import './App.css';

import { CreateTripPage } from './pages/CreateTripPage';

function App() {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <ReduxProvider store={reduxStore}>
        <MapProvider>
          <CreateTripPage />
        </MapProvider>
      </ReduxProvider>
    </LocalizationProvider>
  );
}

export default App;
