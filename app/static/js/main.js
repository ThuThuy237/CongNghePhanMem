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

function getQuantity(){

}

function addToSell() {
    id = document.getElementById("name").value;
    name = $( "#name option:selected" ).text();
    price = $( "#name option:selected" ).attr("name");
    cus_id = document.getElementById("customer").value;
    fetch('/api/sellcart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "cus_id": cus_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);

        addProduct(id, name, price)

        document.getElementById("customer").value = cus_id;
        var value = parseInt(document.getElementById(id ).value) ;
        document.getElementById(id ).value = value + 1;
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}


function addToBuy() {
    id = document.getElementById("name").value;
    name = $( "#name option:selected" ).text();
    price = $( "#name option:selected" ).attr("name");
    sup_id = document.getElementById("supplier").value;
    fetch('/api/buy-cart', {
        method: "post",
        body: JSON.stringify({
            "sup_id": sup_id,
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        addProduct(id, name, price)

        document.getElementById("supplier").value = sup_id;
        var value = parseInt(document.getElementById(id ).value) ;
        document.getElementById(id ).value = value + 1;

    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}


function submitOder() {
    fetch('/api/submit-order', {
        method: "post",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        location.reload();
    }).catch(err => {
        console.log(err);
    })
}


function submitBuy() {
    fetch('/api/submit-buy', {
        method: "post",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        location.reload();
    }).catch(err => {
        console.log(err);
    })
}


function addProduct(id, name, price){
if (document.getElementById(id ) == null){
            var newProduct = document.getElementById("new-product");
            var tr = document.createElement('tr');
            var tdId = document.createElement('td');
            var tdName = document.createElement('td');
            var tdPrice = document.createElement('td');
            var tdInput = document.createElement('td');
            var div = document.createElement('div');
            div.class = `form-group`;
            var input = document.createElement('input');
            input.type = `number`;
            input.value = `0`;
            input.class = `form-control`;
            input.id = `${id}`;
            input.style = `width: 100px;`;
            newProduct.appendChild(tr);
            tr.appendChild(tdId);
            tdId.appendChild(document.createTextNode(id));
            tr.appendChild(tdName);
            tdName.appendChild(document.createTextNode(name));
            tr.appendChild(tdPrice);
            tdPrice.appendChild(document.createTextNode(price));
            tr.appendChild(tdInput);
            tdInput.appendChild(div);
            div.appendChild(input);
            }
}

