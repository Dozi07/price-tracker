import "./Register.css"
import { useNavigate } from "react-router-dom"
import { useState } from "react"; //Объявления для useState, иначе ошибка

function Register(){
    const navigate = useNavigate()
    //Создание переменной email со значением "" и функции, которая изменяет этот email
    //Аналогично с password
    const [email,setEmail] = useState("")
    const [password,setPassword] = useState("")
    const [error, setError] = useState("") //Состояние ошибки, для пользователя!

    async function startRegistration(){
      
        const response = await fetch("http://localhost:8000/registrated", { //Отправление запроса, не двигаемся дальше,если не вернулся ответ
            method: "POST", //передача серверу данных
            headers: { "Content-Type": "application/json" }, //Передаем инфу, что внутри лежит формат JSON
            body: JSON.stringify({ email, password }) //Передача переменных и сплющивание их в единую фтроку формата JSON
    });
    //Убираем navigate("/profile") напрямую для кнопки "Созадть аккаунт"
    //Проверка, чтобы избежать смены страницы до того, как пользователь попал в бд 
    const data = await response.json(); //Превращаем ответ сервера в понятный объект

    if (response.ok) {
        console.log("Регистрация прошла успешно!",data);
        navigate("/login"); //Как раз из кнопки перекинули сюда, в проверку
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
                {/*Если вдруг существует error, выведем для пользователя инфу об ошибке*/}
                {error && <p style={{ color: "red", fontSize: "14px", marginBottom: "10px" }}>{error}</p>} 

                {/*Создание объекта события(е),нахождения объекта которые его вызвал(target),и достать оттуда value. */}
                {/*Onchange срабатывает каждый раз при вводе символа. Новый символ - вызов onChange */}
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