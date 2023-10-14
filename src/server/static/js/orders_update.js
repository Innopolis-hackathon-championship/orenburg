const urlMap = {
    orders: "/api/new-orders/",
    orderReady: "/api/order/ready/",

    findDelivery: "/api/delivery/find/?",
    statusDelivery: "/api/delivery/status/?",
    giveDelivery: "/api/order/take/?",
}

const get = (url) => {
    
}

const update = () => {
    fetch(urlMap.orders).then(response => response.json()).then(json => {
        let orders = document.getElementById("order-list")
        orders.innerHTML = ""

        json.forEach(element => {
            let products = ""
            let price = 0

            element.products.forEach(product => {
                products += `
                <li>
                    <div class="item">
                        <img src="${product.product.image}" alt="123" >
                        <p>${product.product.name}</p>
                        <p>${product.amount}</p>
                    </div>
                </li>
                `

                price += product.product.price * product.amount
            })

            orders.innerHTML += `
            <li>
                <div class="order order_${element.id}">
                    <p><span class="bold">Адрес доставки:</span> ${element.delivery_address || "Cамовывоз"}</p>
                    <p><span class="bold">Список продуктов:</span></p>
                    <ul>
                        ${products}
                    </ul>
                    <p><span class="bold">Стоимость: </span>${price} p.</p>

                    ${
                        element.status === "prepare" ?
                            element.delivery_address ?
                            `<input class="send" type="submit" value="Отправить в доставку" onclick="sendDelivery(${element.id})">`
                            :
                            `<input class="send" type="submit" value="Сообщить о готовности" onclick="orderReady(${element.id})">`
                        :
                            element.status === "ready" ?
                            `<p>Ищем курьера...</p>`
                            :
                            `
                            <div style="display: flex;">
                                <input class="send" type="submit" value="Отдать курьеру" onclick="giveDelivery(${element.id})">
                                <p style="margin-left: 30px;">PIN код для проверки: ${element.code}</p>
                            </div>
                            `
                    }
                </div>
            </li>
            `
        });
    })
}

const sendDelivery = (orderId) => {
    fetch(urlMap.findDelivery + new URLSearchParams({
        order_id: orderId,
    }))
}

const orderReady = (orderId) => {
    fetch(urlMap.orderReady + new URLSearchParams({
        order_id: orderId,
    }))
}

const giveDelivery = (orderId) => {
    fetch(urlMap.giveDelivery + new URLSearchParams({
        order_id: orderId,
    }))
}

// document.getElementById('send-delivery').addEventListener('submit', function(event) {
//     event.preventDefault();
//     fetch("")
// });

update()
const interId = setInterval(update, 1000)
