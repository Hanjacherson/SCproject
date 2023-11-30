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




