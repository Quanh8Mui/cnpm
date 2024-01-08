var myArray = []; // Mảng để lưu trữ các phần tử đã chọn

    function addToMyArray() {
        var selectElement = document.getElementById("mySelect");
        var selectedValue = selectElement.options[selectElement.selectedIndex].value;

        // Kiểm tra xem phần tử đã được chọn có trong mảng chưa
        if (myArray.indexOf(selectedValue) === -1) {
            // Nếu chưa có, thêm vào mảng
            myArray.push(selectedValue);

            // Cập nhật nội dung hiển thị trên trang
            updateDisplay();
        }
    }

    function updateDisplay() {
        var myDiv = document.getElementById("myDiv");

        // Xóa nội dung hiện tại của div
        myDiv.innerHTML = "";

        // Hiển thị các phần tử trong mảng
        for (var i = 0; i < myArray.length; i++) {
            var newElement = document.createElement("span");
            newElement.style.borderColor = 'black'
            newElement.style.borderStyle = 'solid'
            newElement.style.paddingLeft = '7px'
            newElement.style.paddingRight = '7px'
            newElement.textContent = myArray[i];
            newElement.style.margin = '30px'
            newElement.className = 'rooms_ordered'
            myDiv.appendChild(newElement);
        }
    }