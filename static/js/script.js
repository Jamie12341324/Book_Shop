// tests to see if a input is a number
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
        alert("isbn number is too big - it should be 13 numbers or less");
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
//  tests to see if a number is a decimal
function isDecimal(input) {
    // Use the match() method with a regular expression
    // https://www.geeksforgeeks.org/javascript/how-to-validate-decimal-numbers-in-javascript/
    const isDecimal = input.match(/^\d+(\.\d+)?$/);
    // Return true if it's a valid decimal number, otherwise return false
    return isDecimal !== null;
}

document.addEventListener("DOMContentLoaded", function(){
    let button1=document.getElementById("save");
    if (button1){
        button1.addEventListener("click", function(event){
            let p=document.getElementById("price");
            // generate a message if the price is not a decimal and prevent the form from being submited
            if ( !isDecimal(p.value) ) {
                alert("Invalid decimal or negative number for price!");
                event.preventDefault();
                return false;
            }
            // generate a message if the isbn is not a number or a too large number and prevent the form from being submited
            let p2=document.getElementById("isbn");
            if ( !is_isbnNum(p2) ){
                event.preventDefault();
                return false;
            } 
            // generate a message if the rating is not a decimal and prevent the form from being submited
            let p3=document.getElementById("rating");
            if ( !isDecimal(p3.value) ){
                alert("invalid or negative rating");
                event.preventDefault();
                return false;
            } 
            // generate a message if the category has not been selected and prevent the form from being submited
            let p4=document.getElementById("category");
            if (p4.value == "0"){
                alert("Please select a category");
                event.preventDefault();
                return false;
            }
            
            
        });
    }
    // updates the soruce of the image tag when the isbn number changes
    let isbn1=document.getElementById("isbn");
    if (isbn1){
        isbn1.addEventListener("change", function(event){
            
            document.getElementById('book_image').src='https://covers.openlibrary.org/b/isbn/'+document.getElementById('isbn').value+'-M.jpg';
            }
        )
    };
}

);

