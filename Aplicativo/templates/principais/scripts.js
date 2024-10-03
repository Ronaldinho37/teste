window.onscroll = function() {
    scrollFunction();
  };
  
  function scrollFunction() {
    const header = document.getElementById("main-header");
  
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
      header.classList.add("small-header");
    } else {
      header.classList.remove("small-header");
    }
  }
  