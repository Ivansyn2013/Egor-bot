// src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { AppProvider } from './context/AppContext.jsx' // Импортируем провайдер контекста
import './App.css' // Импортируем глобальные стили

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* Оборачиваем App в AppProvider, чтобы он имел доступ к контексту */}
    <AppProvider>
      <App />
    </AppProvider>
  </React.StrictMode>,
)