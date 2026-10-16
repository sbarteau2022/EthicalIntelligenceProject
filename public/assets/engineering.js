(() => {
  'use strict';

  const menu = document.querySelector('.ae-mobile-menu');
  menu?.querySelectorAll('a').forEach((link) =>
    link.addEventListener('click', () => {
      menu.open = false;
    })
  );
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.open) {
      menu.open = false;
      menu.querySelector('summary')?.focus();
    }
  });

  const tabs = [...document.querySelectorAll('[data-work-tab]')];
  if (tabs.length) {
    const tablist = document.querySelector('.ae-work-tabs');
    tablist.setAttribute('role', 'tablist');
    const activate = (selected, focus = false) => {
      tabs.forEach((tab) => {
        const active = tab === selected;
        const panel = document.getElementById(tab.dataset.workTab);
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        panel.hidden = !active;
      });
      if (focus) selected.focus();
    };
    tabs.forEach((tab, index) => {
      const panel = document.getElementById(tab.dataset.workTab);
      tab.id = `tab-${tab.dataset.workTab}`;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panel.id);
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      panel.tabIndex = 0;
      tab.addEventListener('click', (event) => {
        event.preventDefault();
        activate(tab);
      });
      tab.addEventListener('keydown', (event) => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) {
          event.preventDefault();
          activate(tabs[next], true);
        }
      });
    });
    const selectHash = () => activate(tabs.find((tab) => `#${tab.dataset.workTab}` === location.hash) || tabs[0]);
    selectHash();
    window.addEventListener('hashchange', () => {
      const selected = tabs.find((tab) => `#${tab.dataset.workTab}` === location.hash);
      if (selected) activate(selected);
    });
  }

  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('ae-seen');
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12 }
    );
    document
      .querySelectorAll('.ae-mission h2,.ae-section-heading,.ae-process,.ae-pledge-intro,.ae-contact-copy')
      .forEach((element) => observer.observe(element));
  }

  const form = document.getElementById('brief-form');
  if (form) {
    const fields = document.getElementById('brief-fields');
    const result = document.getElementById('brief-result');
    const text = document.getElementById('brief-text');
    const goal = document.getElementById('brief-goal');
    const status = document.getElementById('brief-status');
    goal.addEventListener('input', () => goal.setCustomValidity(''));
    document.querySelectorAll('[data-project-choice]').forEach((link) =>
      link.addEventListener('click', () => {
        document.getElementById('brief-type').value = link.dataset.projectChoice;
        form.hidden = false;
        result.hidden = true;
      })
    );
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (goal.value.trim().length < 10) {
        goal.setCustomValidity('Please describe the goal in at least 10 characters.');
        goal.reportValidity();
        return;
      }
      const name = document.getElementById('brief-name').value.trim().slice(0, 120);
      const org = document.getElementById('brief-org').value.trim().slice(0, 160);
      const type = document.getElementById('brief-type');
      const timing = document.getElementById('brief-timing').value;
      text.value = [
        'ATOMA ENGINEERING — PROJECT BRIEF',
        '',
        `Name: ${name || 'To be discussed'}`,
        `Organization: ${org || 'To be discussed'}`,
        `Project: ${type.options[type.selectedIndex].text}`,
        `Timing: ${timing}`,
        '',
        'WHAT I WOULD LIKE TO MAKE BETTER',
        goal.value.trim().slice(0, 4000),
        '',
        'A useful first conversation: scope, existing materials, important constraints, and what success should look like.',
        '',
        'Prepared locally. This brief has not been submitted. Contact destination is a placeholder.',
      ].join('\n');
      form.hidden = true;
      result.hidden = false;
      status.textContent = 'Ready to save. Your brief has not been sent.';
      result.focus();
    });
    document.getElementById('edit-brief').addEventListener('click', () => {
      result.hidden = true;
      form.hidden = false;
      goal.focus();
    });
    document.getElementById('copy-brief').addEventListener('click', async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(text.value);
        status.textContent = 'Copied. Your project brief is ready to share.';
      } catch {
        text.focus();
        text.select();
        status.textContent = 'Select and copy the brief with Command+C or Ctrl+C, or download it below.';
      }
    });
    document.getElementById('download-brief').addEventListener('click', () => {
      const url = URL.createObjectURL(new Blob([text.value], { type: 'text/plain;charset=utf-8' }));
      const link = document.createElement('a');
      link.href = url;
      link.download = 'atoma-project-brief.txt';
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      status.textContent = 'Download prepared. Your brief has not been sent.';
    });
    // Enable the native form only after every submit/download handler is ready.
    fields.disabled = false;
  }

  document.querySelectorAll('[data-copy-color]').forEach((button) =>
    button.addEventListener('click', async () => {
      const status = document.querySelector('.ae-copy-status');
      const color = button.dataset.copyColor;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(color);
        status.textContent = `${color} copied to clipboard.`;
      } catch {
        status.textContent = `Color value: ${color}. Select this text to copy it.`;
      }
    })
  );
  document.querySelector('[data-print-brand]')?.addEventListener('click', () => window.print());
})();
