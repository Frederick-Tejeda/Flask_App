document.getElementById('form').addEventListener('submit', (e) => {
	e.preventDefault()
	document.getElementById("button-submit").disabled = true
	const username = document.getElementById('inputUsername').value
	const password = document.getElementById('inputPassword').value
	fetch(`/verify/${username}/${password}`)
	.then(res => res.json())
	.then(res => {
		if(res['isUser'] === true){
			window.location += `dashboard?role=${res['role']}&username=${res['username']}&password=${res['password']}`
		}else{
			document.getElementById("button-submit").disabled = false
			alert('Username or Password wrong...')
		}
	})
	.catch(err => {
		console.log('error')
		alert('Algo salió mal, intente de nuevo más tarde...')
	})
})