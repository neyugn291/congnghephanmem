
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
        console.log(data)
        let selectedItem = document.getElementById("cart-id-" + id);
        if (selectedItem) {
            selectedItem.remove(); //xoa item da chon
        }
        renderInfoCart(data)
    });
}

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
            "id": id,
            "quantity": quantity
        }),
    }).then(response => response.json()).then(data => {
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



function addComment(bookId) {
    fetch(`/api/books/${bookId}/comments`, {
        method: "post",
        body: JSON.stringify({
            'content': document.getElementById("comment").value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(c => {
        location.reload();
    })
}

function inputFormReceive() {
    if (confirm("Bạn chắc chắn nhập sách không?") === true) {
        fetch('/api/receive', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.status === 200) {
                alert("Nhập sách thành công!");
                console.log(data)
                location.reload();
                //let tr = document.querySelector("tbody.warehouse").classList.add('none');
            }
        })
    }
}

function addToReceiveNote(id, book_id, name, author, type ,quantity) {
    fetch("/receive", {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "book_id": book_id,
            "name": name,
            "author": author,
            "type": type,
            "quantity": quantity
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            console.log(`${data['receive'].id}`);
            let tbo = document.querySelector(`.input-${data['receive'].id}`);
            console.log(tbo);
            tbo.children[0].textContent = data['receive'].id;
            tbo.children[1].name = data['receive'].book_id;
            tbo.children[2].textContent = data['receive'].type;
            tbo.children[3].textContent = data['receive'].author;
            tbo.children[4].children[0].value = data['receive'].quantity;
        })
}

let row_id_warehouse = 0;

function renderRowInputWareHouse() {
    row_id_warehouse++;
    let tbody = document.querySelector("tbody");
    let newTr = document.createElement("tr");
    newTr.classList.add(`input-${row_id_warehouse}`);
    newTr.id = `${row_id_warehouse}`;
    newTr.innerHTML = `
        <td class="text-center">${row_id_warehouse}</td>
        <td>
                <input class="form-control search-input" list="suggestions" oninput="searchInputReceiveNote()" name="${row_id_warehouse}" placeholder="Nhập từ khóa..." />
        </td>
        <td></td>
        <td></td>
        <td><input type="number" oninput="searchInputReceiveNote()" value="1" class="form-control"></td>
    `;
    // Thêm dòng mới vào tbody
    tbody.appendChild(newTr);
    // Tăng giá trị row_id_warehouse sau mỗi lần gọi
}

function searchInputReceiveNote() {
    let input = event.target;
    //console.log(input)
    let tr_parent =input.closest('[id]');
    console.log(tr_parent.children[1].children[0].name);
    if (input.name === tr_parent.id) {
        let selectedOption = Array.from(document.querySelectorAll("#suggestions option")).find(option => option.value === input.value);
        if (selectedOption) {
            let book_id = selectedOption.getAttribute("data-id");
            let name = selectedOption.value;
            let author = selectedOption.getAttribute("data-author");
            let type = selectedOption.getAttribute("data-type");
            let quantity = parseInt(tr_parent.children[4].children[0].value);
            //console.log(typeof(quantity));
            // Gọi hàm addToReceiveNote với các tham số đã chọn
            addToReceiveNote(tr_parent.id, book_id, name, author, type, quantity);

        }
    }
    else {
        console.log(input);
        let book_id = tr_parent.children[1].name;
        let name = tr_parent.children[1].value;
        let author = tr_parent.children[3].textContent;
        let type = tr_parent.children[2].textContent;
        let quantity = parseInt(tr_parent.children[4].children[0].value);
        addToReceiveNote(tr_parent.id, book_id, name, author, type, quantity);
    }
}

function deleteReceives() {
    if (confirm("Bạn chắc chắn xóa không?") === true) {
        fetch('/api/receive', {
            method: "delete"
        }).then(res => res.json()).then(data => {
            alert("Xóa thành công!");
            location.reload();
        })
    }
}

//SELLER
let row_id_seller = 0;

function renderRowInputSeller() {
    row_id_seller++;
    let tbody = document.querySelector("tbody");
    let newTr = document.createElement("tr");
    newTr.classList.add(`input-${row_id_seller}`);
    newTr.id = `${row_id_seller}`;
    newTr.innerHTML = `
        <td class="text-center">${row_id_seller}</td>
        <td>
                <input class="form-control search-input" list="suggestions" oninput="searchInputSell()" name="${row_id_seller}" placeholder="Nhập từ khóa..." />
        </td>
        <td></td>
        <td><input type="number" oninput="searchInputSell()" value="1" class="form-control"></td>
        <td></td>
    `;

    tbody.appendChild(newTr);

}

function searchInputSell() {
    let input = event.target;
    //console.log(input)
    let tr_parent =input.closest('[id]');
    console.log(tr_parent.children[1].children[0].name);
    if (input.name === tr_parent.id) {
        let selectedOption = Array.from(document.querySelectorAll("#suggestions option")).find(option => option.value === input.value);
        if (selectedOption) {
            let book_id = selectedOption.getAttribute("data-id");
            let name = selectedOption.value;
            let price = selectedOption.getAttribute("data-price");
            let type = selectedOption.getAttribute("data-type");
            let quantity = parseInt(tr_parent.children[3].children[0].value);
            //console.log(typeof(quantity));
            // Gọi hàm addToReceiveNote với các tham số đã chọn
            addToReceipt(tr_parent.id, book_id, name, price, type, quantity);
        }
    }
    else {
        console.log(input);
        let book_id = tr_parent.children[1].name;
        let name = tr_parent.children[1].value;
        let price = tr_parent.children[4].textContent.replace(" VND", "").replace(/,/g, "");
        let type = tr_parent.children[2].textContent;
        let quantity = parseInt(tr_parent.children[3].children[0].value);
        addToReceipt(tr_parent.id, book_id, name, price, type, quantity);
    }
}

function addToReceipt(id, book_id, name, price, type, quantity) {
    fetch("/receipt_sell", {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "book_id": book_id,
            "name": name,
            "price": price,
            "type": type,
            "quantity": quantity
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
            console.log(data);
            console.log(`${data['receipt'].id}`);
            let tbo = document.querySelector(`.input-${data['receipt'].id}`);
            console.log(tbo);
            tbo.children[0].textContent = data['receipt'].id;
            tbo.children[1].name = data['receipt'].book_id;
            tbo.children[2].textContent = data['receipt'].type;
            tbo.children[3].children[0].value = data['receipt'].quantity;
            tbo.children[4].textContent = Number(data['receipt'].price).toLocaleString() + " VND";

            let total = document.querySelector(".total_amount");
            total.textContent = Number(data['receipt_stats'].total_amount).toLocaleString() + " VND";
        })
}

function inputFormReceipt() {
    if (confirm("Bạn chắc chắn thanh toán không?") === true) {
        fetch('/api/receipt_sell', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.status === 200) {
                alert("Thanh toán thành công!");
                console.log(data)
                location.reload();
                //let tr = document.querySelector("tbody.warehouse").classList.add('none');
            }
        })
    }
}

function deleteReceipts() {
    if (confirm("Bạn chắc chắn xóa không?") === true) {
        fetch('/api/receipt_sell', {
            method: "delete"
        }).then(res => res.json()).then(data => {
            alert("Xóa thành công!");
            location.reload();
        })
    }
}

function renderTableOrderDetail() {
    let input = event.target;
    console.log(parseInt(input.value));
    if (parseInt(input.value)){
    console.log("in");
        fetch('/receipt_order', {
            method: 'POST',
            body: JSON.stringify({
                'order_id': input.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
                let tbody = document.querySelector("tbody.order");
                //console.log(tbody);
                if (tbody.hasChildNodes()){
                    tbody.innerHTML ='';
                }
                console.log(data['receipts']);
                console.log(data['receipts'][1]['customer_id']);
                for (let r_id in data['receipts']){
                    //console.log(r_id);
                    let receipt = data['receipts'][r_id];
                    //console.log(receipt['name']);
                    let newTr = document.createElement("tr");
                    newTr.classList.add(`input-${r_id}`);
                    newTr.id = `${r_id}`;
                    newTr.innerHTML = `
                        <td class="text-center">${r_id}</td>
                        <td>${receipt['name']}</td>
                        <td>${receipt['type']}</td>
                        <td>${receipt['quantity']}</td>
                        <td>${receipt['price']}</td>
                    `;

                    tbody.appendChild(newTr);
                }
                let total = document.querySelector(".total_amount_order");
                //console.log(total);
                total.textContent = Number(data['receipt_stats'].total_amount).toLocaleString() + " VND";
            })
        }
}

function inputFormReceiptOrder() {
    if (confirm("Bạn chắc chắn thanh toán không?") === true) {
        fetch('/api/receipt_order', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.status === 200) {
                alert("Thanh toán thành công!");
                console.log(data)
                location.reload();
                //let tr = document.querySelector("tbody.warehouse").classList.add('none');
            }
        })
    }
}

function addOrder(cart) {
    fetch("/order", {
        method: "post",
        body: JSON.stringify({
            "cart":cart
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.log(data)
        if (data.status === 200) {
                alert("Đặt hàng thành công!");
                window.location.reload();
            }
    })
}

function pay(cart) {
    if (confirm("Bạn chắc chắn thanh toán không?") === true) {
        fetch('/api/pay', {
            method: 'post',
            body: {
                "cart": cart
            }
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.status === 200) {
                alert("Thanh toán thành công!");
                window.location.reload();
            }
        });
    }
}

function selectPay(cart) {
    const radios = document.querySelector('input[name="paymentMethod"]:checked')

    if(radios.value === "bankTransfer") {
        pay(cart);

    } else if(radios.value === "cash") {
        addOrder(cart);
    }
  }
