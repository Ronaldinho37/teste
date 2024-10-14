setInterval(()=>{
    console.log('oi')
    fetch('json')
    .then(res=>res.text())
    .then(res=>{
        let myDict = JSON.parse(res);
        let user = myDict.substring(10, 15);

        if(user == "ADMIN" || user == "admin"){
            window.location.href = "/"
        }
    })
},1000)

