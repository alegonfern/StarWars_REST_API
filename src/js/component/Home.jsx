import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useContext, useState, useEffect } from "react";
import { UserContext } from "../store/UserContext";
import { useNavigate, useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as faSolidHeart, faHeart } from "@fortawesome/free-solid-svg-icons";
import { faHeart as faRegularHeart } from "@fortawesome/free-regular-svg-icons";
import Footer from "./Footer";

const Home = () => {
    const { characterData, planetData, addFavorite, removeFavorite, isFavorite } = useContext(UserContext);
    const storedFavorites = JSON.parse(localStorage.getItem('favorites')) || [];


    return (<>

        <section className="py-5" >
            <h1> Characters: </h1>
            <div className="container px-4 px-lg-5 mt-5" >

                <div className="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center" >
                    {characterData.map((character) => (
                        <div className="col mb-5" key={character.result.uid}>
                            <div className="card h-100">

                                <img className="card-img-top" src="https://dummyimage.com/450x300/dee2e6/6c757d.jpg" alt="..." />

                                <div className="card-body p-4">
                                    <div className="text-center">

                                        <h5 className="fw-bolder">{character.result.properties.name}</h5>

                                        {character.result.properties.gender}
                                    </div>
                                </div>

                                <div className="card-footer p-4 pt-0 border-top-0 bg-transparent">

                                    <div className="text-center d-flex justify-content-between align-items-center">
                                        <Link to={`/detail_character/${character.result.uid}`} className="btn btn-outline-dark mt-auto">View details</Link>
                                        <FontAwesomeIcon icon={isFavorite(`C_${character.result.uid}`) ? faSolidHeart : faRegularHeart} style={{ color: isFavorite(`C_${character.result.uid}`) ? "#f90606" : "" }} className="fa-xl" onClick={() => {
                                            const favorite = {
                                                id: `C_${character.result.uid}`,
                                                name: character.result.properties.name
                                            };

                                            if (storedFavorites.some((item) => item.id === favorite.id)) {
                                                removeFavorite(favorite);
                                            } else {
                                                addFavorite(favorite);
                                            }
                                        }}
                                        />
                                    </div>

                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
        <section className="mt-0" >
            <h1> Planets: </h1>
            <div className="container px-4 px-lg-5 mt-5" >

                <div className="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center" >
                    {planetData.map((planet) => (
                        <div className="col mb-5" key={planet.result.uid}>
                            <div className="card h-100">

                                <img className="card-img-top" src="https://dummyimage.com/450x300/dee2e6/6c757d.jpg" alt="..." />

                                <div className="card-body p-4">
                                    <div className="text-center">

                                        <h5 className="fw-bolder">{planet.result.properties.name}</h5>

                                        Population: {planet.result.properties.population}
                                    </div>
                                </div>
                                <div className="card-footer p-4 pt-0 border-top-0 bg-transparent">
                                    <div className="text-center d-flex justify-content-between align-items-center">
                                        <Link to={`/detail_planet/${planet.result.uid}`} className="btn btn-outline-dark mt-auto">View details</Link>
                                        <FontAwesomeIcon icon={isFavorite(`P_${planet.result.uid}`) ? faSolidHeart : faRegularHeart} style={{ color: isFavorite(`P_${planet.result.uid}`) ? "#f90606" : "" }} className="fa-xl" onClick={() => {
                                            const favorite = {
                                                id: `P_${planet.result.uid}`,
                                                name: planet.result.properties.name
                                            };

                                            if (storedFavorites.some((item) => item.id === favorite.id)) {
                                                removeFavorite(favorite);
                                            } else {
                                                addFavorite(favorite);
                                            }
                                        }}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

            </div>
        </section>

        <Footer />

    </>
    )
};

export default Home;