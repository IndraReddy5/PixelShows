<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  methods: {
    handleFormSubmit: function () {
      const headers = { 'Content-Type': 'application/json', 'Auth-Token': localStorage.getItem("Auth-Token") }
      if (this.location && this.tag) {
        fetch("http://127.0.0.1:8000/api/searchshows?location=" + this.location + "&tag=" + this.tag, { headers: headers, body: JSON.stringify(formdata), method: "POST" })
          .then(response => {
            return response.json();
          })
          .then((data) => {
            let temp_shows = JSON.parse(data);
            let new_shows = [];
            for (var x of Object.keys(temp_shows.shows)) { new_shows.push(temp_shows.shows[x]) }
            this.shows = new_shows;
          })
      }
      else if (this.location) {
        fetch("http://127.0.0.1:8000/api/searchshows?location=" + this.location, { headers: headers, body: JSON.stringify(formdata), method: "POST" })
          .then(response => {
            return response.json();
          })
          .then((data) => {
            let temp_shows = JSON.parse(data);
            let new_shows = [];
            for (var x of Object.keys(temp_shows.shows)) { new_shows.push(temp_shows.shows[x]) }
            this.shows = new_shows;
          })
      }
      else if (this.tag) {
        fetch("http://127.0.0.1:8000/api/searchshows?tag=" + this.tag, { headers: headers, body: JSON.stringify(formdata), method: "POST" })
          .then(response => {
            return response.json();
          })
          .then((data) => {
            let temp_shows = JSON.parse(data);
            let new_shows = [];
            for (var x of Object.keys(temp_shows.shows)) { new_shows.push(temp_shows.shows[x]) }
            this.shows = new_shows;
          })
      }
      else {
        alert("Please enter a location or tag to search for a show.")
      }
    }
  }
}
</script>