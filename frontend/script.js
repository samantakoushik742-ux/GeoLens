
/* ==========================================
   GEO LENS — ENVIRONMENTAL MONITORING
   Illustrative placeholders — not live data
========================================== */

const environmentalData = {
    flood: {
        label: "FLOOD MONITORING",
        value: "Moderate",
        status: "moderate",
        description: "Illustrative flood status",
        color: "#4D829B"
    },
    drought: {
        label: "DROUGHT MONITORING",
        value: "Low",
        status: "low",
        description: "Illustrative drought status",
        color: "#A78342"
    },
    vegetation: {
        label: "VEGETATION MONITORING",
        value: "Healthy",
        status: "healthy",
        description: "Illustrative vegetation status",
        color: "#4F805C"
    }
};

const categoryInfo = {
    flood: {
        title: "Flood Monitoring",
        description: "Browse locations for flood-related environmental monitoring.",
        eyebrow: "WATER SYSTEMS"
    },
    drought: {
        title: "Drought Monitoring",
        description: "Browse locations for drought-related environmental monitoring.",
        eyebrow: "WATER AVAILABILITY"
    },
    vegetation: {
        title: "Vegetation Monitoring",
        description: "Browse locations for vegetation and land-cover monitoring.",
        eyebrow: "LAND SYSTEMS"
    }
};

const monitoringLocations = {
    flood: [
        { name: "Kolkata", region: "West Bengal, India" },
        { name: "Sundarbans", region: "West Bengal, India" },
        { name: "Malda", region: "West Bengal, India" },
        { name: "Murshidabad", region: "West Bengal, India" },
        { name: "Howrah", region: "West Bengal, India" }
    ],
    drought: [
        { name: "Bankura", region: "West Bengal, India" },
        { name: "Purulia", region: "West Bengal, India" },
        { name: "Jhargram", region: "West Bengal, India" },
        { name: "Birbhum", region: "West Bengal, India" },
        { name: "Paschim Medinipur", region: "West Bengal, India" }
    ],
    vegetation: [
        { name: "Sundarbans", region: "West Bengal, India" },
        { name: "Dooars", region: "North Bengal, India" },
        { name: "Darjeeling", region: "West Bengal, India" },
        { name: "Jalpaiguri", region: "West Bengal, India" },
        { name: "Purulia", region: "West Bengal, India" }
    ]
};

/* ==========================================
   LOCATION IMAGERY (Wikimedia Commons)
   Keyed by "category:Location". Each entry is
   [Commons file name, caption, photographer].
   Images are linked from Commons, not stored here.
========================================== */

const locationImages = {
    "flood:Kolkata": [
        ["Torrential rain lash Kolkata, many areas waterlogged- Kolkata-West Bengal-September 2021-IMG 20210915 205028.jpg", "Monsoon downpour floods city streets, September 2021", "", 3]
    ],
    "flood:Sundarbans": [
        ["Dense Mangrove Forest of the Sundarban Tiger Reserve during High Tide, West Bengal, India 02.jpg", "Mangroves submerged at high tide, Sundarban Tiger Reserve", "Herpking"],
        ["Tropical Cyclone Amphan approaching the coasts of India and Bangladesh - May 20th, 2020 (49915736373).jpg", "Cyclone Amphan nearing the delta (Sentinel imagery), May 2020", "Pierre Markuse"],
        ["Riverlets of sundarbans.jpg", "Tidal creeks cutting through the delta", ""]
    ],
    "flood:Malda": [
        ["Manikchak Ghat.jpg", "The Ganga at Manikchak, an erosion hotspot", "Shubh.ch1994"],
        ["Mahananda River.jpg", "The Mahananda, one of Malda's flood-prone rivers", "Aual97"],
        ["Ganga river (2).jpg", "The Ganga near Farakka on the Malda–Murshidabad border", ""]
    ],
    "flood:Murshidabad": [
        ["Bhagirathi River Behind Hazarduari Palace Murshidabad.JPG", "The Bhagirathi behind Hazarduari Palace", "PP Yoonus"],
        ["Highway on Farakka Barrage, a barrage in Farakka, West Bengal 16.jpg", "Farakka Barrage across the Ganga", "Pinakpani"],
        ["Bridge over Bhagirathi river - Murshidabad.jpg", "Bridge over the Bhagirathi", "Ansuman Bhattachraya"]
    ],
    "flood:Howrah": [
        ["Damodar River at Raspur, Howrah 11.jpg", "The Damodar at Raspur, Amta", "Pinakpani"],
        ["Bagnan bridge on Rupnarayan river, Howrah, in West Bengal, India, photographed by Yogabrata Chakraborty, November 9, 2022.jpg", "Bagnan bridge over the Rupnarayan", "Yogabrata Chakraborty"],
        ["Ghat on Hooghly River in Howrah.jpg", "Ghat on the Hooghly, Howrah", "Bernard Gagnon"]
    ],
    "drought:Bankura": [
        ["Koro Hill.jpg", "Steps up Koro Hill, near Susunia", "AbhiMukh97", 2],
        ["Mukutmanipur dam.jpg", "Road along the Mukutmanipur dam, March", "Tarunsamanta", 3]
    ],
    "drought:Purulia": [
        ["Ajodhya Purulia 21.jpg", "Reservoir among the Ajodhya Hills", "Paramanu Sarkar"],
        ["Purulia hills.jpg", "Chota Nagpur plateau hills", ""],
        ["Ajodhya Hill Water reservoir at Purulia.jpg", "Hill reservoir on the Ajodhya plateau", ""]
    ],
    "drought:Jhargram": [
        ["View from top of a hill...in belpahari,jhargram ,west bengal.jpg", "Belpahari uplands", ""],
        ["A click from a top of the hill....at belpahari,jhargram.jpg", "Forested hills around Belpahari", ""],
        ["Jhargram Kanak Durga Mandir.jpg", "Sal forest path near Chilkigarh", "SOUWIKI2016"]
    ],
    "drought:Birbhum": [
        ["Khoai at Shantiniketan in Birbhum district 12.jpg", "Khoai: eroded red laterite at Sonajhuri", "Pinakpani"],
        ["Khoai at Shantiniketan in Birbhum district 04.jpg", "Gullied laterite badlands near Santiniketan", "Pinakpani"],
        ["River Kopai - Ballavpur - Birbhum 2014-06-29 5627.JPG", "The Kopai river at Ballavpur", "Biswarup Ganguly"]
    ],
    "drought:Paschim Medinipur": [
        ["Ravines on the banks of Shilabati.jpg", "Eroded laterite ravines along the Shilabati", ""],
        ["Gangani canyon at Garbeta, Paschim Medinipur 01.jpg", "Road to the Gangani gorge, Garbeta", ""],
        ["Shilabati river or Shilai river near Gangani at Garbeta 01.jpg", "The Shilabati near Gangani", ""]
    ],
    "vegetation:Sundarbans": [
        ["Sundarbans.jpg", "Landsat view of the mangrove forest (dark green)", "NASA Earth Observatory"],
        ["Sundarban Mangrove forest 02.jpg", "Mangrove forest, West Bengal", "Pinakpani"],
        ["Mangrove Forest.jpg", "Mangrove cover at low tide", "Basundhara Chowdhury"]
    ],
    "vegetation:Dooars": [
        ["Tea garden in dooars.jpg", "Tea estate in the Dooars foothills", "Rajibnandi"],
        ["Jaldapara National park Forest.jpg", "Forest at Jaldapara National Park", ""],
        ["Road through Lataguri Forest.jpg", "Road through Lataguri forest", ""]
    ],
    "vegetation:Darjeeling": [
        ["Tea plantation Darjeeling.JPG", "Mist over a Darjeeling tea garden", "Joydeep"],
        ["2024-03-14 Forest seen from Senchal Road 1.jpg", "Forest along Senchal Road", ""],
        ["Darjeeling, India, Trees in the forest near Darjeeling.jpg", "Hill forest near Darjeeling", ""]
    ],
    "vegetation:Jalpaiguri": [
        ["Gairkata Tea Estate 06.jpg", "Gairkata Tea Estate", "Pinakpani"],
        ["Chapramari Wildlife Sanctuary.jpg", "Grassland and wetland at Chapramari", ""],
        ["Gajoldoba Barrage on Teesta river in Gajoldoba 04.jpg", "Gajoldoba Barrage on the Teesta", "Pinakpani"]
    ],
    "vegetation:Purulia": [
        ["Palash flowers in Purulia district.jpg", "Palash in bloom, Purulia", ""],
        ["Sal forests in Purulia, West Bengal, India.jpg", "Sal forest, Purulia", "Xzantiyamoloy"],
        ["Ajodhya Pahar Pathway at Purulia.jpg", "Woodland path on Ajodhya Pahar", "Amitabha Gupta"]
    ]
};

