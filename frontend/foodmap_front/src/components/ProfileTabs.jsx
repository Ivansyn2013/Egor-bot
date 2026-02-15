// src/components/ProfileTabs.jsx
import React from 'react';
import { useAppContext } from '../context/AppContext';

const ProfileTabs = ({ activeTab, onTabChange }) => {
    const { state } = useAppContext();

    return (
        <div className="profile-tabs">
            <button
                className={`tab-btn ${activeTab === 'products' ? 'active' : ''}`}
                onClick={() => onTabChange('products')}
            >
                Продукты ({state.favorites.products.length})
            </button>
            <button
                className={`tab-btn ${activeTab === 'recipes' ? 'active' : ''}`}
                onClick={() => onTabChange('recipes')}
            >
                Рецепты ({state.favorites.recipes.length})
            </button>
            <button
                className={`tab-btn ${activeTab === 'doctors' ? 'active' : ''}`}
                onClick={() => onTabChange('doctors')}
            >
                Врачи ({state.favorites.doctors.length})
            </button>
            <button
                className={`tab-btn ${activeTab === 'recommended' ? 'active' : ''}`}
                onClick={() => onTabChange('recommended')}
            >
                Товары ({state.favorites.recommended.length})
            </button>
        </div>
    );
};

export default ProfileTabs;