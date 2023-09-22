<template>
  <Nav />
  <main class="p-3">
    <div class="container">
      <h1>This is an about page</h1>
      <p></p>
    </div>
  </main>
</template>

<script>
import Nav from '@/components/Nav.vue';

export default {
  data: function () {
    return {
      role: localStorage.getItem("role"),
      flag: false,
    }
  },
  name: 'DashboardView',
  components: {
    Nav,
  },
  beforeMount() {
  },
};
</script>