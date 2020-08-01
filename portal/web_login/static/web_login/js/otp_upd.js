var hotp_img;
window.onload = function(){
    hotp_img = document.getElementById("hotp_img");
    var t = new Date();
    setInterval(()=>{
        hotp_img.src = "/qr?nocache=" + t.getTime();
    },5000);
};
