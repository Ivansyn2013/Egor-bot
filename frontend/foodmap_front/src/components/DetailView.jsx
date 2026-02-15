// src/components/DetailView.jsx
import React from 'react';
import { useAppContext } from '../context/AppContext';

const DetailView = ({ item, type, onBack }) => {
    const { isFavorite, toggleFavorite } = useAppContext();
    const isFav = isFavorite(type, item.id);

    const handleToggleFavorite = () => {
        toggleFavorite(type, item.id);
    };

    // Определение содержимого детального вида в зависимости от типа
    let detailContent;
    switch (type) {
        case 'products':
            detailContent = (
                <>
                    <div className="detail-content">
                        <div className="emoji-large">{item.emoji}</div>
                        <h1>{item.name}</h1>
                        <span className={`badge-${item.fodmap_level}`}>{item.fodmap_level.toUpperCase()} FODMAP</span>
                        <div className="doses">
                            <div className="dose-card green">
                                <h3>{item.safe_dose || '-'}</h3>
                                <p>Безопасная доза (г)</p>
                                <p>{item.safe_fodmaps || '-'}</p>
                            </div>
                            <div className="dose-card yellow">
                                <h3>{item.medium_dose || '-'}</h3>
                                <p>Средняя доза (г)</p>
                                <p>{item.medium_fodmaps || '-'}</p>
                            </div>
                            <div className="dose-card red">
                                <h3>{item.high_dose !== null ? item.high_dose : '-'}</h3>
                                <p>Опасная доза (г)</p>
                                <p>{item.high_fodmaps || '-'}</p>
                            </div>
                        </div>
                        <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#F5F5F5', borderRadius: '12px' }}>
                            <h3>Примечание</h3>
                            <p style={{ color: '#666', marginTop: '0.5rem' }}>{item.note}</p>
                        </div>
                    </div>
                </>
            );
            break;
        case 'recipes':
            detailContent = (
                <>
                    <div className="detail-content">
                        <div className="emoji-large">{item.emoji}</div>
                        <h1>{item.name}</h1>
                        <div className="recipe-info">
                            <div className="recipe-info-item">
                                <strong>{item.time}</strong>
                                <span>минут</span>
                            </div>
                            <div className="recipe-info-item">
                                <strong>{item.servings}</strong>
                                <span>порций</span>
                            </div>
                            <div className="recipe-info-item">
                                <strong>{item.difficulty}</strong>
                                <span>сложность</span>
                            </div>
                        </div>
                        <div className="ingredients-list">
                            <h3>Ингредиенты</h3>
                            <ul>
                                {item.ingredients.map((ing, idx) => <li key={idx}>{ing}</li>)}
                            </ul>
                        </div>
                        <div className="instructions-list">
                            <h3>Инструкция</h3>
                            <ol>
                                {item.instructions.map((step, idx) => <li key={idx}>{step}</li>)}
                            </ol>
                        </div>
                        <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#E8F5E9', borderRadius: '12px' }}>
                            <h3>💡 Совет</h3>
                            <p style={{ color: '#2E7D32', marginTop: '0.5rem' }}>{item.tips}</p>
                        </div>
                        <div className="nutrition">
                            <div className="nutrition-item">
                                <strong>{item.calories}</strong>
                                <span>ккал</span>
                            </div>
                            <div className="nutrition-item">
                                <strong>{item.protein}г</strong>
                                <span>белки</span>
                            </div>
                            <div className="nutrition-item">
                                <strong>{item.carbs}г</strong>
                                <span>углеводы</span>
                            </div>
                            <div className="nutrition-item">
                                <strong>{item.fat}г</strong>
                                <span>жиры</span>
                            </div>
                        </div>
                    </div>
                </>
            );
            break;
        case 'doctors':
            detailContent = (
                <>
                    <div className="detail-content">
                        <div className="emoji-large">{item.emoji}</div>
                        <h1>{item.name}</h1>
                        <p style={{ fontSize: '1.25rem', color: '#666', marginBottom: '1rem' }}>{item.specialty}</p>
                        <div className="doctor-info">
                            <div className="info-row">
                                <strong>Опыт:</strong>
                                <span>{item.experience} лет</span>
                            </div>
                            <div className="info-row">
                                <strong>Образование:</strong>
                                <span>{item.education}</span>
                            </div>
                            <div className="info-row">
                                <strong>Клиника:</strong>
                                <span>{item.clinic}</span>
                            </div>
                            <div className="info-row">
                                <strong>Город:</strong>
                                <span>{item.city}</span>
                            </div>
                            <div className="info-row">
                                <strong>Рейтинг:</strong>
                                <span className="rating">{'⭐'.repeat(Math.floor(item.rating))} {item.rating} ({item.reviews} отзывов)</span>
                            </div>
                            <div className="info-row">
                                <strong>Цена:</strong>
                                <span><strong>от {item.price}₽</strong></span>
                            </div>
                        </div>
                        <div className="specializations">
                            {item.specializations.map((spec, idx) => <span key={idx} className="spec-badge">{spec}</span>)}
                        </div>
                        <p style={{ margin: '2rem 0', color: '#666' }}>{item.description}</p>
                        <div className="achievements">
                            <h3>Достижения</h3>
                            <ul>
                                {item.achievements.map((ach, idx) => <li key={idx}>{ach}</li>)}
                            </ul>
                        </div>
                        <a href={`tel:${item.phone}`}>
                            <button className="call-btn">📞 Позвонить {item.phone}</button>
                        </a>
                    </div>
                </>
            );
            break;
        case 'recommended':
            detailContent = (
                <>
                    <div className="detail-content">
                        <div className="emoji-large">{item.emoji}</div>
                        <h1>{item.name}</h1>
                        <p style={{ fontSize: '1.25rem', color: '#666', marginBottom: '0.5rem' }}>{item.brand}</p>
                        <span className="badge-low">{item.category}</span>
                        <div className="price-tag">{item.price}₽</div>
                        <p style={{ color: '#666' }}>Объем: {item.volume}</p>
                        <p style={{ margin: '2rem 0', color: '#666' }}>{item.description}</p>
                        <div className="benefits">
                            <h3>✓ Преимущества</h3>
                            <ul>
                                {item.benefits.map((benefit, idx) => <li key={idx}>{benefit}</li>)}
                            </ul>
                        </div>
                        <h3 style={{ textAlign: 'center', marginTop: '2rem' }}>Где купить:</h3>
                        <div className="stores">
                            {item.where_to_buy.map((store, idx) => <span key={idx} className="store-badge">{store}</span>)}
                        </div>
                        <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#E8F5E9', borderRadius: '12px', textAlign: 'center' }}>
                            <h3 style={{ color: '#2E7D32' }}>✓ Low FODMAP Безопасно</h3>
                        </div>
                    </div>
                </>
            );
            break;
        default:
            detailContent = <p>Тип неизвестен</p>;
    }

    return (
        <div className="detail-view">
            <div className="detail-header">
                <button className="back-btn" onClick={onBack}>← Назад</button>
                <button
                    className={`fav-btn ${isFav ? 'active' : ''}`}
                    onClick={handleToggleFavorite}
                >
                    {isFav ? '⭐' : '☆'}
                </button>
            </div>
            {detailContent}
        </div>
    );
};

export default DetailView;