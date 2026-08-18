document.addEventListener('DOMContentLoaded', () => {
    initDock();
    initMatchBars();
    initCreditSlider();
    initFlashDismiss();
    initCardAnimations();
});

function initDock() {
    const dock = document.querySelector('.dock');
    if (!dock) return;

    const items = dock.querySelectorAll('.dock-item');
    items.forEach((item) => {
        item.addEventListener('mouseenter', () => {
            items.forEach((i) => {
                if (i !== item && !i.classList.contains('active')) {
                    i.style.opacity = '0.65';
                }
            });
        });
        item.addEventListener('mouseleave', () => {
            items.forEach((i) => { i.style.opacity = ''; });
        });
    });
}

function initMatchBars() {
    document.querySelectorAll('.match-fill').forEach((bar) => {
        const target = bar.dataset.width || bar.style.width;
        bar.style.width = '0%';
        requestAnimationFrame(() => {
            setTimeout(() => {
                bar.style.width = target;
            }, 200);
        });
    });
}

function initCreditSlider() {
    const slider = document.getElementById('max_credits');
    const display = document.getElementById('credit-display');
    if (!slider || !display) return;

    const update = () => { display.textContent = slider.value; };
    slider.addEventListener('input', update);
    update();
}

function initFlashDismiss() {
    document.querySelectorAll('.flash').forEach((flash) => {
        setTimeout(() => flash.remove(), 4500);
    });
}

function initCardAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    document.querySelectorAll('.course-card, .stat-card, .feature-item').forEach((el) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    const style = document.createElement('style');
    style.textContent = '.visible { opacity: 1 !important; transform: translateY(0) !important; }';
    document.head.appendChild(style);
}

function filterCourses() {
    const faculty = document.getElementById('filter-faculty')?.value || '';
    const difficulty = document.getElementById('filter-difficulty')?.value || '';
    const params = new URLSearchParams();
    if (faculty && faculty !== 'all') params.set('faculty', faculty);
    if (difficulty) params.set('difficulty', difficulty);
    const qs = params.toString();
    window.location.href = '/courses' + (qs ? '?' + qs : '');
}
