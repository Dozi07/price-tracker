import "./Register.css"
import { useNavigate } from "react-router-dom"

function Register(){
    const navigate = useNavigate()
    return(
        <div className="Register">
            <div className="frame">
                <h1>Регистрация</h1>
                <input type="email" placeholder="Почта" />
                <input type="password" placeholder="Пароль" />
                <input type="password" placeholder="Повторите пароль" />
                <button className="but2" onClick={() => navigate("/profile")}>Создать аккаунт</button>
                <p className="link" onClick={() => navigate("/login")}>Уже есть аккаунт? <span>Войти</span></p>
            </div>
        </div>
    )

}
export default Register