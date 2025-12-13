gsap.registerPlugin(ScrollTrigger);



gsap.from(".about__title", {
    scrollTrigger: {
        trigger: ".about__inner",
        start: "top 80%",
        toggleActions: "play none none none"
    },
    opacity: 0,
    scale: 0.8,
    filter: "blur(10px)",
    duration: 1.5,
    ease: "power3.out"
});


gsap.from(".about__description", {
    scrollTrigger: {
        trigger: ".about__inner",
        start: "top 80%",
        toggleActions: "play none none none"
    },
    opacity: 0,
    y: 80,
    duration: 1.5,
    ease: "back.out(1.7)",
    delay: 0.3
});


gsap.from(".about__shadow", {
    scrollTrigger: {
        trigger: ".about__inner",
        start: "top 80%",
        toggleActions: "play none none none"
    },
    opacity: 0,
    y: 50,
    duration: 1.5,
    ease: "power2.out",
    delay: 0.1,
    scrub: true
});

// Заголовок блока НОМИНАЦИИ
gsap.from(".nomination__header-title", {
    scrollTrigger: {
        trigger: ".nomination__header",
        start: "top 80%",
        toggleActions: "play none none none"
    },
    opacity: 0,
    y: 50,
    duration: 1.5,
    ease: "power2.out"
});

gsap.from(".nomination__header-decoration", {
    scrollTrigger: {
        trigger: ".nomination__header",
        start: "top 80%",
        toggleActions: "play none none none"
    },
    opacity: 0,
    y: -30,
    duration: 1.5,
    ease: "power2.out",
    delay: 0.2
});

// Основные номинации (FLAY KING / QUEEN)
gsap.from(".nomination__major", {
    scrollTrigger: {
        trigger: ".nomination__major-wrapper",
        start: "top 85%",
        toggleActions: "play none none none"
    },
    opacity: 0,
    y: 100,
    duration: 1.5,
    ease: "back.out(1.7)",
    stagger: 0.2
});

// Минорные номинации (все остальные)
gsap.from(".nomination__minor-wrapper .nomination__item", {
    scrollTrigger: {
        trigger: ".nomination__minor-wrapper",
        start: "top 85%",
        toggleActions: "play none none none"
    },
    opacity: 0,
    y: 80,
    duration: 1.5,
    ease: "power2.out",
    stagger: 0.1
});

gsap.from(".winner", {
    scrollTrigger: {
        trigger: ".nomination",
        start: "bottom center+=100",
        toggleActions: "play none none none"
    },
    y: 60,
    opacity: 0,
    duration: 1.5,
    ease: "power2.out"
});


gsap.fromTo(".footer",
    {opacity: 0, y: 50},
    {
        opacity: 1,
        y: 0,
        duration: 1.5,
        ease: "power2.out",
        scrollTrigger: {
            trigger: ".footer",
            start: "top 90%",
            toggleActions: "play none none none",
        }
    }
);