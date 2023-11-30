async function fetchAndRenderBarChart() {
    try {
        // Fetch data from the API endpoint
        const response = await fetch('/api/bar_chart');
        const data = await response.json();

        // Extract labels and data from the response
        const labels = data.labels;
        const chartData = data.data;

        // Get the canvas element and create a 2d context
        const ctx = document.getElementById('myBarChart').getContext('2d');

        // Create a bar chart
        const myBarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '소리 이상 횟수',
                    data: chartData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        stepSize: 1, // 간격
                        min: 0,     // 최소값
                        max: 10     // 최대값
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching and rendering bar chart:', error);
    }
}

// Call the function to fetch and render the bar chart when the page loads
document.addEventListener('DOMContentLoaded', fetchAndRenderBarChart);






