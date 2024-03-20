const pageUrl = (new URL(window.location))['href']
	const params = pageUrl.split('?')[1]
	let queryString = new URLSearchParams(params);
	let credentials = []
	for(let q of queryString.entries()) credentials.push(q[1]);
	function GetUserInfo(){
          fetch(`/GetUserInfo/${credentials[1]}/${credentials[2]}`)
          .then(res => res.json())
          .then(res => {
              document.getElementById('role_tag').innerText = `Role: ${res['role']}`
              document.getElementById('username_tag').innerText = `Username: ${res['username']}`
              document.getElementById('password_tag').innerText = `Password: ${res['password']}`
          })
          .catch(err => console.log(err))
      }

      GetUserInfo()

      


      // JavaScript code to create and customize your chart
      const voltageData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
          label: 'Voltage Usage',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          data: [65, 59, 80, 81, 56, 55, 40] // Sample voltage values
        }]
      };

      // Configuration options
      const chartOptions = {
        scales: {
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Voltage (V)'
            }
          }],
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Month'
            }
          }]
        }
      };

      // Get the canvas element
      const ctx = document.getElementById('voltageChart').getContext('2d');

      // Create the voltage usage chart
      const voltageChart = new Chart(ctx, {
        type: 'line',
        data: voltageData,
        options: chartOptions
      });

document.getElementById("voltageChart-container").style = "width: 80%; margin: auto;"