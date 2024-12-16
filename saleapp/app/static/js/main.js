function addToCart(id, name, price) {
    fetch("/api/carts", {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    });
}

function removeFromCart(id) {
    fetch("/api/carts", {
        method: "DELETE",
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity; //cap nhat lai so luong trong gio hang

        let selectedItem = document.getElementById("cart-id-"+id);
        if (selectedItem) {
            selectedItem.remove(); //xoa item da chon
        }
        let info = document.querySelectorAll(".cart-info h3");
        let formattedTotalAmount = new Intl.NumberFormat('en-US').format(data.total_amount);

        info[0].textContent = "Tổng sản phẩm: " + data.total_quantity;
        info[1].textContent = "Tổng tiền: " + formattedTotalAmount + "VNĐ";
    });
}


