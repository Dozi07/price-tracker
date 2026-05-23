import "./Settings.css"
import { useNavigate } from "react-router-dom"

function Settings() {
    const navigate = useNavigate()

    return (
        <div className="settings">
            <h1>Настройки</h1>
            <div className="settings-section">
                <h2>Изменить email</h2>
                <input type="email" placeholder="Новый email" className="settings-input" />
                <button className="settings-btn">Сохранить</button>
            </div>
             <div className="settings-section">
                <h2>Изменить пароль</h2>
                <input type="password" placeholder="Старый пароль" className="settings-input" />
                <input type="password" placeholder="Новый пароль" className="settings-input" />
                <input type="password" placeholder="Повторите новый пароль" className="settings-input" />
                <button className="settings-btn">Сохранить</button>
            </div>
            <div className="settings-section">
                <h2>Удалить аккаунт</h2>
                <p>Это действие нельзя отменить</p>
                <button className="settings-btn-delete">Удалить аккаунт</button>
            </div>
        </div>
    )
}

export default Settings