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


function getValue(id){
    return document.getElementById(id).value;
}

function addToSell() {
    id = document.getElementById("name").value;
    fetch('/api/sellcart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        location.reload();
//
        var value = parseInt(document.getElementById(id ).value) ;
        document.getElementById(id ).value = value + 1;
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}

function addToBuy(id, name, price) {
    fetch('/api/buycart', {
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
        console.log(err);
//        location.href = '/';
    })
}


//function add_book() {
//    var supplier = document.getElementById("supplier").value;
//    var name = document.getElementById("name").value;
//    var author = document.getElementById("author").value;
//    var category = document.getElementById("category").value;
//    var price = document.getElementById("price").value;
//    var image = document.getElementById("image").value;
//
//    fetch('/api/buy-cart', {
////        method: "post",
//        body: JSON.stringify({
//            "supplier": supplier,
////            "id": id,
//            "name": name,
//            "author": author,
//            "category": category,
//            "price": price
//        }),
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    }).then(res => res.json()).then(data => {
//        console.info(data);
//        var cart = document.getElementById("cart-info");
//        cart.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`;
//    }).catch(err => {
//        console.log(err);
//    })
//
//}

