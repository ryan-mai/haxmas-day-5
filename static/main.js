const form = document.getElementById("giftForm");
const giftContainer = document.getElementById("gifts");

async function loadGifts() {
    const res = await fetch("/gifts");
    const gifts = await res.json();

    giftContainer.innerHTML = '';
    gifts.forEach(gift => {
        const item = document.createElement("p");
        item.textContent = `Gift for ${gift.name}: ${gift.gift}`;
        giftContainer.appendChild(item);
    });
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = form.elements.name.value;
    const gift = form.elements.gift.value;

    await fetch("/gifts", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, gift })
    });

    form.reset();
    await loadGifts();
});

loadGifts();