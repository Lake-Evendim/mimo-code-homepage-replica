(function () {
        const titles = document.querySelectorAll(".card__text h3");
        if (!titles.length || !("IntersectionObserver" in window)) return;

        const CHAR_DELAY = 130; // ms between characters

        titles.forEach((h3) => {
          const text = h3.textContent;
          h3.textContent = "";
          for (const c of text) {
            const span = document.createElement("span");
            span.className = "char";
            span.textContent = c;
            h3.appendChild(span);
          }
          const cursor = document.createElement("span");
          cursor.className = "cursor";
          cursor.setAttribute("aria-hidden", "true");
          h3.appendChild(cursor);
        });

        function animateType(h3) {
          if (h3.dataset.typed === "1") return;
          h3.dataset.typed = "1";
          h3.classList.add("is-active");
          const chars = h3.querySelectorAll(".char");
          chars.forEach((char, i) => {
            setTimeout(() => char.classList.add("is-typed"), i * CHAR_DELAY);
          });
          setTimeout(
            () => h3.classList.add("is-done"),
            chars.length * CHAR_DELAY + 120,
          );
        }

        function snapShow(h3) {
          if (h3.dataset.typed === "1") return;
          h3.dataset.typed = "1";
          h3.classList.add("is-active", "is-done");
          h3
            .querySelectorAll(".char")
            .forEach((c) => c.classList.add("is-typed"));
        }

        const obs = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) animateType(entry.target);
            });
          },
          { threshold: 0.25 },
        );
        titles.forEach((h3) => obs.observe(h3));

        // Safety net: title scrolled past the trigger zone without animation
        // (e.g. user jumped via anchor or scrolled very fast) → snap visible.
        window.addEventListener(
          "scroll",
          () => {
            const cut = window.innerHeight * 0.5;
            titles.forEach((h3) => {
              if (h3.dataset.typed === "1") return;
              if (h3.getBoundingClientRect().bottom < cut) snapShow(h3);
            });
          },
          { passive: true },
        );
      })();

(function () {
        const sub = document.querySelector(".hero__subtitle");
        if (!sub) return;
        // Keep it simple on small screens: no typewriter, allow wrapping.
        if (window.matchMedia("(max-width: 700px)").matches) return;
        const original = sub.textContent.trim();

        function type() {
          // Measure the full single-line width and lock it, so characters
          // print left→right inside a box that stays centered in the hero.
          sub.style.whiteSpace = "nowrap";
          sub.textContent = original;
          const fullW = sub.getBoundingClientRect().width;
          if (fullW > 0) sub.style.width = Math.ceil(fullW) + "px";
          sub.textContent = "";
          sub.classList.add("is-typing");

          const chars = [];
          for (const ch of original) {
            const s = document.createElement("span");
            s.className = "char";
            s.textContent = ch;
            sub.appendChild(s);
            chars.push(s);
          }
          const caret = document.createElement("span");
          caret.className = "type-caret";
          caret.setAttribute("aria-hidden", "true");
          sub.appendChild(caret);

          const DELAY = 55; // ms per character — printer-like cadence
          const START = 350;
          chars.forEach((c, i) => {
            setTimeout(() => c.classList.add("is-typed"), START + i * DELAY);
          });
          setTimeout(
            () => sub.classList.add("is-done"),
            START + chars.length * DELAY + 150,
          );
        }

        if (document.fonts && document.fonts.ready) {
          document.fonts.ready.then(type);
        } else {
          type();
        }
      })();
