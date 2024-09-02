const counter = document.querySelector(".counter-number");
async function updateCounter() {
    let response = await fetch("https://ngdh3uhkxlzhjmltldkecgrgjm0ndahn.lambda-url.us-west-1.on.aws/");
    let data = await response.json();
    counter.innerHTML = ` Views: ${data}`;
}

updateCounter();