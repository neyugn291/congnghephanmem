
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

// function addToReceiveNote(id,name,author,category_id) {
//     fetch("/api/receive", {
//         method: "POST",
//         body: JSON.stringify({
//             "id": id,
//             "name": name,
//             "author": author,
//             "type": category_id,
//         }),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     }).then(res => res.json()).then(data => {
//         let input = document.getElementById("input-warehouse");
//         input.children[2].textContent = data.author;
//         input.children[3].textContent = data.type;
//         let inputName = document.getElementById('dropdownMenuButton');
//         inputName.value = data.name;
//         console.log(data);
//     });
// }
function addToReceiveNote(id, book_id, name, author, type) {
    fetch("/api/receive", {
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
            data.id -= 1;
            let tbo = document.querySelector(`.input-${data.id}`);
            console.log(data.id -1)
            tbo.children[0].textContent = data.id;
            tbo.children[2].textContent = data.type;
            tbo.children[3].textContent = data.author;
            tbo.children[4].value = parseInt(data.quantity, 10);
            console.log(tbo);

        })
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
//        let html =  `
//            <li class="list-group-item">
//
//              <div class="row">
//                  <div class="col-md-1 col-6">
//                      <img src="${ c.user.avatar }" class="img-fluid rounded-circle" />
//                  </div>
//                  <div class="col-md-1"></div>
//                  <div class="col-md-10 col-6">
//                      <p>${ c.user.name }</p>
//                      <p>${ c.content }</p>
//                      <p class="date">${ c.created_date }</p>
//                  </div>
//              </div>
//
//          </li>
//        `;
//        let h = document.getElementById("comments");
//        h.innerHTML = html + h.innerHTML;
        location.reload();
    })
}




let row_id = 1;


function renderRowInput() {
    let tbody = document.querySelector("tbody");
    let newTr = document.createElement("tr");
    newTr.classList.add(`input-${row_id}`);  // Thêm class cho mỗi dòng mới
    newTr.innerHTML = `
        <td class="text-center">${row_id}</td>
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
            addToReceiveNote(row_id, book_id, name, author, type);
        }
    });

    // Thêm dòng mới vào tbody
    tbody.appendChild(newTr);

    // Tăng giá trị row_id sau mỗi lần gọi
    row_id++;
}
