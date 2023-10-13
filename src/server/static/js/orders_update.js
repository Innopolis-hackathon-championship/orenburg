const urlMap = {
    orders: "/api/order/test/"
}

const get = (url) => {
    
}

const update = () => {
    return fetch(urlMap.orders).then(response => response.json()).then(json => {
        let orders = document.getElementById("orders")
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
                        <p>${product.quantity}</p>
                    </div>
                </li>
                `

                price += product.product.price
            })

            orders.innerHTML += `
            <li>
                <div class="order">
                    <p><span class="bold">Адрес доставки:</span> ${element.delivery_address}</p>
                    <p><span class="bold">Список продуктов:</span></p>
                    <ul>
                        ${products}
                    </ul>
                    <p><span class="bold">Стоимость: </span>${price} p.</p>
                </div>
            </li>
            `
        });
    })
}

update()
// const interId = setInterval(update, 1000)
