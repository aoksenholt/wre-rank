import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { Amplify, API } from 'aws-amplify';
import config from './aws-exports';


Amplify.configure(config)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

const getData = async () => {
  const data = await API.get('wrerankingapi', '/seed')
  console.log(data)
}