function slugify(value) {
    return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

/* Local copy (made by download-images.ps1) is tried first,
   then the same photo straight from Wikimedia Commons. */
function commonsImage(file, caption, credit, localPath) {
    const encoded = encodeURIComponent(file.replace(/ /g, "_"));
    return {
        sources: [
            localPath,
            "https://commons.wikimedia.org/wiki/Special:FilePath/" + encoded + "?width=1280",
            "https://commons.wikimedia.org/wiki/Special:FilePath/" + encoded
        ],
        page: "https://commons.wikimedia.org/wiki/File:" + encoded,
        caption: caption,
        credit: credit
    };
}

function getLocationImages(category, locationName) {
    const entries = locationImages[category + ":" + locationName] || [];
    return entries.map(function (entry, index) {
        const fileNumber = entry[3] || index + 1;
        const localPath =
            "assets/locations/" + category + "-" + slugify(locationName) + "-" + fileNumber + ".jpg";
        return commonsImage(entry[0], entry[1], entry[2], localPath);
    });
}

/* ==========================================
   DOM ELEMENTS
========================================== */

const layerButtons = document.querySelectorAll(".layer-button");
const navItems = document.querySelectorAll(".nav-item");
const statusCards = document.querySelectorAll(".status-card");

const monitoringTitle = document.querySelector("#monitoringTitle");
const floodValue = document.querySelector("#floodValue");
const droughtValue = document.querySelector("#droughtValue");
const vegetationValue = document.querySelector("#vegetationValue");

const lastUpdated = document.querySelector("#lastUpdated");
const refreshButton = document.querySelector("#refreshButton");
const systemStatus = document.querySelector("#systemStatus");
const themeToggle = document.querySelector("#themeToggle");

const mapLegendText = document.querySelector("#mapLegendText");
const mapLegendColor = document.querySelector(".legend-color");

const locationSearch = document.querySelector("#locationSearch");
const searchMessage = document.querySelector("#searchMessage");
const categoryCards = document.querySelectorAll(".category-card");
const categoryButtons = document.querySelectorAll("[data-open-category]");

const homepage = document.querySelector("#home");
const legacyDashboard = document.querySelector("#legacyDashboard");
const categoryPage = document.querySelector("#categoryPage");
const locationAnalysisPage = document.querySelector("#locationAnalysisPage");

const homepageLocationResults =
    document.querySelector("#homepageLocationResults");

const backToLocations = document.querySelector("#backToLocations");
const analysisCategoryLink = document.querySelector("#analysisCategoryLink");
const analysisHomeLink = document.querySelector("#analysisHomeLink");
const backToHome = document.querySelector("#backToHome");

let currentCategory = null;
let currentLocation = null;

/* ==========================================
   THEME TOGGLE
========================================== */

function setTheme(theme, savePreference = true) {
    const isDark = theme === "dark";

    document.body.classList.toggle("dark-theme", isDark);
    document.body.classList.toggle("light-theme", !isDark);

    if (themeToggle) {
        themeToggle.setAttribute(
            "aria-label",
            isDark ? "Switch to light theme" : "Switch to dark theme"
        );

        themeToggle.setAttribute("aria-pressed", String(isDark));
        themeToggle.textContent = isDark ? "☀ Light mode" : "◐ Dark mode";
    }

    if (savePreference) {
        try {
            localStorage.setItem("geolens-theme", isDark ? "dark" : "light");
        } catch (error) {
            // Theme still works when storage is unavailable.
        }
    }
}

function initializeTheme() {
    let savedTheme = "light";

    try {
        savedTheme = localStorage.getItem("geolens-theme") || "light";
    } catch (error) {
        // Use light theme when browser storage is unavailable.
    }

    setTheme(savedTheme, false);
}

if (themeToggle) {
    themeToggle.addEventListener("click", function () {
        const isDark = document.body.classList.contains("dark-theme");
        setTheme(isDark ? "light" : "dark");
    });
}

initializeTheme();

/* ==========================================
   PAGE VISIBILITY AND NAVIGATION
========================================== */

function hideAllMainViews() {
    if (homepage) homepage.hidden = true;
    if (categoryPage) categoryPage.hidden = true;
    if (locationAnalysisPage) locationAnalysisPage.hidden = true;

    if (legacyDashboard) {
        legacyDashboard.hidden = true;
        legacyDashboard.setAttribute("aria-hidden", "true");
    }
}

function showHomepageSection(sectionId) {
    const target = document.getElementById(sectionId);

    if (!target || !homepage) return;

    hideAllMainViews();
    homepage.hidden = false;

    requestAnimationFrame(function () {
        target.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    });
}

function returnToHomepage() {
    hideAllMainViews();

    if (homepage) homepage.hidden = false;

    window.scrollTo({ top: 0, behavior: "smooth" });
}

function handleTopNavigation(event) {
    const link = event.currentTarget;
    const href = link.getAttribute("href") || "";
    const target = link.dataset.navTarget || "";
    const label = link.textContent.trim().toLowerCase();

    if (href === "#home" || target === "home" || label === "home") {
        event.preventDefault();
        returnToHomepage();
        return;
    }

    const sectionId = target || href.replace(/^#/, "");
    const section = document.getElementById(sectionId);
    if (section && homepage && homepage.contains(section)) {
        event.preventDefault();
        showHomepageSection(sectionId);
    }
}

document.querySelectorAll(
    ".home-nav a, .navbar nav a, a[data-nav-target]"
).forEach(function (link) {
    link.addEventListener("click", handleTopNavigation);
});

/* ==========================================
   STATUS COLOURS
========================================== */

function updateStatusColor(element, status) {
    if (!element) return;

    const statusColors = {
        high: "#955C58",
        moderate: "#A78342",
        low: "#4F805C",
        healthy: "#4F805C"
    };

    element.style.color = statusColors[status] || "";
}

/* ==========================================
   TIME FORMAT
========================================== */

function getFormattedTime() {
    return new Date().toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

/* ==========================================
   LEGACY MAP
========================================== */

let map = null;
let floodLayer = null;
let droughtLayer = null;
let vegetationLayer = null;

function initializeMap() {
    const mapElement = document.querySelector("#map");

    if (!mapElement || typeof L === "undefined" || map !== null) {
        return;
    }

    map = L.map("map").setView([22.5726, 88.3639], 7);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    L.marker([22.5726, 88.3639])
        .addTo(map)
        .bindPopup(
            "<strong>West Bengal</strong><br>" +
            "Illustrative monitoring location"
        );

    floodLayer = L.circle([22.5726, 88.3639], {
        radius: 50000,
        color: "#4D829B",
        fillColor: "#4D829B",
        fillOpacity: 0.2
    });

    droughtLayer = L.circle([22.5726, 88.3639], {
        radius: 50000,
        color: "#A78342",
        fillColor: "#A78342",
        fillOpacity: 0.2
    });

    vegetationLayer = L.circle([22.5726, 88.3639], {
        radius: 50000,
        color: "#4F805C",
        fillColor: "#4F805C",
        fillOpacity: 0.2
    });

    showMapLayer("flood");
}

function showMapLayer(layer) {
    if (!map) return;

    [floodLayer, droughtLayer, vegetationLayer].forEach(function (item) {
        if (item && map.hasLayer(item)) {
            map.removeLayer(item);
        }
    });

    const selectedLayers = {
        flood: floodLayer,
        drought: droughtLayer,
        vegetation: vegetationLayer
    };

    if (selectedLayers[layer]) {
        selectedLayers[layer].addTo(map);
    }
}

/* ==========================================
   LEGACY MONITORING CONTROLS
========================================== */

function selectMonitoringLayer(selectedLayer) {
    const selectedData = environmentalData[selectedLayer];

    if (!selectedData) return;

    layerButtons.forEach(function (button) {
        button.classList.toggle(
            "active",
            button.dataset.layer === selectedLayer
        );
    });

    statusCards.forEach(function (card) {
        card.classList.toggle(
            "selected",
            card.classList.contains(selectedLayer + "-card")
        );
    });

    if (monitoringTitle) monitoringTitle.textContent = selectedData.label;

    const valueElements = {
        flood: floodValue,
        drought: droughtValue,
        vegetation: vegetationValue
    };

    if (valueElements[selectedLayer]) {
        valueElements[selectedLayer].textContent = selectedData.value;
        updateStatusColor(valueElements[selectedLayer], selectedData.status);
    }

    const selectedCard = document.querySelector("." + selectedLayer + "-card");

    if (selectedCard) {
        const description = selectedCard.querySelector("p");
        if (description) description.textContent = selectedData.description;
    }

    if (mapLegendText) {
        mapLegendText.textContent =
            selectedData.label + " — illustrative overlay";
    }

    if (mapLegendColor) {
        mapLegendColor.style.background = selectedData.color;
    }

    showMapLayer(selectedLayer);
}

layerButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        selectMonitoringLayer(button.dataset.layer);
    });
});

