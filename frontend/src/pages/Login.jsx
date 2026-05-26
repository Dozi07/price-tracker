import LineTracker from "./LineTracker"
import "./Login.css"
import { useNavigate } from "react-router-dom"
import React, { useState } from 'react';

function Login() {
    const navigate = useNavigate()
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("") 

    async function startLogin() {
        setError("") 

        const response = await fetch("http://localhost:8000/login", { 
            method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify({ email, password }) 
        })

        const data = await response.json()

        if (response.ok) {
            console.log("Вход выполнен!", data)   
            localStorage.setItem("token", data.access_token) 
            navigate("/profile") 
        } else {
            setError(data.detail || "Ошибка входа")
        }
    }
    return (
        <div className="Login">
            <LineTracker />
            <div className="login-frame">
                <h1>Вход</h1>
                <input type="email" placeholder="Почта" value={email} onChange={(e) => setEmail(e.target.value)}/>
                <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)}/>
                <button className="login-btn" onClick={startLogin}>Войти</button>
                <p className="login-link" onClick={() => navigate("/register")}>
                    Нет аккаунта? <span>Зарегистрироваться</span>
                </p>
            </div>
        </div>
    )
}

export default Login