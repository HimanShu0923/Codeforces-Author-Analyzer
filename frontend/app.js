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
        var barGraph = document.getElementsByClassName('barGraph')[0];
        barGraph.innerHTML = "";
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
    if(author_name == ""){
        document.getElementById("empty").innerHTML = "";
        var barGraph = document.getElementsByClassName('barGraph')[0];
        barGraph.innerHTML = "";
        console.log("Kuch na mila");
        return;
    }
    var loader = document.getElementById("invalidWarning");
    loader.style.display = "inline";

    getData(author_name);
});

function show(data) {
    console.log("mil gya");
    var totalQuestions = new Set();
    messageObj = data.message;
    let tab = `<div class="accordion-item accordionbtn">`;

    Object.keys(messageObj).forEach((key, index) => {

        tab += ` <h2 class="accordion-header">
        <button class="accordion-button accordpart1 collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse${index}" aria-expanded="true" aria-controls="panelsStayOpen-collapse${index}">
            <strong>${key.toUpperCase()}</strong>
        </button>
      </h2>`;

        messageObj[key].forEach(obj => {

            tab += ` <div id="panelsStayOpen-collapse${index}" class="accordion-collapse collapse collapsed">
            <div class="accordion-body accordpart2">
                <ul>
                    <li>
                        <p>
                            <strong>Problem Name :</strong> <a href="${obj.problem_url}" target="_blank">${obj.name.toUpperCase()}</a>
                        </p>
                    </li>
                </ul>
            </div>
          </div>
        </div>`;
            totalQuestions.add(obj.problem_url)
        });

        document.getElementById("accordionPanelsStayOpenExample").innerHTML = tab;
    });

    var barElement = "";
    Object.keys(messageObj).forEach((key, index) => {

        questions = messageObj[key].length
        var temp = (questions / totalQuestions.size) * 100;
        barElement += `<div class="graph-legend">${key}</div>
        <span class="graph-barBack">
            <li class="graph-bar" data-value=${temp} style="width:${temp}%">
            </li>
        </span> `;
    });
    var barGraph = document.getElementsByClassName('barGraph')[0];
    barGraph.innerHTML = barElement;
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

