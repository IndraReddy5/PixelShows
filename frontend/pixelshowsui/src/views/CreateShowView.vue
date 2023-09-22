<template>
  <Nav />
  <main class="p-3">
    <div class="col-md-10 mx-auto col-lg-5 p-4 p-md-5">
      <form method="POST" @submit.prevent="handleFormSubmit">
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
        <hr class="my-4">
        <div class="alert alert-danger alert-dismissible fade show" role="alert" v-if="errStatus">
          <strong>{{ errormsg }}</strong>.
          <button type="button" class="btn-close" aria-label="Close" @click="errStatus = false"></button>
        </div>
        <button class="w-100 btn btn-lg btn-primary" type="submit">Change Password</button>
      </form>
    </div>
  </main>
</template>

<script>
import Nav from '@/components/Nav.vue';
import { useVuelidate } from '@vuelidate/core'
import { required, sameAs, helpers } from '@vuelidate/validators'
export default {
  setup() {
    return {
      v$: useVuelidate()
    }
  },
  name: 'EditPasswordView',
  components: {
    Nav,
  },
  data: function () {
    return {
      username: localStorage.getItem("username"),
      password: '',
      repeatPassword: '',
      errormsg: '',
      errStatus: false
    }
  },
  validations() {
    return {
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
        const headers = { 'Content-Type': 'application/json', 'Auth-Token': localStorage.getItem("Auth-Token") }
        const formdata = { password: this.password }
        if (localStorage.getItem("role") === "admin") {
          fetch("http://127.0.0.1:8000/api/changepassword/admin", { headers: headers, body: JSON.stringify(formdata), method: "PUT" })
            .then(response => {
              return response.json();
            })
            .then((data) => {
              if (data.meta.code == 200) {
                alert("Password changed successfully");
                this.$router.push({ path: '/dashboard' });
              }
              else {
                this.errormsg = data.meta.message;
                this.errStatus = true;
              }
            })
        }
        else {
          fetch("http://127.0.0.1:8000/api/userprofile/" + this.username, { headers: headers, body: JSON.stringify(formdata), method: "PUT" })
            .then(response => {
              if (response.status == 200) {
                return response.json();
              }
              else {
                return response.json().then((data) => {
                  console.log(data)
                  throw new Error(data.error_message);
                })
              }
            })
            .then((data) => {
              console.log(data)
              if (data.meta.code == 200) {
                alert(data);
                this.$router.push({ path: '/dashboard' });
              }
            })
            .catch((error) => {
              console.log(error)
              this.errormsg = error + ". We are logging you out. Please login again, this should fix the issue";
              this.errStatus = true;
              setTimeout(() => this.$router.push({ path: '/logout' }), 5000);
            })
        }
      }
    }
  }
};
</script>