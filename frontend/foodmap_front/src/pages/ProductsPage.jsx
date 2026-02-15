// src/pages/ProductsPage.jsx
import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext'; // Импортируем наш контекст
import Card from '../components/Card'; // Импортируем универсальный компонент карточки
import SearchBar from '../components/SearchBar'; // Импортируем компонент поиска

const ProductsPage = () => {
  // Получаем глобальное состояние (включая DATA и favorites) и функции из контекста
  const { state } = useAppContext();
  // Локальное состояние для строки поиска
  const [searchTerm, setSearchTerm] = useState('');

  // Фильтруем продукты на основе строки поиска
  // Используем state.data.products, который при переходе к API будет содержать данные из него
  // В текущей версии с статическими данными, state.data заполняется в AppContext
  const filteredProducts = state.data.products.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="content-wrapper">
      <h1 className="page-title">Поиск продуктов</h1>
      {/* Используем компонент SearchBar, передав ему локальное состояние */}
      <SearchBar
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)} // Обновляем локальное состояние при вводе
      />
      <div className="cards-grid">
        {/* Рендерим отфильтрованные продукты */}
        {filteredProducts.map(product => (
          // Каждый элемент списка должен иметь уникальный ключ
          // Card сам обрабатывает клик и вызывает navigateTo через контекст
          <Card key={product.id} item={product} type="products" />
        ))}
      </div>
    </div>
  );
};

export default ProductsPage;