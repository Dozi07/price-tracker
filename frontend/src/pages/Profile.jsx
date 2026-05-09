import "./Profile.css"
import { useNavigate } from "react-router-dom"
import { useState } from "react"

function Profile() {
    const navigate = useNavigate()
    const [categories, setCategories] = useState([
    { id: 1, name: "Тестовая категория - показывает карточку товара с ценой", open: true, addingProduct: false, products: [
        { marketplace: "OZON" }
    ]}
    ])
    const [showCategoryInput, setShowCategoryInput] = useState(false)
    const [categoryName, setCategoryName] = useState("")

    function createCategory() {
        setShowCategoryInput(true)
    }

    function saveCategory() {
        if (categoryName.trim() === "") return
        const newCategory = { id: Date.now(), name: categoryName, open: true, products: [], addingProduct: false }
        setCategories([...categories, newCategory])
        setCategoryName("")
        setShowCategoryInput(false)
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

    function deleteCategory(id) {
        setCategories(categories.filter(cat => cat.id !== id))
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
                                    <div className="product-desc">Описание товара</div>
                                    <div className="product-prices">
                                        <span className="price-tag">{p.marketplace}</span>
                                        <span className="price-tag">Цена</span>
                                    </div>
                                </div>
                            ))}

                            {cat.addingProduct && (
                                <div className="add-product-form">
                                    <input
                                        type="text"
                                        placeholder="Вставьте ссылку на товар"
                                        className="product-input"
                                    />
                                    <select className="marketplace-select">
                                        <option value="">Выберите маркетплейс</option>
                                        <option value="wildberries">Wildberries</option>
                                        <option value="ozon">OZON</option>
                                        <option value="yandex">Яндекс Маркет</option>
                                    </select>
                                    <button className="product-confirm">Добавить</button>
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