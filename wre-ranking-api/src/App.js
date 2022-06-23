import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';



function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);

  useEffect(() => {
    async function getData() {
      fetch('https://k3gem29sn7.execute-api.eu-north-1.amazonaws.com/dev/seed')
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP-feil: ${response.status}`)
          }
          return response.json()
        })
        .then((actualData) => {
          setData(actualData)
          setError(null)
        })
        .catch((err) => {
          setError(err.message)
          setData(null)
        })
        .finally(() => {
          setLoading(false)
        })
    }
    getData()
  }, [])

  return (
    <div>
      {JSON.stringify(data)}
    </div>
  );
}

export default App;
