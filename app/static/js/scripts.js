document.addEventListener('DOMContentLoaded', function() {
    console.log('NewsletterChat is ready.');
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Offset for fixed navbar
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath || (currentPath === '/' && linkPath === '/')) {
            link.classList.add('active');
        }
    });
    
    // Animate elements on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.card, .feature-icon, h1, h2, .btn-lg');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (elementPosition < screenPosition) {
                element.classList.add('fade-in');
            }
        });
    };
    
    // Run once on load
    animateOnScroll();
    
    // Run on scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // News functionality
    const btn = document.getElementById('get-news-btn');
    const input = document.getElementById('topic-input');
    const newsContainer = document.getElementById('news-container');
    
    function displayNews(data) {
        if (!newsContainer) return;
        
        newsContainer.innerHTML = "";
        
        // Show loading spinner
        const loadingSpinner = document.createElement('div');
        loadingSpinner.className = 'text-center my-5';
        loadingSpinner.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">Processing your request...</p>
        `;
        newsContainer.appendChild(loadingSpinner);
        
        // Simulate loading time (remove in production)
        setTimeout(() => {
            newsContainer.innerHTML = "";
            
            // Create container for results
            const resultsContainer = document.createElement('div');
            resultsContainer.className = 'news-results';
            
            // Results section
            if (data.results && data.results.length > 0) {
                const resultsSection = document.createElement("div");
                resultsSection.className = 'mb-5';
                resultsSection.innerHTML = "<h3 class='mb-4'>Latest News</h3>";
                
                data.results.forEach(result => {
                    const card = document.createElement("div");
                    card.className = "card mb-4 shadow-sm fade-in";
                    
                    const cardBody = document.createElement("div");
                    cardBody.className = "card-body";
                    
                    const title = document.createElement("h4");
                    title.className = "card-title";
                    const titleLink = document.createElement("a");
                    titleLink.href = result.url || "#";
                    titleLink.target = "_blank";
                    titleLink.textContent = result.title || "Untitled";
                    titleLink.className = "text-decoration-none";
                    title.appendChild(titleLink);
                    
                    const description = document.createElement("p");
                    description.className = "card-text";
                    description.textContent = result.description || "";
                    
                    const snippet = document.createElement("p");
                    snippet.className = "card-text small text-muted";
                    snippet.innerHTML = result.snippets ? `<strong>Excerpt:</strong> ${result.snippets}` : "";
                    
                    const source = document.createElement("div");
                    source.className = "d-flex align-items-center mt-3";
                    source.innerHTML = `
                        <i data-lucide="globe" class="me-2 text-primary"></i>
                        <small class="text-muted">Source: ${new URL(result.url || "https://example.com").hostname}</small>
                    `;
                    
                    cardBody.appendChild(title);
                    cardBody.appendChild(description);
                    cardBody.appendChild(snippet);
                    cardBody.appendChild(source);
                    card.appendChild(cardBody);
                    
                    resultsSection.appendChild(card);
                });
                
                resultsContainer.appendChild(resultsSection);
            } else {
                const noResults = document.createElement("div");
                noResults.className = "alert alert-info";
                noResults.innerHTML = `
                    <i data-lucide="info" class="me-2"></i>
                    No news results found for this topic. Try a different search term.
                `;
                resultsContainer.appendChild(noResults);
            }
            
            // Q&A section
            if (data.qnas && data.qnas.length > 0) {
                const qnaSection = document.createElement("div");
                qnaSection.className = 'mb-5';
                qnaSection.innerHTML = "<h3 class='mb-4'>Questions & Answers</h3>";
                
                data.qnas.forEach(qna => {
                    const card = document.createElement("div");
                    card.className = "card mb-4 shadow-sm fade-in";
                    
                    const cardBody = document.createElement("div");
                    cardBody.className = "card-body";
                    
                    const question = document.createElement("h5");
                    question.className = "card-title d-flex align-items-center";
                    question.innerHTML = `<i data-lucide="help-circle" class="me-2 text-primary"></i> ${qna.question}`;
                    
                    const answer = document.createElement("p");
                    answer.className = "card-text";
                    answer.innerHTML = `<strong>Answer:</strong> ${qna.answer}`;
                    
                    cardBody.appendChild(question);
                    cardBody.appendChild(answer);
                    card.appendChild(cardBody);
                    
                    qnaSection.appendChild(card);
                });
                
                resultsContainer.appendChild(qnaSection);
            }
            
            // Videos section
            if (data.videos && data.videos.length > 0) {
                const videoSection = document.createElement("div");
                videoSection.className = 'mb-5';
                videoSection.innerHTML = "<h3 class='mb-4'>Related Videos</h3>";
                
                const videoRow = document.createElement("div");
                videoRow.className = "row g-4";
                
                data.videos.forEach(video => {
                    const col = document.createElement("div");
                    col.className = "col-md-6 col-lg-4 fade-in";
                    
                    const card = document.createElement("div");
                    card.className = "card h-100 shadow-sm";
                    
                    // YouTube-URL in Embed-URL umwandeln, falls zutreffend
                    let embedUrl = video.src.includes("youtube.com/watch?v=")
                        ? video.src.replace("watch?v=", "embed/")
                        : video.src;
                    
                    const iframe = document.createElement("div");
                    iframe.className = "ratio ratio-16x9";
                    iframe.innerHTML = `<iframe src="${embedUrl}" frameborder="0" allowfullscreen></iframe>`;
                    
                    const cardBody = document.createElement("div");
                    cardBody.className = "card-body";
                    cardBody.innerHTML = `
                        <h5 class="card-title">${video.title || "Video"}</h5>
                        <p class="card-text small text-muted">${video.description || ""}</p>
                    `;
                    
                    card.appendChild(iframe);
                    card.appendChild(cardBody);
                    col.appendChild(card);
                    videoRow.appendChild(col);
                });
                
                videoSection.appendChild(videoRow);
                resultsContainer.appendChild(videoSection);
            }
            
            // Related topics section
            if (data.related && data.related.length > 0) {
                const relatedSection = document.createElement("div");
                relatedSection.className = 'mb-5';
                relatedSection.innerHTML = "<h3 class='mb-4'>Related Topics</h3>";
                
                const topicsContainer = document.createElement("div");
                topicsContainer.className = "d-flex flex-wrap gap-2";
                
                data.related.forEach(item => {
                    const badge = document.createElement("a");
                    badge.href = "#";
                    badge.className = "badge bg-light text-primary text-decoration-none p-2 fade-in";
                    badge.innerHTML = `<i data-lucide="hash" class="me-1"></i> ${item}`;
                    badge.addEventListener('click', function(e) {
                        e.preventDefault();
                        if (input) {
                            input.value = item;
                            if (btn) btn.click();
                        }
                    });
                    
                    topicsContainer.appendChild(badge);
                });
                
                relatedSection.appendChild(topicsContainer);
                resultsContainer.appendChild(relatedSection);
            }
            
            newsContainer.appendChild(resultsContainer);
            
            // Initialize Lucide icons for dynamically added content
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }, 1000); // Simulated loading time
    }
    
    if (btn && input) {
        btn.addEventListener('click', function() {
            const topic = input.value.trim();
            if (!topic) {
                // Show error toast
                const toastContainer = document.createElement('div');
                toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
                toastContainer.innerHTML = `
                    <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="toast-header bg-danger text-white">
                            <i data-lucide="alert-circle" class="me-2"></i>
                            <strong class="me-auto">Error</strong>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                        <div class="toast-body">
                            Please enter a topic to search for news.
                        </div>
                    </div>
                `;
                document.body.appendChild(toastContainer);
                
                // Initialize Lucide icons for toast
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
                
                // Remove toast after 3 seconds
                setTimeout(() => {
                    toastContainer.remove();
                }, 3000);
                
                return;
            }
            
            btn.disabled = true;
            btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`;
            
            if (newsContainer) {
                newsContainer.innerHTML = `
                    <div class="text-center my-5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <p class="mt-3">Searching for news about "${topic}"...</p>
                    </div>
                `;
            }
            
            fetch('/get_news', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic: topic })
            })
            .then(response => {
                btn.disabled = false;
                btn.innerHTML = 'Get News';
                
                if (!response.ok) {
                    throw new Error('Error retrieving news');
                }
                return response.json();
            })
            .then(data => {
                displayNews(data);
            })
            .catch(error => {
                if (newsContainer) {
                    newsContainer.innerHTML = `
                        <div class="alert alert-danger" role="alert">
                            <i data-lucide="alert-triangle" class="me-2"></i>
                            ${error.message}
                        </div>
                    `;
                    
                    // Initialize Lucide icons for error message
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }
            });
        });
        
        // Allow pressing Enter in the input field to trigger the search
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                btn.click();
            }
        });
    }
    
    // Pricing toggle functionality (if exists)
    const pricingToggle = document.getElementById('pricing-toggle');
    const monthlyPrices = document.querySelectorAll('.monthly-price');
    const yearlyPrices = document.querySelectorAll('.yearly-price');
    
    if (pricingToggle) {
        pricingToggle.addEventListener('change', function() {
            if (this.checked) {
                monthlyPrices.forEach(el => el.classList.add('d-none'));
                yearlyPrices.forEach(el => el.classList.remove('d-none'));
            } else {
                monthlyPrices.forEach(el => el.classList.remove('d-none'));
                yearlyPrices.forEach(el => el.classList.add('d-none'));
            }
        });
    }
});