// src/components/Badge.jsx
import React from 'react';

const Badge = ({ type, children }) => {
    let className = 'badge';
    if (type) {
        className += ` badge-${type}`;
    }
    return <span className={className}>{children}</span>;
};

export default Badge;