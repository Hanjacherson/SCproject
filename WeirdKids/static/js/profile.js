function handleMyPageButtonClick() {
    var enteredPassword = prompt("비밀번호를 입력하세요:");

    if (enteredPassword) {
        fetch('/profile/check_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: enteredPassword }),
            credentials: 'include',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/profile';
            } else {
                alert('비밀번호가 일치하지 않습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('오류가 발생했습니다.');
        });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var existingPetUpdateButton = document.getElementById("existing-pet-update-button");
    var newPetRegisterButton = document.getElementById("new-pet-register-button");

    existingPetUpdateButton.addEventListener('click', function () {
        // 강아지 정보 수정 버튼을 눌렀을 때 실행할 코드 추가
        updatePetInfo();
    });

    newPetRegisterButton.addEventListener('click', function () {
        // 강아지 등록 버튼을 눌렀을 때 실행할 코드 추가
        registerNewPet();
    });

    // 기존의 다른 JavaScript 코드들...

    function updatePetInfo() {
        // AJAX를 사용하여 서버로 강아지 정보 업데이트 요청 보내기
        $.ajax({
            type: "POST",
            url: "/update_pet_info",
            data: {
                pet_name: $("#existing_pet_name").val(),
                pet_birth_year: $("#existing_pet_birth_year").val(),
                pet_birth_month: $("#existing_pet_birth_month").val(),
                pet_birth_day: $("#existing_pet_birth_day").val(),
                pet_submit_type: "강아지 정보 수정"
            },
            success: function (response) {
                alert("강아지 정보가 성공적으로 수정되었습니다.");
                // 추가로 할 작업을 작성하세요.
            },
            error: function (error) {
                alert("강아지 정보 수정 중 오류가 발생했습니다.");
                console.error(error);
            }
        });
    }

    function registerNewPet() {
        // AJAX를 사용하여 서버로 강아지 등록 요청 보내기
        $.ajax({
            type: "POST",
            url: "/update_pet_info",
            data: {
                pet_name: $("#new_pet_name").val(),
                pet_birth_year: $("#new_pet_birth_year").val(),
                pet_birth_month: $("#new_pet_birth_month").val(),
                pet_birth_day: $("#new_pet_birth_day").val(),
                pet_submit_type: "강아지 등록"
            },
            success: function (response) {
                alert("강아지가 성공적으로 등록되었습니다.");
                // 추가로 할 작업을 작성하세요.
            },
            error: function (error) {
                alert("강아지 등록 중 오류가 발생했습니다.");
                console.error(error);
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    var profileUpdateButton = document.getElementById("profile-update-button");
    var existingPetUpdateButton = document.getElementById("existing-pet-update-button");
    var newPetRegisterButton = document.getElementById("new-pet-register-button");

    profileUpdateButton.addEventListener('click', function () {
        // 프로필 정보 수정 버튼을 눌렀을 때 실행할 코드
        var profileForm = document.getElementById("profile-form");
        $.ajax({
            type: "POST",
            url: "/update_profile",
            data: $(profileForm).serialize(),
            success: function (response) {
                alert("수정 성공");  
                location.reload();  // 페이지 새로고침
            },
            error: function (error) {
                alert("수정 실패");
                console.error(error);
            }
        });
    });

    existingPetUpdateButton.addEventListener('click', function () {
        // 강아지 정보 수정 버튼을 눌렀을 때 실행할 코드
        var formData = $("#pet-form").serialize();
        $.ajax({
            type: "POST",
            url: "/update_pet_info",
            data: formData,
            success: function (data) {
                alert(data);  // 서버에서 반환한 메시지를 알림으로 표시
                location.reload();  // 페이지 새로고침
            },
            error: function (error) {
                alert("강아지 정보 수정 실패");
                console.error(error);
            }
        });
    });

    newPetRegisterButton.addEventListener('click', function () {
        // 강아지 등록 버튼을 눌렀을 때 실행할 코드
        var formData = $("#pet-form").serialize();
        $.ajax({
            type: "POST",
            url: "/update_pet_info",
            data: formData,
            success: function (data) {
                alert(data);  // 서버에서 반환한 메시지를 알림으로 표시
                location.reload();  // 페이지 새로고침
            },
            error: function (error) {
                alert("강아지 등록 실패");
                console.error(error);
            }
        });
    });
});
