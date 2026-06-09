import "./Profile.css"
import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import { Settings, RefreshCw, Bell } from "lucide-react" // Добавили RefreshCw и Bell

import Notifications from "./Notifications";

function Profile() {
    const navigate = useNavigate()
    const [categories, setCategories] = useState([])
    const [showCategoryInput, setShowCategoryInput] = useState(false)
    const [categoryName, setCategoryName] = useState("")
    const [newProductUrl, setNewProductUrl] = useState("")
    const [selectedMarketplace, setSelectedMarketplace] = useState("")

    // Стейт для анимации загрузки при обновлении цен
    const [isUpdating, setIsUpdating] = useState(false)

    async function fetchCategories() {
        const token = localStorage.getItem("token")
        const response = await fetch("http://localhost:8000/categories", {
            headers: { "Authorization": `Bearer ${token}` }
        })
        if (response.ok) {
            const data = await response.json()
            setCategories(data.map(cat => ({
                ...cat,
                open: true,
                addingProduct: false
            })))
        } else if (response.status === 401) {
            navigate("/login")
        }
    }

    useEffect(() => {
        fetchCategories()
    }, [])

    // --- НОВАЯ ФУНКЦИЯ: Принудительное обновление цен ---
    async function handleForceUpdatePrices() {
        if (isUpdating) return;
        setIsUpdating(true);
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8000/system/update-prices", {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.message); // Уведомляем, что процесс пошел

                // Ждем 5 секунд, пока бэкенд парсит, и обновляем категории с новыми ценами
                setTimeout(async () => {
                    await fetchCategories();
                    setIsUpdating(false);
                }, 5000);
            } else {
                alert("Ошибка при запуске обновления цен.");
                setIsUpdating(false);
            }
        } catch (error) {
            console.error("Ошибка при обновлении цен:", error);
            alert("Не удалось соединиться с сервером.");
            setIsUpdating(false);
        }
    }

    function createCategory() {
        setShowCategoryInput(true)
    }

    async function saveCategory() {
        if (categoryName.trim() === "") return
        const token = localStorage.getItem("token")
        const response = await fetch("http://localhost:8000/categories", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ name: categoryName })
        })
        if (response.ok) {
            setCategoryName("")
            setShowCategoryInput(false)
            fetchCategories()
        }
    }

    function toggleCategory(id) {
        setCategories(categories.map(cat =>
            cat.id === id ? { ...cat, open: !cat.open } : cat
        ))
    }

    function toggleAddProduct(id) {
        setCategories(categories.map(cat =>
            cat.id === id ? { ...cat, addingProduct: !cat.addingProduct } : cat
        ))
    }

    async function deleteCategory(id) {
        const token = localStorage.getItem("token")
        const response = await fetch(`http://localhost:8000/categories/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        })
        if (response.ok) {
            setCategories(categories.filter(cat => cat.id !== id))
        }
    }

    async function addProduct(categoryId) {
        if (newProductUrl.trim() === "") return;

        if (selectedMarketplace === "") {
            alert("Пожалуйста, выберите маркетплейс");
            return;
        }

        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:8000/add_product", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                url: newProductUrl,
                category_id: categoryId,
                marketplace_id: parseInt(selectedMarketplace)
            })
        });

        if (response.ok) {
            setNewProductUrl("");
            setSelectedMarketplace("");
            fetchCategories();
        } else {
            const errData = await response.json();
            alert(errData.detail || "Ошибка при добавлении товара");
        }
    }

    async function deleteProduct(productId) {
        const token = localStorage.getItem("token")
        const response = await fetch(`http://localhost:8000/products/${productId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        })
        if (response.ok) {
            setCategories(categories.map(cat => ({
                ...cat,
                products: cat.products.filter(p => p.id !== productId)
            })))
        }
    }

    async function clearCategory(id) {
        const token = localStorage.getItem("token")
        const response = await fetch(`http://localhost:8000/clear_category/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        })
        if (response.ok) {
            setCategories(categories.map(cat =>
                cat.id === id ? { ...cat, products: [] } : cat
            ))
        }
    }

    return (
        <div className="profile">
            <div className="profile_n">
                <div className="logo">price<span>tracker</span></div>

                {/* ПРАВАЯ ЧАСТЬ ШАПКИ СО ВСЕМИ КНОПКАМИ */}
                <div className="profile-nav-right">

                    {/* Кнопка обновления цен */}
                    <button
                        className={`update-prices-btn ${isUpdating ? "spinning" : ""}`}
                        onClick={handleForceUpdatePrices}
                        disabled={isUpdating}
                        title="Обновить цены сейчас"
                    >
                        <RefreshCw size={18} />
                        {isUpdating ? "Обновление..." : "Обновить цены"}
                    </button>

                    {/* Место для компонента Уведомлений */}
                    {/* Если у тебя есть <Notifications />, просто вставь его сюда вместо кнопки с Bell */}
                    <Notifications />

                    <button className="settings-btn-nav" onClick={() => navigate("/settings")} title="Настройки">
                        <Settings size={20} />
                    </button>
                    <button className="exit" onClick={() => navigate("/")}>Выйти</button>
                </div>
            </div>

            <button className="profile-create" onClick={createCategory}>+ Создать категорию</button>

            {showCategoryInput && (
                <div className="category-form">
                    <input
                        type="text"
                        placeholder="Название категории"
                        className="category-input"
                        value={categoryName}
                        onChange={(e) => setCategoryName(e.target.value)}
                    />
                    <button className="category-save" onClick={saveCategory}>Сохранить</button>
                </div>
            )}

            {categories.map(cat => (
                <div className="category" key={cat.id}>
                    <div className="category-header" onClick={() => toggleCategory(cat.id)}>
                        <div className="category-left">
                            <span className="arrow">{cat.open ? "▼" : "▶"}</span>
                            <span className="category-name">{cat.name}</span>
                        </div>
                        <div className="category-right">
                            <button className="cat-clear" onClick={(e) => { e.stopPropagation(); clearCategory(cat.id) }}>Очистить</button>
                            <button className="cat-delete" onClick={(e) => { e.stopPropagation(); deleteCategory(cat.id) }}>Удалить</button>
                        </div>
                    </div>

                    {cat.open && (
                        <div className="category-body">
                            {cat.products.map((p, i) => (
                                <div className="product-card" key={i}>
                                    <img
                                        className="product-img"
                                        src={p.image_url}
                                        alt={p.name}
                                    />
                                    <div className="product-desc">{p.name}</div>
                                    <div className="product-prices">
                                        <span className="price-tag">{p.price} ₽</span>
                                        <span className="price-min">min: {p.min_price} ₽</span>
                                        <span className="price-max">max: {p.max_price} ₽</span>
                                        <button className="delete-product-btn" onClick={() => deleteProduct(p.id)}>Удалить</button>
                                    </div>
                                </div>
                            ))}

                            {cat.addingProduct && (
                                <div className="add-product-form">
                                    <input
                                        type="text"
                                        placeholder="Вставьте ссылку на товар"
                                        className="product-input"
                                        value={newProductUrl}
                                        onChange={(e) => setNewProductUrl(e.target.value)}
                                    />
                                    <select
                                        className="marketplace-select"
                                        value={selectedMarketplace}
                                        onChange={(e) => setSelectedMarketplace(e.target.value)}
                                    >
                                        <option value="">Выберите маркетплейс</option>
                                        <option value="1">OZON</option>
                                        <option value="2">Wildberries</option>
                                        <option value="3">Яндекс Маркет</option>
                                    </select>
                                    <button className="product-confirm" onClick={() => addProduct(cat.id)}>Добавить</button>
                                </div>
                            )}

                            <button className="cat-add" onClick={() => toggleAddProduct(cat.id)}>+ Добавить товар</button>
                        </div>
                    )}
                </div>
            ))}
        </div>
    )
}

export default Profile