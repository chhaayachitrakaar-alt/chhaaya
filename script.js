document.addEventListener("DOMContentLoaded", () => {
    // Register ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // 1. Reveal Animations (Fade in and slide up)
    const revealElements = document.querySelectorAll(".gs-reveal");
    
    revealElements.forEach((el) => {
        gsap.fromTo(el, 
            { 
                autoAlpha: 0, 
                y: 50 
            }, 
            {
                duration: 1, 
                autoAlpha: 1, 
                y: 0, 
                ease: "power3.out",
                scrollTrigger: {
                    trigger: el,
                    start: "top 85%", // Starts when the top of the element hits 85% of the viewport height
                    toggleActions: "play none none reverse"
                }
            }
        );
    });

    // 2. Removed sticky nav scroll trigger since it's now a permanent header

    // 3. Highlight Active Navigation Link based on Scroll
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-links a");

    sections.forEach(section => {
        ScrollTrigger.create({
            trigger: section,
            start: "top center",
            end: "bottom center",
            onToggle: self => {
                if(self.isActive) {
                    // Remove active class from all links
                    navLinks.forEach(link => link.classList.remove("active"));
                    
                    // Add active class to the corresponding link
                    const targetId = section.getAttribute("id");
                    const activeLink = document.querySelector(`.nav-links a[data-target="${targetId}"]`);
                    if(activeLink) {
                        activeLink.classList.add("active");
                    }
                }
            }
        });
    });

    // 4. Smooth Scrolling for Navigation Links
    navLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const targetId = this.getAttribute("href");
            const targetSection = document.querySelector(targetId);
            
            if(targetSection) {
                // Scroll to section smoothly
                window.scrollTo({
                    top: targetSection.offsetTop,
                    behavior: "smooth"
                });
            }
        });
    });
    
    // Add same smooth scrolling for Hero menu Start button
    const startBtn = document.querySelector(".hero-menu a[href='#about']");
    if(startBtn) {
        startBtn.addEventListener("click", function(e) {
            e.preventDefault();
            const targetSection = document.querySelector("#about");
            if(targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop,
                    behavior: "smooth"
                });
            }
        });
    }

    // Video Controls
    const muteBtns = document.querySelectorAll('.mute-btn');
    muteBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const video = this.previousElementSibling;
            if (video && video.tagName === 'VIDEO') {
                video.muted = !video.muted;
                video.volume = 1; // Ensure volume is up
                this.innerHTML = video.muted ? '🔇' : '🔊';
                
                // Some browsers pause the video when unmuted if not fully interacted with
                if (!video.muted && video.paused) {
                    video.play().catch(e => console.log("Play failed:", e));
                }
            }
        });
    });
});
