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

        function addToMyArray2() {
        var selectElement2 = document.getElementById("mySelect2");

        var selectedValue2 = selectElement2.options[selectElement2.selectedIndex].value;

        // Kiểm tra xem phần tử đã được chọn có trong mảng chưa
        if (myArray.indexOf(selectedValue2) === -1) {
            // Nếu chưa có, thêm vào mảng
            myArray.push(selectedValue2);
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
            var newElement = document.createElement("input");
            newElement.style.borderColor = 'black'
            newElement.style.borderStyle = 'solid'
            newElement.textContent = myArray[i];
            newElement.name = 'rooms_ordered'
            newElement.value = myArray[i]
            newElement.readOnly = true
            newElement.style.textAlign = 'center'
            myDiv.appendChild(newElement);
        }
    }