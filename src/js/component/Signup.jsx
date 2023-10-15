import React, { useState } from 'react';

const Signup = () => {
    const [userData, setUserData] = useState({
        mail: '',
        password: '',
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        const url = "http://127.0.0.1:5000/signup"; // URL del servidor Flask

        const postOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Request-Method': 'POST'
            },
            body: JSON.stringify(userData),
        };

        try {
            const response = await fetch(url, postOptions);

            if (response.ok) {

                window.location.href = '/login';
                console.log("Usuario Creado con Exito.")
            } else {
                console.error('Revisa los datos ingresados');
            }
        } catch (error) {
            console.error('Error al enviar la solicitud', error);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUserData({
            ...userData,
            [name]: value,
        });
    };

    return (
        <div className="container">
            <div className="form-container col-12 col-md-8 col-lg-6 border rounded">
                <div className=' card singup_form p-3'><h3>¡Regístrate!</h3></div>

                <form className="row g-3 m-2" onSubmit={handleSubmit}>

                    <div className="col-md-6">
                        <label htmlFor="email" className="form-label">Email</label>
                        <input type="email" className="form-control" id="mail" name="mail" value={userData.mail} onChange={handleInputChange} required />
                    </div>

                    <div className="col-md-6">
                        <label htmlFor="password" className="form-label">Contraseña</label>
                        <input type="password" className="form-control" id="password" name="password" value={userData.password} onChange={handleInputChange} required />
                    </div>

                    <div className='col-md-6 offset-md-3'>
                        <button type='submit' className='btn btn-dark d-grid gap-2 mx-auto'>¡Registrate!</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Signup;