navItems.forEach(function (item) {
    item.addEventListener("click", function (event) {
        event.preventDefault();

        navItems.forEach(function (navItem) {
            navItem.classList.remove("active");
        });

        item.classList.add("active");

        const section = item.dataset.section;
        selectMonitoringLayer(section === "dashboard" ? "flood" : section);
    });
});

updateStatusColor(floodValue, environmentalData.flood.status);

/* ==========================================
   REFRESH BUTTON
   No live environmental data is fetched.
========================================== */

if (lastUpdated) {
    lastUpdated.textContent = "Illustrative data · No live feed connected";
}

if (refreshButton) {
    refreshButton.addEventListener("click", function () {
        if (systemStatus) {
            systemStatus.textContent =
                "No live data source is connected. No data was fetched.";
        }

        if (lastUpdated) {
            lastUpdated.textContent = "Last checked: " + getFormattedTime();
        }
    });
}
/* ==========================================
   LOCATION GALLERY AND LATEST REPORT
========================================== */

function updateGalleryCount() {
    const grid = document.querySelector(".place-gallery-grid");
    const section = document.querySelector(".place-gallery-section");
    if (!grid) return;
    const visible = grid.querySelectorAll(".place-image-card:not([hidden])").length;
    grid.dataset.count = String(visible);
    if (section) section.hidden = visible === 0;
}

function updatePlaceGallery(images) {
    const items = (Array.isArray(images) ? images : []).slice(0, 3);
    currentGalleryItems = items;

    document.querySelectorAll("[data-place-image]").forEach(function (image) {
        const index = Number(image.dataset.placeImage);
        const card = document.querySelector('[data-place-card="' + index + '"]');
        const placeholder = document.querySelector('[data-place-placeholder="' + index + '"]');
        const caption = document.querySelector('[data-place-caption="' + index + '"]');
        const item = items[index];

        image.onload = null;
        image.onerror = null;
        image.removeAttribute("src");
        image.alt = "";
        if (card) card.classList.remove("is-loaded", "is-missing");
        if (placeholder) {
            const label = placeholder.querySelector("small");
            if (label) label.textContent = "Loading image " + String(index + 1).padStart(2, "0");
        }
        if (caption) caption.textContent = "";

        if (card) card.hidden = !item;
        if (!item) return;

        // Try each source in order: local copy first, then Wikimedia Commons.
        const sources = (item.sources || [item.url]).filter(function (src) {
            return typeof src === "string" && src.length > 0;
        });
        let attempt = 0;

        image.onload = function () {
            if (card) card.classList.add("is-loaded");
        };

        image.onerror = function () {
            attempt += 1;
            if (attempt < sources.length) {
                image.src = sources[attempt];
                return;
            }
            if (card) card.hidden = true;
            updateGalleryCount();
        };

        image.alt = item.caption || "";
        image.src = sources[0];

        if (caption) {
            const text = document.createElement("span");
            text.className = "place-image-caption-text";
            text.textContent = item.caption || "";
            caption.appendChild(text);

            if (item.page) {
                const credit = document.createElement("a");
                credit.className = "place-image-credit";
                credit.href = item.page;
                credit.target = "_blank";
                credit.rel = "noopener noreferrer";
                credit.textContent = item.credit
                    ? "© " + item.credit + " · Wikimedia Commons"
                    : "Wikimedia Commons";
                caption.appendChild(credit);
            }
        }
    });

    updateGalleryCount();
}

/* ----- Full-size image viewer ----- */
let currentGalleryItems = [];

(function initializePlaceLightbox() {
    const dialog = document.getElementById("placeLightbox");
    const viewerImage = document.getElementById("placeLightboxImage");
    const viewerCaption = document.getElementById("placeLightboxCaption");
    const viewerCredit = document.getElementById("placeLightboxCredit");
    if (!dialog || !viewerImage || typeof dialog.showModal !== "function") return;

    document.querySelectorAll("[data-place-open]").forEach(function (button) {
        button.addEventListener("click", function () {
            const index = Number(button.dataset.placeOpen);
            const card = document.querySelector('[data-place-card="' + index + '"]');
            const thumb = document.querySelector('[data-place-image="' + index + '"]');
            const item = currentGalleryItems[index];
            if (!item || !card || !card.classList.contains("is-loaded")) return;

            viewerImage.src = thumb.currentSrc || thumb.src;
            viewerImage.alt = item.caption || "";
            viewerCaption.textContent = item.caption || "";
            viewerCredit.textContent = item.credit
                ? "Photo: " + item.credit + " · view original on Wikimedia Commons ↗"
                : "View original on Wikimedia Commons ↗";
            viewerCredit.href = item.page || "#";
            dialog.showModal();
        });
    });

    dialog.addEventListener("click", function (event) {
        if (event.target === dialog || event.target.closest("[data-lightbox-close]")) {
            dialog.close();
        }
    });
})();

/* ==========================================
   HOMEPAGE SEARCH — INTERACTIVE ENHANCEMENTS
========================================== */

/* Add a clear button without changing index.html. */
let clearSearchButton = null;

function initializeSearchEnhancements() {
    if (!locationSearch) return;

    locationSearch.setAttribute("aria-label", "Search monitoring categories and locations");
    locationSearch.setAttribute("aria-describedby", "searchMessage");

    if (searchMessage) {
        searchMessage.setAttribute("role", "status");
        searchMessage.setAttribute("aria-live", "polite");
    }

    if (homepageLocationResults) {
        homepageLocationResults.setAttribute("role", "list");
        homepageLocationResults.setAttribute("aria-label", "Matching locations");
    }

    clearSearchButton = document.createElement("button");
    clearSearchButton.type = "button";
    clearSearchButton.className = "clear-search-button";
    clearSearchButton.textContent = "Clear";
    clearSearchButton.setAttribute("aria-label", "Clear location search");
    clearSearchButton.hidden = true;

    locationSearch.insertAdjacentElement("afterend", clearSearchButton);

    clearSearchButton.addEventListener("click", function () {
        locationSearch.value = "";
        locationSearch.dispatchEvent(new Event("input", { bubbles: true }));
        locationSearch.focus();
    });

    locationSearch.addEventListener("input", function () {
        clearSearchButton.hidden = !locationSearch.value.trim();
    });
}

/* Safely highlight matching text without inserting HTML. */
function appendHighlightedText(container, text, query) {
    const normalizedText = String(text);
    const normalizedQuery = String(query || "").trim();

    if (!normalizedQuery) {
        container.textContent = normalizedText;
        return;
    }

    const lowerText = normalizedText.toLowerCase();
    const lowerQuery = normalizedQuery.toLowerCase();

    let currentIndex = 0;
    let matchIndex = lowerText.indexOf(lowerQuery);

    while (matchIndex !== -1) {
        if (matchIndex > currentIndex) {
            container.append(
                document.createTextNode(
                    normalizedText.slice(currentIndex, matchIndex)
                )
            );
        }

        const highlight = document.createElement("mark");
        highlight.className = "search-match";
        highlight.textContent = normalizedText.slice(
            matchIndex,
            matchIndex + normalizedQuery.length
        );

        container.append(highlight);

        currentIndex = matchIndex + normalizedQuery.length;
        matchIndex = lowerText.indexOf(lowerQuery, currentIndex);
    }

    if (currentIndex < normalizedText.length) {
        container.append(
            document.createTextNode(normalizedText.slice(currentIndex))
        );
    }
}

function renderHomepageLocationResults(results, query) {
    if (!homepageLocationResults) return;

    homepageLocationResults.replaceChildren();

    results.forEach(function (result) {
        const item = document.createElement("div");
        item.className = "homepage-location-result";
        item.setAttribute("role", "listitem");

        const details = document.createElement("div");
        details.className = "homepage-location-result-details";

        const name = document.createElement("h3");
        appendHighlightedText(name, result.location.name, query);

        const region = document.createElement("p");
        appendHighlightedText(region, result.location.region, query);

        const categoryLabel = document.createElement("span");
        categoryLabel.className = "search-result-category";
        categoryLabel.textContent = categoryInfo[result.category].title;

        const viewButton = document.createElement("button");
        viewButton.type = "button";
        viewButton.textContent = "View Analysis ↗";

        viewButton.addEventListener("click", function () {
            openLocationAnalysis(result.category, result.location);
        });

        details.append(name, region, categoryLabel);
        item.append(details, viewButton);
        homepageLocationResults.append(item);
    });

    homepageLocationResults.hidden = results.length === 0;
}

