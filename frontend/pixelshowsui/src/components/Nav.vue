<template>
    <div class="about">
        <PatronNav v-if="!flag" />
        <AdminNav v-if="flag" />
        <h1>This is an about page</h1>

    </div>
</template>
  
<script>
import PatronNav from '@/components/PatronNav.vue';
import AdminNav from '@/components/AdminNav.vue';

export default {
    data: function () {
        return {
            role: localStorage.getItem("role"),
            flag: false,
        }
    },
    name: 'Nav',
    components: {
        PatronNav,
        AdminNav,
    },
    beforeMount() {
        if (this.role == "admin") {
            this.flag = true;
        }
    },
};
</script>