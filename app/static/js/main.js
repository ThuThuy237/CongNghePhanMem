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
//        neu chua co san pham trong gio hang thi them ga tri san pham moi vao gio hang thanh toan
        if (document.getElementById(id ) == null){
            document.getElementById("nothing ").innerHTML = ``
            document.getElementById("list-product").innerHTML = `
            <td>${id}</td>
            <td>${name}</td>
            <td>${price}</td>
            <td>
                <div class="form-group">
                    <input type="number"
                           value="0"
                           class="form-control " id="${id}" style="width: 100px;"/>
                </div>
            </td>`;}
//        so luong san pham them 1 moi khi bam vao san pham
        var value = parseInt(document.getElementById(id ).value) ;
        document.getElementById(id ).value = value + 1;
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

function show(){
    if($("input[id='new']:checked")){
        document.getElementById("hide-if-old").innerHTML = `<div class="form-group">
            <label for="category">Category</label>
            <input list="list-of-cate" name="category" id="category" class="form-control" required/>
        </div>
        <div class="form-group">
            <label for="author">Author</label>
            <input type="text"
                   required
                   autocomplete="on"
                   id="author"
                   name="author"
                   class="form-control"/>
        </div>
        <div class="form-group">
            <label for="quantity">Price </label>
            <input type="number "
                   required
                   id="price"
                   name="price"
                   class="form-control"/>
        </div>
        <div class="form-group">
            <label for="image">Image </label>
            <input type="file"
                   required
                   id="image"
                   name="image"
                   class="form-control"/>
        </div>`
    }
}

function hide(){
    if($("input[id='old']:checked")){
        document.getElementById("hide-if-old").innerHTML =`` ;
    }
}