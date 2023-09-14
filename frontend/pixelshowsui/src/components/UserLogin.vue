<template>
  <div class="col-md-10 mx-auto col-lg-5 p-4 p-md-5">
    <h1>Log in to Pixelshows</h1>
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
      <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="errStatus">
        <strong>{{ errormsg }}</strong>.
        <button type="button" class="btn-close" aria-label="Close" @click="errStatus=false"></button>
      </div>
      <small class="text-muted">New to Pixel Shows? <router-link to="/signup">Sign up now</router-link> </small>
    </form>
  </div>
</template>
  
<script>
import { useVuelidate } from '@vuelidate/core'
import { required, alphaNum, helpers } from '@vuelidate/validators'
export default {
  setup() {
    return {
      v$: useVuelidate()
    }
  },
  name: 'UserLogin',
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
      required: helpers.withMessage('The username field is required', required),
      alphaNum: helpers.withMessage('The username must contain only letters and numbers', alphaNum),
    },
    password: { required: helpers.withMessage('The password field is required', required) }
  },
  methods: {
    handleFormSubmit: function () {
      this.v$.$touch()
      if (!this.v$.$error) {
        const headers = { 'Content-Type': 'application/json' }
        const formdata = { username: this.username, password: this.password }
        fetch("http://127.0.0.1:8000/api/login?include_auth_token", { headers: headers, body: JSON.stringify(formdata), method: "POST" })
          .then(response => {
            return response.json();
          })
          .then((data) => {
            if (data.meta.code == 200) {
              localStorage.setItem("Auth-Token", data.response.user.authentication_token);
              if (this.username.toLowerCase() === "admin") {
                localStorage.setItem("role", "admin");
              }
              else {
                localStorage.setItem("role", "patron");
              }
              localStorage.setItem("username", this.username.toLowerCase());
              this.$router.push('/dashboard');
            }
            else {
              this.errStatus = true;
              throw new Error(data.response.errors[0]);
            }
          })
          .catch((error) => {
            this.errormsg = error;
            console.log(error)
          })
      }
    }
  }
}
</script>
  
<style></style>