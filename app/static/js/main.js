function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        var cart = document.getElementById("cart-info");
        cart.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`;
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}

function addToSell(id, name, price) {
    fetch('/api/sellcart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        location.reload();
        var cart = document.getElementById("cart-info");
        cart.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`;
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}

function pay() {
    fetch('/api/pay', {
        method: "post",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        location.reload();
    }).catch(err => {
        location.href = '/admin/sellview';
    })
}