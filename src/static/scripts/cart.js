saved_changes = true;
changed_elements = new Array();

function save_changes() {
    changed_elements.forEach(element => {
        new_size = $("#" + element.toString()).find(".item_size option:selected").html();
        new_color = $("#" + element.toString()).find(".item_color option:selected").html();
        new_quantity = $("#" + element.toString()).find(".cart_quantity_input").val();
        $.ajax({data: {id: element.slice(1), size: new_size, color:  new_color, quantity:  new_quantity}, type:'POST', url:'/alter-item-order'}).done(function(data) {
            if(data.status == "SUCCESS") {
                saved_changes = true;
            }
		});
    });
}

function change_total(row, new_value) {
    price = $('#' + row + ' .cart_price .item_price').html();
    oldprice = $('#' + row + ' .cart_total .cart_total_price').html();
    newprice = new_value * price;
    $('#' + row + ' .cart_total .cart_total_price').html(newprice);
    $("#final_price").html(parseInt($("#final_price").html(), 10) + newprice - oldprice);
}

window.addEventListener("beforeunload", function (e) {
    if (!saved_changes) {
        save_changes();
        location.reload();
    }
});

$(document).ready(function() {
    $(".item_row select").change(function() {
        saved_changes = false;
        itemid = $(this).closest(".item_row").attr("id");
        if(!changed_elements.includes(itemid)) {
            changed_elements.push(itemid);
        }
        console.log(changed_elements);
    });
    $(".item_row .cart_quantity_input").change(function() {
        saved_changes = false;
        itemid = $(this).closest(".item_row").attr("id");
        if($(this).val() < 1 || $(this).val() > 32) {
            $(this).val('1');
        }
        change_total(itemid, $(this).val());
        if(!changed_elements.includes(itemid)) {
            changed_elements.push(itemid);
        }
        console.log(changed_elements);  
    });
});

$(".btn").on("click", function() {
    save_changes();
});

$(".cart_quantity_indec").on("click", function() {
    curr_value = parseInt($(this).siblings(".cart_quantity_input").val(), 10);
    new_val = curr_value;
    switch($(this).html()) {
        case '+':
            if(curr_value + 1 <= 32) {
                new_val = parseInt(curr_value, 10) + 1;
            }
            break;
        case '-':
            if(curr_value -1 >= 1) {
                new_val = parseInt(curr_value, 10) - 1;
            }
            break;
    }
    $(this).siblings(".cart_quantity_input").val(new_val);
    itemid = $(this).closest(".item_row").attr("id");
    change_total(itemid, new_val);
    saved_changes = false;
    if(!changed_elements.includes(itemid)) {
        changed_elements.push(itemid);
    }
});

$(".cart_delete").on("click", function() {
    order_id = $(this).parent().attr('id');
    $.ajax({data: {id: order_id.slice(1)}, type:'POST', url:'/delete-item-order'}).done(function(data) {
        if(data.status == "SUCCESS") {
            $('#' + order_id).remove();
            location.reload();
        }
    });
});