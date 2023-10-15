import React, { useState, useContext } from 'react';
import { UserContext } from "../store/UserContext";
import { useNavigate } from 'react-router-dom';


const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const { flogin } = useContext(UserContext);
    const navigate = useNavigate();

    const handleInputChange = (event) => {
        if (event.target.name === 'email') {
            setEmail(event.target.value);
        } else if (event.target.name === 'password') {
            setPassword(event.target.value);
        }
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        const resultado = await flogin(email, password);
        console.log("success:", resultado, "Estas siendo redirigido al Home");
        if (resultado) {
            // Redirigo al usuario a la ruta.
            navigate("/home");
        }

    }



    return (
        <form onSubmit={handleSubmit} className="container mt-4">
            {error && <div className="alert alert-danger">{error}</div>}
            <div className="form-group">
                <label htmlFor="email">Correo electrónico</label>
                <input type="email" className="form-control" id="email" name="email" value={email} onChange={handleInputChange} />
            </div>

            <div className="form-group">
                <label htmlFor="password">Contraseña</label>
                <input type="password" className="form-control" id="password" name="password" value={password} onChange={handleInputChange} />
            </div>

            <button type="submit" className="btn btn-primary">
                Iniciar sesión
            </button>
        </form>
    );
}

export default Login;
