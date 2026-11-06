document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* ==================================================
           FOOTER CSS
        ================================================== */

        const footerStyleAlreadyLoaded =
            document.querySelector(
                'link[href*="footer.css"]'
            );


        if (!footerStyleAlreadyLoaded) {

            const footerStyles =
                document.createElement(
                    "link"
                );

            footerStyles.rel =
                "stylesheet";

            footerStyles.href =
                "/static/dealership/footer.css";

            document.head.appendChild(
                footerStyles
            );

        }



        /* ==================================================
           CLICKABLE CAR CARDS
        ================================================== */

        const clickableCarCards =
            document.querySelectorAll(
                ".home-car-card, .inventory-card"
            );


        clickableCarCards.forEach(
            function (card) {


                const carLink =
                    card.querySelector(
                        'a[href*="/masini/"]'
                    );


                if (!carLink) {
                    return;
                }


                card.style.cursor =
                    "pointer";


                card.setAttribute(
                    "tabindex",
                    "0"
                );


                card.setAttribute(
                    "role",
                    "link"
                );


                /*
                Clicking anywhere on the card opens
                the car detail page.

                Existing buttons/links continue to work
                normally.
                */

                card.addEventListener(
                    "click",
                    function (event) {


                        if (
                            event.target.closest(
                                "a, button, input, select, textarea, label"
                            )
                        ) {

                            return;

                        }


                        window.location.href =
                            carLink.href;

                    }
                );


                /*
                Keyboard accessibility:
                Enter or Space opens the car too.
                */

                card.addEventListener(
                    "keydown",
                    function (event) {


                        if (
                            event.key !== "Enter"
                            &&
                            event.key !== " "
                        ) {

                            return;

                        }


                        if (
                            event.target.closest(
                                "a, button, input, select, textarea"
                            )
                            !== card
                            &&
                            event.target !== card
                        ) {

                            return;

                        }


                        event.preventDefault();


                        window.location.href =
                            carLink.href;

                    }
                );


            }
        );



        /* ==================================================
           MOBILE MENU
        ================================================== */

        const toggle =
            document.getElementById(
                "mobileMenuToggle"
            );


        const navigation =
            document.getElementById(
                "mainNavigation"
            );


        const backdrop =
            document.getElementById(
                "mobileMenuBackdrop"
            );


        function openMenu() {

            if (
                !toggle
                ||
                !navigation
                ||
                !backdrop
            ) {

                return;

            }


            navigation.classList.add(
                "open"
            );


            toggle.classList.add(
                "open"
            );


            backdrop.classList.add(
                "show"
            );


            document.body.classList.add(
                "mobile-menu-open"
            );


            toggle.setAttribute(
                "aria-expanded",
                "true"
            );

        }



        function closeMenu() {

            if (
                !toggle
                ||
                !navigation
                ||
                !backdrop
            ) {

                return;

            }


            navigation.classList.remove(
                "open"
            );


            toggle.classList.remove(
                "open"
            );


            backdrop.classList.remove(
                "show"
            );


            document.body.classList.remove(
                "mobile-menu-open"
            );


            toggle.setAttribute(
                "aria-expanded",
                "false"
            );

        }



        function toggleMenu() {

            if (!navigation) {
                return;
            }


            if (
                navigation.classList.contains(
                    "open"
                )
            ) {

                closeMenu();

            } else {

                openMenu();

            }

        }



        if (toggle) {

            toggle.addEventListener(
                "click",
                toggleMenu
            );

        }



        if (backdrop) {

            backdrop.addEventListener(
                "click",
                closeMenu
            );

        }



        if (navigation) {

            navigation
                .querySelectorAll("a")
                .forEach(
                    function (link) {

                        link.addEventListener(
                            "click",
                            closeMenu
                        );

                    }
                );

        }



        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Escape"
                ) {

                    closeMenu();

                }

            }
        );



        window.addEventListener(
            "resize",
            function () {

                if (
                    window.innerWidth > 800
                ) {

                    closeMenu();

                }

            }
        );



        /* ==================================================
           HOMEPAGE ACTIVE NAVIGATION
        ================================================== */

        if (
            window.location.pathname === "/"
        ) {


            const homeLink =
                document.querySelector(
                    '[data-nav="home"]'
                );


            const findLink =
                document.querySelector(
                    '[data-nav="find-car"]'
                );


            const reviewsLink =
                document.querySelector(
                    '[data-nav="reviews"]'
                );


            const contactLink =
                document.querySelector(
                    '[data-nav="contact"]'
                );


            const observedSections = [

                {
                    element:
                        document.getElementById(
                            "acasa"
                        ),

                    link:
                        homeLink
                },

                {
                    element:
                        document.getElementById(
                            "gaseste-masina"
                        ),

                    link:
                        findLink
                },

                {
                    element:
                        document.getElementById(
                            "recenzii"
                        ),

                    link:
                        reviewsLink
                },

                {
                    element:
                        document.getElementById(
                            "contact"
                        ),

                    link:
                        contactLink
                }

            ];


            const sectionLinks = [
                homeLink,
                findLink,
                reviewsLink,
                contactLink
            ];


            const observer =
                new IntersectionObserver(
                    function (entries) {


                        entries.forEach(
                            function (entry) {


                                if (
                                    !entry.isIntersecting
                                ) {

                                    return;

                                }


                                sectionLinks.forEach(
                                    function (link) {

                                        if (link) {

                                            link.classList.remove(
                                                "active"
                                            );

                                        }

                                    }
                                );


                                const match =
                                    observedSections.find(
                                        function (item) {

                                            return (
                                                item.element
                                                === entry.target
                                            );

                                        }
                                    );


                                if (
                                    match
                                    &&
                                    match.link
                                ) {

                                    match.link.classList.add(
                                        "active"
                                    );

                                }


                            }
                        );


                    },
                    {
                        rootMargin:
                            "-30% 0px -60% 0px"
                    }
                );


            observedSections.forEach(
                function (item) {

                    if (item.element) {

                        observer.observe(
                            item.element
                        );

                    }

                }
            );

        }



        /* ==================================================
           FOOTER
        ================================================== */

        if (
            !document.querySelector(
                ".site-footer"
            )
        ) {


            const currentYear =
                new Date().getFullYear();


            const footer =
                document.createElement(
                    "footer"
                );


            footer.className =
                "site-footer";


            footer.innerHTML = `

                <div class="footer-main">


                    <div class="footer-brand">

                        <a
                            href="/#acasa"
                            class="footer-brand-logo"
                        >

                            <div class="footer-brand-main">

                                AUTO CARS
                                <span>GML</span>

                            </div>

                            <div class="footer-brand-srl">
                                SRL
                            </div>

                        </a>


                        <div class="footer-gold-line"></div>


                        <p class="footer-description">

                            Mașini atent selecționate și
                            servicii personalizate pentru cei
                            care caută următoarea lor mașină.

                        </p>

                    </div>



                    <div class="footer-column">

                        <p class="footer-column-title">
                            NAVIGARE
                        </p>


                        <div class="footer-links">

                            <a href="/#acasa">
                                Acasă
                            </a>

                            <a href="/masini/disponibile/">
                                Mașini disponibile
                            </a>

                            <a href="/masini/vandute/">
                                Mașini vândute
                            </a>

                            <a href="/#gaseste-masina">
                                Găsește-mi o mașină
                            </a>

                            <a href="/#recenzii">
                                Recenzii
                            </a>

                            <a href="/#contact">
                                Contact
                            </a>

                        </div>

                    </div>



                    <div class="footer-column">

                        <p class="footer-column-title">
                            CONTACT
                        </p>


                        <div class="footer-contact-item">

                            <span>
                                TELEFON
                            </span>

                            <strong>
                                +40 757 337 253
                            </strong>

                        </div>


                        <div class="footer-contact-item">

                            <span>
                                LOCAȚIE
                            </span>

                            <a href="/#contact">

                                Piața Auto Korona

                                <br>

                                Brașov, România

                            </a>

                        </div>


                        <div class="footer-contact-item">

                            <a
                                href="https://wa.me/40757337253?text=Bun%C4%83%20ziua!%20V%C4%83%20contactez%20de%20pe%20site-ul%20Auto%20Cars%20GML."
                                target="_blank"
                                rel="noopener noreferrer"
                                class="footer-whatsapp"
                            >

                                Scrie pe WhatsApp

                                <span>→</span>

                            </a>

                        </div>

                    </div>


                </div>



                <div class="footer-bottom">

                    <div class="footer-bottom-inner">


                        <p class="footer-copyright">

                            © ${currentYear}
                            AUTO CARS GML SRL.
                            Toate drepturile rezervate.

                        </p>


                        <div class="footer-bottom-links">

                            <a href="/#contact">
                                Contact
                            </a>

                            <a href="/recenzii/">
                                Toate recenziile
                            </a>

                        </div>


                    </div>

                </div>

            `;


            document.body.appendChild(
                footer
            );

        }


    }
);