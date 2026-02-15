// src/context/AppContext.jsx
import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { DATA } from '../data/data';

// Инициализация состояния из localStorage ИЛИ значения по умолчанию (с ПУСТЫМИ, но определенными данными)
const loadState = () => {
    const saved = localStorage.getItem('fodmap_favorites');
    if (saved) {
        try {
            const parsed = JSON.parse(saved);
            return {
                currentSection: 'products',
                currentView: 'list',
                selectedId: null,
                favorites: {
                    products: parsed.products || [],
                    recipes: parsed.recipes || [],
                    doctors: parsed.doctors || [],
                    recommended: parsed.recommended || [],
                },
                // --- КЛЮЧЕВОЙ МОМЕНТ: ВСЕГДА включаем 'data' с пустыми массивами ---
                data: {
                    products: [],
                    recipes: [],
                    doctors: [],
                    recommended: [],
                },
                loading: true, // <-- Изначально true, так как данные еще не загружены
                error: null,
                // --- /КОНЕЦ ---
            };
        } catch (e) {
            console.error('Ошибка загрузки избранного:', e);
        }
    }
    // Возвращаем начальное состояние с пустыми данными
    return {
        currentSection: 'products',
        currentView: 'list',
        selectedId: null,
        favorites: {
            products: [],
            recipes: [],
            doctors: [],
            recommended: []
        },
        // --- КЛЮЧЕВОЙ МОМЕНТ: ВСЕГДА включаем 'data' с пустыми массивами ---
        data: {
            products: [],
            recipes: [],
            doctors: [],
            recommended: [],
        },
        loading: true, // <-- Изначально true, так как данные еще не загружены
        error: null,
        // --- /КОНЕЦ ---
    };
};

// Определение действий (actions)
const AppReducer = (state, action) => {
    

    switch (action.type) {
        
        
        case 'FETCH_DATA_REQUEST':
            // Устанавливаем флаг загрузки, очищаем ошибку
            return { ...state, loading: true, error: null };
        case 'LOAD_STATIC_DATA_SUCCESS': // Или 'FETCH_DATA_SUCCESS' в будущем
            // Обновляем 'data' на основе payload, сбрасываем флаг загрузки, очищаем ошибку
            return { ...state, data: action.payload, loading: false, error: null };
        case 'FETCH_DATA_FAILURE':
            // Сбрасываем флаг загрузки, устанавливаем ошибку
            return { ...state, loading: false, error: action.payload };
        case 'NAVIGATE':
            return {
                ...state,
                currentSection: action.section,
                currentView: action.view,
                selectedId: action.id,
            };
        case 'TOGGLE_FAVORITE':
            const { type, id } = action.payload;
            const newFavorites = { ...state.favorites };
            const index = newFavorites[type].indexOf(id);

            if (index > -1) {
                newFavorites[type].splice(index, 1);
            } else {
                newFavorites[type].push(id);
            }
            return {
                ...state,
                favorites: newFavorites
            };
        default:
            return state;
    }
};

const AppContext = createContext();

export const AppProvider = ({ children }) => {
    // Используем loadState как функцию инициализации для useReducer
    // Это гарантирует, что начальное состояние всегда будет корректным
    const [state, dispatch] = useReducer(AppReducer, undefined, loadState);

    // --- useEffect для загрузки данных при монтировании провайдера ---
    useEffect(() => {
        const fetchData = async () => {
            dispatch({ type: 'FETCH_DATA_REQUEST' });
            
            try {
                const apiUrl = import.meta.env.VITE_API_URL || '';
                const response = await fetch(`${apiUrl}/api/products`);
                if (!response.ok) throw new Error('Failed to fetch products');
                const products = await response.json();
                
                // Since we only have products in DB for now, we merge with other static data
                const updatedData = {
                    ...DATA,
                    products: products.map(p => ({
                        ...p,
                        // Add defaults for fields missing from minimal DB request
                        status: p.status || 'unknown',
                        description: p.description || '',
                        image: p.image || '/api/placeholder/400/320'
                    }))
                };
                
                dispatch({ type: 'LOAD_STATIC_DATA_SUCCESS', payload: updatedData });
            } catch (error) {
                console.error('Error fetching data:', error);
                // Fallback to static data on error
                dispatch({ type: 'LOAD_STATIC_DATA_SUCCESS', payload: DATA });
            }
        };

        fetchData();
    }, []); // Пустой массив зависимостей означает выполнение только при монтировании
    // --- /useEffect ---

    // useEffect для сохранения избранного в localStorage
    useEffect(() => {
        localStorage.setItem('fodmap_favorites', JSON.stringify(state.favorites));
    }, [state.favorites]);

    const navigateTo = (section, view = 'list', id = null) => {
        dispatch({ type: 'NAVIGATE', section, view, id });
    };

    const toggleFavorite = (type, id) => {
        dispatch({ type: 'TOGGLE_FAVORITE', payload: { type, id } });
    };

    const isFavorite = (type, id) => {
        return state.favorites[type].includes(id);
    };

    const getTotalFavorites = () => {
        return Object.values(state.favorites).reduce((sum, arr) => sum + arr.length, 0);
    };

    // Объект value, который будет доступен через useAppContext
    const value = {
        state, // Состояние включает data, loading, error
        navigateTo,
        toggleFavorite,
        isFavorite,
        getTotalFavorites
    };

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () =>  {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};