function searchHomepage(query) {
    const normalizedQuery = query.trim().toLowerCase();
    const matchingLocations = [];
    let matchingCategories = 0;

    if (!normalizedQuery) {
        categoryCards.forEach(function (card) {
            card.classList.remove("search-hidden");
        });

        if (homepageLocationResults) {
            homepageLocationResults.replaceChildren();
            homepageLocationResults.hidden = true;
        }

        if (searchMessage) {
            searchMessage.textContent = "";
            searchMessage.hidden = true;
        }

        return;
    }

    categoryCards.forEach(function (card) {
        const searchableText = (
            card.innerText + " " + (card.dataset.search || "")
        ).toLowerCase();

        const matches = searchableText.includes(normalizedQuery);

        card.classList.toggle("search-hidden", !matches);

        if (matches) matchingCategories++;
    });

    Object.entries(monitoringLocations).forEach(function ([category, locations]) {
        locations.forEach(function (location) {
            const searchableText = (
                location.name + " " +
                location.region + " " +
                category + " " +
                categoryInfo[category].title
            ).toLowerCase();

            if (searchableText.includes(normalizedQuery)) {
                matchingLocations.push({ category, location });
            }
        });
    });

    renderHomepageLocationResults(matchingLocations, query);

    if (!searchMessage) return;

    const parts = [];

    if (matchingCategories) {
        parts.push(
            matchingCategories + " categor" +
            (matchingCategories === 1 ? "y" : "ies")
        );
    }

    if (matchingLocations.length) {
        parts.push(
            matchingLocations.length + " location" +
            (matchingLocations.length === 1 ? "" : "s")
        );
    }

    if (parts.length === 0) {
        searchMessage.textContent =
            'No results for "' + query.trim() + '". Try a location such as Kolkata or Bankura.';
    } else {
        searchMessage.textContent = "Found " + parts.join(" and ") + ".";
    }

    searchMessage.hidden = false;
}

if (locationSearch) {
    locationSearch.addEventListener("input", function () {
        searchHomepage(locationSearch.value);
    });
}

initializeSearchEnhancements();

/* ==========================================
   OPEN CATEGORY PAGE
========================================== */

function openCategory(category) {
    const info = categoryInfo[category];

    if (!info || !categoryPage || !homepage) {
        console.error("Category page or category information is missing.");
        return;
    }

    hideAllMainViews();
    categoryPage.hidden = false;
    categoryPage.dataset.category = category;

    const title = document.querySelector("#categoryPageTitle");
    const description = document.querySelector("#categoryPageDescription");
    const eyebrow = document.querySelector("#categoryPageEyebrow");

    if (title) title.textContent = info.title;
    if (description) description.textContent = info.description;
    if (eyebrow) eyebrow.textContent = info.eyebrow;

    currentCategory = category;
    currentLocation = null;
    updateImagePairStatus();
    renderLocationList(category);

    window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ==========================================
   RENDER LOCATION LIST
========================================== */

function renderLocationList(category) {
    const list = document.querySelector("#locationList");
    const search = document.querySelector("#locationListSearch");
    const message = document.querySelector("#locationListMessage");

    if (!list || !message) return;

    const locations = monitoringLocations[category] || [];

    function displayLocations(query = "") {
        const filtered = locations.filter(function (location) {
            return (location.name + " " + location.region)
                .toLowerCase()
                .includes(query.toLowerCase());
        });

        list.replaceChildren();

        filtered.forEach(function (location) {
            const card = document.createElement("article");
            card.className = "location-card";

            const details = document.createElement("div");
            details.className = "location-card-details";

            const name = document.createElement("h3");
            appendHighlightedText(name, location.name, query);

            const region = document.createElement("p");
            region.textContent = location.region;

            const status = document.createElement("span");
            status.className = "location-data-status";
            status.textContent = "Analysis data not connected";

            const action = document.createElement("button");
            action.type = "button";
            action.className = "location-analysis-button";
            action.textContent = "View Analysis ↗";

            action.addEventListener("click", function () {
                openLocationAnalysis(category, location);
            });

            details.append(name, region, status);
            card.append(details, action);
            list.append(card);
        });

        message.textContent = filtered.length
            ? filtered.length + " location" +
                (filtered.length === 1 ? "" : "s") + " listed."
            : "No locations match your search.";
    }

    if (search) {
        search.value = "";
        search.oninput = function () {
            displayLocations(search.value.trim());
        };
    }

    displayLocations();
}

/* ==========================================
   OPEN LOCATION ANALYSIS
========================================== */

function openLocationAnalysis(category, location) {
    if (!categoryInfo[category] || !locationAnalysisPage || !location) {
        console.error("Location analysis page or location data is missing.");
        return;
    }

    currentCategory = category;
    currentLocation = location;
    updateImagePairStatus();

    const title = document.querySelector("#analysisLocationTitle");
    const region = document.querySelector("#analysisLocationRegion");
    const breadcrumbLocation = document.querySelector("#analysisBreadcrumbLocation");
    const categoryLabel = document.querySelector("#analysisCategoryLabel");
    const categoryLink = document.querySelector("#analysisCategoryLink");
    const dataStatus = document.querySelector("#analysisDataStatus");

    if (title) title.textContent = location.name;
    if (region) region.textContent = location.region;
    if (breadcrumbLocation) breadcrumbLocation.textContent = location.name;

    if (categoryLabel) {
        categoryLabel.textContent = categoryInfo[category].title.toUpperCase();
    }

    if (categoryLink) {
        categoryLink.textContent = categoryInfo[category].title;
    }

    if (dataStatus) dataStatus.textContent = "DATA NOT CONNECTED";

    updatePlaceGallery(
        location.images || getLocationImages(category, location.name)
    );

    const newsButton = document.querySelector("#analysisNewsButton");
    if (newsButton) {
        newsButton.dataset.location = location.name;
        newsButton.textContent = "Recent news for " + location.name + " →";
    }

    hideAllMainViews();
    locationAnalysisPage.hidden = false;

    window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ==========================================
   RETURN NAVIGATION
========================================== */

function returnToCategoryPage() {
    if (!currentCategory) {
        returnToHomepage();
        return;
    }

    hideAllMainViews();

    if (categoryPage) categoryPage.hidden = false;

    window.scrollTo({ top: 0, behavior: "smooth" });
}

if (backToLocations) {
    backToLocations.addEventListener("click", returnToCategoryPage);
}

if (analysisCategoryLink) {
    analysisCategoryLink.addEventListener("click", function (event) {
        event.preventDefault();
        returnToCategoryPage();
    });
}

if (analysisHomeLink) {
    analysisHomeLink.addEventListener("click", function (event) {
        event.preventDefault();
        returnToHomepage();
    });
}

categoryButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        openCategory(button.dataset.openCategory);
    });
});

if (backToHome) {
    backToHome.addEventListener("click", function (event) {
        event.preventDefault();
        returnToHomepage();
    });
}

/* ==========================================
   INITIALIZE
========================================== */

initializeMap();


/* ==========================================
   IMAGE ANALYSIS API
========================================== */

const imageAnalysisForm = document.querySelector("#imageAnalysisForm");
const submitAnalysisImage = document.querySelector("#submitAnalysisImage");
const imageAnalysisStatus = document.querySelector("#imageAnalysisStatus");
const integrationBadge = document.querySelector(".integration-badge");
const integrationNote = document.querySelector(".integration-note");
const analysisHistoryList = document.querySelector("#analysisHistoryList");
const analysisCategoryInputs = document.querySelectorAll('input[name="analysisCategory"]');
let selectedAnalysisCategory = "";
let analysisSubmissionInProgress = false;
const apiBaseUrl = (
    window.GEOLENS_API && typeof window.GEOLENS_API.BASE_URL === "string"
        ? window.GEOLENS_API.BASE_URL
        : ""
).replace(/\/+$/, "");
const localFrontendHosts = ["", "localhost", "127.0.0.1", "::1"];
const isLocalFrontend = localFrontendHosts.includes(window.location.hostname);

const imageSlots = {
    one: {
        input: document.querySelector("#analysisImageInputOne"),
        panel: document.querySelector("#imagePreviewPanelOne"),
        preview: document.querySelector("#analysisImagePreviewOne"),
        name: document.querySelector("#analysisImageNameOne"),
        size: document.querySelector("#analysisImageSizeOne"),
        file: null,
        objectUrl: null,
        previewRequestId: 0
    },
    two: {
        input: document.querySelector("#analysisImageInputTwo"),
        panel: document.querySelector("#imagePreviewPanelTwo"),
        preview: document.querySelector("#analysisImagePreviewTwo"),
        name: document.querySelector("#analysisImageNameTwo"),
        size: document.querySelector("#analysisImageSizeTwo"),
        file: null,
        objectUrl: null,
        previewRequestId: 0
    }
};

