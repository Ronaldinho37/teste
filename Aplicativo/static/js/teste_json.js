setInterval(()=>{
    let user = sessionStorage.getItem('user');
    if(user != "None"){
        window.location.href = "/"
    }
},1000)

