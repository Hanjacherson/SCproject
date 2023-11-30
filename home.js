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
document.addEventListener('DOMContentLoaded', async function () {
    await initialize();

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

//import { initialize } from './chart.js'; // 모듈 import

//initialize(); // 모듈 함수 호출
