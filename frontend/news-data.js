/* ==========================================
   GEO LENS — CURATED LOCATION NEWS
   ------------------------------------------
   Hand-curated headlines for each monitored location.
   Last curated: 14 November 2026.

   HOW TO UPDATE
   Add an object to GEOLENS_NEWS.items with:
     title      Headline (short)
     source     Publisher name
     date       Publication date, "YYYY-MM-DD"
     url        Link to the original article
     summary    One or two sentences, in your own words
     topics     Any of: "flood", "drought", "vegetation"
     locations  Location names exactly as used on the map

   The Recent News tab shows the last 1 month for the selected
   location; if nothing is found it widens to 3 months; if there
   is still nothing it shows the latest older items, labelled as
   older. When the backend is ready, replace this file with an API
   response in the same shape.
========================================== */

const GEOLENS_NEWS = {
    lastCurated: "2026-11-14",

    items: [
        /* ---------- Cyclone Arnab (late October 2026) ---------- */
        {
            title: "Cyclone Arnab triggers rain in Bengal, alerts issued for more districts",
            source: "UNI India",
            date: "2026-10-28",
            url: "https://www.uniindia.com/east-india/cyclone-wb-arnab-weather-alert/228502",
            summary: "The cyclone came ashore in Andhra Pradesh, but its outer bands brought overnight rain to Kolkata, Howrah, South 24 Parganas and both Midnapore districts, with fresh weather alerts for Gangetic Bengal.",
            topics: ["flood"],
            locations: ["Kolkata", "Howrah", "Sundarbans", "Paschim Medinipur", "Jhargram"]
        },
        {
            title: "Cyclone Arnab: heavy rain warning for south Bengal, Kolkata flights cancelled",
            source: "NewKerala / IANS",
            date: "2026-10-28",
            url: "https://www.newkerala.com/news/a/heavy-rain-warning-south-bengal-as-cyclone-arnab-712.htm",
            summary: "Some flights out of Kolkata were cancelled as a precaution, although the direct impact on West Bengal stayed limited while the storm made landfall far to the south.",
            topics: ["flood"],
            locations: ["Kolkata"]
        },
        {
            title: "Rain lashes Bengal as Cyclone Arnab weakens into a depression",
            source: "Siasat / PTI",
            date: "2026-10-29",
            url: "https://www.siasat.com/rain-lashes-bengal-as-cyclone-arnab-turns-into-depression-3566467/",
            summary: "Rain and squally winds continued across parts of the state as the remnant system moved inland over Chhattisgarh and Odisha; Kolkata stayed overcast with light to moderate spells.",
            topics: ["flood"],
            locations: ["Kolkata", "Howrah"]
        },
        {
            title: "Cyclone Arnab: Bengal braces for heavy rain, landslides likely in the hills",
            source: "NewKerala / IANS",
            date: "2026-10-27",
            url: "https://www.newkerala.com/news/a/cyclone-arnab-bengal-braces-heavy-rain-landslides-likely-358.htm",
            summary: "The Kolkata Met centre warned of heavy rain along the coast and possible landslides in the northern hill districts. Civil Defence teams were posted in coastal Sundarbans pockets such as Sagar and Namkhana.",
            topics: ["flood"],
            locations: ["Sundarbans", "Darjeeling"]
        },
        {
            title: "Bengal braces for rain as Cyclone Arnab nears the Andhra coast",
            source: "NewKerala / IANS",
            date: "2026-10-26",
            url: "https://www.newkerala.com/news/a/bengal-braces-rain-as-cyclone-arnab-nears-andhra-901.htm",
            summary: "Fishermen were told to stay ashore. Heavy showers were forecast for South 24 Parganas, both Midnapores and Jhargram, with wet weather expected later in the week in Darjeeling, Jalpaiguri and Alipurduar.",
            topics: ["flood"],
            locations: ["Sundarbans", "Paschim Medinipur", "Jhargram", "Darjeeling", "Jalpaiguri", "Dooars"]
        },
        {
            title: "Cyclone Arnab's remnants may bring heavy rain to north Bengal",
            source: "NewKerala / IANS",
            date: "2026-10-31",
            url: "https://www.newkerala.com/news/a/cyclone-arnabs-aftermath-may-bring-heavy-rain-north-227.htm",
            summary: "Leftover moisture from the cyclone was expected to push heavy rain into the northern districts, while a fresh depression formed over the south Andaman Sea.",
            topics: ["flood"],
            locations: ["Darjeeling", "Jalpaiguri", "Dooars"]
        },

        /* ---------- Post-monsoon dryness ---------- */
        {
            title: "IMD: early-October rainfall far below normal across Gangetic Bengal",
            source: "India Meteorological Department",
            date: "2026-10-10",
            url: "https://mausam.imd.gov.in/Rainfall/DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd.pdf",
            summary: "IMD's district table for 1–10 October 2026 placed most south Bengal districts in the 'large deficient' band: West Midnapore about −93%, Jhargram −90%, Purulia −79%, Bankura and Birbhum −78%. Howrah (−40%) and Kolkata (−26%) were also short. Note: IMD updates this file daily, so the link may now show a later period.",
            topics: ["drought"],
            locations: ["Bankura", "Purulia", "Jhargram", "Birbhum", "Paschim Medinipur", "Howrah", "Kolkata"]
        },
        {
            title: "Monsoon tally: Gangetic Bengal above normal, sub-Himalayan Bengal slightly short",
            source: "ICAR-CRIDA rainfall bulletin",
            date: "2026-09-02",
            url: "https://icar-crida.res.in/season_c/Sep_2026/02-Sep-2026.pdf",
            summary: "From 1 June to 2 September, Gangetic West Bengal had received about 11% more rain than normal, while Sub-Himalayan West Bengal and Sikkim was about 10% below normal, which is still inside IMD's 'normal' range.",
            topics: ["drought"],
            locations: ["Bankura", "Purulia", "Jhargram", "Birbhum", "Paschim Medinipur", "Darjeeling", "Jalpaiguri", "Dooars"]
        },

        /* ---------- Ganga erosion: Malda & Murshidabad ---------- */
        {
            title: "Bengal to seek Jharkhand's nod to dredge the Ganga to curb erosion in Malda",
            source: "Dredgewire",
            date: "2026-10-28",
            url: "https://dredgewire.com/bengal-government-to-seek-jharkhands-nod-to-dredge-ganga-riverbed-to-curb-erosion-in-malda/",
            summary: "After an aerial survey, the state wants to dredge the riverbed near Rajmahal in Jharkhand to stop recurring erosion and floods. The report notes that the problem affects Malda and Murshidabad alike.",
            topics: ["flood"],
            locations: ["Malda", "Murshidabad"]
        },
        {
            title: "Ganga–Fulahar confluence poses threat to north Bengal connectivity",
            source: "UNI India",
            date: "2026-10-25",
            url: "https://www.uniindia.com/east-india/environment-north-bengal-ganga-fulahar-threat/225497",
            summary: "The Chief Secretary flew over Malda to review erosion and flooding along the Ganga, Fulahar and Kosi ahead of a Ganga Flood Control Commission meeting.",
            topics: ["flood"],
            locations: ["Malda"]
        },
        {
            title: "Bridge brings relief to flood-hit Bhutni as fresh erosion triggers panic",
            source: "UNI India",
            date: "2026-10-16",
            url: "https://www.uniindia.com/east-india/admin-wb-bridge-bhutni/216504",
            summary: "A temporary bridge restored access to flood-ravaged Bhutni before Durga Puja, while new erosion at Panchanandapur along the Ganga worried residents.",
            topics: ["flood"],
            locations: ["Malda"]
        },
        {
            title: "Ganga eats into Srirampur, houses collapse into the river",
            source: "UNI India",
            date: "2026-09-24",
            url: "https://www.uniindia.com/east-india/disaster-wb-srirampur-erosion/191826",
            summary: "Severe bank erosion in Srirampur village of Malda district brought several houses down into the swollen Ganga, forcing families to move.",
            topics: ["flood"],
            locations: ["Malda"]
        },
        {
            title: "IIT-Kanpur experts to study Ganga erosion in Malda",
            source: "UNI India",
            date: "2026-09-19",
            url: "https://www.uniindia.com/east-india/environment-wb-malda-erosion-iitk/185241",
            summary: "An IIT-Kanpur team will visit Manikchak, Ratua and nearby areas to study the river and help design a permanent protection scheme.",
            topics: ["flood"],
            locations: ["Malda"]
        },
        {
            title: "Ganga rises above extreme danger level, fresh areas inundated in Malda",
            source: "UNI India",
            date: "2026-09-10",
            url: "https://www.uniindia.com/east-india/environment-wb-ganga-rise/175063",
            summary: "The rising Ganga flooded new areas of Ratua-I block, and fresh erosion was reported near Milki in English Bazar block.",
            topics: ["flood"],
            locations: ["Malda"]
        },
        {
            title: "West Bengal proposes ₹3,600 crore Centre–state plan against Ganga erosion",
            source: "NewKerala / ANI",
            date: "2026-07-11",
            url: "https://www.newkerala.com/news/a/west-bengal-proposes-rs-3600-crore-centre-state-plan-525.htm",
            summary: "The state submitted a proposal for permanent anti-erosion works in Murshidabad and Malda, with the cost to be split equally between the Centre and the state.",
            topics: ["flood"],
            locations: ["Murshidabad", "Malda"]
        },

        /* ---------- Lower Damodar / Howrah ---------- */
        {
            title: "State reviews Lower Damodar floods; Udaynarayanpur at danger mark",
            source: "ThePrint / PTI",
            date: "2026-09-04",
            url: "https://theprint.in/india/cm-suvendu-reviews-bengal-flood-situation-says-no-need-for-panic-heaps-praise-on-dvc/3034126/",
            summary: "Rivers reached the danger mark at Khanakul, Jangipara and Udaynarayanpur after heavy rain and DVC releases. Officials said no embankment had been breached.",
            topics: ["flood"],
            locations: ["Howrah", "Bankura"]
        },
        {
            title: "Flood assessments completed for Udaynarayanpur and Amta",
            source: "NewKerala / ANI",
            date: "2026-09-05",
            url: "https://www.newkerala.com/news/a/west-bengal-cm-suvendu-adhikari-reviews-malda-flood-410.htm",
            summary: "A state review covered Malda's flood and erosion, Lower Damodar flooding across Bankura, Hooghly and Howrah, and track subsidence near New Farakka. Damage assessments in Howrah's Udaynarayanpur and Amta were reported complete.",
            topics: ["flood"],
            locations: ["Howrah", "Malda", "Bankura"]
        },

        /* ---------- South-west Bengal rain events ---------- */
        {
            title: "Rivers breach embankments in Bankura, Purulia and West Medinipur",
            source: "All India Radio News",
            date: "2026-08-18",
            url: "https://newsonair.gov.in/west-bengal-flood-like-situation-in-southern-part-after-rivers-breach-embankments/",
            summary: "Days of heavy rain pushed rivers over their banks in these usually drought-prone districts, leaving several bridges and causeways under water.",
            topics: ["flood"],
            locations: ["Bankura", "Purulia", "Paschim Medinipur"]
        },
        {
            title: "₹1,200 crore allocated for the Ghatal Master Plan",
            source: "ThePrint / PTI",
            date: "2026-09-30",
            url: "https://theprint.in/india/suvendu-announces-rs-1200-crore-allocation-for-ghatal-master-plan-to-mitigate-floods/3057778/",
            summary: "Money was set aside this financial year for the long-delayed flood-control plan covering 11 blocks across Purba and Paschim Medinipur: embankments, dredging, pump houses and sluice gates.",
            topics: ["flood"],
            locations: ["Paschim Medinipur"]
        },

        /* ---------- Kolkata urban flooding ---------- */
        {
            title: "Heavy rain hits Kolkata as IMD issues fresh alert",
            source: "Business Today",
            date: "2026-09-12",
            url: "https://www.businesstoday.in/india/story/west-bengal-weather-heavy-rain-hits-kolkata-as-imd-issues-fresh-alert-till-september-13-555158-2026-09-12",
            summary: "A low-pressure system over the north-west Bay of Bengal brought more than 45 mm of rain to the city and unsettled weather across the state.",
            topics: ["flood"],
            locations: ["Kolkata"]
        },
        {
            title: "Heavy rain paralyses Kolkata, waterlogging disrupts traffic",
            source: "The Star / PTI",
            date: "2026-08-17",
            url: "https://www.thestar.com.my/aseanplus/aseanplus-news/2026/08/17/heavy-rain-paralyses-kolkata-waterlogging-disrupts-traffic-weatherman-forecasts-more-intense-showers",
            summary: "Several low-lying areas flooded and commuters were delayed. The Met office warned of intense spells of 2–3 cm an hour and possible underpass closures.",
            topics: ["flood"],
            locations: ["Kolkata"]
        },

        /* ---------- Sundarbans ---------- */
        {
            title: "Netherlands-funded Sundarbans flood mitigation study completed",
            source: "ThePrint / PTI",
            date: "2026-10-13",
            url: "https://theprint.in/india/netherlands-funded-sundarbans-flood-mitigation-study-complete-report-submitted-to-bengal-govt/3070658/",
            summary: "A study on nature-based coastal protection and dyke design for the Sundarbans has been handed to the state, which is weighing World Bank support to act on it.",
            topics: ["flood"],
            locations: ["Sundarbans"]
        },
        {
            title: "Sundarbans sees fewer seedlings survive as Gewa and Kankra spread",
            source: "bdnews24.com",
            date: "2026-10-16",
            url: "https://bdnews24.com/environment/imqo0hiwma",
            summary: "Reporting from the Bangladesh side of the forest says more than half of seedlings died between 2010 and 2020 as falling freshwater flow and rising salinity changed which species thrive.",
            topics: ["vegetation"],
            locations: ["Sundarbans"]
        },
        {
            title: "Women of Jharkhali restoring mangroves in the Sundarbans",
            source: "NewKerala / IANS",
            date: "2026-09-27",
            url: "https://www.newkerala.com/news/a/mangrove-plantation-providing-livelihoods-women-sundarbans-pm-modi-473.htm",
            summary: "A national radio address highlighted a women's group in Jharkhali that grows and replants mangroves, giving them a livelihood while strengthening the coast.",
            topics: ["vegetation"],
            locations: ["Sundarbans"]
        },
        {
            title: "Forest department starts restoring 1,600 ha of encroached mangrove land",
            source: "Telangana Today / IANS",
            date: "2026-07-29",
            url: "https://telanganatoday.com/bengal-govt-starts-process-for-mangrove-restoration-on-encroached-sundarbans-forestland",
            summary: "Illegal brackish-water fisheries are being cleared and the land replanted with mangrove saplings.",
            topics: ["vegetation"],
            locations: ["Sundarbans"]
        },

        /* ---------- North Bengal vegetation ---------- */
        {
            title: "Tea industry seeks a state policy push for Darjeeling and Dooars–Terai",
            source: "Business Standard",
            date: "2026-08-26",
            url: "https://www.business-standard.com/topic/darjeeling-tea",
            summary: "Indian Tea Association white papers asked for money to replant ageing tea areas, modernise factories and reform trade so that north Bengal's plantations can recover.",
            topics: ["vegetation"],
            locations: ["Darjeeling", "Dooars", "Jalpaiguri"]
        },
        {
            title: "Makaibari brings Darjeeling's small tea growers into a new collective",
            source: "Business Standard",
            date: "2026-09-01",
            url: "https://www.business-standard.com/topic/darjeeling-tea",
            summary: "A Darjeeling estate has formed a collective of small growers, an attempt to keep small hill plots productive as yields in the region continue to fall.",
            topics: ["vegetation"],
            locations: ["Darjeeling"]
        }
    ]
};
