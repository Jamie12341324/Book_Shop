// checks if a isbn number is valid
function is_isbnNum(p){

    if (p.value=="0"){
        return false;
    }
    if(p.value.trim() == "" ){
        alert("You cannot enter blank  isbn - the field has been reset to zero");
        p.value="0";
        p.focus();
        return true;
    }
    if(p.value.trim().includes("-") ){
        alert("isbn Numbers cannot be negative or contain dashes");
        p.value="0";
        p.focus();
        return false;
    }
    if(String(p.value).includes(".")){
        alert("isbn number cannot contain decimals");
        p.value="0";
        p.focus();
        return false;
    }
    if(String(p.value).length>13){
        alert("isbn number is too big - it should be a thousand or less");
        p.value="0";
        p.focus();
        return false;
    }
    if (isNaN(p.value)){
        alert("isbn number is invalid");
        
        p.focus();
        return false;
    }
    return true;
}
// checks if a number is a decimal
function isDecimal(input) {
    const isDecimal = input.match(/^-?\d*\.?\d+$/);
    // Return true if it's a valid decimal number, otherwise return false
    return isDecimal !== null;
}
// adds an event listner which calls the isbn, price and rating valid checkers
document.addEventListener("DOMContentLoaded", function(){
    let button1=document.getElementById("save");
    if (button1){
        button1.addEventListener("click", function(event){
            let p=document.getElementById("price");
            if ( !isDecimal(p.value) ) {
                alert("Invalid decimal number for price!");
                event.preventDefault();
                return false;
            }
            let p2=document.getElementById("isbn");
            if ( !is_isbnNum(p2) ){
                event.preventDefault();
                return false;
            } 
           
            let p3=document.getElementById("rating");
            if ( !isDecimal(p3.value) ){
                alert("invalid rating");
                event.preventDefault();
                return false;
            } 
            
        });
    }
    // puts a image of a book with the isbn number on the add book form so you know if you got the number right 
    let isbn1=document.getElementById("isbn");
    if (isbn1){
        // event listener with change from stack overflow
        isbn1.addEventListener("change", function(event){
            
            document.getElementById('book_image').src='https://covers.openlibrary.org/b/isbn/'+document.getElementById('isbn').value+'-M.jpg';
            }
        )
    };

    //return false;
}

);

