import "./Login.css"
import { useNavigate } from "react-router-dom"

function Login() {
    const navigate = useNavigate()
    return (
        <div className="Login">
            <div className="login-frame">
                <h1>Вход</h1>
                <input type="email" placeholder="Почта" />
                <input type="password" placeholder="Пароль" />
                <button className="login-btn" onClick={() => navigate("/profile")}>Войти</button>
                <p className="login-link" onClick={() => navigate("/register")}>
                    Нет аккаунта? <span>Зарегистрироваться</span>
                </p>
            </div>
        </div>
    )
}

export default Login