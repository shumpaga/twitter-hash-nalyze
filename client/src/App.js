import React from 'react'
import './App.css';

import Table from './Table'

const App = () => {

  return <div>
    <h1 style={{ textAlign: 'center'}}>
      Recent Twitter data matching #Arcane
    </h1>
    <Table />
  </div>
}

export default App;
