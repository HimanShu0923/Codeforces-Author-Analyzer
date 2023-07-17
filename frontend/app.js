const url = "https://iamh2yk9k4.execute-api.us-east-1.amazonaws.com/requesthandler";

async function getData(author_name) {

    var obj = {
        "author": author_name
    }
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(obj),
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (response) {
        var loader = document.getElementById("invalidWarning");
        loader.style.display = "none";
    }

    var data = await response.json();

    console.log(data);

    if (response.status === 404) {
        document.getElementById("empty").innerHTML = "<strong>Sorry No Data Found !!</strong>";
        console.log("Kuch na mila");
    }
    else {
        show(data);
    }
}

let submit_Form = document.getElementById("SubmitForm");

submit_Form.addEventListener("submit", (e) => {
    e.preventDefault();
    document.getElementById("empty").innerHTML = " ";
    let tab = ``;
    document.getElementById("accordionPanelsStayOpenExample").innerHTML = tab;
    let author_name = document.getElementById("userIdInput").value;
    console.log(author_name);

    var loader = document.getElementById("invalidWarning");
    loader.style.display = "inline";

    getData(author_name);
});

function show(data) {
    console.log("mil gya");
    messageObj = data.message;
    let tab = `<div class="accordion-item accordionbtn">`;

    Object.keys(messageObj).forEach(key => {

        tab += ` <h2 class="accordion-header">
        <button class="accordion-button accordpart1" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
            <strong>${key.toUpperCase()}</strong>
        </button>
      </h2>`;

        console.log(`Key: ${key}`);

        messageObj[key].forEach(obj => {

            tab += ` <div id="panelsStayOpen-collapseOne" class="accordion-collapse collapse show">
            <div class="accordion-body accordpart2">
                <ul>
                    <li>
                        <p>
                            <strong>Problem URL :</strong> ${obj.problem_url}
                        </p>    
                        <p>
                            <strong>Problem Name :</strong> ${obj.name.toUpperCase()}
                        </p> 
                    </li>
                </ul>
            </div>
          </div>
        </div>`;
            console.log(`Problem URL: ${obj.problem_url}`);
            console.log(`Name: ${obj.name}`);
        });

        document.getElementById("accordionPanelsStayOpenExample").innerHTML = tab;
    });
}

var btn = document.getElementById("myBtn");
btn.onclick = function () {
    var mdl = document.getElementById("myModal");
    mdl.style.display = "block";
    console.log("Hello btn");
};

var ban = document.getElementById("ban");
ban.onclick = function () {
    var mdl = document.getElementById("myModal");
    mdl.style.display = "none";
    console.log("Hello ban");
}

