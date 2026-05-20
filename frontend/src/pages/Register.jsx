import "./Register.css"
import { useNavigate } from "react-router-dom"
import { useState } from "react";

function Register(){
    const navigate = useNavigate()
    const [email,setEmail] = useState("")
    const [password,setPassword] = useState("")
    const [error, setError] = useState("") 

    async function startRegistration(){
      
        const response = await fetch("http://localhost:8000/registrated", {
            method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify({ email, password }) 
    });
    const data = await response.json(); 

    if (response.ok) {
        console.log("Регистрация прошла успешно!",data);
        navigate("/login");
    } else {
        console.log("Ошибка сервера:", data);
        setError(data.detail || "Произошла ошибка при регистрации");
    }

    console.log("Запрос улетел, ответ получен!");
}
    

    return(
        <div className="Register">
            <div className="frame">
                <h1>Регистрация</h1>
                {error && <p style={{ color: "red", fontSize: "14px", marginBottom: "10px" }}>{error}</p>} 
                <input type="email" placeholder="Почта" value={email} onChange={(e) => setEmail(e.target.value)}/>
                <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)}/>
                <input type="password" placeholder="Повторите пароль" />
                <button className="but2" onClick={startRegistration}>Создать аккаунт</button>
                <p className="link" onClick={() => navigate("/login")}>Уже есть аккаунт? <span>Войти</span></p>
            </div>
        </div>
    )

}
export default Register