<template>
    <nav class="navbar navbar-dark bg-dark fixed-top">
        <div class="container-fluid">
            <router-link to='/dashboard' class="navbar-brand"
                style="font-family: 'Sacramento', cursive; font-size: 27px; color: aliceblue;"><strong>PixelShows</strong></router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDarkNavbar"
                aria-controls="offcanvasDarkNavbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="offcanvas offcanvas-end text-bg-dark" tabindex="-1" id="offcanvasDarkNavbar"
                aria-labelledby="offcanvasDarkNavbarLabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">PixelShows</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
                        aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                        <li class="nav-item">
                            <router-link to="/editaccount" class="nav-link active" aria-current="page">change
                                password</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/createshow" class="nav-link active" aria-current="page">create
                                show</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/createvenue" class="nav-link active" aria-current="page">create
                                venue</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/createvenuetype" class="nav-link active" aria-current="page">create
                                venue type</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/createtag" class="nav-link active" aria-current="page">create
                                tag</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/edittag" class="nav-link active" aria-current="page">edit tag</router-link>
                        </li>


                        <form class="d-grid gap-3 pt-3" role="search" @submit.prevent="handleFormSubmit">
                            <div>
                                <input type="text" class="form-control" id="showNameInput" v-model="form_show_name"
                                    placeholder="Enter Show Name">
                            </div>
                            <div class="form-floating">
                                <select class="form-select" id="floatingSelect1" aria-label="Floating label select example"
                                    v-model="form_location">
                                    <option v-for="item in tags" :value="item[0]">{{ item[1] }}</option>
                                </select>
                                <label for="floatingSelect2">Tags</label>
                            </div>
                            <div class="form-floating">
                                <select class="form-select" id="floatingSelect2" aria-label="Floating label select example"
                                    v-model="form_tag">
                                    <option v-for="item in locations" :value="item">{{ item }}</option>
                                </select>
                                <label for="floatingSelect2">Locations</label>
                            </div>
                            <button class="btn btn-success" type="submit">Search</button>
                        </form>
                        <li class="nav-item">
                            <router-link to="/logout" class="nav-link active" aria-current="page">logout</router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'PatronNav',
    data: function () {
        return {
            form_location: '',
            form_tag: '',
            form_show_name: '',
            shows: [],
            email: '',
            locations: [],
            tags: [],
            queryParams: {},
        }
    },
    beforeMount() {
        const headers = { 'Content-Type': 'application/json', 'Auth-Token': localStorage.getItem("Auth-Token") }
        fetch("http://127.0.0.1:8000/api/getvenuelocations", { headers: headers, method: "GET" })
            .then(response => {
                return response.json();
            })
            .then((data) => {
                this.locations = JSON.parse(data)['locations'];
            })
        fetch("http://127.0.0.1:8000/api/getshowtags", { headers: headers, method: "GET" })
            .then(response => {
                return response.json();
            })
            .then((data) => {
                this.tags = JSON.parse(data)['tags'];
            })

    },
    methods: {
        handleFormSubmit: function () {
            if (this.form_show_name) {
                this.queryParams.show_name = this.form_show_name;
            }
            if (this.form_location) {
                this.queryParams.location = this.form_location;
            }
            if (this.form_tag) {
                this.queryParams.form_tag = this.form_tag;
            }
            console.log(this.queryParams)
            this.$router.push({ path: '/searchshow', query: this.queryParams })
        }

    }
}
</script>