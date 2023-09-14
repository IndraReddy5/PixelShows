<template>
  <div class="col-md-10 mx-auto col-lg-5 p-4 p-md-5">
    <h1>Register for Pixelshows Account</h1>
    <br>
    <form method="POST" @submit.prevent="handleFormSubmit">
      <div class="form-floating mb-3">
        <input type="text" :class='{ "form-control": true, "is-invalid": v$.username.$error }' v-model="username"
          name="username" id="floatingInput1" placeholder="username" autocomplete="off">
        <label for="floatingInput1">username</label>
        <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.username.$error">
          <span>{{ v$.username.$errors[0].$message }}</span>
        </div>
      </div>
      <div class="form-floating mb-3">
        <input type="email" :class='{ "form-control": true, "is-invalid": v$.email.$error }' v-model="email" name="email"
          id="floatingInput2" placeholder="email" autocomplete="off">
        <label for="floatingInput2">email</label>
        <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.email.$error">
          <span>{{ v$.email.$errors[0].$message }}</span>
        </div>
      </div>
      <div class="form-floating mb-3">
        <input type="password" :class='{ "form-control": true, "is-invalid": v$.password.$error }' v-model="password"
          name="password" id="floatingPassword1" placeholder="Password" autocomplete="off">
        <label for="floatingPassword1">Password</label>
        <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.password.$error">
          <span>{{ v$.password.$errors[0].$message }}</span>
        </div>
      </div>
      <div class="form-floating mb-3">
        <input type="password" :class='{ "form-control": true, "is-invalid": v$.repeatPassword.$error }'
          v-model="repeatPassword" name="repeat_password" id="floatingPassword2"
          placeholder="repeat the same password as above" autocomplete="off">
        <label for="floatingPassword2">Repeat Password</label>
        <div class="invalid-feedback" style="color: #dc3545 !important" v-if="v$.repeatPassword.$error">
          <span>{{ v$.repeatPassword.$errors[0].$message }}</span>
        </div>
      </div>
      <button class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
      <hr class="my-4">
      <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="errStatus">
        <strong>{{ errormsg }}</strong>.
        <button type="button" class="btn-close" aria-label="Close" @click="errStatus = false"></button>
      </div>
      <small class="text-muted">Have an account? <router-link to="/login">Login now</router-link> </small>
    </form>
  </div>
</template>
    
<script>
import { useVuelidate } from '@vuelidate/core'
import { required, alphaNum, email, sameAs, helpers } from '@vuelidate/validators'
export default {
  setup() {
    return {
      v$: useVuelidate()
    }
  },
  name: 'SignUp',
  data: function () {
    return {
      username: '',
      email: ' ',
      password: '',
      repeatPassword: '',
      errormsg: '',
      errStatus: false
    }
  },
  validations() {
    return {
      username: {
        required: helpers.withMessage('The username field is required', required),
        alphaNum: helpers.withMessage('The username must contain only letters and numbers', alphaNum),
      },
      email: {
        required: helpers.withMessage('The email field is required', required),
        email: helpers.withMessage('The email must be valid', email),
      },
      password: { required: helpers.withMessage('The password field is required', required) },
      repeatPassword: {
        required: helpers.withMessage('The confirm password field is required', required),
        sameAsPassword: helpers.withMessage('The passwords should match', sameAs(this.password)),
      },
    }
  },
  methods: {
    handleFormSubmit: function () {
      this.v$.$touch()
      if (!this.v$.$error) {
        const headers = { 'Content-Type': 'application/json' }
        const formdata = { username: this.username, email: this.email, password: this.password }
        fetch("http://localhost:8000/api/createuserprofile", { headers: headers, body: JSON.stringify(formdata), method: "POST" })
          .then(response => {
            if (response.status == 200) {
              return response.json();
            }
            else {
              this.errStatus = true;
              throw new Error("Username or email already exists");
            }
          })
          .then((data) => {
            console.log(data)
            fetch("http://127.0.0.1:8000/api/login?include_auth_token", { headers: headers, body: JSON.stringify(formdata), method: "POST" })
              .then(response => {
                return response.json();
              })
              .then((data) => {
                if (data.meta.code == 200) {
                  localStorage.setItem("Auth-Token", data.response.user.authentication_token);
                  localStorage.setItem("role", "patron");
                  localStorage.setItem("username", this.username.toLowerCase());
                  this.$router.push('/dashboard');
                }
                else {
                  this.errStatus = true;
                  throw new Error(data.response.errors[0]);
                }
              })
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