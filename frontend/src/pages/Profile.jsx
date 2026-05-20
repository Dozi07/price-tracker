import "./Profile.css"
import { useNavigate } from "react-router-dom"
import { useState, useEffect, useRef } from "react"

function Profile() {
    const navigate = useNavigate()
    const [categories, setCategories] = useState([])
    const [showCategoryInput, setShowCategoryInput] = useState(false)
    const [categoryName, setCategoryName] = useState("")
    const [newProductUrl, setNewProductUrl] = useState("")
    const [userEmail, setUserEmail] = useState("Пользователь");
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    async function fetchCategories() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8000/categories", {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
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

    useEffect(() => {
        fetchCategories();
        
        const savedEmail = localStorage.getItem("user_email");
        if (savedEmail) {
            setUserEmail(savedEmail);
        }
    }, []);

    useEffect(() => {
        function handleClickOutside(event) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

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
                fetchCategories();
            }
        } catch (error) {
            console.error("Ошибка создания категории:", error);
        }
    }

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
                body: JSON.stringify({
                    url: newProductUrl,
                    category_id: categoryId
                })
            });

            if (response.ok) {
                setNewProductUrl("");
                fetchCategories();
            } else {
                const err = await response.json();
                alert("Ошибка: " + JSON.stringify(err));
            }
        } catch (error) {
            console.error("Ошибка добавления товара:", error);
        }
    }

    async function handleDeleteProduct(productId) {
        if (!window.confirm("Вы уверены, что хотите удалить этот товар?")) return;
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`http://localhost:8000/products/${productId}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (response.ok) {
                setCategories(prev => prev.map(cat => ({
                    ...cat,
                    products: cat.products.filter(p => p.id !== productId)
                })));
            } else {
                alert("Ошибка при удалении товара");
            }
        } catch (error) {
            console.error("Ошибка:", error);
        }
    }

    async function handleDeleteCategory(categoryId) {
        if (!window.confirm("Вы уверены, что хотите удалить ВСЮ категорию и ВСЕ товары в ней?")) return;
        try {
            const token = localStorage.getItem("token");
            const response = await fetch(`http://localhost:8000/categories/${categoryId}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (response.ok) {
                setCategories(prev => prev.filter(cat => cat.id !== categoryId));
            } else {
                alert("Ошибка при удалении категории");
            }
        } catch (error) {
            console.error("Ошибка удаления категории:", error);
        }
    }

    function createCategory() { setShowCategoryInput(true); }
    
    function toggleCategory(id) {
        setCategories(categories.map(cat => cat.id === id ? { ...cat, open: !cat.open } : cat));
    }
    
    function toggleAddProduct(id) {
        setCategories(categories.map(cat => cat.id === id ? { ...cat, addingProduct: !cat.addingProduct } : cat));
    }

    return (
        <div className="profile" style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto', position: 'relative' }}>
            <div className="profile_n" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px', width: '100%' }}>
                <div className="user-menu-wrapper" ref={dropdownRef} style={{ position: 'relative' }}>
                    <div 
                        className="profile-capsule" 
                        onClick={() => setDropdownOpen(!dropdownOpen)}
                        style={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: '10px', 
                            padding: '8px 16px', 
                            borderRadius: '24px', 
                            backgroundColor: '#ffffff', 
                            border: '1px solid #d1d5db', 
                            cursor: 'pointer',
                            userSelect: 'none',
                            boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
                        }}
                    >
                        <div className="profile-avatar" style={{ width: '26px', height: '26px', borderRadius: '50%', backgroundColor: '#1d4ed8', color: '#ffffff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '13px', fontWeight: 'bold' }}>
                            {userEmail[0].toUpperCase()}
                        </div>
                        <span style={{ fontSize: '14px', color: '#374151', fontWeight: '500' }}>{userEmail}</span>
                        <span style={{ fontSize: '11px', color: '#9ca3af' }}>{dropdownOpen ? '▲' : '▼'}</span>
                    </div>
                    {dropdownOpen && (
                        <div className="profile-dropdown-content" style={{ position: 'absolute', right: 0, top: '100%', marginTop: '8px', backgroundColor: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', width: '170px', zIndex: 999, overflow: 'hidden' }}>
                            <div style={{ padding: '5px 14px', borderBottom: '1px solid #f3f4f6', fontSize: '14px', color: '#9ca3af' }}>
                                Личный кабинет
                            </div>
                            <button 
                                className="exit" 
                                onClick={() => { 
                                    localStorage.removeItem("token"); 
                                    navigate("/"); 
                                }}
                                style={{ width: '100%', padding: '10px 14px', textAlign: 'left', background: 'none', border: 'none', color: '#dc2626', fontSize: '14px', cursor: 'pointer', fontWeight: '500' }}
                            >
                                Выйти
                            </button>
                        </div>
                    )}
                </div>
            </div>

            <button className="profile-create" onClick={createCategory}>+ Создать категорию</button>

            {showCategoryInput && (
                <div className="category-form" style={{ margin: '15px 1' }}>
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
                    <div className="category-header" onClick={() => toggleCategory(cat.id)} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                        <div className="category-left">
                            <span className="arrow">{cat.open ? "▼" : "▶"}</span>
                            <span className="category-name">{cat.name}</span>
                        </div>
                        <button 
                            className="delete-category-btn"
                            onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteCategory(cat.id);
                            }}
                        >
                            Удалить категорию
                        </button>
                    </div>

                    {cat.open && (
                        <div className="category-body">
                            {cat.products.map(p => (
                                <div key={p.id} className="category-products" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid #f3f4f6' }}>
                                    <div className="product-info">
                                        <strong className="product-title" style={{ fontSize: '16px' }}>{p.name}</strong>
                                        <div className="price-history-summary" style={{ display: 'flex', gap: '8px', fontSize: '13px', color: '#6b7280', margin: '6px 0' }}>
                                            <span>min: <strong style={{ color: '#16a34a' }}>{p.min_price || p.price} ₽</strong></span>
                                            <span>|</span>
                                            <span>max: <strong style={{ color: '#dc2626' }}>{p.max_price || p.price} ₽</strong></span>
                                        </div>
                                        <small><a href={p.url} target="_blank" rel="noreferrer" style={{ color: '#2563eb', textDecoration: 'underline' }}>Ссылка на товар</a></small>
                                    </div>

                                    <div className="product-prices" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                                        <span className="price-tag" style={{ fontWeight: 'bold', fontSize: '15px' }}>{p.price} ₽</span>
                                        <button 
                                            className="delete-product-btn" 
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleDeleteProduct(p.id);
                                            }}
                                        >
                                            Удалить
                                        </button>
                                    </div>
                                </div>
                            ))}

                            {cat.addingProduct && (
                                <div className="add-product-form" style={{ marginTop: '15px' }}>
                                    <input
                                        type="text"
                                        placeholder="Вставьте ссылку на товар"
                                        className="product-input"
                                        value={newProductUrl}
                                        onChange={(e) => setNewProductUrl(e.target.value)}
                                    />
                                    <button 
                                        className="product-confirm" 
                                        onClick={async () => {
                                            if (!newProductUrl) {
                                                alert("Пожалуйста, вставьте ссылку");
                                                return;
                                            }
                                            await handleAddProduct(cat.id);
                                            setNewProductUrl("");
                                        }}
                                    >
                                        Добавить
                                    </button>
                                </div>
                            )}
                            <button className="cat-add" onClick={() => toggleAddProduct(cat.id)}>+ Добавить товар</button>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}

export default Profile;