import { Bell, Check, CheckCheck } from "lucide-react"
import { useState, useEffect } from "react"
import "./Notifications.css"

function Notifications() {
    const [isOpen, setIsOpen] = useState(false)
    const [notifications, setNotifications] = useState([])

    // 1. Загрузка уведомлений
    async function fetchNotifications() {
        const token = localStorage.getItem("token")
        if (!token) return
        try {
            const response = await fetch("http://localhost:8000/notifications", {
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (response.ok) {
                const data = await response.json()
                setNotifications(data)
            }
        } catch (error) {
            console.error("Ошибка загрузки уведомлений:", error)
        }
    }

    // 2. Прочитать ОДНО конкретное уведомление
    async function handleMarkAsRead(id) {
        const token = localStorage.getItem("token")
        if (!token) return
        try {
            const response = await fetch(`http://localhost:8000/notifications/${id}/read`, {
                method: "PATCH",
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (response.ok) {
                // Удаляем прочитанное уведомление из стейта на фронте
                setNotifications(notifications.filter(n => n.id !== id))
            }
        } catch (error) {
            console.error("Ошибка при прочтении уведомления:", error)
        }
    }

    // 3. Прочитать ВСЕ уведомления разом
    async function handleMarkAllAsRead() {
        const token = localStorage.getItem("token")
        if (!token || notifications.length === 0) return
        try {
            const response = await fetch("http://localhost:8000/notifications/read", {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}` }
            })
            if (response.ok) {
                setNotifications([])
            }
        } catch (error) {
            console.error("Ошибка при прочтении всех уведомлений:", error)
        }
    }

    // Периодический опрос сервера раз в 15 секунд
    useEffect(() => {
        fetchNotifications()
        const interval = setInterval(() => {
            fetchNotifications()
        }, 15000)
        return () => clearInterval(interval)
    }, [])

    return (
        <div className="notifications">
            <button className="notif-bell" onClick={() => setIsOpen(!isOpen)}>
                <Bell size={20} />
                {notifications.length > 0 && <span className="notif-badge">{notifications.length}</span>}
            </button>

            {isOpen && (
                <div className="notif-dropdown">
                    <div className="notif-header">
                        <span>Уведомления</span>
                        {notifications.length > 0 && (
                            <button className="notif-read-all-btn" onClick={handleMarkAllAsRead}>
                                <CheckCheck size={14} /> Прочитать всё
                            </button>
                        )}
                    </div>

                    <div className="notif-list">
                        {notifications.length > 0 ? (
                            notifications.map(n => (
                                <div className="notif-item" key={n.id}>
                                    <div className="notif-content">
                                        <p className="notif-product">{n.product_name}</p>
                                        <p className="notif-text">{n.text}</p>
                                        <p className="notif-category">{n.category_name}</p>
                                    </div>

                                    {/* Отдельная кнопка «Прочитать» для каждого элемента */}
                                    <button
                                        className="notif-read-single-btn"
                                        onClick={() => handleMarkAsRead(n.id)}
                                        title="Пометить как прочитанное"
                                    >
                                        <Check size={16} />
                                    </button>
                                </div>
                            ))
                        ) : (
                            <div className="notif-empty">Нет новых уведомлений</div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}

export default Notifications