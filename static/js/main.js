document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-header nav');
    var header = document.querySelector('.site-header');
    var progress = document.querySelector('.scroll-progress');

    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            nav.classList.toggle('open');
            toggle.classList.toggle('active');
        });
    }

    function updateProgress() {
        var scrollTop = window.scrollY || document.documentElement.scrollTop;
        var height = document.documentElement.scrollHeight - window.innerHeight;
        var percent = height > 0 ? (scrollTop / height) * 100 : 0;

        if (progress) {
            progress.style.width = percent + '%';
        }

        if (header) {
            header.classList.toggle('scrolled', scrollTop > 18);
        }
    }

    updateProgress();
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);

    document.querySelectorAll('.message').forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.4s';
            msg.style.opacity = '0';
            setTimeout(function () { msg.remove(); }, 400);
        }, 6000);
    });

    var revealTargets = document.querySelectorAll('.hero, .section, .info-card, .doctor-card, .testimonial-card, .cta-section, .choice-card, .auth-card');
    revealTargets.forEach(function (el) {
        el.classList.add('reveal-on-scroll');
    });

    var revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    document.querySelectorAll('.reveal-on-scroll').forEach(function (el) {
        revealObserver.observe(el);
    });

    var hero = document.querySelector('.hero');
    if (hero) {
        hero.addEventListener('mousemove', function (event) {
            var rect = hero.getBoundingClientRect();
            var x = ((event.clientX - rect.left) / rect.width - 0.5) * 10;
            var y = ((event.clientY - rect.top) / rect.height - 0.5) * 10;
            hero.style.setProperty('--hero-x', x + 'px');
            hero.style.setProperty('--hero-y', y + 'px');
            hero.style.transform = 'perspective(1000px) rotateY(' + (x / 2) + 'deg) rotateX(' + (-y / 2) + 'deg)';
        });

        hero.addEventListener('mouseleave', function () {
            hero.style.transform = '';
            hero.style.setProperty('--hero-x', '0px');
            hero.style.setProperty('--hero-y', '0px');
        });
    }
});
