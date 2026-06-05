import { Bell } from "lucide-react"
import { useState } from "react"
import "./Notifications.css"

function Notifications() {
    const [isOpen, setIsOpen] = useState(false)

    const notifications = [
        { id: 1, product_name: "Пусть тут будет", category: "Категория 1" },
        { id: 2, product_name: "Ваши обещания", category: "Категория 2" }
    ]

    return (
        <div className="notifications">
            <button className="notif-bell" onClick={() => setIsOpen(!isOpen)}>
                <Bell size={20} />
                {notifications.length > 0 && <span className="notif-badge">{notifications.length}</span>}
            </button>

            {isOpen && (
                <div className="notif-dropdown">
                    <div className="notif-header">Уведомления</div>
                    <div className="notif-list">
                        {notifications.map(n => (
                            <div className="notif-item" key={n.id}>
                                <p className="notif-product">{n.product_name}</p>
                                <p className="notif-category">{n.category}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}

export default Notifications