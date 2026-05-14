import "./Profile.css"
import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"

function Profile() {
    const navigate = useNavigate()
    const [categories, setCategories] = useState([])
    const [showCategoryInput, setShowCategoryInput] = useState(false)
    const [categoryName, setCategoryName] = useState("")
    const [newProductUrl, setNewProductUrl] = useState("")

    // 1. Скачиваем категории (вместе с товарами) из БД
    async function fetchCategories() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8000/categories", {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                // Добавляем к данным из БД свойства для визуала (открыта ли вкладка)
                const categoriesWithUI = data.map(cat => ({
                    ...cat,
                    open: true,
                    addingProduct: false
                }));
                setCategories(categoriesWithUI);
            } else if (response.status === 401) {
                navigate("/login");
            }
        } catch (error) {
            console.error("Ошибка загрузки категорий:", error);
        }
    }

    // Вызываем при загрузке страницы
    useEffect(() => {
        fetchCategories();
    }, []);

    // 2. Создание новой категории в БД
    async function saveCategory() {
        if (categoryName.trim() === "") return;
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8000/categories", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ name: categoryName })
            });

            if (response.ok) {
                setCategoryName("");
                setShowCategoryInput(false);
                fetchCategories(); // Перезапрашиваем список после создания
            }
        } catch (error) {
            console.error("Ошибка создания категории:", error);
        }
    }

    // 3. Добавление товара (теперь передаем category_id)
    async function handleAddProduct(categoryId) {
        if (!newProductUrl) return;

        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8000/add_product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                // ВАЖНО: теперь отправляем и url, и category_id
                body: JSON.stringify({
                    url: newProductUrl,
                    category_id: categoryId
                })
            });

            if (response.ok) {
                setNewProductUrl("");
                fetchCategories(); // Перезапрашиваем всё, чтобы товар появился в списке
            } else {
                const err = await response.json();
                alert("Ошибка: " + JSON.stringify(err));
            }
        } catch (error) {
            console.error("Ошибка добавления товара:", error);
        }
    }

    // Визуальные переключалки
    function createCategory() { setShowCategoryInput(true); }
    function toggleCategory(id) {
        setCategories(categories.map(cat => cat.id === id ? { ...cat, open: !cat.open } : cat));
    }
    function toggleAddProduct(id) {
        setCategories(categories.map(cat => cat.id === id ? { ...cat, addingProduct: !cat.addingProduct } : cat));
    }

    return (
        <div className="profile">
            <div className="profile_n">
                <button className="exit" onClick={() => { localStorage.removeItem("token"); navigate("/"); }}>Выйти</button>
            </div>

            <button className="profile-create" onClick={createCategory}>+ Создать категорию</button>

            {showCategoryInput && (
                <div className="category-form">
                    <input type="text" placeholder="Название категории" className="category-input" value={categoryName} onChange={(e) => setCategoryName(e.target.value)} />
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
                    </div>

                    {cat.open && (
                        <div className="category-body">
                            {cat.products && cat.products.map((p) => (
                                <div className="product-card" key={p.id}>
                                    <div className="product-img"></div>
                                    <div className="product-desc">
                                        <strong>{p.name}</strong><br/>
                                        <small><a href={p.url} target="_blank" rel="noreferrer">Ссылка на товар</a></small>
                                    </div>
                                    <div className="product-prices">
                                        <span className="price-tag">{p.price} ₽</span>
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
                                    <button className="product-confirm" onClick={() => handleAddProduct(cat.id)}>Добавить</button>
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