// src/components/Card.jsx
import React from 'react';
import { useAppContext } from '../context/AppContext';

const Card = ({ item, type }) => {
    const { navigateTo } = useAppContext();

    const handleClick = () => {
        navigateTo(type, 'detail', item.id);
    };

    // Определение содержимого карточки в зависимости от типа
    let cardContent;
    switch (type) {
        case 'products':
            cardContent = (
                <>
                    <div className="card-emoji">{item.emoji}</div>
                    <h3>{item.name}</h3>
                    <span className={`badge-${item.fodmap_level}`}>{item.fodmap_level.toUpperCase()} FODMAP</span>
                    <p>{item.safe_dose ? `Безопасная доза: ${item.safe_dose}г` : 'Избегайте'}</p>
                </>
            );
            break;
        case 'recipes':
            cardContent = (
                <>
                    <div className="card-emoji">{item.emoji}</div>
                    <h3>{item.name}</h3>
                    <p>⏱ {item.time} минут | 🍽 {item.servings} порций</p>
                    <p>{item.meal_type} • {item.difficulty}</p>
                </>
            );
            break;
        case 'doctors':
            cardContent = (
                <>
                    <div className="card-emoji">{item.emoji}</div>
                    <h3>{item.name}</h3>
                    <p>{item.specialty}</p>
                    <p className="rating">{'⭐'.repeat(Math.floor(item.rating))} {item.rating} ({item.reviews} отзывов)</p>
                    <p><strong>от {item.price}₽</strong></p>
                </>
            );
            break;
        case 'recommended':
            cardContent = (
                <>
                    <div className="card-emoji">{item.emoji}</div>
                    <h3>{item.name}</h3>
                    <p><strong>{item.brand}</strong></p>
                    <p>{item.category}</p>
                    <p><strong style={{ color: '#4CAF50', fontSize: '1.25rem' }}>{item.price}₽</strong></p>
                </>
            );
            break;
        default:
            cardContent = <p>Тип неизвестен</p>;
    }

    return (
        <div className="card" onClick={handleClick}>
            {cardContent}
        </div>
    );
};

export default Card;