let tiffPreviewLibraryPromise;

function loadTiffPreviewLibrary() {
    if (window.GeoTIFF && typeof window.GeoTIFF.fromBlob === "function") {
        return Promise.resolve(window.GeoTIFF);
    }

    if (!tiffPreviewLibraryPromise) {
        tiffPreviewLibraryPromise = new Promise(function (resolve, reject) {
            const script = document.createElement("script");
            script.src = "https://cdn.jsdelivr.net/npm/geotiff@2.1.3/dist-browser/geotiff.js";
            script.async = true;
            script.onload = function () {
                if (window.GeoTIFF && typeof window.GeoTIFF.fromBlob === "function") {
                    resolve(window.GeoTIFF);
                } else {
                    tiffPreviewLibraryPromise = null;
                    reject(new Error("The TIFF preview library did not load correctly."));
                }
            };
            script.onerror = function () {
                tiffPreviewLibraryPromise = null;
                reject(new Error("The TIFF preview library could not be loaded."));
            };
            document.head.append(script);
        });
    }

    return tiffPreviewLibraryPromise;
}

function percentileRange(values, pixelCount, sampleCount, sampleIndex) {
    const sampleStride = Math.max(1, Math.floor(pixelCount / 4096));
    const samples = [];
    for (let pixel = 0; pixel < pixelCount; pixel += sampleStride) {
        const value = Number(values[pixel * sampleCount + sampleIndex]);
        if (Number.isFinite(value)) samples.push(value);
    }
    if (!samples.length) return null;

    samples.sort(function (left, right) {
        return left - right;
    });
    return {
        low: samples[Math.floor((samples.length - 1) * 0.02)],
        high: samples[Math.floor((samples.length - 1) * 0.98)]
    };
}

async function createTiffPreview(file) {
    const GeoTIFF = await loadTiffPreviewLibrary();
    const tiff = await GeoTIFF.fromBlob(file);
    const image = await tiff.getImage();
    const width = image.getWidth();
    const height = image.getHeight();
    const scale = Math.min(1, 512 / Math.max(width, height));
    const previewWidth = Math.max(1, Math.round(width * scale));
    const previewHeight = Math.max(1, Math.round(height * scale));
    const sampleCount = Math.max(1, Math.min(image.getSamplesPerPixel() || 1, 3));
    const samples = Array.from({ length: sampleCount }, function (_value, index) {
        return index;
    });
    const raster = await image.readRasters({
        samples: samples,
        interleave: true,
        width: previewWidth,
        height: previewHeight
    });
    const pixelCount = previewWidth * previewHeight;
    const ranges = samples.map(function (sampleIndex) {
        return percentileRange(raster, pixelCount, sampleCount, sampleIndex);
    });
    const canvas = document.createElement("canvas");
    canvas.width = previewWidth;
    canvas.height = previewHeight;
    const context = canvas.getContext("2d");
    if (!context) throw new Error("A canvas is unavailable for TIFF preview rendering.");

    const imageData = context.createImageData(previewWidth, previewHeight);
    for (let pixel = 0; pixel < pixelCount; pixel += 1) {
        for (let channel = 0; channel < 3; channel += 1) {
            const band = sampleCount === 1 ? 0 : Math.min(channel, sampleCount - 1);
            const value = Number(raster[pixel * sampleCount + band]);
            const range = ranges[band];
            const scaled = !Number.isFinite(value) || !range
                ? 0
                : range.high <= range.low
                    ? 127
                    : Math.round(Math.max(0, Math.min(1,
                        (value - range.low) / (range.high - range.low)
                    )) * 255);
            imageData.data[pixel * 4 + channel] = scaled;
        }
        imageData.data[pixel * 4 + 3] = 255;
    }
    context.putImageData(imageData, 0, 0);

    return new Promise(function (resolve, reject) {
        canvas.toBlob(function (blob) {
            if (blob) {
                resolve(blob);
            } else {
                reject(new Error("The TIFF preview could not be converted to PNG."));
            }
        }, "image/png");
    });
}

async function apiRequest(path, options) {
    if (!apiBaseUrl && !isLocalFrontend) {
        throw new Error("Production API URL is not configured. Set the Render URL in frontend/api-config.js.");
    }

    if (apiBaseUrl) {
        let configuredUrl;
        try {
            configuredUrl = new URL(apiBaseUrl);
        } catch (error) {
            throw new Error("The configured backend URL is invalid.");
        }
        if (!["http:", "https:"].includes(configuredUrl.protocol)) {
            throw new Error("The backend URL must use HTTP or HTTPS.");
        }
        if (configuredUrl.protocol !== "https:" && window.location.protocol === "https:") {
            throw new Error("The deployed frontend requires an HTTPS backend URL.");
        }
        if (!isLocalFrontend && localFrontendHosts.includes(configuredUrl.hostname)) {
            throw new Error("A production frontend cannot use a localhost backend URL.");
        }
    }

    let response;
    try {
        response = await fetch(apiBaseUrl + path, options);
    } catch (error) {
        throw new Error("Could not reach the analysis service. Check the backend URL and network connection.");
    }

    let payload;
    try {
        payload = await response.json();
    } catch (error) {
        throw new Error("The backend returned an invalid response. Check its URL and deployment logs.");
    }

    if (!response.ok) {
        throw new Error(payload.message || payload.error || "Request failed with HTTP " + response.status + ".");
    }
    return payload;
}

function refreshHistory() {
    return apiRequest("/api/history")
        .then(function (payload) {
            const records = Array.isArray(payload.records) ? payload.records : [];
            if (!analysisHistoryList || !records.length) return;

            const heading = document.createElement("h3");
            heading.textContent = "Recent analyses";
            const list = document.createElement("ol");
            list.className = "analysis-history-items";

            records.forEach(function (record) {
                const item = document.createElement("li");
                const result = document.createElement("strong");
                result.textContent = (record.hazard || "Analysis") + ": " +
                    (record.prediction || "Result unavailable");
                const details = document.createElement("p");
                const timestamp = new Date(record.timestamp);
                const date = record.timestamp && !Number.isNaN(timestamp.getTime())
                    ? timestamp.toLocaleString()
                    : "Date unavailable";
                details.textContent = (record.location ? record.location + " · " : "") + date;
                item.append(result, details);
                list.append(item);
            });

            analysisHistoryList.replaceChildren(heading, list);
        })
        .catch(function (error) {
            console.error("Could not load analysis history:", error);
            if (analysisHistoryList) {
                const message = document.createElement("p");
                message.textContent = error.message;
                analysisHistoryList.replaceChildren(message);
            }
        });
}

function checkBackendStatus() {
    return apiRequest("/api/health")
        .then(function (payload) {
            const databaseConfigured = payload.database && payload.database.configured;
            const databaseUnavailable = databaseConfigured && !payload.database.available;
            const modelAvailable = payload.model && payload.model.available;
            if (integrationBadge) {
                integrationBadge.textContent = databaseUnavailable
                    ? "DATABASE UNAVAILABLE"
                    : !databaseConfigured
                        ? "AIVEN DATABASE NOT CONFIGURED"
                        : modelAvailable
                            ? "ANALYSIS SERVICE CONNECTED"
                            : "MODEL CHECKPOINT MISSING";
            }
            if (integrationNote) {
                integrationNote.textContent = databaseUnavailable
                    ? "The backend is reachable, but Aiven database connectivity is unavailable."
                    : !databaseConfigured
                        ? "The backend is reachable, but Aiven is not configured. Local history is stored in a JSON file."
                    : payload.message ||
                        "The backend is reachable, but its model status could not be confirmed.";
            }
        })
        .catch(function (error) {
            if (integrationBadge) integrationBadge.textContent = "ANALYSIS SERVICE UNAVAILABLE";
            if (integrationNote) integrationNote.textContent = error.message;
        });
}

