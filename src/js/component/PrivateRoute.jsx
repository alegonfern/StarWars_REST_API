import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ element }) => {
    const isAuthenticated = sessionStorage.getItem('token'); // Verificar si el usuario está autenticado

    if (isAuthenticated) {
        // Si el usuario está autenticado, permito el acceso a la ruta
        return element; // Retorno el elemento directamente
    } else {
        // Si el usuario no está autenticado, redirigo a la página de Login
        return <Navigate to="/login" />;
    }
};

export default PrivateRoute;
