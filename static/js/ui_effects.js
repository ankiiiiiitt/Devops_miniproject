/**
 * FocusVault Premium 3D UI Engine
 * Handles Universal Tilt, Mouse Parallax, and GSAP Orbitals
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. UNIVERSAL 3D TILT ENGINE
    const tiltElements = document.querySelectorAll('.card, .sidebar, .chat-container, .subject-card, .bookmark-card, .note-card');
    
    tiltElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            gsap.to(el, {
                rotateX: rotateX,
                rotateY: rotateY,
                duration: 0.5,
                ease: "power2.out",
                transformPerspective: 2000,
                transformStyle: "preserve-3d"
            });
        });
        
        el.addEventListener('mouseleave', () => {
            gsap.to(el, {
                rotateX: 0,
                rotateY: 0,
                duration: 1,
                ease: "elastic.out(1, 0.3)"
            });
        });
    });

    // 2. MOUSE PARALLAX (Interactive Background Orbs)
    const orbs = document.querySelectorAll('.orb');
    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth - 0.5;
        const mouseY = e.clientY / window.innerHeight - 0.5;
        
        orbs.forEach((orb, i) => {
            const depth = (i + 1) * 30;
            gsap.to(orb, {
                x: mouseX * depth,
                y: mouseY * depth,
                duration: 2 + i,
                ease: "power1.out"
            });
        });
    });

    // 3. GSAP FLOATING IDLE ANIMATIONS
    gsap.to('.sidebar', {
        y: "-=10",
        duration: 3,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });

    // 4. PARTICLES (Refined for Performance)
    if (document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            "particles": {
                "number": { "value": 60, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": ["#38bdf8", "#a855f7"] },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.3, "random": true },
                "size": { "value": 2, "random": true },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#38bdf8",
                    "opacity": 0.1,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 1,
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false
                }
            },
            "interactivity": {
                "detect_on": "window",
                "events": {
                    "onhover": { "enable": true, "mode": "bubble" },
                    "onclick": { "enable": true, "mode": "push" },
                    "resize": true
                },
                "modes": {
                    "bubble": { "distance": 100, "size": 4, "duration": 2, "opacity": 1, "speed": 3 },
                    "push": { "particles_nb": 4 }
                }
            },
            "retina_detect": true
        });
    }

    // 5. 3D HERO TILT (index.html specific)
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 40;
            const y = (e.clientY / window.innerHeight - 0.5) * -40;
            
            gsap.to('.hero-3d-stack', {
                rotateY: x,
                rotateX: y,
                duration: 1,
                ease: "power2.out"
            });
        });
    }
});