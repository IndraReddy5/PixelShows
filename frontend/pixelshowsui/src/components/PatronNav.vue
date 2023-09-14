<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" aria-label="Fifth navbar example">
        <div class="container-fluid">
            <router-link to='/dashboard' class="navbar-brand"
                style="font-family: 'Sacramento', cursive; font-size: 27px;"><strong>Blog Lite</strong></router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample05"
                aria-controls="navbarsExample05" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarsExample05">
                <!-- <ul class="navbar-nav me-auto mb-2 mb-lg-0"> -->
                <!-- <li><a class="nav-link disable_dropdown" href="{{url_for('create_post',username=user)}}">New Post</a>
                    </li>
                    <li><a class="nav-link disable_dropdown" href="{{url_for('load_profile',username=user)}}">View
                            Profile</a></li>
                    <li><a class="nav-link disable_dropdown" href="{{url_for('logout')}}">Sign out</a></li> -->
                <!-- </ul> -->

                <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search" action="{{url_for('search')}}"
                    method="GET">
                    <input type="search" name="search" class="form-control" placeholder="Search..." aria-label="Search"
                        autocomplete="off">
                </form>
                <div class="dropdown text-end logout_class">
                    <a href="#" class="d-block link-dark text-decoration-none dropdown-toggle" data-bs-toggle="dropdown"
                        aria-expanded="false">
                        <img :src="imageSrc" alt="profile_pic" width="40" height="40" class="rounded-circle">
                    </a>
                    <ul class="dropdown-menu text-small"
                        style="position: absolute; font-size: 85%; inset: 0px 4px auto auto; margin: 0px; transform: translate(0px, 34px);"
                        data-popper-placement="static">
                        <li><span class="dropdown-item text-muted">{{ this.$store.state.username }}</span></li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li><a class="dropdown-item" href="{{url_for('create_post',username=user)}}">New Post</a></li>
                        <li><a class="dropdown-item" href="{{url_for('load_profile',username=user)}}">View Profile</a></li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li><a class="dropdown-item" href="{{url_for('logout')}}">Sign out</a></li>
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
            location: '',
            tag: '',
            shows: {},
        }
    },
    methods: {
        handleFormSubmit: function () {
            const headers = { 'Content-Type': 'application/json', 'Auth-Token': localStorage.getItem("Auth-Token") }
            if (this.location && this.tag) {
                fetch("http://127.0.0.1:8000/api/searchshows?location="+this.location+"&tag="+this.tag, { headers: headers, body: JSON.stringify(formdata), method: "POST" })
                    .then(response => {
                        return response.json();
                    })
                    .then((data) => {
                        this.shows = JSON.parse(data);
                    })
            }
            else if (this.location) {
                fetch("http://127.0.0.1:8000/api/searchshows?location="+this.location, { headers: headers, body: JSON.stringify(formdata), method: "POST" })
                    .then(response => {
                        return response.json();
                    })
                    .then((data) => {
                        this.shows = JSON.parse(data);
                    })
            }
            else if (this.tag) {
                fetch("http://127.0.0.1:8000/api/searchshows?tag="+this.tag, { headers: headers, body: JSON.stringify(formdata), method: "POST" })
                    .then(response => {
                        return response.json();
                    })
                    .then((data) => {
                        this.shows = JSON.parse(data);
                    })
            }
            else {
                alert("Please enter a location or tag to search for a show.")
            }
        }
    }
}
</script>