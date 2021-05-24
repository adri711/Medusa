$(".add-to-cart").on("click", function(e) {
    e.preventDefault();
    parent_element = $(this).closest(".product_displayer");
    product_id = parent_element.data("productid");
    tcolor = $(parent_element).find(".color option:selected").val();
    tsize = $(parent_element).find(".size option:selected").val();
    $.ajax({data: {color: tcolor, size:tsize}, type:'POST', url:'/add-to-cart' + '/' +product_id.toString()}).done(function(data) {
        console.log(data);
        if(data.state) {
            console.log("added to cart.");
            $('.toast').toast('show');
            //window.location.href = "/cart";
        } else {
            console.log("Failed to add item to cart.");
        }
    });
});