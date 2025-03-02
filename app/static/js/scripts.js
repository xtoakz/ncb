document.addEventListener('DOMContentLoaded', function() {
    console.log('WebApp is ready.');

    const btn = document.getElementById('get-news-btn');
    const input = document.getElementById('topic-input');
    const newsContainer = document.getElementById('news-container');

    function displayNews(data) {
        newsContainer.innerHTML = "";

        // Ergebnisse anzeigen
        if (data.results && data.results.length > 0) {
            let resultsSection = document.createElement("div");
            resultsSection.innerHTML = "<h3>Ergebnisse</h3>";
            data.results.forEach(result => {
                let div = document.createElement("div");
                div.classList.add("result-item");
                let title = `<h4><a href="${result.url}" target="_blank">${result.title}</a></h4>`;
                let description = result.description ? `<p>${result.description}</p>` : "";
                let snippet = result.snippets ? `<p><strong>Snippet:</strong> ${result.snippets}</p>` : "";
                div.innerHTML = title + description + snippet;
                resultsSection.appendChild(div);
            });
            newsContainer.appendChild(resultsSection);
        }

        // QnA anzeigen
        if (data.qnas && data.qnas.length > 0) {
            let qnaSection = document.createElement("div");
            qnaSection.innerHTML = "<h3>Fragen & Antworten</h3>";
            data.qnas.forEach(qna => {
                let div = document.createElement("div");
                div.classList.add("qna-item");
                let question = `<p><strong>Frage:</strong> ${qna.question}</p>`;
                let answer = `<p><strong>Antwort:</strong> ${qna.answer}</p>`;
                div.innerHTML = question + answer;
                qnaSection.appendChild(div);
            });
            newsContainer.appendChild(qnaSection);
        }

        // Videos anzeigen
        if (data.videos && data.videos.length > 0) {
            let videoSection = document.createElement("div");
            videoSection.innerHTML = "<h3>Videos</h3>";
            data.videos.forEach(video => {
                let div = document.createElement("div");
                div.classList.add("video-item");
                // YouTube-URL in Embed-URL umwandeln, falls zutreffend
                let embedUrl = video.src.includes("youtube.com/watch?v=")
                    ? video.src.replace("watch?v=", "embed/")
                    : video.src;
                let iframe = `<iframe width="560" height="315" src="${embedUrl}" frameborder="0" allowfullscreen></iframe>`;
                div.innerHTML = iframe;
                videoSection.appendChild(div);
            });
            newsContainer.appendChild(videoSection);
        }

        // Verwandte Themen anzeigen
        if (data.related && data.related.length > 0) {
            let relatedSection = document.createElement("div");
            relatedSection.innerHTML = "<h3>Verwandte Themen</h3>";
            let list = "<ul>";
            data.related.forEach(item => {
                list += `<li>${item}</li>`;
            });
            list += "</ul>";
            relatedSection.innerHTML += list;
            newsContainer.appendChild(relatedSection);
        }
    }

    if (btn) {
        btn.addEventListener('click', function() {
            const topic = input.value.trim();
            if (!topic) {
                alert("Bitte geben Sie ein Thema ein.");
                return;
            }
            btn.disabled = true;
            newsContainer.textContent = "Lade Nachrichten...";
            
            fetch('/get_news', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic: topic })
            })
            .then(response => {
                btn.disabled = false;
                if (!response.ok) {
                    throw new Error('Fehler beim Abrufen der Nachrichten');
                }
                return response.json();
            })
            .then(data => {
                displayNews(data);
            })
            .catch(error => {
                newsContainer.textContent = error.message;
            });
        });
    }
});
