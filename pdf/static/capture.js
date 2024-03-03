var c;
function generatecapture(){
    var a=Math.floor((Math.random()*10));
    var b=Math.floor((Math.random()*10));
    var c=Math.floor((Math.random()*10));
    var d=Math.floor((Math.random()*10));
    var e=Math.floor((Math.random()*10));
    var f=Math.floor((Math.random()*10));
    c=a.toString()+b.toString()+c.toString()+d.toString()+e.toString()+f.toString();
    document.getElementById("captcha").value=c;
}