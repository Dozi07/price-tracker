import "./Profile.css"
import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"

function Profile() {
    const navigate = useNavigate()
    const [categories, setCategories] = useState([])
    const [showCategoryInput, setShowCategoryInput] = useState(false)
    const [categoryName, setCategoryName] = useState("")
    const [newProductUrl, setNewProductUrl] = useState("")
    const [selectedMarketplace, setSelectedMarketplace] = useState("")

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
        if (newProductUrl.trim() === "") return
        const token = localStorage.getItem("token")
        const response = await fetch("http://localhost:8000/add_product", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ url: newProductUrl, category_id: categoryId })
        })
        if (response.ok) {
            setNewProductUrl("")
            fetchCategories()
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

    return (
        <div className="profile">
            <div className="profile_n">
                <button className="exit" onClick={() => navigate("/")}>Выйти</button>
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
                            <button className="cat-clear" onClick={(e) => e.stopPropagation()}>Очистить</button>
                            <button className="cat-delete" onClick={(e) => { e.stopPropagation(); deleteCategory(cat.id) }}>Удалить</button>
                        </div>
                    </div>

                    {cat.open && (
                        <div className="category-body">
                            {cat.products.map((p, i) => (
                                <div className="product-card" key={i}>
                                    <div className="product-img"></div>
                                    <div className="product-desc">{p.name}</div>
                                    <div className="product-prices">
                                        <span className="price-tag">{p.price} ₽</span>
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
                                        <option value="wildberries">Wildberries</option>
                                        <option value="ozon">OZON</option>
                                        <option value="yandex">Яндекс Маркет</option>
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