function updateImagePairStatus() {
    const firstSelected = Boolean(imageSlots.one.file);
    const secondSelected = Boolean(imageSlots.two.file);
    const categorySelected = Boolean(selectedAnalysisCategory);
    if (submitAnalysisImage) {
        submitAnalysisImage.disabled =
            !firstSelected || !secondSelected || !categorySelected || analysisSubmissionInProgress;
    }

    if (!imageAnalysisStatus) return;
    if (!firstSelected) {
        imageAnalysisStatus.textContent = "Select the first image before submitting.";
    } else if (!secondSelected) {
        imageAnalysisStatus.textContent = "Select the second image before submitting.";
    } else if (!categorySelected) {
        imageAnalysisStatus.textContent =
            "Choose a Flood, Drought, or Vegetation monitoring category before submitting.";
    } else {
        imageAnalysisStatus.textContent =
            "Both images are ready for " + selectedAnalysisCategory + " monitoring.";
    }
}

function clearImageSlot(key) {
    const slot = imageSlots[key];
    if (!slot) return;

    slot.previewRequestId += 1;
    if (slot.objectUrl) URL.revokeObjectURL(slot.objectUrl);
    slot.objectUrl = null;
    slot.file = null;
    slot.input.value = "";
    slot.preview.removeAttribute("src");
    slot.preview.hidden = false;
    slot.panel.hidden = true;
    slot.name.textContent = "";
    slot.size.textContent = "";
    updateImagePairStatus();
}

Object.keys(imageSlots).forEach(function (key) {
    const slot = imageSlots[key];
    slot.input.accept = ".tif,.tiff,.png,.jpg,.jpeg,.bmp,.webp";
    slot.input.addEventListener("change", async function () {
        const file = slot.input.files && slot.input.files[0];
        const previewRequestId = ++slot.previewRequestId;
        if (slot.objectUrl) URL.revokeObjectURL(slot.objectUrl);
        slot.objectUrl = null;
        slot.file = null;
        slot.preview.removeAttribute("src");
        slot.preview.hidden = false;
        slot.panel.hidden = true;

        if (!file) {
            updateImagePairStatus();
            return;
        }

        const extension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
        const supportedExtensions = [
            ".tif",
            ".tiff",
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".webp"
        ];
        if (!supportedExtensions.includes(extension)) {
            slot.input.value = "";
            imageAnalysisStatus.textContent = "Choose a supported image file for both image slots.";
            updateImagePairStatus();
            return;
        }

        if (file.size > 50 * 1024 * 1024) {
            slot.input.value = "";
            imageAnalysisStatus.textContent = "Each image must be 50 MB or smaller.";
            updateImagePairStatus();
            return;
        }

        slot.file = file;
        slot.name.textContent = file.name;
        slot.size.textContent = (file.size / (1024 * 1024)).toFixed(2) + " MB";
        slot.panel.hidden = false;
        updateImagePairStatus();

        const selectedExtension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
        if (selectedExtension === ".tif" || selectedExtension === ".tiff") {
            imageAnalysisStatus.textContent = "Generating a browser preview for the TIFF…";
            try {
                const preview = await createTiffPreview(file);
                if (slot.previewRequestId !== previewRequestId || slot.file !== file) return;
                slot.objectUrl = URL.createObjectURL(preview);
                slot.preview.src = slot.objectUrl;
                updateImagePairStatus();
            } catch (error) {
                if (slot.previewRequestId !== previewRequestId || slot.file !== file) return;
                console.warn("Could not generate TIFF preview:", error);
                slot.preview.hidden = true;
                imageAnalysisStatus.textContent =
                    "The TIFF preview is unavailable, but the original file can still be submitted.";
            }
            return;
        }

        slot.objectUrl = URL.createObjectURL(file);
        slot.preview.src = slot.objectUrl;
    });
});

document.querySelectorAll("[data-clear-image]").forEach(function (button) {
    button.addEventListener("click", function () {
        clearImageSlot(button.dataset.clearImage);
    });
});

analysisCategoryInputs.forEach(function (input) {
    input.addEventListener("change", function () {
        if (input.checked) selectedAnalysisCategory = input.value;
        updateImagePairStatus();
    });
});

if (imageAnalysisForm) {
    imageAnalysisForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        if (!imageSlots.one.file) {
            imageAnalysisStatus.textContent = "Select the first image before submitting.";
            return;
        }
        if (!imageSlots.two.file) {
            imageAnalysisStatus.textContent = "Select the second image before submitting.";
            return;
        }
        if (!selectedAnalysisCategory) {
            imageAnalysisStatus.textContent =
                "Choose a Flood, Drought, or Vegetation monitoring category before submitting.";
            return;
        }

        const formData = new FormData();
        formData.append("historical", imageSlots.one.file);
        formData.append("recent", imageSlots.two.file);
        formData.append("hazard", selectedAnalysisCategory);
        if (currentLocation) formData.append("location", currentLocation.name);

        analysisSubmissionInProgress = true;
        submitAnalysisImage.disabled = true;
        imageAnalysisStatus.textContent = "Uploading the image pair and running the model…";
        try {
            const result = await apiRequest("/api/analyze", {
                method: "POST",
                body: formData
            });
            const confidence = typeof result.confidence === "number"
                ? " (" + (result.confidence * 100).toFixed(1) + "% class confidence)"
                : "";
            const summary = result.message ||
                "Prediction: " + (result.predicted_class || result.prediction || "complete") + confidence;
            imageAnalysisStatus.textContent =
                summary + (!result.message && result.change_index != null
                    ? " Change index: " + Number(result.change_index).toFixed(2) + "."
                    : "");
            await refreshHistory();
        } catch (error) {
            imageAnalysisStatus.textContent = error.message;
        } finally {
            analysisSubmissionInProgress = false;
            submitAnalysisImage.disabled =
                !imageSlots.one.file || !imageSlots.two.file || !selectedAnalysisCategory;
        }
    });
}

updateImagePairStatus();
checkBackendStatus();
refreshHistory();



/* ========================================
   FIX: GEOLENS SCROLL & NAVIGATION
======================================== */

(() => {
    function initGeoLensScrollEffects() {
        const homepage = document.querySelector("#home");
        const navLinks = document.querySelectorAll(
            ".home-nav .home-nav-link"
        );

        if (!homepage || !navLinks.length) return;

        /* Subtle section reveal animation */
        const revealTargets = homepage.querySelectorAll(
            ".hero-section, .platform-overview, #monitoring, .shared-quick-guide, #imageAnalysis, #recentNews, #history, #about"
        );

        const reducedMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        if (reducedMotion || !("IntersectionObserver" in window)) {
            revealTargets.forEach((section) => {
                section.classList.add("is-visible");
            });
        } else {
            const revealObserver = new IntersectionObserver(
                (entries, observer) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add("is-visible");
                            observer.unobserve(entry.target);
                        }
                    });
                },
                {
                    threshold: 0.05,
                    rootMargin: "0px 0px -30px 0px"
                }
            );

            revealTargets.forEach((section) => {
                section.classList.add("scroll-reveal");
                revealObserver.observe(section);
            });
        }

        
function updateActiveNavigation() {
    if (homepage.hidden) return;

    const scrollPosition = window.scrollY;
    const activationLine = window.innerHeight * 0.35;
    const sectionIds = ["monitoring", "imageAnalysis", "recentNews", "history", "about"];

    const pageBottom =
        window.scrollY + window.innerHeight >=
        document.documentElement.scrollHeight - 5;

    let activeId = pageBottom ? "about" : "home";
    sectionIds.forEach((sectionId) => {
        const section = document.getElementById(sectionId);
        if (!section) return;
        const sectionTop = section.getBoundingClientRect().top + scrollPosition;
        if (scrollPosition + activationLine >= sectionTop) activeId = sectionId;
    });
    if (pageBottom) activeId = "about";

    navLinks.forEach((link) => {
        const isActive = link.getAttribute("href") === "#" + activeId;

        link.classList.toggle("active", isActive);

        if (isActive) {
            link.setAttribute("aria-current", "location");
        } else {
            link.removeAttribute("aria-current");
        }
    });
}

        window.addEventListener(
            "scroll",
            updateActiveNavigation,
            { passive: true }
        );

        window.addEventListener("resize", updateActiveNavigation);

        navLinks.forEach((link) => {
            link.addEventListener("click", () => {
                window.setTimeout(updateActiveNavigation, 300);
            });
        });

        updateActiveNavigation();
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initGeoLensScrollEffects,
            { once: true }
        );
    } else {
        initGeoLensScrollEffects();
    }
})();



/* =========================================
   GEO LENS — INTERACTIVE LOCATION MAP
========================================= */

