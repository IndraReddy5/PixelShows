<template>
    <div class="col-md-10 mx-auto col-lg-5 p-4 p-md-5">
      <h1>Log in to Blog Lite</h1>
      <br>
      <form method="POST" @submit.prevent="handleFormSubmit">
        <div class="form-floating mb-3">
          <input type="text" :class='{ "form-control": true, "is-invalid": v$.username.$error }' v-model="username"
            name="username" id="floatingInput" placeholder="username" autocomplete="off">
          <label for="floatingInput">username</label>
          <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.username.$error">
            <span>{{ v$.username.$errors[0].$message }}</span>
          </div>
        </div>
        <div class="form-floating mb-3">
          <input type="password" :class='{ "form-control": true, "is-invalid": v$.password.$error }' v-model="password"
            name="password" id="floatingPassword" placeholder="Password" autocomplete="off">
          <label for="floatingPassword">Password</label>
          <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.password.$error">
            <span>{{ v$.password.$errors[0].$message }}</span>
          </div>
        </div>
        <button class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
        <hr class="my-4">
        <small class="text-muted">New to Blog Lite? <router-link to="/signup">Sign up now</router-link> </small>
      </form>
    </div>
  </template>
  
  <script>
  // import router from '@/router' // es-lint-disable
  import { useVuelidate } from '@vuelidate/core'
  import { required, alphaNum } from '@vuelidate/validators'
  export default {
    setup () {
      return {
        v$: useVuelidate()
      }
    },
    name: 'LoginForm',
    data: function () {
      return {
        username: '',
        password: '',
        errormsg: '',
        errStatus: false
      }
    },
    validations: {
      username: {
        required,
        alphaNum,
        $params: {
          required: { message: 'The username field is required' },
          alphaNum: { message: 'The username must contain only letters and numbers' }
        }
      },
      password: { required }
    },
    methods: {
      handleFormSubmit: function () {
        this.v$.$touch()
        if (!this.v$.$error) {
          const headers = { 'Content-Type': 'application/json' }
          const formdata = { username: this.username, password: this.password }
          fetch("http://127.0.0.1:8000/login?include_auth_token", {headers:{'content-type': 'application/json'},body:JSON.stringify(formdata),method:"POST"})
           .then(response => this.$store.dispatch('userLogin', { username: this.username, authToken: response.data.response.user.authentication_token }))
            .catch((error) => {
              if (error.response) {
                const message = error.response.data.response.errors[0]
                console.clear()
                this.errormsg = message
                this.errStatus = true
              } else {
                console.log(error)
              }
            })
        }
        if (this.$store.state.logged_in) {
          // http://127.0.0.1:8000/api/Feed/FrustratedMonk
          // http://127.0.0.1:8000/api/Posts_User/FrustratedMonk
          // http://127.0.0.1:8000/api/FrustratedMonk/Network
          // http://127.0.0.1:8000/api/User_profile/Paradox
          this.$router.push('/feed')
        }
      }
    }
  }
  </script>
  
  <style></style>