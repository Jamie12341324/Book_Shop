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

function isDecimal(input) {
    // Use the match() method with a regular expression
    // https://www.geeksforgeeks.org/javascript/how-to-validate-decimal-numbers-in-javascript/
    const isDecimal = input.match(/^-?\d*\.?\d+$/);
    // Return true if it's a valid decimal number, otherwise return false
    return isDecimal !== null;
}

document.addEventListener("DOMContentLoaded", function(){
    // alert("add listener");
    let button1=document.getElementById("save");
    if (button1){
        button1.addEventListener("click", function(event){
            //alert("validate form");
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
            let p4=document.getElementById("category");
            if (p4.value == "0"){
                alert("Please select a category");
                event.preventDefault();
                return false;
            }
            
            
        });
    }

    let isbn1=document.getElementById("isbn");
    if (isbn1){
        isbn1.addEventListener("change", function(event){
            
            document.getElementById('book_image').src='https://covers.openlibrary.org/b/isbn/'+document.getElementById('isbn').value+'-M.jpg';
            }
        )
    };

    //return false;
}

);

