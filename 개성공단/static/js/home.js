document.addEventListener('DOMContentLoaded', function () {
    // Get all elements with class 'timeline-content'
    var timelineContents = document.querySelectorAll('.timeline-component.timeline-content');

    // Add a click event listener to each timeline content
    timelineContents.forEach(function (content, index) {
        content.addEventListener('click', function () {
            // Toggle the 'expanded' class on click
            content.classList.toggle('expanded');
        });
    });
});
// Add these functions to your existing script
function toggleSideNav() {
    var sideNav = document.getElementById("mySidenav");
    if (sideNav.style.width === "400px") {
        closeSideNav();
    } else {
        openSideNav();
    }
}

function openSideNav() {
    document.getElementById("mySidenav").style.width = "400px";
}

function closeSideNav() {
    document.getElementById("mySidenav").style.width = "0";
}

// Redirect to the profile page
function redirectToProfilePage() {
    window.location.href = '/profile';
}

// Add this script to your existing script
document.addEventListener('DOMContentLoaded', function () {
    // Get all elements with class 'timeline-content'
    var timelineContents = document.querySelectorAll('.timeline-component.timeline-content');

    // Add a click event listener to each timeline content
    timelineContents.forEach(function (content, index) {
        content.addEventListener('click', function () {
            // Get the current timestamp in 24-hour format
            var timestamp = new Date().toLocaleString('en-US', { hour12: false });

            // Display the timestamp in an alert (you can customize this part)
            alert('Message received at: ' + timestamp);
        });
    });
});
        // 임의의 데이터 생성 함수
function generateRandomData() {
    var data = [];
    for (var i = 0; i < 7; i++) {
        data.push(Math.floor(Math.random() * 10) + 1);
    }
    return data;
}

// 날짜 레이블 생성 함수
function generateDateLabels() {
    var dateLabels = [];
    var today = new Date();
    for (var i = 6; i >= 0; i--) {
        var day = new Date(today);
        day.setDate(today.getDate() - i);
        var formattedDate = day.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
        dateLabels.push(formattedDate);
    }
    return dateLabels;
}

// 데이터 생성
var dataset1 = generateRandomData();
var dataset2 = generateRandomData();

// 차트 생성
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: generateDateLabels(), // 날짜 레이블 추가
        datasets: [
            {
                label: 'Whimmping',
                backgroundColor: '#FF5712',
                data: dataset1
            },
            {
                label: 'Barking',
                backgroundColor: 'rgba(255, 87, 18, 0.5)',
                data: dataset2
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 10,
                ticks: {
                    stepSize: 5
                }
            }
        },
        plugins: {
            legend: {
                position: 'top'
            }
        }
    }
});