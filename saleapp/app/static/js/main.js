
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
                window.location.href = "/cart";  // Chuyển hướng đến trang cart
                window.location.reload();
            }
        });
    }
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

function addToReceiveNote(id, book_id, name, author, type) {
    fetch("/receive", {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "book_id": book_id,
            "name": name,
            "author": author,
            "type": type,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            let tbo = document.querySelector(`.input-${data['receive'].id}`);
            //console.log(tbo)
            tbo.children[0].textContent = data['receive'].id;
            tbo.children[2].textContent = data['receive'].type;
            tbo.children[3].textContent = data['receive'].author;
            tbo.children[4].value = parseInt(data['receive'].quantity, 10);
        })
}

let row_id_warehouse = 0;

function renderRowInputWareHouse() {
    row_id_warehouse++;
    let tbody = document.querySelector("tbody");
    let newTr = document.createElement("tr");
    newTr.classList.add(`input-${row_id_warehouse}`);  // Thêm class cho mỗi dòng mới
    newTr.innerHTML = `
        <td class="text-center">${row_id_warehouse}</td>
        <td>
            <div class="container">
                <input class="form-control search-input" list="suggestions" placeholder="Nhập từ khóa..." />
            </div>
        </td>
        <td></td>
        <td></td>
        <td><input type="number" class="form-control"></td>
    `;

    // Lựa chọn trường tìm kiếm duy nhất với class "search-input"
    let searchInput = newTr.querySelector(".search-input");

    // Thêm sự kiện "input" vào trường tìm kiếm
    searchInput.addEventListener("input", function (event) {
        let input = event.target;
        let selectedOption = Array.from(document.querySelectorAll("#suggestions option")).find(option => option.value === input.value);

        if (selectedOption) {
            let book_id = selectedOption.getAttribute("data-id");
            let name = selectedOption.value;
            let author = selectedOption.getAttribute("data-author");
            let type = selectedOption.getAttribute("data-type");

            // Gọi hàm addToReceiveNote với các tham số đã chọn
            addToReceiveNote(row_id_warehouse, book_id, name, author, type);

        }
    });

    // Thêm dòng mới vào tbody
    tbody.appendChild(newTr);
    // Tăng giá trị row_id_warehouse sau mỗi lần gọi
}

//SELLER
let row_id_seller = 0;

function renderRowInputSeller() {
    row_id_seller++;
    let tbody = document.querySelector("tbody");
    let newTr = document.createElement("tr");
    newTr.classList.add(`input-${row_id_seller}`);  // Thêm class cho mỗi dòng mới
    newTr.innerHTML = `
        <td class="text-center">${row_id_seller}</td>
        <td>
            <div class="container">
                <input class="form-control search-input" list="suggestions" placeholder="Nhập từ khóa..." />
            </div>
        </td>
        <td></td>
        <td><input type="number" class="form-control"></td>
        <td></td>
    `;

    // Lựa chọn trường tìm kiếm duy nhất với class "search-input"
    let searchInput = newTr.querySelector(".search-input");

    // Thêm sự kiện "input" vào trường tìm kiếm
    searchInput.addEventListener("input", function (event) {
        let input = event.target;
        let selectedOption = Array.from(document.querySelectorAll("#suggestions option")).find(option => option.value === input.value);

        if (selectedOption) {
            let book_id = selectedOption.getAttribute("data-id");
            let name = selectedOption.value;
            let price = selectedOption.getAttribute("data-price");
            let type = selectedOption.getAttribute("data-type");

            // Gọi hàm addToReceiveNote với các tham số đã chọn
            addToReceipt(row_id_seller, book_id, name, price, type);

        }
    });
    // Thêm dòng mới vào tbody
    tbody.appendChild(newTr);
    // Tăng giá trị row_id_seller sau mỗi lần gọi
}

function addToReceipt(id, book_id, name, price, type) {
    fetch("/receipt_sell", {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "book_id": book_id,
            "name": name,
            "price": price,
            "type": type,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            let tbo = document.querySelector(`.input-${data['receipt'].id}`);
            //console.log(tbo)
            tbo.children[0].textContent = data['receipt'].id;
            tbo.children[2].textContent = data['receipt'].type;
            tbo.children[3].getAttribute('')
            tbo.children[3].value = parseInt(data['receipt'].quantity, 10);
            tbo.children[4].textContent = Number(data['receipt'].price).toLocaleString() + " VND";
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



function selectPay(cart) {
    const radios = document.querySelector('input[name="paymentMethod"]:checked')

    if(radios.value === "bankTransfer") {
        pay(cart);

    } else if(radios.value === "cash") {
        alert("cash");
    }
  }