(function initializeLocationExplorer() {
    const mapElement = document.getElementById("locationMap");

    if (!mapElement) return;

    const statusMessage = document.getElementById("locationMapMessage");
    const filterButtons = document.querySelectorAll("[data-map-filter]");

    if (typeof L === "undefined") {
        if (statusMessage) {
            statusMessage.textContent =
                "Map library unavailable. Check your internet connection.";
        }
        return;
    }

    const categoryColors = {
        flood: "#628ca1",
        drought: "#b39a67",
        vegetation: "#668b6a"
    };

    // One marker per unique location.
    // Some locations belong to more than one monitoring category.
    const mapLocations = [
        {
            name: "Kolkata",
            region: "South Bengal",
            coordinates: [22.5726, 88.3639],
            categories: ["flood"]
        },
        {
            name: "Sundarbans",
            region: "South Bengal",
            coordinates: [21.9497, 88.8958],
            categories: ["flood", "vegetation"]
        },
        {
            name: "Malda",
            region: "North Bengal",
            coordinates: [25.0108, 88.1411],
            categories: ["flood"]
        },
        {
            name: "Murshidabad",
            region: "South Bengal",
            coordinates: [24.1759, 88.2802],
            categories: ["flood"]
        },
        {
            name: "Howrah",
            region: "South Bengal",
            coordinates: [22.5958, 88.2636],
            categories: ["flood"]
        },
        {
            name: "Bankura",
            region: "South Bengal",
            coordinates: [23.2324, 87.0784],
            categories: ["drought"]
        },
        {
            name: "Purulia",
            region: "South Bengal",
            coordinates: [23.3322, 86.3652],
            categories: ["drought", "vegetation"]
        },
        {
            name: "Jhargram",
            region: "South Bengal",
            coordinates: [22.4530, 86.9977],
            categories: ["drought"]
        },
        {
            name: "Birbhum",
            region: "South Bengal",
            coordinates: [23.9080, 87.5270],
            categories: ["drought"]
        },
        {
            name: "Paschim Medinipur",
            region: "South Bengal",
            coordinates: [22.4257, 87.3199],
            categories: ["drought"]
        },
        {
            name: "Dooars",
            region: "North Bengal",
            coordinates: [26.8500, 88.8500],
            categories: ["vegetation"]
        },
        {
            name: "Darjeeling",
            region: "North Bengal",
            coordinates: [27.0360, 88.2627],
            categories: ["vegetation"]
        },
        {
            name: "Jalpaiguri",
            region: "North Bengal",
            coordinates: [26.5167, 88.7333],
            categories: ["vegetation"]
        }
    ];

    let activeFilter = "all";
    const markerRecords = [];

    const map = L.map("locationMap", {
        scrollWheelZoom: false,
        zoomControl: true
    });

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);

    const westBengalBounds = L.latLngBounds(
        [21.4, 85.7],
        [27.5, 89.9]
    );

    map.fitBounds(westBengalBounds, {
        padding: [18, 18]
    });

    function getMarkerColor(location) {
        const category =
            activeFilter !== "all" &&
            location.categories.includes(activeFilter)
                ? activeFilter
                : location.categories[0];

        return categoryColors[category];
    }

    function getPopupCategory(location) {
        if (
            activeFilter !== "all" &&
            location.categories.includes(activeFilter)
        ) {
            return activeFilter;
        }

        return location.categories[0];
    }

    function createPopupContent(location) {
        const categories = location.categories
            .map(category =>
                category.charAt(0).toUpperCase() + category.slice(1)
            )
            .join(" · ");

        return `
            <div class="map-popup-content">
                <strong>${location.name}</strong>
                <div>${location.region}</div>
                <div class="map-popup-categories">${categories}</div>
                <button
                    type="button"
                    class="map-popup-open"
                    data-map-location="${location.name}"
                    data-map-category="${getPopupCategory(location)}"
                >
                    Explore location →
                </button>
            </div>
        `;
    }

    mapLocations.forEach(location => {
        const marker = L.circleMarker(location.coordinates, {
            radius: 7,
            color: "#ffffff",
            weight: 2,
            fillColor: getMarkerColor(location),
            fillOpacity: 0.95
        });

        marker.bindPopup(createPopupContent(location), {
            maxWidth: 220
        });

        marker.addTo(map);

        markerRecords.push({
            location,
            marker
        });
    });

    function applyMapFilter(filter) {
        activeFilter = filter;

        filterButtons.forEach(button => {
            const isActive = button.dataset.mapFilter === filter;

            button.classList.toggle("active", isActive);
            button.setAttribute("aria-pressed", String(isActive));
        });

        const visibleLocations = [];

        markerRecords.forEach(({ location, marker }) => {
            const isVisible =
                filter === "all" ||
                location.categories.includes(filter);

            if (isVisible) {
                if (!map.hasLayer(marker)) {
                    marker.addTo(map);
                }

                marker.setStyle({
                    fillColor: getMarkerColor(location),
                    opacity: 1,
                    fillOpacity: 0.95
                });

                marker.setPopupContent(createPopupContent(location));
                visibleLocations.push(location);
            } else {
                if (map.hasLayer(marker)) {
                    map.removeLayer(marker);
                }
            }
        });

        if (visibleLocations.length === 1) {
            map.setView(visibleLocations[0].coordinates, 8);
        } else if (filter === "all") {
            map.fitBounds(westBengalBounds, {
                padding: [18, 18]
            });
        } else if (visibleLocations.length > 1) {
            const filteredBounds = L.latLngBounds(
                visibleLocations.map(location => location.coordinates)
            );

            map.fitBounds(filteredBounds, {
                padding: [24, 24],
                maxZoom: 8
            });
        }
    }

    filterButtons.forEach(button => {
        button.addEventListener("click", () => {
            applyMapFilter(button.dataset.mapFilter);
        });
    });

    // Open a location in the existing analysis view when supported.
    map.on("popupopen", event => {
        const popupElement = event.popup.getElement();

        if (!popupElement) return;

        const exploreButton = popupElement.querySelector(
            "[data-map-location]"
        );

        if (!exploreButton) return;

        exploreButton.addEventListener("click", () => {
            const locationName = exploreButton.dataset.mapLocation;
            const category = exploreButton.dataset.mapCategory;

            const location = mapLocations.find(
                item => item.name === locationName
            );

            if (!location) return;

            if (typeof openLocationAnalysis === "function") {
                openLocationAnalysis(category, {
                    name: location.name,
                    region: location.region
                });
            } else {
                // Keep the map usable even if the analysis function
                // has a different name in the existing project.
                console.info(
                    "Location selected:",
                    location.name,
                    "Category:",
                    category
                );
            }
        });
    });

    if (statusMessage) {
        statusMessage.hidden = true;
    }

    // Correct Leaflet sizing after the page layout is painted.
    requestAnimationFrame(() => {
        map.invalidateSize();
    });

    // Allow the map to respond to viewport changes.
    window.addEventListener("resize", () => {
        map.invalidateSize();
    });
})();


/* =========================================
   GEO LENS — RECENT NEWS BY LOCATION
   Reads GEOLENS_NEWS from news-data.js.
   Window: last 1 month → last 3 months →
   latest older items (clearly labelled).
========================================= */

