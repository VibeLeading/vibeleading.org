/* VibeLeading — vibeleading.org
   Interactions: starfield, parallax orbs, scroll reveals, HUD counters, copy pills, mobile nav. */

(function () {
  "use strict";

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Starfield ---------- */
  const canvas = document.getElementById("starfield");
  const ctx = canvas.getContext("2d");
  let stars = [];
  const STAR_COLORS = ["0,212,255", "255,45,149", "255,255,255"];

  function resizeCanvas() {
    canvas.width = window.innerWidth * devicePixelRatio;
    canvas.height = window.innerHeight * devicePixelRatio;
    ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
  }

  function seedStars() {
    const count = Math.min(140, Math.floor((window.innerWidth * window.innerHeight) / 9000));
    stars = Array.from({ length: count }, () => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      r: 0.4 + Math.random() * 1.4,
      color: STAR_COLORS[(Math.random() * STAR_COLORS.length) | 0],
      drift: 0.08 + Math.random() * 0.3,
      twinkle: 0.5 + Math.random() * 0.5,
      phase: Math.random() * Math.PI * 2,
    }));
  }

  function drawStars() {
    ctx.clearRect(0, 0, canvas.width / devicePixelRatio, canvas.height / devicePixelRatio);
    const t = performance.now() / 1000;
    for (const s of stars) {
      if (!prefersReducedMotion) {
        s.y += s.drift * 0.25;
        if (s.y > window.innerHeight) s.y = -2;
      }
      const alpha = 0.18 + 0.7 * Math.abs(Math.sin(t * s.twinkle + s.phase));
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${s.color},${alpha})`;
      ctx.fill();
    }
  }

  let rafId = null;
  function loop() {
    drawStars();
    rafId = requestAnimationFrame(loop);
  }

  if (ctx) {
    resizeCanvas();
    seedStars();
    if (prefersReducedMotion) {
      drawStars(); /* static render */
    } else {
      loop();
    }
  }

  window.addEventListener("resize", () => {
    resizeCanvas();
    seedStars();
    if (prefersReducedMotion) drawStars();
  });

  /* ---------- Parallax orbs ---------- */
  const orbs = document.querySelectorAll(".orb");
  if (orbs.length && !prefersReducedMotion) {
    window.addEventListener("mousemove", (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 2;
      const y = (e.clientY / window.innerHeight - 0.5) * 2;
      orbs[0].style.transform = `translate(${x * -30}px, ${y * -30}px)`;
      orbs[1].style.transform = `translate(${x * 26}px, ${y * 26}px)`;
    });
  }

  /* ---------- Scroll reveals ---------- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- HUD counters ---------- */
  const counterEls = document.querySelectorAll("[data-count]");
  function animateCounter(el) {
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || "";
    if (prefersReducedMotion) {
      el.textContent = target + suffix;
      return;
    }
    const duration = 1600;
    const start = performance.now();
    function frame(now) {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  if (counterEls.length && "IntersectionObserver" in window) {
    const cio = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            cio.unobserve(entry.target);
          }
        }
      },
      { threshold: 0.6 }
    );
    counterEls.forEach((el) => cio.observe(el));
  } else if (counterEls.length) {
    counterEls.forEach(animateCounter);
  }

  /* ---------- Copy pills ---------- */
  document.querySelectorAll(".copy__btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
      } catch (err) {
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (_) {}
        ta.remove();
      }
      const prev = btn.textContent;
      btn.textContent = "COPIED";
      btn.classList.add("copied");
      setTimeout(() => {
        btn.textContent = prev;
        btn.classList.remove("copied");
      }, 1600);
    });
  });

  /* ---------- Mobile nav ---------- */
  const toggle = document.querySelector(".nav__toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  if (toggle && mobileMenu) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mobileMenu.hidden = open;
    });
    mobileMenu.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        toggle.setAttribute("aria-expanded", "false");
        mobileMenu.hidden = true;
      })
    );
  }

  /* ---------- Footer year ---------- */
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();