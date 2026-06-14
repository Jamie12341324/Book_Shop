function isNum(p){
    if (p.value=="0"){
        return;
    }
    if(p.value.trim() == "" ){
        alert("You cannot enter blank - the field has been reset to zero");
        p.value="0";
        p.focus();
        return;
    }
    if(p.value.trim().includes("-") ){
        alert("Numbers cannot be negative or contain dashes");
        p.value="0";
        p.focus();
        return;
    }
    if(String(p.value).includes(".")){
        alert("The number cannot contain decimals");
        p.value="0";
        p.focus();
        return;
    }
    if(String(p.value).length>9){
        alert("The number is far too big - it should be a thousand or less");
        p.value="0";
        p.focus();
        return;
    }
    if (isNaN(p.value)){
        alert("The number is invalid");
        p.value="0";
        p.focus();
    }

    num = parseInt(p.value);
    
    if(num > 1000 || num < 0 ){
        alert("The number cannot be greater than 1000 or negative");
        p.value="0";
        p.focus();
        return false;
    }

}
function is_isbnNum(p){

    if (p.value=="0"){
        return;
    }
    if(p.value.trim() == "" ){
        alert("You cannot enter blank - the field has been reset to zero");
        p.value="0";
        p.focus();
        return;
    }
    if(p.value.trim().includes("-") ){
        alert("Numbers cannot be negative or contain dashes");
        p.value="0";
        p.focus();
        return;
    }
    if(String(p.value).includes(".")){
        alert("The number cannot contain decimals");
        p.value="0";
        p.focus();
        return;
    }
    if(String(p.value).length>13){
        alert("The number is far too big - it should be a thousand or less");
        p.value="0";
        p.focus();
        return;
    }
    if (isNaN(p.value)){
        alert("The number is invalid");
        p.value="0";
        p.focus();
    }

}
document.addEventListener("DOMContentLoaded", function(){
    
    let button1=document.getElementById("create");
    if (button1){
        button1.addEventListener("click", function(event){
           
            let p=document.getElementById("price");
            alert("validate "+ p.id);
            if ( !isNum(p) ) {
                p.focus();
                event.preventDefault();
                return false;
            }
            let p2=document.getElementById("isbn");
            if ( !is_isbnNum(p2) ) return false;
        });
    }
    return false;
});