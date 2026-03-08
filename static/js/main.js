/* ============================================
   main.js — Mobile menu, scroll, animations
   No conflicts with HTMX (separate concerns)
   ============================================ */

(function () {
  'use strict';

  /* ── Mobile menu ── */
  const burger = document.getElementById('burger-btn');
  const mobileNav = document.getElementById('mobile-nav');

  function toggleNav(open) {
    if (!burger || !mobileNav) return;
    burger.setAttribute('aria-expanded', String(open));
    mobileNav.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (burger) {
    burger.addEventListener('click', function () {
      const isOpen = burger.getAttribute('aria-expanded') === 'true';
      toggleNav(!isOpen);
    });
  }

  /* Close on nav link tap */
  document.querySelectorAll('[data-close-nav]').forEach(function (el) {
    el.addEventListener('click', function () { toggleNav(false); });
  });

  /* Close on outside tap */
  document.addEventListener('click', function (e) {
    if (
      mobileNav &&
      mobileNav.classList.contains('open') &&
      !mobileNav.contains(e.target) &&
      e.target !== burger &&
      !burger.contains(e.target)
    ) {
      toggleNav(false);
    }
  });

  /* ── Header scroll shadow ── */
  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Active nav link on scroll (IntersectionObserver) ── */
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav__link[href^="#"]');

  if ('IntersectionObserver' in window && sections.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          navLinks.forEach(function (link) {
            var href = link.getAttribute('href');
            var active = href === '#' + entry.target.id;
            link.classList.toggle('active', active);
          });
        }
      });
    }, { rootMargin: '-50% 0px -50% 0px' });

    sections.forEach(function (s) { observer.observe(s); });
  }

  if ('IntersectionObserver' in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var delay = entry.target.style.getPropertyValue('--reveal-delay') || '0s';
          entry.target.style.transitionDelay = delay;
          entry.target.classList.add('revealed');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0 });

    document.querySelectorAll('.js-reveal').forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    /* Fallback: show all immediately */
    document.querySelectorAll('.js-reveal').forEach(function (el) {
      el.classList.add('revealed');
    });
  }

  /* ── Services tabs ── */
  var tabs = document.querySelectorAll('.services__tab');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var panelId = tab.getAttribute('aria-controls');
      tabs.forEach(function (t) {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      document.querySelectorAll('.services__panel').forEach(function (p) {
        p.classList.remove('active');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      var panel = document.getElementById(panelId);
      if (panel) panel.classList.add('active');
    });
  });

  /* ── FAQ: exclusive accordion via <details> ── */
  var faqItems = document.querySelectorAll('details.faq__item');
  faqItems.forEach(function (det) {
    var summary = det.querySelector('summary');
    if (!summary) return;
    summary.addEventListener('click', function (e) {
      /* Close all siblings first, then let browser toggle the clicked one */
      faqItems.forEach(function (other) {
        if (other !== det && other.open) {
          other.removeAttribute('open');
        }
      });
    });
  });

  /* ── HTMX: re-observe reveals after swap ── */
  document.body.addEventListener('htmx:afterSwap', function () {
    if (!('IntersectionObserver' in window)) return;
    document.querySelectorAll('.js-reveal:not(.revealed)').forEach(function (el) {
      revealObserver.observe(el);
    });
  });

  /* ── Hero modal ── */
  var modalOverlay = document.getElementById('hero-modal');
  var modalTitle = document.getElementById('modal-title');
  var modalCloseBtn = document.getElementById('modal-close-btn');

  var MODAL_TITLES = {
    buy: 'Замовити продукцію',
    sell: 'Отримати консультацію'
  };

  function openModal(interest) {
    if (!modalOverlay) return;
    if (modalTitle && MODAL_TITLES[interest]) {
      modalTitle.textContent = MODAL_TITLES[interest];
    }
    var radio = modalOverlay.querySelector('input[type="radio"][value="' + interest + '"]');
    if (radio) radio.checked = true;
    modalOverlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    if (modalCloseBtn) modalCloseBtn.focus();
  }

  function closeModal() {
    if (!modalOverlay) return;
    modalOverlay.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  document.querySelectorAll('[data-modal-interest]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      openModal(btn.getAttribute('data-modal-interest'));
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay) closeModal();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modalOverlay && modalOverlay.classList.contains('is-open')) {
      closeModal();
    }
  });

  /* ── Phone modal ── */
  var phoneModal = document.getElementById('phone-modal');
  var phoneModalCloseBtn = document.getElementById('phone-modal-close-btn');

  function openPhoneModal() {
    if (!phoneModal) return;
    phoneModal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closePhoneModal() {
    if (!phoneModal) return;
    phoneModal.classList.remove('open');
    document.body.style.overflow = '';
  }

  document.querySelectorAll('[data-modal-target="phone-modal"]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      openPhoneModal();
    });
  });

  if (phoneModalCloseBtn) {
    phoneModalCloseBtn.addEventListener('click', closePhoneModal);
  }

  if (phoneModal) {
    phoneModal.addEventListener('click', function (e) {
      if (e.target === phoneModal) closePhoneModal();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && phoneModal && phoneModal.classList.contains('open')) {
      closePhoneModal();
    }
  });

})();
