import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom"; // Agrega useNavigate
import { UserContext } from "../store/UserContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart, faUser } from "@fortawesome/free-regular-svg-icons";
import { faTrash } from "@fortawesome/free-solid-svg-icons";

const Navbar = () => {
    const { favorites, removeFavorite, logout } = useContext(UserContext);
    const navigate = useNavigate(); // Obtiene la función navigate

    // Verifico si el usuario está autenticado 
    const isAuthenticated = sessionStorage.getItem('token');

    // Realizo el logout y redirigir al usuario al login
    const handleLogout = () => {
        logout(); // Llamo a la función de logout en el contexto
        navigate('/login'); // Redirigo al usuario a la página de inicio de sesión
    };

    return (
        <nav className="navbar navbar-expand-lg bg-light">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">Stars Wars</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav ms-auto bg-primary rounded">
                        {isAuthenticated && ( // Muestro solo si el usuario está autenticado
                            <li className="nav-item dropdown">
                                <div className="dropdown">
                                    <a className="nav-link dropdown-toggle" href="#" role="button" id="favorites-dropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                        <FontAwesomeIcon icon={faHeart} className="me-1" />
                                        Favorites <span className="badge bg-dark text-white ms-1 rounded-pill">{favorites.length}</span>
                                    </a>
                                    <ul className="dropdown-menu" aria-labelledby="favorites-dropdown">
                                        {favorites.length > 0 ? (
                                            favorites.map((favorite, index) => (
                                                <li key={index} className="d-flex justify-content-between">
                                                    <a className="dropdown-item" href="#">{favorite.name}</a>
                                                    <button
                                                        className="btn"
                                                        onClick={() => removeFavorite(favorite)}
                                                    >
                                                        <FontAwesomeIcon icon={faTrash} />
                                                    </button>
                                                </li>
                                            ))
                                        ) : (
                                            <li><a className="dropdown-item disabled" href="#">No favorites selected</a></li>
                                        )}
                                    </ul>
                                </div>
                            </li>
                        )}

                        <li className="nav-item dropdown">
                            <div className="dropdown">
                                {isAuthenticated ? (
                                    <button className="btn btn-link text-white" onClick={handleLogout}>Logout</button>
                                ) : (
                                    <a className="nav-link dropdown-toggle" href="#" role="button" id="account-dropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                        <FontAwesomeIcon icon={faUser} className="me-1" />
                                        Account
                                    </a>
                                )}
                                <ul className="dropdown-menu" aria-labelledby="account-dropdown">
                                    <li><Link to="/login" className="dropdown-item">Login</Link></li>
                                    <li><Link to="/signup" className="dropdown-item">Signup</Link></li>
                                </ul>
                            </div>
                        </li>

                    </ul>

                </div>
            </div>
        </nav>
    );
};

export default Navbar;
