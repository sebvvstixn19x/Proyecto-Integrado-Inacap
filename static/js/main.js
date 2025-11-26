// ============================================
// LIBRERÍA DIGITAL - MAIN JAVASCRIPT
// Animations, Interactions & UX Enhancements
// ============================================

// Declare AOS and bootstrap variables
const AOS = window.AOS
const bootstrap = window.bootstrap

document.addEventListener("DOMContentLoaded", () => {
  // Initialize AOS (Animate On Scroll)
  AOS.init({
    duration: 800,
    easing: "ease-out-cubic",
    once: true,
    offset: 50,
  })

  // ============================================
  // NAVBAR SCROLL EFFECT
  // ============================================
  const navbar = document.querySelector(".glass-navbar")
  let lastScroll = 0

  window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset

    if (currentScroll > 50) {
      navbar.classList.add("scrolled")
    } else {
      navbar.classList.remove("scrolled")
    }

    lastScroll = currentScroll
  })

  // ============================================
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // ============================================
  // CATEGORY FILTER BUTTONS
  // ============================================
  const categoryButtons = document.querySelectorAll(".category-btn")
  categoryButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      categoryButtons.forEach((b) => b.classList.remove("active"))
      this.classList.add("active")
      // Add filter logic here if needed
    })
  })

  // ============================================
  // BOOK CARDS HOVER EFFECT
  // ============================================
  const bookCards = document.querySelectorAll(".book-card")
  bookCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-10px)"
    })

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)"
    })
  })

  // ============================================
  // FAVORITE BUTTON ANIMATION
  // ============================================
  const favoriteButtons = document.querySelectorAll(".btn-favorite")
  favoriteButtons.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      if (this.classList.contains("is-favorite")) {
        return // Let the form submit
      }

      // Add heart animation
      const heart = document.createElement("span")
      heart.innerHTML = "❤️"
      heart.style.cssText = `
                position: absolute;
                font-size: 2rem;
                pointer-events: none;
                animation: heartFloat 1s ease-out forwards;
            `

      const rect = this.getBoundingClientRect()
      heart.style.left = rect.left + rect.width / 2 + "px"
      heart.style.top = rect.top + "px"
      document.body.appendChild(heart)

      setTimeout(() => heart.remove(), 1000)
    })
  })

  // Heart float animation
  const style = document.createElement("style")
  style.textContent = `
        @keyframes heartFloat {
            0% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
            100% {
                opacity: 0;
                transform: translateY(-50px) scale(1.5);
            }
        }
    `
  document.head.appendChild(style)

  // ============================================
  // STAR RATING INTERACTION
  // ============================================
  const ratingSelects = document.querySelectorAll("#calificacion, #id_calificacion")
  ratingSelects.forEach((select) => {
    // Create visual star rating
    const container = document.createElement("div")
    container.className = "star-rating-visual"
    container.style.cssText = `
            display: flex;
            gap: 8px;
            margin-bottom: 10px;
        `

    for (let i = 1; i <= 5; i++) {
      const star = document.createElement("span")
      star.innerHTML = "★"
      star.dataset.value = i
      star.style.cssText = `
                font-size: 2rem;
                cursor: pointer;
                color: #4a4a4a;
                transition: color 0.2s ease, transform 0.2s ease;
            `

      star.addEventListener("mouseenter", function () {
        this.style.transform = "scale(1.2)"
        highlightStars(container, i)
      })

      star.addEventListener("mouseleave", function () {
        this.style.transform = "scale(1)"
        highlightStars(container, select.value)
      })

      star.addEventListener("click", () => {
        select.value = i
        highlightStars(container, i)
      })

      container.appendChild(star)
    }

    select.parentNode.insertBefore(container, select)
    select.style.display = "none"

    // Initialize with current value
    highlightStars(container, select.value)
  })

  function highlightStars(container, rating) {
    const stars = container.querySelectorAll("span")
    stars.forEach((star, index) => {
      star.style.color = index < rating ? "#ffc107" : "#4a4a4a"
    })
  }

  // ============================================
  // AUTO-DISMISS ALERTS
  // ============================================
  const alerts = document.querySelectorAll(".alert-custom")
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.remove("show")
      setTimeout(() => alert.remove(), 300)
    }, 5000)
  })

  // ============================================
  // FORM VALIDATION ENHANCEMENT
  // ============================================
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const submitBtn = this.querySelector('[type="submit"]')
      if (submitBtn) {
        submitBtn.disabled = true
        const originalText = submitBtn.innerHTML
        submitBtn.innerHTML = '<span class="spinner me-2"></span>Procesando...'

        // Re-enable after 3 seconds as fallback
        setTimeout(() => {
          submitBtn.disabled = false
          submitBtn.innerHTML = originalText
        }, 3000)
      }
    })
  })

  // ============================================
  // SEARCH INPUT ENHANCEMENT
  // ============================================
  const searchInputs = document.querySelectorAll('.search-form input[type="text"], .search-form input[type="search"]')
  searchInputs.forEach((input) => {
    input.addEventListener("focus", function () {
      this.parentElement.style.boxShadow = "0 0 0 3px rgba(233, 69, 96, 0.2)"
    })

    input.addEventListener("blur", function () {
      this.parentElement.style.boxShadow = "none"
    })
  })

  // ============================================
  // PARALLAX EFFECT FOR HERO
  // ============================================
  const heroSection = document.querySelector(".hero-section")
  if (heroSection) {
    window.addEventListener("scroll", () => {
      const scrolled = window.pageYOffset
      const rate = scrolled * 0.3
      heroSection.style.backgroundPositionY = rate + "px"
    })
  }

  // ============================================
  // TYPED TEXT EFFECT (Optional)
  // ============================================
  const typedElements = document.querySelectorAll(".typed-text")
  typedElements.forEach((el) => {
    const text = el.textContent
    el.textContent = ""
    let i = 0

    function type() {
      if (i < text.length) {
        el.textContent += text.charAt(i)
        i++
        setTimeout(type, 50)
      }
    }

    // Start typing when element is in view
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          type()
          observer.unobserve(entry.target)
        }
      })
    })

    observer.observe(el)
  })

  // ============================================
  // RIPPLE EFFECT FOR BUTTONS
  // ============================================
  const rippleButtons = document.querySelectorAll(".btn-hero, .btn-primary-custom, .btn-submit")
  rippleButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      const ripple = document.createElement("span")
      const rect = this.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height)
      const x = e.clientX - rect.left - size / 2
      const y = e.clientY - rect.top - size / 2

      ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                left: ${x}px;
                top: ${y}px;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `

      this.style.position = "relative"
      this.style.overflow = "hidden"
      this.appendChild(ripple)

      setTimeout(() => ripple.remove(), 600)
    })
  })

  // Ripple animation
  const rippleStyle = document.createElement("style")
  rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `
  document.head.appendChild(rippleStyle)

  // ============================================
  // COUNTER ANIMATION
  // ============================================
  const counters = document.querySelectorAll(".stat-number")
  counters.forEach((counter) => {
    const target = Number.parseInt(counter.textContent.replace(/\D/g, ""))
    const duration = 2000
    const increment = target / (duration / 16)
    let current = 0

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const timer = setInterval(() => {
            current += increment
            if (current >= target) {
              counter.textContent = target.toLocaleString() + (counter.textContent.includes("+") ? "+" : "")
              clearInterval(timer)
            } else {
              counter.textContent = Math.floor(current).toLocaleString()
            }
          }, 16)
          observer.unobserve(entry.target)
        }
      })
    })

    observer.observe(counter)
  })

  // ============================================
  // IMAGE LAZY LOADING WITH FADE IN
  // ============================================
  const lazyImages = document.querySelectorAll("img[data-src]")
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target
        img.src = img.dataset.src
        img.classList.add("fade-in")
        observer.unobserve(img)
      }
    })
  })

  lazyImages.forEach((img) => imageObserver.observe(img))

  // ============================================
  // TOOLTIP INITIALIZATION
  // ============================================
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  tooltipTriggerList.forEach((el) => {
    new bootstrap.Tooltip(el)
  })

  // ============================================
  // MOBILE MENU ANIMATION
  // ============================================
  const navbarToggler = document.querySelector(".navbar-toggler")
  const navbarCollapse = document.querySelector(".navbar-collapse")

  if (navbarToggler && navbarCollapse) {
    navbarToggler.addEventListener("click", function () {
      this.classList.toggle("active")
    })
  }

  console.log("✨ Librería Digital initialized successfully!")
})
