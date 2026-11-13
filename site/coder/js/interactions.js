(function () {
        const btn = document.querySelector(".terminal__copy");
        const terminal = document.querySelector(".terminal");
        if (!btn || !terminal) return;

        let resetTimer = 0;

        function fallbackCopy(text) {
          try {
            const ta = document.createElement("textarea");
            ta.value = text;
            ta.setAttribute("readonly", "");
            ta.style.position = "fixed";
            ta.style.top = "-1000px";
            ta.style.left = "0";
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            ta.setSelectionRange(0, text.length);
            const ok = document.execCommand("copy");
            ta.remove();
            return ok;
          } catch (err) {
            return false;
          }
        }

        function copy() {
          const text = terminal.getAttribute("data-copy-text") || "";
          // Run execCommand synchronously first — awaiting the Clipboard API
          // consumes the transient user activation token, after which
          // execCommand is also denied.
          const ok = fallbackCopy(text);

          // Best-effort upgrade to the modern API (fire and forget).
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).catch(() => {});
          }

          if (!ok) return;

          btn.classList.add("is-copied");
          if (resetTimer) clearTimeout(resetTimer);
          resetTimer = window.setTimeout(() => {
            btn.classList.remove("is-copied");
          }, 1500);
        }

        btn.addEventListener("click", copy);
      })();

(function () {
        const switcher = document.querySelector(".platform-switch");
        const terminal = document.querySelector(".terminal");
        if (!switcher || !terminal) return;
        const cmdText = terminal.querySelector(".terminal__text");
        const options = Array.from(
          switcher.querySelectorAll(".platform-switch__option")
        );

        const commands = {
          unix: "curl -fsSL https://mimo.xiaomi.com/install | bash",
          windows:
            'powershell -ep Bypass -c "irm https://mimo.xiaomi.com/install.ps1 | iex"',
        };

        function applyPlatform(platform) {
          const cmd = commands[platform] || commands.unix;
          if (cmdText) cmdText.textContent = cmd;
          terminal.setAttribute("data-copy-text", cmd);
          options.forEach((opt) => {
            const active = opt.dataset.platform === platform;
            opt.classList.toggle("is-active", active);
            opt.setAttribute("aria-pressed", active ? "true" : "false");
          });
        }

        options.forEach((opt) => {
          opt.addEventListener("click", () =>
            applyPlatform(opt.dataset.platform)
          );
        });
      })();
