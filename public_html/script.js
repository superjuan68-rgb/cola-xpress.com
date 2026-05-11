document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.querySelector(".nav-toggle");
  const navMobile = document.querySelector(".nav-mobile");

  if (navToggle && navMobile) {
    navToggle.addEventListener("click", () => {
      const isOpen = navMobile.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    navMobile.addEventListener("click", (event) => {
      const target = event.target;
      if (target instanceof HTMLElement && target.tagName === "A") {
        navMobile.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  const faqSearchInput = document.getElementById("faq-search");
  if (faqSearchInput) {
    const faqContainer = document.getElementById("faq-container");
    const details = faqContainer ? [...faqContainer.querySelectorAll("details")] : [];
    const groups = faqContainer ? [...faqContainer.querySelectorAll(".faq-group")] : [];

    faqSearchInput.addEventListener("input", () => {
      const query = faqSearchInput.value.toLowerCase().trim();

      details.forEach((detail) => {
        const summary = detail.querySelector("summary");
        const text = `${summary ? summary.innerText : ""} ${detail.innerText}`.toLowerCase();
        const matches = text.includes(query);
        detail.classList.toggle("is-hidden", !matches);
      });

      groups.forEach((group) => {
        const visibleDetails = [...group.querySelectorAll("details")].some(
          (detail) => !detail.classList.contains("is-hidden")
        );
        group.classList.toggle("is-hidden", !visibleDetails);
      });
    });
  }

  const siteSearchInput = document.getElementById("site-search");
  const resultsContainer = document.getElementById("search-results");
  const searchCount = document.getElementById("search-count");
  const normalizeSearchText = (value) =>
    String(value || "")
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/['\u2018\u2019]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();

  const buildSearchText = (item) =>
    normalizeSearchText(`${item.title} ${item.category} ${item.content} ${item.searchTerms || ""}`);

  const renderSearchThumbnail = (item) => {
    if (item.image) {
      return `
        <a class="search-thumb" href="${item.url}" aria-hidden="true" tabindex="-1">
          <img src="${item.image}" alt="${item.imageAlt || ""}" loading="lazy" />
        </a>
      `;
    }

    return `
      <a class="search-thumb search-thumb-fallback" href="${item.url}" aria-hidden="true" tabindex="-1">
        <span>${item.thumbLabel || item.category}</span>
      </a>
    `;
  };

  const renderSearchResults = (query) => {
    if (!resultsContainer) {
      return;
    }

    resultsContainer.innerHTML = "";

    if (!query) {
      if (searchCount) {
        searchCount.textContent =
          "Try VGrow, curing, trichomes, financing, or sickle cell to explore the library.";
      }
      resultsContainer.innerHTML =
        '<div class="empty-state">Search across the grow system, guide hub, equipment page, FAQ, and the full seed-to-jar library. Try a stage, a tool, a symptom, or a question.</div>';
      return;
    }

    const normalized = normalizeSearchText(query);
    const queryTokens = normalized.split(" ").filter(Boolean);

    if (!normalized) {
      if (searchCount) {
        searchCount.textContent =
          "Try VGrow, curing, trichomes, financing, or sickle cell to explore the library.";
      }
      resultsContainer.innerHTML =
        '<div class="empty-state">Search across the grow system, guide hub, equipment page, FAQ, and the full seed-to-jar library. Try a stage, a tool, a symptom, or a question.</div>';
      return;
    }

    const results = searchData.filter((item) => {
      const searchText = buildSearchText(item);
      return searchText.includes(normalized) || queryTokens.every((token) => searchText.includes(token));
    });

    if (searchCount) {
      searchCount.textContent =
        results.length === 0
          ? `No results for "${query}". Try broader terms like VGrow, harvest, cure, or financing.`
          : `${results.length} result${results.length === 1 ? "" : "s"} for "${query}".`;
    }

    if (results.length === 0) {
      resultsContainer.innerHTML =
        '<div class="empty-state">No direct match yet. Try broader terms like DWC, 12/12, drying, trichomes, legality, or FAQ. If the exact term is still fuzzy, use the guide hub or FAQ as a starting point.</div>';
      return;
    }

    results.forEach((item) => {
      const resultEl = document.createElement("article");
      resultEl.className = "search-result";
      const snippet =
        item.content.length > 180 ? `${item.content.slice(0, 180)}...` : item.content;
      resultEl.innerHTML = `
        ${renderSearchThumbnail(item)}
        <div class="search-result-copy">
          <div class="search-meta">${item.category}</div>
          <h3><a href="${item.url}">${item.title}</a></h3>
          <p>${snippet}</p>
        </div>
      `;
      resultsContainer.appendChild(resultEl);
    });
  };

  if (siteSearchInput && resultsContainer) {
    const params = new URLSearchParams(window.location.search);
    const initialQuery = params.get("q") || "";
    siteSearchInput.value = initialQuery;
    renderSearchResults(initialQuery.trim());

    siteSearchInput.addEventListener("input", () => {
      renderSearchResults(siteSearchInput.value.trim());
    });
  }

  document.querySelectorAll(".video-facade").forEach((facade) => {
    facade.addEventListener("click", () => {
      const videoId = facade.dataset.youtubeId;
      if (!videoId) {
        return;
      }

      const iframe = document.createElement("iframe");
      iframe.className = "video-iframe";
      iframe.width = "1280";
      iframe.height = "720";
      iframe.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(videoId)}?autoplay=1&rel=0`;
      iframe.title = facade.dataset.videoTitle || "YouTube video";
      iframe.allow =
        "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.referrerPolicy = "strict-origin-when-cross-origin";
      iframe.allowFullscreen = true;

      facade.replaceWith(iframe);
    });
  });
});

const searchData = [
  {
    title: "Home",
    url: "../index.html",
    category: "Overview",
    content:
      "ColaXpress is a guided grow app for compact cannabis cultivation built around the VGrow Smart Box, the matching DWC kit, and a seed-to-jar workflow."
  },
  {
    title: "Grow System",
    url: "../grow/index.html",
    category: "System",
    content:
      "The grow system page explains how VGrow hardware, DWC hydroponics, 12/12 from seed, financing, and the drying-curing process fit together in one compact setup."
  },
  {
    title: "Craft Cannabis Cultivation",
    url: "../learn/craft-cannabis-cultivation.html",
    category: "Craft Guide",
    image: "../assets/images/craft-vs-max-weight-board.webp",
    imageAlt: "Comparison board showing craft-first cultivation versus max-weight cultivation.",
    thumbLabel: "Craft",
    searchTerms:
      "craft cannabis cultivation finish first craft vs max weight method maturity harvest finish compact room process honesty readable room quality proof",
    content:
      "This guide explains what craft cannabis cultivation really means, how it differs from max-weight growing, why compact systems can support craft well, and how method, harvest, drying, and cure all shape the final result."
  },
  {
    title: "What Is Craft Cannabis?",
    url: "../learn/craft-cannabis.html",
    category: "Craft Definition",
    image: "../assets/images/craft-definition-hero.webp",
    imageAlt: "Editorial still life showing a cannabis jar, pruning shears, a loupe, and craft handling notes.",
    thumbLabel: "Craft",
    searchTerms:
      "what craft is not craft signals before you buy open the jar producer language jar evidence cultivation method handling harvest and finish packaging thc hype thc worship boutique branding small batch finish quality quality proof field guide craft definition",
    content:
      "This guide explains what craft cannabis means, why the term gets diluted, what craft is not, why packaging THC hype branding and small batch claims do not prove quality by themselves, how craft differs from commercial flower, what proves craft through cultivation handling harvest and jar evidence, how to spot credible craft signals, and why cultivation harvest drying and curing are what make the word real."
  },
  {
    title: "Craft Cannabis vs Commercial Cannabis",
    url: "../learn/craft-cannabis-vs-commercial-cannabis.html",
    category: "Craft Comparison",
    image: "../assets/images/craft-protects-commercial-protects.webp",
    imageAlt: "Comparison board showing what craft-first cultivation protects versus what commercial cultivation protects.",
    thumbLabel: "Compare",
    searchTerms:
      "craft versus commercial cannabis commercial cannabis comparison craft cannabis vs commercial premium proof jar behavior handling pressure process proof scale quality value",
    content:
      "This comparison guide explains what actually separates craft cannabis from commercial cannabis, including handling pressure, harvest and cure decisions, jar behavior, when a premium is earned, when commercial is still a fair value, and what the labels do and do not really prove."
  },
  {
    title: "Compact Craft Cannabis Grow",
    url: "../grow/compact-craft-cannabis-grow.html",
    category: "Compact Craft",
    image: "../assets/images/compact-craft-vs-compact-max-weight.webp",
    imageAlt: "Comparison board showing compact craft growing versus compact max-weight growing.",
    thumbLabel: "Compact",
    searchTerms:
      "compact craft cannabis grow compact max weight small space craft grow room fit quality proof compact cultivation finish discipline smaller corrections",
    content:
      "This guide explains why compact rooms can support craft cannabis unusually well, what small spaces protect, what they punish immediately, how compact craft differs from compact max-weight growing, and which methods fit the room cleanly."
  },
  {
    title: "Best Cannabis Strains for Small Spaces",
    url: "../grow/best-cannabis-strains-for-small-spaces.html",
    category: "Strain Decision",
    image: "../assets/images/best-cannabis-strains-for-small-spaces-example-2.webp",
    imageAlt: "Timeline board comparing compact cultivar profiles, moderate-stretch profiles, and long-stretch profiles across canopy control and finish timing in small spaces.",
    thumbLabel: "Strains",
    searchTerms:
      "best cannabis strains for small spaces compact cultivar selection moderate stretch small tent cabinet grow strain fit branch width flowering time compact room trait checklist trait based strain choice named strain hype cultivar fit first run",
    content:
      "This decision page explains how to choose the best cannabis strains for small spaces by filtering for structure, stretch, branch habit, finish timing, and method fit instead of chasing generic strain-list hype or famous-name shortcuts."
  },
  {
    title: "Compact Cannabis Grow Setup for Apartments",
    url: "../grow/compact-grow-setup-for-apartments.html",
    category: "Apartment Setup",
    image: "../assets/images/compact-grow-setup-for-apartments-example-2.webp",
    imageAlt: "Apartment fit-check board showing enclosure footprint, access lane, odor path, and height clearance for a compact indoor cannabis grow.",
    thumbLabel: "Apartment",
    searchTerms:
      "compact cannabis grow setup for apartments apartment grow setup lease landlord building rules odor control shared walls secured enclosure personal use compact cabinet apartment fit renter shared space finish path housing first",
    content:
      "This support guide explains how to plan a compact cannabis grow setup for apartments by clearing housing rules first, keeping the enclosure readable, respecting odor and airflow limits, and matching the plant, method, and finish path to a shared residential space."
  },
  {
    title: "Low Odor Cannabis Grow Setup",
    url: "../grow/low-odor-cannabis-grow-setup.html",
    category: "Odor Setup",
    image: "../assets/images/low-odor-cannabis-grow-setup-example-2.webp",
    imageAlt: "Airflow diagram showing a small grow enclosure, intake, carbon-filtered exhaust, and surrounding room air used to reduce odor drift.",
    thumbLabel: "Odor",
    searchTerms:
      "low odor cannabis grow setup low smell grow setup carbon filter filtered exhaust odor nuisance apartment grow shared walls compact grow drying smell drift humidity canopy size finish path",
    content:
      "This support guide explains how to build a low odor cannabis grow setup by controlling the air path, keeping canopy size realistic, managing humidity, and planning drying and curing so odor drift stays lower in a compact home."
  },
  {
    title: "How Long a Compact Grow Actually Takes",
    url: "../grow/how-long-a-compact-grow-actually-takes.html",
    category: "Timeline",
    image: "../assets/images/harvest-jar-finished-timeline.webp",
    imageAlt: "Timeline board showing harvest-ready, jar-ready, and actually finished cannabis flower.",
    thumbLabel: "Timeline",
    searchTerms:
      "harvest ready harvest-ready jar ready jar-ready finished jar chop ready cure timeline seed to jar compact grow takes drying cure actually finished",
    content:
      "This guide explains how long a compact cannabis grow actually takes from sprout to finished jar, including the faster 12/12 path, the longer compact photoperiod path, drying time, cure time, and the difference between chop-ready and truly finished flower."
  },
  {
    title: "Vivosun VGrow DWC Guide",
    url: "../equipment/vivosun-vgrow-dwc-guide.html",
    category: "VGrow DWC",
    image: "../assets/images/vgrow-dwc-system-hero.webp",
    imageAlt: "Compact VGrow-style grow cabinet and DWC reservoir setup arranged with pH, EC, aeration, and finish tools for a craft-first workflow.",
    thumbLabel: "VGrow",
    searchTerms:
      "official setup video Vivosun official manufacturer video DWC setup video VGrow hydroponics system kit official walkthrough deep water culture setup order reservoir assembly pH EC water level air stones Hydroponics System Kit",
    content:
      "This guide explains how the Vivosun VGrow DWC path works, who it fits, how the cabinet and DWC kit function together, what to buy first, why the stack works best as a craft-first compact workflow, and includes Vivosun's official DWC setup video walkthrough."
  },
  {
    title: "Guides",
    url: "index.html",
    category: "Guide Hub",
    image: "../assets/images/harvest-window-chart.webp",
    imageAlt: "Harvest timing chart used as a visual guide thumbnail.",
    thumbLabel: "Guides",
    content:
      "The guide hub organizes the ColaXpress library by situation and stage, routing readers through setup, DWC basics, 12/12 from seed, harvest timing, drying, curing, and beginner mistake guides in a clean order."
  },
  {
    title: "Equipment",
    url: "../equipment/index.html",
    category: "Equipment",
    content:
      "The equipment page explains what the flagship setup includes, what each tool actually does in the workflow, what to buy first, what can wait, and how beginners waste money by buying in the wrong order."
  },
  {
    title: "About",
    url: "about.html",
    category: "About",
    content:
      "The about page explains why ColaXpress exists, the founder's sickle-cell-rooted motivation, how the project handles trust and claim boundaries, and what kind of compact growing guidance the app is built to give."
  },
  {
    title: "FAQ",
    url: "faq.html",
    category: "FAQ",
    content:
      "The FAQ is a searchable answer center covering setup, VGrow, DWC, 12/12 from seed, yield expectations, harvest timing, jars, curing, legality, financing, and medical boundaries."
  },
  {
    title: "Is Home Grow Legal in New York?",
    url: "new-york-home-grow-law.html",
    category: "Legal Guide",
    image: "../assets/images/new-york-home-grow-law-example-2.webp",
    imageAlt:
      "Apartment and landlord context board showing state home-grow law, lease terms, federal-benefit risk, and local-rule checks for New York home cultivation.",
    thumbLabel: "NY Law",
    searchTerms:
      "is home grow legal in new york new york home cultivation plant limits household limits landlord apartment personal use OCM adults 21 secure plants local rules municipality personal home cultivation federal benefits",
    content:
      "This legal guide explains New York home grow rules for adults, including plant limits, household limits, security requirements, local-rule context, landlord questions, personal-use boundaries, and why ColaXpress keeps the guidance educational rather than legal advice."
  },
  {
    title: "Can Landlords Ban Home Grow in New York?",
    url: "can-landlords-ban-home-grow-in-new-york.html",
    category: "Legal Guide",
    image: "../assets/images/can-landlords-ban-home-grow-in-new-york-example-1.webp",
    imageAlt:
      "New York renter decision board showing state home-grow law, lease terms, building policy, and federal-benefit checks in a practical review order.",
    thumbLabel: "Renters",
    searchTerms:
      "can landlords ban home grow in new york landlord renter lease apartment co-op condo federal benefits cannabis cultivation premises policy odor smoke free nuisance home cultivation faq adult use",
    content:
      "This renter-focused legal guide explains how New York landlord guidance, home-cultivation FAQ language, lease terms, premises rules, federal-benefit exceptions, and compact-grow realities fit together before a home grow is treated as cleared."
  },
  {
    title: "Contact",
    url: "contact.html",
    category: "Support",
    content:
      "The contact page explains what to reach out about, where to send questions, and how to use ColaXpress support alongside the FAQ and guide library."
  },
  {
    title: "12/12 From Seed",
    url: "../grow/12-12-from-seed.html",
    category: "Grow Method",
    content:
      "This guide explains the 12/12 from seed method, what it changes, who it fits, what tradeoffs it brings, why it works in compact craft grows, and what beginners usually get wrong."
  },
  {
    title: "When 12/12 From Seed Is a Bad Idea",
    url: "../grow/when-12-12-from-seed-is-a-bad-idea.html",
    category: "Method Decision",
    image: "../assets/images/when-12-12-from-seed-is-a-bad-idea-example-1.webp",
    imageAlt: "Timeline board showing when a 12/12 from seed plan still fits a compact room and when it starts to mismatch the plant or goal.",
    thumbLabel: "Fit Check",
      searchTerms:
        "when 12/12 from seed is a bad idea 12/12 from seed wrong fit compact grow small space cabinet grow flowering from seed yield structure recovery cultivar fit check stretch veg time canopy goal method mismatch",
      content:
        "This counterweight page explains when 12/12 from seed stops fitting the room, the cultivar, or the goal, including stretch pressure, recovery margin, wider-canopy ambition, compact DWC cabinet fit, and when a longer vegetative path makes more sense."
  },
  {
    title: "Harvest Ripeness",
    url: "../learn/harvest-ripeness.html",
    category: "Harvest",
    image: "../assets/images/harvest-peak.webp",
    imageAlt: "Mature cannabis flower used for the harvest guide hero image.",
    thumbLabel: "Harvest",
    content:
      "The harvest guide explains when to harvest cannabis by reading trichomes, pistils, canopy variation, and ripeness signals together so growers can decide whether to cut now, wait, or recheck."
  },
  {
    title: "What Are Trichomes?",
    url: "../learn/what-are-trichomes.html",
    category: "Harvest Quick Answer",
    image: "../assets/images/what-are-trichomes-example-2.webp",
    imageAlt: "Comparison board showing clear, cloudy, amber, and mixed trichome inspection states.",
    thumbLabel: "Trichomes",
    searchTerms:
      "what are trichomes cannabis trichomes definition resin glands harvest timing quick answer clear cloudy amber inspection sugar leaves buds finish vocabulary",
    content:
      "This quick-answer page explains what trichomes are, why growers inspect them, how they relate to harvest timing, and which finish pages to use next for vocabulary, stage comparison, and the full harvest call."
  },
  {
    title: "What Is Curing?",
    url: "../learn/what-is-curing.html",
    category: "Curing Quick Answer",
    image: "../assets/images/what-is-curing-example-2.webp",
    imageAlt: "Curing state board comparing too wet, on track, and too dry jars after the drying-to-cure handoff.",
    thumbLabel: "Cure",
    searchTerms:
      "what is curing cannabis curing definition quick answer cure after drying jar ready buds jars moisture redistribution burping finish post harvest compact grow definition versus full cure process mistakes handoff",
    content:
      "This quick-answer page explains what curing means, why it happens after drying, how it fits into compact grow finishing, and when to move next into jar readiness, common mistakes, or the full cure workflow."
  },
  {
    title: "How to Dry and Cure Cannabis",
    url: "../learn/how-to-cure-cannabis.html",
    category: "Drying and Curing",
    image: "../assets/images/cure-hero.webp",
    imageAlt: "Cannabis curing jar used for the cure guide hero image.",
    thumbLabel: "Cure",
    content:
      "This guide covers drying, curing, jar moisture, self-burping lids, common mistakes, and how to finish flower cleanly after harvest."
  },
  {
    title: "Compact Grow Setup Checklist",
    url: "../grow/compact-grow-setup-checklist.html",
    category: "Beginner Setup",
    content:
      "This checklist explains how to build a compact cannabis grow in the right order, covering enclosure, DWC or root-zone planning, monitoring tools, drying, curing, and the common setup mistakes beginners make."
  },
  {
    title: "What to Buy First for a Small Cannabis Grow",
    url: "../equipment/what-to-buy-first.html",
    category: "Buying Guide",
    content:
      "This buying guide explains what should go in the first cart, what can wait until later, what belongs in the pre-harvest cart, and which gear beginners should stop buying just to calm nerves."
  },
  {
    title: "DWC Basics for Beginners",
    url: "../grow/dwc-basics-for-beginners.html",
    category: "DWC Guide",
    image: "../assets/images/dwc-cutaway-diagram.webp",
    imageAlt: "Cutaway diagram of a DWC reservoir showing roots, nutrient solution, and an air stone.",
    thumbLabel: "DWC",
    content:
      "This guide explains deep water culture basics for beginners, including oxygenation, nutrient solution, pH, EC, root health, and why DWC fits compact cannabis growing so well."
  },
  {
    title: "What Is DWC?",
    url: "../grow/what-is-dwc.html",
    category: "DWC Quick Answer",
    image: "../assets/images/what-is-dwc-example-2.webp",
    imageAlt: "Compact DWC grow setup with a clean reservoir, measurement tools, and a readable cabinet workflow.",
    thumbLabel: "DWC",
    searchTerms:
      "what is DWC deep water culture hydroponics definition quick answer roots in water oxygenated nutrient solution reservoir air stone compact grow hydro basics beginner guide",
    content:
      "This quick-answer page explains what DWC means, how deep water culture works, why growers use it in compact setups, and which follow-up pages to use next for the full beginner walkthrough, method fit, and troubleshooting."
  },
  {
    title: "Root Problems in DWC",
    url: "../grow/root-problems-in-dwc.html",
    category: "DWC Troubleshooting",
      image: "../assets/images/root-problems-in-dwc-example-3.webp",
      imageAlt: "Educational comparison board showing healthy DWC roots, roots to watch, and roots that need inspection.",
    thumbLabel: "Roots",
      searchTerms:
        "root problems in DWC root issues hydro roots brown roots slimy roots bad smell root rot oxygen water temperature reservoir compact grow diagnosis humidity room drift what is DWC root zone stress",
      content:
        "This troubleshooting page explains how to read root problems in DWC, including oxygen loss, warm water, reservoir cleanliness, slower drinking, off smells, room-level humidity and heat drift, and how compact grow systems make root-zone stress easier to notice before the whole workflow slides."
  },
  {
    title: "Cabinet Grow vs Grow Tent",
    url: "../grow/cabinet-grow-vs-grow-tent.html",
    category: "Setup Decision",
    image: "../assets/images/cabinet-grow-vs-grow-tent-example-2.webp",
    imageAlt:
      "Airflow and access comparison between a compact grow cabinet and a small grow tent, showing filtered exhaust, service lane, and enclosure footprint.",
    thumbLabel: "Enclosure",
    searchTerms:
      "cabinet grow vs grow tent grow box versus tent compact grow comparison small space setup odor control enclosed room fit method choice apartment enclosure decision DWC cabinet smart grow box versus tent airflow footprint",
    content:
      "This comparison page explains whether a cabinet grow or grow tent makes more sense for a compact cannabis setup, including containment, flexibility, airflow, plant size, DWC fit, VGrow fit, shared-space pressure, and beginner tradeoffs."
  },
  {
    title: "Humidity Problems in a Grow Cabinet",
    url: "../grow/humidity-problems-in-a-grow-cabinet.html",
    category: "Troubleshooting",
    image: "../assets/images/humidity-problems-in-a-grow-cabinet-example-2.webp",
    imageAlt:
      "Airflow board for a compact enclosure showing intake, exhaust, circulation, canopy blockage, and where heavy wet air gets trapped.",
    thumbLabel: "Humidity",
    searchTerms:
      "humidity problems in a grow cabinet high humidity cabinet grow wet air airflow exhaust compact room climate diagnosis condensation plant too large heavy air damp cabinet canopy density stale room VGrow DWC humidity",
    content:
      "This troubleshooting guide explains why humidity problems show up in a grow cabinet, how to separate room drift from canopy overload, where DWC and VGrow fit, and how airflow, plant size, and routine drift create repeat moisture problems."
  },
  {
    title: "How to Lower Humidity in a Small Grow Tent",
    url: "../grow/how-to-lower-humidity-in-a-small-grow-tent.html",
    category: "Humidity Quick Answer",
    image: "../assets/images/how-to-lower-humidity-in-a-small-grow-tent-example-2.webp",
    imageAlt: "Small grow tent airflow board showing intake, exhaust, circulation, and canopy notes for lowering humidity.",
    thumbLabel: "Humidity",
    searchTerms:
      "how to lower humidity in a small grow tent lower humidity small tent high humidity tent wet tent airflow exhaust canopy damp lung room lights off heavy air",
    content:
      "This quick-answer page explains how to lower humidity in a small grow tent by fixing the air path, reducing canopy crowding, checking the surrounding room, and knowing when to step into the deeper enclosure diagnosis."
  },
  {
    title: "DWC vs Soil for Small Cannabis Grows",
    url: "../grow/dwc-vs-soil-for-small-grows.html",
    category: "Method Decision",
    image: "../assets/images/dwc-vs-soil-for-small-grows-example-2.webp",
    imageAlt: "Comparison chart showing feedback speed, forgiveness, cleanup, and room discipline differences between DWC and soil in small spaces.",
    thumbLabel: "Compare",
    searchTerms:
      "DWC vs soil for small cannabis grows hydroponics versus soil compact grow cabinet method choice reservoir medium forgiveness root zone comparison feedback speed cleanup room discipline contained workflow",
    content:
      "This decision page explains whether DWC or soil makes more sense in a compact cannabis grow, including feedback speed, forgiveness, cleanup, room discipline, cabinet fit, and finish implications."
  },
  {
    title: "Why Growth Is Slow in a Compact Setup",
    url: "../grow/why-growth-is-slow-in-a-compact-setup.html",
    category: "Troubleshooting",
    image: "../assets/images/why-growth-is-slow-in-a-compact-setup-example-2.webp",
    imageAlt: "Compact system map showing how stale air, crowded canopy, root drag, and changing routines can combine to slow cannabis growth.",
    thumbLabel: "Slowdown",
    searchTerms:
      "why growth is slow in a compact setup slow cannabis growth cabinet grow stalled growth compact room diagnosis weak roots weak airflow plant too large stale air crowded canopy routine drift room drag",
    content:
      "This troubleshooting page explains why growth slows in a compact cannabis setup, how to diagnose room drag calmly, and which root-zone, airflow, canopy, and routine problems usually create stalled momentum."
  },
  {
    title: "What to Monitor Every Day in a Compact Grow",
    url: "../grow/daily-grow-checks.html",
    category: "Daily Routine",
    content:
      "This guide explains what to monitor every day in a compact cannabis grow, including environment, plant posture, reservoir behavior, pH and EC patterns, and how to keep the routine useful without overreacting."
  },
  {
    title: "Beginner Mistakes in Small-Space Grows",
    url: "../grow/beginner-mistakes-small-space-grows.html",
    category: "Beginner Mistakes",
    content:
      "This guide covers the most common beginner mistakes in small-space cannabis grows, including overbuying, overfeeding, environment drift, overcorrection, and poor harvest or cure planning."
  },
  {
    title: "Cloudy vs Amber Trichomes",
    url: "../learn/cloudy-vs-amber-trichomes.html",
    category: "Harvest Timing",
    image: "../assets/images/harvest-window-chart.webp",
    imageAlt: "Comparison chart showing trichome maturity stages.",
    thumbLabel: "Timing",
    content:
      "This guide compares cloudy vs amber trichomes, explains what each stage looks like, how growers use those signals for harvest timing, and what beginners usually misread."
  },
  {
    title: "How to Tell Buds Are Ready for Jars",
    url: "../learn/buds-ready-for-jars.html",
    category: "Dry-to-Cure",
    image: "../assets/images/jar-reading-panel.webp",
    imageAlt: "Jar reading diagram for smell, feel, and moisture behavior.",
    thumbLabel: "Jars",
    content:
      "This guide explains how to tell when cannabis buds are ready for jars after drying, including stem behavior, outer texture, hidden interior moisture, and the signs you are moving into cure too early."
  },
  {
    title: "Common Drying Mistakes",
    url: "../learn/common-drying-mistakes.html",
    category: "Drying Guide",
    content:
      "This guide covers common cannabis drying mistakes, including too much direct airflow, unstable humidity, overcrowded hanging conditions, overdrying, and moving flower into jars too early."
  },
  {
    title: "Common Curing Mistakes",
    url: "../learn/common-curing-mistakes.html",
    category: "Curing Guide",
    image: "../assets/images/cure-states-board.webp",
    imageAlt: "Cure state board comparing too wet, on track, and too dry jars.",
    thumbLabel: "Curing",
    content:
      "This guide covers common cannabis curing mistakes, including wet rebound in jars, grassy or musty smell warnings, overhandling, overdrying after the move to jars, and how to read whether a cure is stabilizing or drifting."
  },
  {
    title: "Craft, Harvest, and Finish",
    url: "../learn/index.html",
    category: "Learn Hub",
    image: "../assets/images/craft-definition-hero.webp",
    imageAlt: "Editorial still life showing craft cannabis handling and finish philosophy.",
    thumbLabel: "Learn",
    searchTerms:
      "craft cannabis philosophy harvest timing trichome inspection drying curing finish discipline learn hub craft cultivation",
    content:
      "The ColaXpress Learn hub organizes craft cannabis philosophy, harvest ripeness, trichome inspection, and the drying and curing finish chain in one place."
  },
  {
    title: "The ColaXpress Grow Series",
    url: "../watch/index.html",
    category: "Video Series",
    image: "../assets/images/vgrow-dwc-system-hero.webp",
    imageAlt: "VIVOSUN vGrow cabinet and DWC reservoir for the ColaXpress Grow Series.",
    thumbLabel: "Watch",
    searchTerms:
      "ColaXpress grow series watch episodes vGrow DWC humidifier craft cannabis automation documentary seed to jar video",
    content:
      "The ColaXpress Grow Series documents a complete craft cannabis grow using the VIVOSUN vGrow cabinet, DWC reservoir, and humidifier from seed to cured jar. Can automation produce craft flower?"
  },
  {
    title: "Episode 1: Can Automation Produce Craft Cannabis?",
    url: "../watch/episode-01.html",
    category: "Video Episode",
    image: "../assets/images/vgrow-dwc-system-hero.webp",
    imageAlt: "VIVOSUN vGrow cabinet and DWC reservoir — Episode 1 of the ColaXpress Grow Series.",
    thumbLabel: "Ep 1",
    searchTerms:
      "episode 1 ColaXpress grow series can automation produce craft cannabis vGrow DWC humidifier VPD vapor pressure deficit root emergence seedling setup first grow",
    content:
      "Episode 1 of the ColaXpress Grow Series. The vGrow cabinet, DWC reservoir, and humidifier are introduced as an interconnected environment. The grow begins at zero — empty reservoir, fresh seed, bare cabinet — and follows the first 24 hours of environmental calibration."
  }
];


