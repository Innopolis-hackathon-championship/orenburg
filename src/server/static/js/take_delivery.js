function setInputFilter(textbox, inputFilter) {
    [ "input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop", "focusout" ].forEach(function(event) {
      textbox.addEventListener(event, function(e) {
        if (inputFilter(this.value)) {
          // Accepted value.
          if ([ "keydown", "mousedown", "focusout" ].indexOf(e.type) >= 0){
            this.classList.remove("input-error");
            this.setCustomValidity("");
          }
  
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        }
        else if (this.hasOwnProperty("oldValue")) {
          // Rejected value: restore the previous one.
          this.classList.add("input-error");
          this.reportValidity();
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        }
        else {
          // Rejected value: nothing to restore.
          this.value = "";
        }
      });
    });
  }


const update = () => {
  return fetch("/api/take-delivery/").then(response => response.json()).then(json => {
      let productsList = document.getElementById("product-list")
      productsList.innerHTML = ""

      let products = ""
      json.forEach(product => {
          products += `
          <tr class="product_id=${product.id}">
              <td>${product.name}</td>
              <td><img class="product-img" src="${product.image}" alt=""></td>
              <td><input type="text" value="${product.price}" id="price_${product.id}"> р.</td>
              <td><span id="product_amount_${product.id}">${product.amount}</span> шт.</td>
              <td><input type="text" value="0" id="amount_${product.id}"> шт.</td>
          </tr>
          `
      });

      productsList.innerHTML = products
  })
}

document.getElementById("take_btn").addEventListener("click", (e) => {
  const rows = document.querySelectorAll('#product-list tr');

  products = []

  rows.forEach(row => {
    const productId = row.getAttribute('class').split('=')[1];
    const price = row.querySelector(`#price_${productId}`).value;
    const amount = row.querySelector(`#amount_${productId}`).value;
    const old_amount = row.querySelector(`#product_amount_${productId}`).textContent;

    products.push({
      id: productId,
      price: price,
      amount: parseInt(amount, 10) + parseInt(old_amount, 10)
    })
  });

  
  fetch("/api/take-delivery/", {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(products)
  });

  setTimeout(update, 500)
})

update()
