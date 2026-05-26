import "./Settings.css"
import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { Mail, Lock, Trash2 } from "lucide-react"

function Settings() {
    const navigate = useNavigate()

    return (
        <div className="settings">
            <button className="settings-back" onClick={() => navigate("/profile")}>← Назад</button>
            <h1>Настройки</h1>

            <motion.div
                className="settings-cards"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
            >
                <div className="settings-card">
                    <div className="settings-card-title">
                        <Mail size={20} /> Изменить email
                    </div>
                    <input type="email" placeholder="Новый email" className="settings-input" />
                    <button className="settings-btn">Сохранить</button>
                </div>

                <div className="settings-card">
                    <div className="settings-card-title">
                        <Lock size={20} /> Изменить пароль
                    </div>
                    <input type="password" placeholder="Старый пароль" className="settings-input" />
                    <input type="password" placeholder="Новый пароль" className="settings-input" />
                    <input type="password" placeholder="Повторите новый пароль" className="settings-input" />
                    <button className="settings-btn">Сохранить</button>
                </div>

                <div className="settings-card">
                    <div className="settings-card-title">
                        <Trash2 size={20} /> Удалить аккаунт
                    </div>
                    <p className="settings-warning">Это действие нельзя отменить</p>
                    <button className="settings-btn-delete">Удалить аккаунт</button>
                </div>
            </motion.div>
        </div>
    )
}

export default Settings