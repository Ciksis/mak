const login_atcerēties = document.getElementById('atcereties');
const login_atc_vērt = document.getElementById('atceretiesV');

login_atcerēties.onclick = function() {
	if (login_atc_vērt.value==1)
	{
		login_atc_vērt.value = 0;
	}
	else
	{
		login_atc_vērt.value = 1;
	}
}


const logs = document.getElementsByClassName('wrapper')[0];
const reg_saite = document.getElementById('reg_saite');
const login_saite = document.getElementById('login_saite');

reg_saite.onclick = function(){
	logs.classList.add('active');
}
login_saite.onclick = function(){
	logs.classList.remove('active');
}



const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('pastav');
if (myParam == 1){
	logs.classList.add('active');
	window.onload = function(){
		alert('Lietotājs ar šādu e-pastu eksistē.')
	}
	
}
