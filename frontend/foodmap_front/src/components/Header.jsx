// src/components/Header.jsx
import React from 'react';
import { useAppContext } from '../context/AppContext';

const Header = () => {
    const { state, navigateTo, getTotalFavorites } = useAppContext();
    const totalFav = getTotalFavorites();

    return (
        <header id="header">
            <div className="nav-container">
                <div className="logo">🥗 FODMAP Помощник</div>
                <nav>
                    <button
                        className={`nav-btn ${state.currentSection === 'products' ? 'active' : ''}`}
                        onClick={() => navigateTo('products')}
                    >
                        🔍 Продукты
                    </button>
                    <button
                        className={`nav-btn ${state.currentSection === 'recipes' ? 'active' : ''}`}
                        onClick={() => navigateTo('recipes')}
                    >
                        🍳 Рецепты
                    </button>
                    <button
                        className={`nav-btn ${state.currentSection === 'doctors' ? 'active' : ''}`}
                        onClick={() => navigateTo('doctors')}
                    >
                        👨‍⚕️ Врачи
                    </button>
                    <button
                        className={`nav-btn ${state.currentSection === 'recommended' ? 'active' : ''}`}
                        onClick={() => navigateTo('recommended')}
                    >
                        ⭐ Рекомендуем
                    </button>
                </nav>
                <button
                    className="profile-btn"
                    onClick={() => navigateTo('profile')}
                >
                    👤 Профиль
                    {totalFav > 0 && <span className="badge">{totalFav}</span>}
                </button>
            </div>
        </header>
    );
};

export default Header;