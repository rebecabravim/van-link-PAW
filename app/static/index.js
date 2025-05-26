document.querySelectorAll('.agendar-button').forEach(button => {
    button.addEventListener('click', function () {
        const card = this.closest('.viagem-card');
        const viagemData = {
            origem: card.dataset.origem,
            destino: card.dataset.destino,
            data: card.dataset.data,
            preco: card.dataset.preco,
            ida: card.dataset.ida,
            volta: card.dataset.volta
        };

        const self = this;
        self.innerHTML = "⏳ Agendando...";
        self.disabled = true;
        self.style.opacity = "0.7";

        fetch('/agendar', {
            method: 'POST',
            body: JSON.stringify(viagemData),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                self.innerHTML = "✔ Agendado";
                self.style.backgroundColor = "#28a745";
                self.style.color = "white";
                self.style.opacity = "1";
                self.style.cursor = "default";
                self.disabled = true;
            } else {
                self.innerHTML = "⚠️ Erro";
                self.style.backgroundColor = "#dc3545";
                self.style.color = "white";
                self.disabled = false;
                self.style.opacity = "1";
            }
        })
        .catch(() => {
            self.innerHTML = "⚠️ Erro";
            self.style.backgroundColor = "#dc3545";
            self.style.color = "white";
            self.disabled = false;
            self.style.opacity = "1";
        });
    });
});
