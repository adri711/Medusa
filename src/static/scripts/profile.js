/* This file is pretty much a copy of store.js but rewritten to fit the profile page. */ 
let holder = document.querySelector("#container");
total_pages = holder.dataset.pages;
curr_page = holder.dataset.page;
user_id = holder.dataset.user;
console.log(user_id);
max_pages = 5; // + 2 cuz first +  last

function add_page_anchor(num, active=false) {
    element = document.createElement('a');
    element.innerHTML = num.toString();
    if(active) {
        element.className = "active";
    }
    document.querySelector("#pagination .dynamic").appendChild(element);
}

function load_profile_page(page) {
	$.post("/user/" + user_id.toString() + '/' + page.toString(), function(data) {
		window.history.pushState("", "", "/user/" + user_id.toString() + '/' + page.toString());
        document.querySelector("#items-container").innerHTML = data;
	});
    pagination = document.querySelector("#pagination .dynamic");
    pagination.innerHTML = '';
    index = page - 2;
    count = 0;
    curr_page = page;
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
            load_profile_page(event.target.innerHTML);
        }
        else {
            switch(event.target.innerHTML.charCodeAt(0)) {
                case 171:
                    if (curr_page > 1) {
                        load_profile_page(parseInt(curr_page, 10) - 1);
                    }
                    break;
                case 187:
                    if (curr_page < total_pages) {
                        load_profile_page(parseInt(curr_page, 10) + 1);
                    }
                    break;
                default:
                    break;
            }
        }
    }
});

load_profile_page(curr_page);