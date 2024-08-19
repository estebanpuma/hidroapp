document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('docsearch-input');
    const searchList = document.getElementById('docsearch-list');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length > 0) {
            fetch(`/report_search?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchList.innerHTML = '';
                    data.results.forEach((item, index) => {
                        const li = document.createElement('li');
                        li.setAttribute('id', `docsearch-item-${index}`);
                        li.className = "list-group-item d-flex justify-content-between align-items-start"
                        const a = document.createElement("a");
                        a.href = `/report_view/${item.id}`;
                        a.className = "text-decoration-none text-black ms-2 me-auto";
                        const divCode = document.createElement("div");
                        divCode.className = "fw-medium fs-6";
                        divCode.textContent = item.code;
                        const div1 = document.createElement("div");
                        div1.className = "fw-bold";
                        div1.textContent = item.activity;
                        const div2 = document.createElement("div");
                        div2.textContent =  item.responsible + " - " + item.request_date;
                        const i = document.createElement("i")
                        i.className = "bi bi-chevron-right"

                        a.appendChild(divCode)
                        a.appendChild(div1);
                        a.appendChild(div2);
                        
                        li.appendChild(a);
                        li.appendChild(i)
                        searchList.appendChild(li);
                    });
                });
        } else {
            searchList.innerHTML = '';
        }
    });
});