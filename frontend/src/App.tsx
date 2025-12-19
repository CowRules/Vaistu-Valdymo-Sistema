import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router'
import LoginPage from './pages/Login'
import 'bootstrap/dist/css/bootstrap.min.css';
import RegisterPage from './pages/RegisterPage'
import HomePage from './pages/HomePage'
import ReserveListPage from './pages/ReserveListPage'

function App() {

  return (
    <>
      <BrowserRouter>
          <Routes>
            <Route path='/login' element={<LoginPage />} />
            <Route path='/register' element={<RegisterPage />} />
            <Route path='/' element={<HomePage/>} />
            <Route path='/reserves' element={<ReserveListPage/>} />
          </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
