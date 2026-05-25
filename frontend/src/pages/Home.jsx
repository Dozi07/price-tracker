import "./Home.css"
import { useNavigate } from "react-router-dom";

function Home(){
      const navigate = useNavigate();
    return(
        <div className="home">

            <div className="top-bar">
                <div className="logo">price<span>tracker</span></div>
                <button className="but_sign" onClick={() => navigate("/login")}>Войти</button>
            </div>

            <header className="New">
                <h1>Начните отслеживать товары{" "}
                    <span className="doubleH1">c маркетплейсов</span></h1>
                <div className="Texts">
                    <p className="text1">Добавляйте ссылки на понравившиеся товары и получайте уведомления о снижении цены</p>
                    <p className="text2">Работает с крупнейшами площадками</p>
                </div>
            </header>

            <div className="Places">
                <div className="place1">Wildberries</div>
                <div className="place1">OZON</div>
                <div className="place1">Яндекс Маркет</div>
            </div>
            
            <button className="but1"
            onClick={() => navigate("register")}>Начать отслеживать</button>
            <div className="fon_icons">
                <div className="icons">
                    <div className="icon1">
                        <h3>Отслеживание цен</h3>
                        <p>Следите из изменением стоимости товара</p>
                    </div>
                    <div className="icon2">
                        <h3>Уведомления</h3>
                        <p>Получайте сообщения о скидках </p>
                    </div>
                    <div className="icon3">
                        <h3>Избранное</h3>
                        <p>Сохраняйте интересующие товары</p>
                    </div>
                </div>
             </div>
        </div>
    )
}

export default Home