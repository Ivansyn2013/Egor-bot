// src/App.jsx
import React from 'react';
import { useAppContext } from './context/AppContext';
import Header from './components/Header';

import ProductsPage from './pages/ProductsPage';
import ProductDetailPage from './pages/ProductDetailPage';
import RecipesPage from './pages/RecipesPage';
import RecipeDetailPage from './pages/RecipeDetailPage';
import DoctorsPage from './pages/DoctorsPage';
import DoctorDetailPage from './pages/DoctorDetailPage';
import RecommendedPage from './pages/RecommendedPage';
import RecommendedDetailPage from './pages/RecommendedDetailPage';
import ProfilePage from './pages/ProfilePage';

const App = () => {
  const { state } = useAppContext();

  // --- ПРОВЕРЯЕМ ФЛАГ ЗАГРУЗКИ ---
  if (state.loading) {
    // Пока данные загружаются, показываем индикатор
    return <div className="loading">Загрузка данных...</div>;
  }

  // Проверка на ошибку (опционально)
  if (state.error) {
     return <div className="error">Ошибка: {state.error}</div>;
  }
  // --- /ПРОВЕРКА ---

  let CurrentPageComponent;
  switch (state.currentSection) {
    case 'products':
      CurrentPageComponent = state.currentView === 'detail' ? ProductDetailPage : ProductsPage;
      break;
    case 'recipes':
      CurrentPageComponent = state.currentView === 'detail' ? RecipeDetailPage : RecipesPage;
      break;
    case 'doctors':
      CurrentPageComponent = state.currentView === 'detail' ? DoctorDetailPage : DoctorsPage;
      break;
    case 'recommended':
      CurrentPageComponent = state.currentView === 'detail' ? RecommendedDetailPage : RecommendedPage;
      break;
    case 'profile':
      CurrentPageComponent = ProfilePage;
      break;
    default:
      CurrentPageComponent = ProductsPage;
  }

  return (
    <div id="app">
      <Header />
      <main id="main-content">
        <CurrentPageComponent />
      </main>
    </div>
  );
};

export default App;