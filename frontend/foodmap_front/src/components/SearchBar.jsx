// src/components/SearchBar.jsx
import React from 'react';

const SearchBar = ({ value, onChange }) => {
    return (
        <div className="search-bar">
            <input
                type="text"
                value={value}
                onChange={onChange}
                placeholder="Поиск продукта..."
            />
        </div>
    );
};

export default SearchBar;