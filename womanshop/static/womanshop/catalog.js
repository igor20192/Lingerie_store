document.addEventListener("DOMContentLoaded", () => {
    const apiURL = document.querySelector("script[src$='catalog.js']").getAttribute("data-api-url");
    let catalogScript = document.getElementById('catalog-script')
    async function getData(url, page, paginateBy, sortBy, sortDirection, bodysuit, bras, tights_and_socks, swimwear, men_underwear, panties, seamless_underwear, thermal_underwear, accessories, basic_underwear, new_style, сomfort_underwear, sexual, lacy, everyday, homewear, sleepwear, for_wedding, avelin, comazo, lauma, melado, milavitsa, serge, teatro, triumph, start, end) {
        const urlWithParams = url + "?" + new URLSearchParams({
            page: page,
            per_page: paginateBy,
            sort_by: sortBy,
            sort_direction: sortDirection,
            bodysuit: bodysuit,
            bras: bras,
            tights_and_socks: tights_and_socks,
            swimwear: swimwear,
            men_underwear: men_underwear,
            panties: panties,
            seamless_underwear: seamless_underwear,
            thermal_underwear: thermal_underwear,
            accessories: accessories,
            basic_underwear: basic_underwear,
            new_style: new_style,
            сomfort_underwear: сomfort_underwear,
            sexual: sexual,
            lacy: lacy,
            everyday: everyday,
            homewear: homewear,
            sleepwear: sleepwear,
            for_wedding: for_wedding,
            avelin: avelin,
            comazo: comazo,
            lauma: lauma,
            melado: melado,
            milavitsa: milavitsa,
            serge: serge,
            teatro: teatro,
            triumph: triumph,
            start: start,
            end: end
        })
        const response = await fetch(urlWithParams);
        return response.json();
    }

    class LoadMorePaginator {
        constructor(perPage) {
            this.perPage = perPage
            this.pageIndex = 1
            this.container = document.querySelector("#a")
            this.next = document.querySelector("#next")
            this.sortBy = document.querySelector("#sort-by")
            this.sortDirection = document.querySelector("#sort-direction")
            this.bodysuit = document.querySelector("#sort_bodysuit")
            this.bras = document.querySelector("#sort_bras")
            this.tights_and_socks = document.querySelector("#sort_tights_and_socks")
            this.swimwear = document.querySelector("#sort_swimwear")
            this.men_underwear = document.querySelector("#sort_men_underwear")
            this.panties = document.querySelector("#sort_panties")
            this.seamless_underwear = document.querySelector("#sort_seamless_underwear")
            this.thermal_underwear = document.querySelector("#sort_thermal_underwear")
            this.accessories = document.querySelector("#sort_accessories")
            this.basic_underwear = document.querySelector("#sort_basic_underwear")
            this.new_style = document.querySelector("#sort_new_style")
            this.сomfort_underwear = document.querySelector("#sort_сomfort_underwear")
            this.sexual = document.querySelector("#sort_sexual")
            this.lacy = document.querySelector("#sort_lacy")
            this.everyday = document.querySelector("#sort_everyday")
            this.homewear = document.querySelector("#sort_homewear")
            this.sleepwear = document.querySelector("#sort_sleepwear")
            this.for_wedding = document.querySelector("#sort_for_wedding")
            this.avelin = document.querySelector("#sort_avelin")
            this.comazo = document.querySelector("#sort_comazo")
            this.lauma = document.querySelector("#sort_lauma")
            this.melado = document.querySelector("#sort_melado")
            this.milavitsa = document.querySelector("#sort_milavitsa")
            this.serge = document.querySelector("#sort_serge")
            this.teatro = document.querySelector("#sort_teatro")
            this.triumph = document.querySelector("#sort_triumph")
            this.start = document.querySelector("#id_start")
            this.end = document.querySelector("#id_end")
            this.next.addEventListener("click", this.onNextClick.bind(this))
            this.sortBy.addEventListener("change", this.onSortByChange.bind(this))
            this.sortDirection.addEventListener("change", this.onSortDirectionChange.bind(this))
            this.bodysuit.addEventListener("change", this.onBodysuitChange.bind(this))
            this.bras.addEventListener("change", this.onBrasChange.bind(this))
            this.tights_and_socks.addEventListener("change", this.onTights_and_socksChange.bind(this))
            this.swimwear.addEventListener("change", this.onSwimwearChange.bind(this))
            this.men_underwear.addEventListener("change", this.onMen_underwearChange.bind(this))
            this.panties.addEventListener("change", this.onPantiesChande.bind(this))
            this.seamless_underwear.addEventListener("change", this.onSeamless_underwearChange.bind(this))
            this.thermal_underwear.addEventListener("change", this.onThermal_underwearChange.bind(this))
            this.accessories.addEventListener("change", this.onAccessoriesChange.bind(this))
            this.basic_underwear.addEventListener("change", this.onBasic_underwearChange.bind(this))
            this.new_style.addEventListener("change", this.onNew_style_Change.bind(this))
            this.сomfort_underwear.addEventListener("change", this.onComfort_underwearChange.bind(this))
            this.sexual.addEventListener("change", this.onSexualChange.bind(this))
            this.lacy.addEventListener("change", this.onLacyChange.bind(this))
            this.everyday.addEventListener("change", this.onEverydayChange.bind(this))
            this.homewear.addEventListener("change", this.onHomewearChange.bind(this))
            this.sleepwear.addEventListener("change", this.onSleepwearChange.bind(this))
            this.for_wedding.addEventListener("change", this.onFor_weddingChange.bind(this))
            this.avelin.addEventListener("change", this.onAvelinChange.bind(this))
            this.comazo.addEventListener("change", this.onComazoChange.bind(this))
            this.lauma.addEventListener("change", this.onLaumaChange.bind(this))
            this.melado.addEventListener("change", this.onMeladoChange.bind(this))
            this.milavitsa.addEventListener("change", this.onMilavitsaChande.bind(this))
            this.serge.addEventListener("change", this.onSergeChange.bind(this))
            this.teatro.addEventListener("change", this.onTeatroChange.bind(this))
            this.triumph.addEventListener("change", this.onTriumphChange.bind(this))
            this.start.addEventListener("change", this.onStartChange.bind(this))
            this.end.addEventListener("change", this.onEndChange.bind(this))
            this.loadMore()
        }
        onNextClick(event) {
            event.preventDefault()
            this.pageIndex++
            this.loadMore()
        }
        onSortByChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onSortDirectionChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onBodysuitChange(event) {

            this.pageIndex = 1
            this.loadMore()
        }
        onBrasChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onTights_and_socksChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onSwimwearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onMen_underwearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onPantiesChande(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onSeamless_underwearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onThermal_underwearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onAccessoriesChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onBasic_underwearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onNew_style_Change(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onComfort_underwearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onSexualChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onLacyChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onEverydayChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onHomewearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onSleepwearChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onFor_weddingChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onAvelinChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onComazoChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onLaumaChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onMeladoChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onMilavitsaChande(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onSergeChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onTeatroChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onTriumphChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onStartChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        onEndChange(event) {
            this.pageIndex = 1
            this.loadMore()
        }
        addElement(product) {
            const div = document.createElement("div");
            const favoriteList = JSON.parse(catalogScript.dataset.favoritelist);
            let favoriteImageURL = catalogScript.dataset.favorites;
            if (favoriteList.includes(product.id)) {
                favoriteImageURL = catalogScript.dataset.life;
            }
            div.innerHTML = `
            <div class="col">
                <img src="${product.image1}" width="273px" height="364px" alt="Not photo">
                <img src="${favoriteImageURL}" style="position: relative; top: -350px;
                left: 235px" width="20px" height="18px" alt="Not photo">
                <p id="name_product">${product.name}</p>
                <p id="name_brn">${product.brand}</p>
                <p id="name_prc">${product.price}₽</p>
                <a id="detail" href="/product/${product.id}" style="color: #C91664;">Подробние</a>
                <p><img id="line25" src="{% static '/img/Line 25.png' %}" alt=""></p>
            </div>
        `;
            this.container.append(div);
            div.style.display = "block";
        }

        loadMore() {
            const sortBy = this.sortBy.value
            const sortDirection = this.sortDirection.value
            const bodysuit = this.bodysuit.checked
            const bras = this.bras.checked
            const tights_and_socks = this.tights_and_socks.checked
            const swimwear = this.swimwear.checked
            const men_underwear = this.men_underwear.checked
            const panties = this.panties.checked
            const seamless_underwear = this.seamless_underwear.checked
            const thermal_underwear = this.thermal_underwear.checked
            const accessories = this.accessories.checked
            const basic_underwear = this.basic_underwear.checked
            const new_style = this.new_style.checked
            const сomfort_underwear = this.сomfort_underwear.checked
            const sexual = this.sexual.checked
            const lacy = this.lacy.checked
            const everyday = this.everyday.checked
            const homewear = this.homewear.checked
            const sleepwear = this.sleepwear.checked
            const for_wedding = this.for_wedding.checked
            const avelin = this.avelin.checked
            const comazo = this.comazo.checked
            const lauma = this.lauma.checked
            const melado = this.melado.checked
            const milavitsa = this.milavitsa.checked
            const serge = this.serge.checked
            const teatro = this.teatro.checked
            const triumph = this.triumph.checked
            const start = this.start.value
            const end = this.end.value

            getData(apiURL, this.pageIndex, this.perPage, sortBy, sortDirection, bodysuit, bras, tights_and_socks, swimwear, men_underwear, panties, seamless_underwear, thermal_underwear, accessories, basic_underwear, new_style, сomfort_underwear, sexual, lacy, everyday, homewear, sleepwear, for_wedding, avelin, comazo, lauma, melado, milavitsa, serge, teatro, triumph, start, end)
                .then(response => {
                    this.container.innerHTML = ""
                    response.data.forEach((el) => {
                        this.addElement(el)
                    });
                    this.next.style.display = !response.has_next ? "none" : "block"
                });
        }
    }


    new LoadMorePaginator(3);
})