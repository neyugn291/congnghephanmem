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


        let selectedItem = document.getElementById("cart-id-" + id);
        if (selectedItem) {
            selectedItem.remove(); //xoa item da chon
        }

        renderInfoCart(data)
    });
}

// function removeFromCart(productId) {
//     if (confirm("Bạn chắc chắn xóa không?") === true) {
//         fetch(`/api/carts/${productId}`, {
//             method: "delete"
//         }).then(res => res.json()).then(data => {
//
//
//             document.getElementById(`cart${productId}`).style.display = "none";
//             renderInfoCart(data);
//         })
//     }
// }

function changeQuantity(id) {
    let quantity = parseInt(document.querySelector(`#cart-id-${id} .quantity`).value);

    if (isNaN(quantity) || quantity < 1) {
        // Nếu số lượng không hợp lệ, reset lại giá trị về 1
        quantity.value = 1;
        quantity = 1;
        alert("Số lượng phải lớn hơn hoặc bằng 1.");
    }

    fetch('/update-quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "id":id,
            "quantity": quantity
        }),
    }).then(response => response.json()).then(data => {
        renderInfoCart(data);
    })
}

function updateCart(productId, obj) {
    fetch(`/api/carts/${productId}`, {
        method: "put",
        body: JSON.stringify({
            quantity: obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {

        renderInfoCart(data);
    })
}

function renderInfoCart(data) {
    let items = document.getElementsByClassName("cart-counter");
    for (let item of items)
        item.innerText = data.total_quantity; //cap nhat lai so luong trong gio hang

    let info = document.querySelectorAll(".cart-info h3");
    let formattedTotalAmount = new Intl.NumberFormat('en-US').format(data.total_amount);


    info[0].textContent = "Tổng sản phẩm: " + data.total_quantity;
    info[1].textContent = "Tổng tiền: " + formattedTotalAmount + "VNĐ";
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?") === true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.status === 200) {
                alert("Thanh toán thành công!");
                location.reload();
            }
        })
    }
}