(function initializeLocationNews() {
    const select = document.getElementById("newsLocationSelect");
    const list = document.getElementById("newsList");
    const windowLabel = document.getElementById("newsWindowLabel");
    const curatedLabel = document.getElementById("newsCuratedLabel");
    const topicButtons = document.querySelectorAll("[data-news-topic]");

    if (!select || !list) return;

    const newsData = (typeof GEOLENS_NEWS !== "undefined" && GEOLENS_NEWS) || { items: [] };
    const items = Array.isArray(newsData.items) ? newsData.items : [];

    const NORTH_BENGAL = ["Malda", "Dooars", "Darjeeling", "Jalpaiguri"];
    const TOPIC_LABELS = { flood: "Flood", drought: "Drought", vegetation: "Vegetation" };
    const DAY = 24 * 60 * 60 * 1000;

    let activeTopic = "all";

    /* ----- Build the location list from the monitoring data ----- */
    const locationCategories = {};

    Object.entries(monitoringLocations).forEach(([category, locations]) => {
        locations.forEach(location => {
            if (!locationCategories[location.name]) locationCategories[location.name] = [];
            if (!locationCategories[location.name].includes(category)) {
                locationCategories[location.name].push(category);
            }
        });
    });

    const names = Object.keys(locationCategories).sort((a, b) => a.localeCompare(b));
    const groups = {
        "South Bengal": names.filter(name => !NORTH_BENGAL.includes(name)),
        "North Bengal": names.filter(name => NORTH_BENGAL.includes(name))
    };

    Object.entries(groups).forEach(([groupName, groupNames]) => {
        const optgroup = document.createElement("optgroup");
        optgroup.label = groupName;

        groupNames.forEach(name => {
            const option = document.createElement("option");
            option.value = name;
            option.textContent = name;
            optgroup.appendChild(option);
        });

        select.appendChild(optgroup);
    });

    let initial = "Kolkata";
    try {
        const saved = localStorage.getItem("geolens-news-location");
        if (saved && locationCategories[saved]) initial = saved;
    } catch (error) {
        // Storage unavailable; keep default.
    }
    select.value = initial;

    if (curatedLabel && newsData.lastCurated) {
        curatedLabel.textContent = "Last updated " + formatDate(newsData.lastCurated);
    }

    /* ----- Helpers ----- */
    function parseDate(value) {
        const parts = String(value).split("-").map(Number);
        return new Date(parts[0], (parts[1] || 1) - 1, parts[2] || 1);
    }

    function formatDate(value) {
        return parseDate(value).toLocaleDateString("en-IN", {
            day: "numeric",
            month: "short",
            year: "numeric"
        });
    }

    function ageInDays(value) {
        const today = new Date();
        const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        return Math.round((startOfToday - parseDate(value)) / DAY);
    }

    function relativeAge(days) {
        if (days <= 0) return "Today";
        if (days === 1) return "Yesterday";
        if (days < 30) return days + " days ago";
        const months = Math.floor(days / 30);
        return months === 1 ? "1 month ago" : months + " months ago";
    }

    function safeUrl(value) {
        try {
            const url = new URL(value);
            return ["http:", "https:"].includes(url.protocol) ? url.href : null;
        } catch (error) {
            return null;
        }
    }

    /* ----- Selection logic ----- */
    function itemsForLocation(locationName) {
        return items
            .filter(item => Array.isArray(item.locations) && item.locations.includes(locationName))
            .map(item => Object.assign({}, item, { age: ageInDays(item.date) }))
            .filter(item => item.age >= 0)
            .sort((a, b) => a.age - b.age);
    }

    function pickWindow(list) {
        const lastMonth = list.filter(item => item.age <= 31);
        if (lastMonth.length) return { mode: "month", items: lastMonth };

        const lastThree = list.filter(item => item.age <= 92);
        if (lastThree.length) return { mode: "quarter", items: lastThree };

        if (list.length) return { mode: "older", items: list.slice(0, 3) };

        return { mode: "none", items: [] };
    }

    function selectNews(locationName, topic) {
        const all = itemsForLocation(locationName);
        const filtered = topic === "all"
            ? all
            : all.filter(item => (item.topics || []).includes(topic));
        return pickWindow(filtered);
    }

    function updateCounts(locationName) {
        const all = itemsForLocation(locationName);
        ["all", "flood", "drought", "vegetation"].forEach(topic => {
            const pool = topic === "all"
                ? all
                : all.filter(item => (item.topics || []).includes(topic));
            const count = pickWindow(pool).items.length;
            const badge = document.querySelector('[data-news-count="' + topic + '"]');
            if (badge) badge.textContent = String(count);
            const button = document.querySelector('[data-news-topic="' + topic + '"]');
            if (button) button.classList.toggle("is-empty", count === 0);
        });
    }

    /* ----- Rendering ----- */
    function topicTags(item) {
        const wrap = document.createElement("div");
        wrap.className = "news-tags";
        (item.topics || []).forEach(topic => {
            const tag = document.createElement("span");
            tag.className = "news-topic-tag news-topic-" + topic;
            tag.textContent = TOPIC_LABELS[topic] || topic;
            wrap.appendChild(tag);
        });
        return wrap;
    }

    function headline(item, level) {
        const heading = document.createElement(level);
        const href = safeUrl(item.url);
        if (href) {
            const link = document.createElement("a");
            link.href = href;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            link.textContent = item.title;
            heading.appendChild(link);
        } else {
            heading.textContent = item.title;
        }
        return heading;
    }

    function renderLead(item) {
        const lead = document.createElement("article");
        const mainTopic = (item.topics || [])[0] || "flood";
        lead.className = "news-lead news-accent-" + mainTopic;

        const top = document.createElement("div");
        top.className = "news-lead-top";
        const kicker = document.createElement("span");
        kicker.className = "news-kicker";
        kicker.textContent = "Latest";
        top.append(kicker, topicTags(item));

        const summary = document.createElement("p");
        summary.className = "news-lead-summary";
        summary.textContent = item.summary || "";

        const foot = document.createElement("div");
        foot.className = "news-lead-foot";
        const source = document.createElement("span");
        source.className = "news-source";
        source.textContent = item.source || "";
        const date = document.createElement("time");
        date.dateTime = item.date;
        date.textContent = formatDate(item.date) + " · " + relativeAge(item.age);
        foot.append(source, date);

        const cta = document.createElement("span");
        cta.className = "news-read-more";
        cta.setAttribute("aria-hidden", "true");
        cta.textContent = "Read the full story ↗";

        lead.append(top, headline(item, "h3"), summary, foot, cta);
        return lead;
    }

    function renderTimelineItem(item) {
        const li = document.createElement("li");
        const mainTopic = (item.topics || [])[0] || "flood";
        li.className = "news-timeline-item news-accent-" + mainTopic;

        const when = document.createElement("time");
        when.className = "news-timeline-date";
        when.dateTime = item.date;
        const d = parseDate(item.date);
        when.innerHTML =
            "<strong>" + d.getDate() + "</strong>" +
            d.toLocaleDateString("en-IN", { month: "short" });

        const body = document.createElement("div");
        body.className = "news-timeline-body";

        const meta = document.createElement("div");
        meta.className = "news-timeline-meta";
        const source = document.createElement("span");
        source.className = "news-source";
        source.textContent = (item.source || "") + " · " + relativeAge(item.age);
        meta.append(topicTags(item), source);

        const summary = document.createElement("p");
        summary.textContent = item.summary || "";

        body.append(headline(item, "h4"), summary, meta);
        li.append(when, body);
        return li;
    }

    function render() {
        const locationName = select.value;
        const result = selectNews(locationName, activeTopic);
        const topicText = activeTopic === "all" ? "" : " " + TOPIC_LABELS[activeTopic].toLowerCase();
        const count = result.items.length;
        const plural = count === 1 ? "y" : "ies";

        updateCounts(locationName);

        list.textContent = "";
        list.dataset.mode = result.mode;

        if (windowLabel) {
            const messages = {
                month: count + topicText + " stor" + plural + " from the last month",
                quarter: "Quiet month — showing " + count + topicText + " stor" + plural + " from the last 3 months",
                older: "Nothing" + topicText + " in the last 3 months — showing the most recent older coverage",
                none: "No" + topicText + " news collected for " + locationName + " yet"
            };
            windowLabel.textContent = messages[result.mode];
            windowLabel.dataset.mode = result.mode;
        }

        if (result.mode === "none") {
            const empty = document.createElement("div");
            empty.className = "news-empty";
            empty.innerHTML =
                '<span class="news-empty-mark" aria-hidden="true">◌</span>' +
                "<h3>No headlines here yet</h3>" +
                "<p>Try another topic, or pick a different location above.</p>";
            list.appendChild(empty);
            return;
        }

        const [first, ...rest] = result.items;
        list.appendChild(renderLead(first));

        if (rest.length) {
            const side = document.createElement("div");
            side.className = "news-timeline-wrap";
            const heading = document.createElement("h3");
            heading.className = "news-timeline-heading";
            heading.textContent = "Earlier";
            const timeline = document.createElement("ol");
            timeline.className = "news-timeline";
            rest.forEach(item => timeline.appendChild(renderTimelineItem(item)));
            side.append(heading, timeline);
            list.appendChild(side);
        } else {
            list.classList.add("is-single");
        }
        if (rest.length) list.classList.remove("is-single");
    }

    /* ----- Events ----- */
    select.addEventListener("change", () => {
        try {
            localStorage.setItem("geolens-news-location", select.value);
        } catch (error) {
            // Ignore storage errors.
        }
        render();
    });

    topicButtons.forEach(button => {
        button.addEventListener("click", () => {
            activeTopic = button.dataset.newsTopic;
            topicButtons.forEach(other => {
                const isActive = other === button;
                other.classList.toggle("active", isActive);
                other.setAttribute("aria-pressed", String(isActive));
            });
            render();
        });
    });

    /* Let other parts of the page jump to a location's news. */
    window.showNewsForLocation = function (locationName) {
        if (!locationCategories[locationName]) return;
        select.value = locationName;
        select.dispatchEvent(new Event("change"));
        if (typeof showHomepageSection === "function") {
            showHomepageSection("recentNews");
        }
    };

    render();
})();

/* Location page → its news */
(function () {
    const button = document.getElementById("analysisNewsButton");
    if (!button) return;
    button.addEventListener("click", () => {
        if (typeof window.showNewsForLocation === "function" && button.dataset.location) {
            window.showNewsForLocation(button.dataset.location);
        }
    });
})();
