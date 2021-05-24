// When the document loads...
let holder = document.querySelector("#container");
store_product = holder.dataset.product;
store_page = holder.dataset.page;
total_pages = holder.dataset.pages;
max_pages = 5; // + 2 cuz first +  last

function add_page_anchor(num, active=false) {
    element = document.createElement('a');
    element.innerHTML = num.toString();
    if(active) {
        element.className = "active";
    }
    document.querySelector("#pagination .dynamic").appendChild(element);
}

function load_page_content(product, page) {
	$.post("/store/" + product + "/" + page.toString(), function(data) {
		window.history.pushState("", "", "/store/" + product + "/" + page.toString());
        document.title = "Medusa | " + product.charAt(0).toUpperCase() + product.slice(1);
        document.querySelector("#items-container").innerHTML = data;
	});
    pagination = document.querySelector("#pagination .dynamic");
    pagination.innerHTML = '';
    index = page - 2;
    count = 0;
    store_page = page;
    add_page_anchor('1', 1 == page);
    if(total_pages > 1) {
        while (count < max_pages && index < total_pages) {
            if(index > 1) {
                count++;
                add_page_anchor(index, page==index);
            }
            index++;
        }
        add_page_anchor(total_pages, total_pages == page)
    }
}

document.addEventListener("click", function(event) {
    if(event.target.matches("#pagination a")) {
        if(!isNaN(event.target.innerHTML)){
            load_page_content(store_product, event.target.innerHTML);
        }
        else {
            switch(event.target.innerHTML.charCodeAt(0)) {
                case 171:
                    if (store_page > 1) {
                        load_page_content(store_product, parseInt(store_page, 10) - 1);
                    }
                    break;
                case 187:
                    if (store_page < total_pages) {
                        load_page_content(store_product, parseInt(store_page, 10) + 1);
                    }
                    break;
                default:
                    break;
            }
        }
    }
});

load_page_content(store_product, store_page);